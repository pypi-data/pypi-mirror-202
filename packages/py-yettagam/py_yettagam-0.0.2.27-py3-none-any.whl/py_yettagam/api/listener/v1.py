# MetariumTopicListener for a substrate chain

# standard imports
import asyncio
import logging
import ipaddress
import math
import os
import shutil
import time
# third party imports
from blake3 import blake3
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
from tinydb import TinyDB, Query
# local imports
from ...substrate.exceptions import ChainConnectionRefusedError


logging.basicConfig(format='%(process)d : %(asctime)s : %(levelname)s\n%(funcName)s():%(lineno)i\n%(message)s\n',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class OutboxTimer(object):
    def __init__(self, outbox_read_duration_seconds: int = 3600) -> None:
        self.outbox_read_duration_seconds = outbox_read_duration_seconds
        self.activated_at = None
        self.activated_by = None

    def activate(self, activated_by: str) -> None:
        self.activated_at = time.time()
        self.activated_by = activated_by

    def is_active(self) -> bool:
        if self.activated_at is None:
            return False
        return time.time() - self.activated_at < self.outbox_read_duration_seconds

    def get_remaining_seconds(self) -> int:
        if self.activated_at is None:
            return 0
        return math.ceil(self.outbox_read_duration_seconds - (time.time() - self.activated_at))

    def deactivate(self) -> None:
        self.activated_at = None
        self.activated_by = None


class ListenerApiModelV1(object):

    RECONNECTION_WAIT_DURATION_SECONDS = 5
    MAX_RECONNECTION_ATTEMPTS = 10

    def __init__(self,
                 key_path: str = None,
                 chain_spec_path: str = None,
                 chain_url: str = None,
                 data_location_path: str = "/home/.metarium",
                 reader_location_path: str = "/home/reader",
                 outbox_read_duration_seconds: int = 3600,
                 ) -> None:
        key_path = key_path or None
        chain_spec_path = chain_spec_path or None
        chain_url = chain_url or None
        assert key_path is not None
        assert chain_spec_path is not None
        assert chain_url is not None
        # check if key_path exists
        if not os.path.exists(key_path):
            logging.error(f"key_path {key_path} does not exist!")
            raise FileNotFoundError
        # check if chain_spec_path exists
        if not os.path.exists(chain_spec_path):
            logging.error(f"chain_spec_path {chain_spec_path} does not exist!")
            raise FileNotFoundError
        # check if chain_url is valid
        if not isinstance(chain_url, str):
            logging.error(f"chain_url {chain_url} is not a string!")
            raise TypeError
        # check if data_location_path is valid
        if not isinstance(data_location_path, str):
            logging.error(
                f"data_location_path {data_location_path} is not a string!")
            raise TypeError
        if not os.path.exists(data_location_path):
            logging.error(
                f"data_location_path {data_location_path} does not exist!")
            raise FileNotFoundError
        # check if reader_location_path is valid
        if not isinstance(reader_location_path, str):
            logging.error(
                f"reader_location_path {reader_location_path} is not a string!")
            raise TypeError
        if not os.path.exists(reader_location_path):
            logging.error(
                f"reader_location_path {reader_location_path} does not exist!")
            raise FileNotFoundError
        # check if outbox_read_duration_seconds is valid
        if not isinstance(outbox_read_duration_seconds, int):
            logging.error(
                f"outbox_read_duration_seconds {outbox_read_duration_seconds} is not an integer!")
            raise TypeError
        if outbox_read_duration_seconds < 1:
            logging.error(
                f"outbox_read_duration_seconds {outbox_read_duration_seconds} is less than 1!")
            raise ValueError
        # get key from key_path file
        with open(key_path, "r") as key_file:
            # create keypair from key
            self.__key = Keypair.create_from_mnemonic(key_file.read())
        # create a blake3 hash of the chain_spec_path file
        self.__chain_spec_hash = self._file_hash(chain_spec_path)
        # set data_location_path
        self.__data_location_path = data_location_path
        # set reader_location_path
        self.__reader_location_path = reader_location_path
        self.__outbox_read_duration_seconds = outbox_read_duration_seconds
        self.__outbox_timer = OutboxTimer(
            outbox_read_duration_seconds=self.__outbox_read_duration_seconds)
        # connect to chain
        reconnection_attempts = 1
        while True:
            try:
                self.__chain = SubstrateInterface(url=chain_url)
            except ConnectionRefusedError:
                if reconnection_attempts == self.__class__.MAX_RECONNECTION_ATTEMPTS:
                    logging.error(
                        f"Chain connection terminated after {reconnection_attempts} attempts.")
                    logging.exception(ChainConnectionRefusedError)
                logging.warning(
                    f"Chain connection refused. Retrying in {self.__class__.RECONNECTION_WAIT_DURATION_SECONDS} seconds ...")
                reconnection_attempts += 1
                time.sleep(self.__class__.RECONNECTION_WAIT_DURATION_SECONDS)
                continue
            break
        logging.info(
            f"connected to {self.__chain.name} {self.__chain_spec_hash} as listener {self.__key.ss58_address}")
        # setup folders
        self.__initialize_folders()
        # setup database
        self.__initialize_database()

    ############################## INITIALIZATION LOGIC ##############################

    def __initialize_database(self):
        # check if the database path exists. if not, raise an error
        if not os.path.exists(self.__database_path):
            logging.error(
                f"database path {self.__database_path} does not exist!")
            raise FileNotFoundError
        # get the database from the database path. if it does not exist, create it
        self.__db = TinyDB(f"{self.__database_path}/yettagam.db", indent=4, separators=(
            ',', ': '), sort_keys=True)
        # get the metariums table. if it does not exist, create it
        self.__table_metariums = self.__db.table("metariums")
        # get the chain_spec_hash record. if it does not exist, create it with the chain name as the value
        self.__table_metariums.upsert(
            {"chain_spec_hash": self.__chain_spec_hash, "name": self.__chain.name}, Query().chain_spec_hash == self.__chain_spec_hash)
        # get the arikuris_state table. if it does not exist, create it
        self.__table_arikuris_state = self.__db.table("arikuris_state")

    def __initialize_folders(self):
        # create the data location directory if it does not exist
        if not os.path.exists(self.__data_location_path):
            os.makedirs(self.__data_location_path)
        ####### generic folders #######
        # create the database directory if it does not exist
        self.__database_path = os.path.join(
            self.__data_location_path, "data/db")
        self._create_folder_if_not_exists(self.__database_path)
        # create the outbox directory if it does not exist
        self.__outbox_path = os.path.join(
            self.__data_location_path, "outbox")
        self._create_folder_if_not_exists(self.__outbox_path)
        ####### chain-specific folders #######
        # create the data files directory for the chain if it does not exist
        self.__data_files_path = os.path.join(
            self.__data_location_path, "data/files", self.__chain_spec_hash)
        self._create_folder_if_not_exists(self.__data_files_path)

    ### FOLDER SYNC ###

    def __add_readers_to_file_system(self, ssh_keys):
        # get the authorized_keys file from reader_path/.ssh/authorized_keys
        authorized_keys_file = os.path.join(
            self.__reader_location_path, ".ssh", "authorized_keys")
        with open(authorized_keys_file, "w") as f:
            for ssh_key in ssh_keys:
                # add the ssh_key to the authorized_keys file
                f.write(f"{ssh_key}")
                logging.info(f"Reader {ssh_key} added to file system")

    def __remove_all_readers_from_file_system(self):
        # get the authorized_keys file from reader_path/.ssh/authorized_keys
        authorized_keys_file = os.path.join(
            self.__reader_location_path, ".ssh", "authorized_keys")
        # empty the authorized_keys file
        with open(authorized_keys_file, "w") as f:
            f.write("")
        logging.info(f"all readers removed from file system")

    ############################## CHAIN QUERYING ##############################

    def __topic_from_chain(self, topic: int):
        # query the chain for the topic
        topic = self.__chain.query(
            module="Metarium", storage_function="Topics", params=[topic])

        topic = topic.serialize()

        if topic == None:
            topic = {}

        return topic

    def __arikuri_from_chain(self, topic: int, kuri: str):
        # query the chain for the arikuri
        arikuri = self.__chain.query(
            module="Metarium", storage_function="Arikuris", params=[topic, kuri])

        arikuri = arikuri.serialize()

        if arikuri == None:
            arikuri = {}

        return arikuri

    def __writer_from_chain(self, writer: str):
        # query the chain for the writer
        writer = self.__chain.query(
            module="Metarium", storage_function="NodeInfoMap", params=[writer])

        writer = writer.serialize()
        if writer == None:
            writer = {}

        return writer

    ############################## DATABASE QUERYING ##############################

    def __chain_spec_hashes_from_db(self):
        chain_spec_hashes = []
        for chain_spec_hash in self.__table_metariums.all():
            chain_spec_hashes.append(chain_spec_hash["chain_spec_hash"])
        return chain_spec_hashes

    ############################## API FUNCTONS ##############################

    def __get_state(self, data: dict = {}) -> dict:
        # check if data is valid
        if not isinstance(data, dict):
            logging.error(f"data {data} is not a dictionary!")
            raise TypeError
        # prepare the response
        response = {
            "found": False,
            "path": None
        }
        # get the kuri from the data
        kuri = data["kuri"]
        # convert the topic id to a string
        topic_id = f"{data['topic_id']}"
        logging.info(
            f"getting state for kuri {kuri} and topic_id {topic_id} and chain_spec_hash {data['chain_spec_hash']}")
        # create a query where kuri == kuri and chain_spec_hash == data["chain_spec_hash"]
        query = (Query().kuri == kuri) & (
            Query().chain_spec_hash == data["chain_spec_hash"])
        # get the arikuri from the database
        arikuri_from_db = self.__table_arikuris_state.get(query)
        logging.info(f"arikuri_from_db: {arikuri_from_db}")
        logging.info(f"type(arikuri_from_db): {type(arikuri_from_db)}")
        # check if the arikuri exists
        if arikuri_from_db in (None, {}):
            # if it does not exist, return response
            logging.error(f"arikuri_from_db is None or empty")
            return response
        # check if the topic_id is in the arikuri
        if topic_id not in arikuri_from_db:
            # if it does not exist, return response
            logging.error(f"topic_id {topic_id} not in arikuri_from_db")
            return response
        # get the filename from the arikuri
        filename = arikuri_from_db[topic_id]
        # check if the filename exists
        if filename == None:
            # if it does not exist, return response
            logging.error(f"filename is None")
            return response
        # check if the filename is not an empty string
        if filename == "":
            # if it does not exist, return response
            logging.error(f"filename is an empty string")
            return response
        # check if the filename exists as a file
        file_path = os.path.join(
            self.__data_location_path, "data/files", data["chain_spec_hash"], topic_id, filename)
        if not os.path.isfile(file_path):
            # if it does not exist, return response
            logging.error(f"file_path {file_path} does not exist")
            return response
        # update the response
        response["found"] = True
        response["path"] = file_path
        return response

    def __validate_state_payload(self, payload: any = None) -> dict:
        # get the data from the payload
        data = {
            "topic_id": payload["topic_id"],
            "kuris": payload["kuris"],
            "chain_spec_hash": payload["chain_spec_hash"]
        }
        result = {
            "errors": []
        }
        # validate the topic_id
        if not isinstance(data["topic_id"], int):
            error_message = f"topic_id {data['topic_id']} is not an integer!"
            logging.error(error_message)
            result["errors"].append(error_message)
        # check if the topic_id is in the chain
        if len(self.__topic_from_chain(data["topic_id"])) == 0:
            error_message = f"topic_id {data['topic_id']} is not in the chain!"
            logging.error(error_message)
            result["errors"].append(error_message)
        # check if each kuri is in the chain
        for kuri in data["kuris"]:
            if len(self.__arikuri_from_chain(topic=data["topic_id"], kuri=kuri)) == 0:
                error_message = f"kuri {kuri} is not in the chain!"
                logging.error(error_message)
                result["errors"].append(error_message)
        # check if the chain_spec_hash is in the chain
        if data["chain_spec_hash"] not in self.__chain_spec_hashes_from_db():
            error_message = f"chain_spec_hash {data['chain_spec_hash']} is not supported here!"
            logging.error(error_message)
            result["errors"].append(error_message)
        # return the result
        return result

    def state(self, payload: any = None):
        # prepare the response
        response = {
            "data": {},
            "errors": []
        }
        # validate the payload
        validation_result = self.__validate_state_payload(payload)
        # check if there are errors
        if len(validation_result["errors"]) > 0:
            response["errors"] = validation_result["errors"]
            return response
        # popuplate the state for each kuri
        for kuri in payload["kuris"]:
            state = self.__get_state(data={
                "topic_id": payload["topic_id"],
                "kuri": kuri,
                "chain_spec_hash": payload["chain_spec_hash"]
            })
            logging.info(f"state: {state}")
            response["data"][kuri] = state["found"]

        return response

    def syn(self, payload: any = None):
        # prepare the response
        response = {
            "synack": False,
            "errors": []
        }
        # validate the payload
        validation_result = self.__validate_state_payload(payload)
        # check if there are errors
        if len(validation_result["errors"]) > 0:
            response["errors"] = validation_result["errors"]
            return response

        file_paths = []
        response["synack"] = True
        # popuplate the state for each kuri
        for kuri in payload["kuris"]:
            state = self.__get_state(data={
                "topic_id": payload["topic_id"],
                "kuri": kuri,
                "chain_spec_hash": payload["chain_spec_hash"]
            })
            response["synack"] = response["synack"] and state["found"]
            if response["synack"] is False:
                error_message = f"state for kuri {kuri} is not found!"
                logging.error(error_message)
                break
            file_paths.append(state["path"])

        if response["synack"] is True:
            # delete the files in the outbox
            self._delete_files(
                folder_path=self.__outbox_path
            )
            # activate the outbox timer
            self.__outbox_timer.activate(
                activated_by=payload["sender"]
            )
            # get writer from the chain for the sender
            writer_from_chain = self.__writer_from_chain(
                writer=payload["sender"])
            # get the ssh_pub_key
            ssh_pub_key = writer_from_chain["ssh_pub_key"]
            # add the ssh_pub_key to the reader authorized_keys
            self.__add_readers_to_file_system(ssh_keys=[ssh_pub_key])
            # copy files in file_paths to the outbox
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                destination_path = os.path.join(self.__outbox_path, filename)
                shutil.copyfile(file_path, destination_path)

        return response

    def ack(self, payload: any = None):
        # get the sender from the payload
        sender = payload["sender"]
        # prepare the response
        response = {
            "ackack": False
        }
        if self.__outbox_timer.activated_by == sender:
            # remove the reader from the file system
            self.__remove_all_readers_from_file_system()
            # delete the files in the outbox
            self._delete_files(
                folder_path=self.__outbox_path
            )
            # deactivate the outbox timer
            self.__outbox_timer.deactivate()
            response["ackack"] = True

        return response

    ############################## UTILITY FUNCTONS ##############################

    def _file_hash(self, file_path: any = None) -> str:
        # check if file_path is valid
        if not isinstance(file_path, str):
            logging.error(f"file_path {file_path} is not a string!")
            raise TypeError
        if not os.path.exists(file_path):
            logging.error(f"file_path {file_path} does not exist!")
            raise FileNotFoundError
        # create a blake3 hash of the content
        hasher = blake3(max_threads=blake3.AUTO)
        with open(file_path, "rb") as f:
            counter = 0
            while True:
                counter += 1
                content = f.read(1024)
                if not content:
                    break
                hasher.update(content)

        return hasher.hexdigest()

    def _create_folder_if_not_exists(self, folder_path: str = None) -> None:
        # check if folder_path is valid
        if not isinstance(folder_path, str):
            logging.error(f"folder_path {folder_path} is not a string!")
            raise TypeError
        # create the folder if it does not exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def _delete_files(self, folder_path: str = None, filenames: list = None) -> None:
        # check if folder_path is valid
        if not isinstance(folder_path, str):
            logging.error(f"folder_path {folder_path} is not a string!")
            raise TypeError
        if not os.path.exists(folder_path):
            logging.error(f"folder_path {folder_path} does not exist!")
            raise FileNotFoundError
        filenames = filenames or []
        if len(filenames) == 0:
            filenames = os.listdir(folder_path)
        # delete the files
        for filename in filenames:
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)

    def _is_valid_ip_address(self, ip_address: str = None) -> bool:
        # check if ip_address is valid
        if not isinstance(ip_address, str):
            logging.error(f"ip_address {ip_address} is not a string!")
            raise TypeError
        # check if ip_address is valid
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False
