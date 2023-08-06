# MetariumTopicCommitter for a substrate chain

# standard imports
import logging
import ipaddress
import json
import os
import requests
import time
# third party imports
from blake3 import blake3
import paramiko
from substrateinterface import SubstrateInterface, Keypair
import sshpubkeys
from sshpubkeys import SSHKey, InvalidKeyError
# local imports
from .decorators import wait_while_querying, wait_while_downloading
from .exceptions import ChainConnectionRefusedError


logging.basicConfig(format='%(process)d : %(asctime)s : %(levelname)s\n%(message)s\n',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class SubstrateDownloader(object):

    RECONNECTION_WAIT_DURATION_SECONDS = 5
    MAX_RECONNECTION_ATTEMPTS = 10

    def __init__(self, config_path: str = None) -> None:
        # set config_path
        self.__config_path = config_path or None
        # verify config_path
        if self.__config_path is not None:
            assert os.path.exists(self.__config_path)
        # get config
        self.__config = self.__get_config()
        # get key_path from config
        key_path = self.__config.get("key_path", None)
        assert key_path is not None
        # check if key_path exists
        if not os.path.exists(key_path):
            error_message = f"key_path {key_path} does not exist!"
            logging.error(error_message)
            raise FileNotFoundError(error_message)
        # get chain_spec_path from config
        chain_spec_path = self.__config.get(
            "chain_spec_path", None)
        assert chain_spec_path is not None
        # check if chain_spec_path exists
        if not os.path.exists(chain_spec_path):
            error_message = f"chain_spec_path {chain_spec_path} does not exist!"
            logging.error(error_message)
            raise FileNotFoundError(error_message)
        # get chain_url from config
        chain_url = self.__config.get("chain_url", None)
        assert chain_url is not None
        # check if chain_url is valid
        if not isinstance(chain_url, str):
            error_message = f"chain_url {chain_url} is not a string!"
            logging.error(error_message)
            raise TypeError(error_message)
        # get ssh_private_key_path from config
        ssh_private_key_path = self.__config.get("ssh_private_key_path", None)
        assert ssh_private_key_path is not None
        # check if ssh_private_key_path is valid
        if not isinstance(ssh_private_key_path, str):
            error_message = f"ssh_private_key_path {ssh_private_key_path} is not a string!"
            logging.error(error_message)
            raise TypeError(error_message)
        if not os.path.exists(ssh_private_key_path):
            error_message = f"ssh_private_key_path {ssh_private_key_path} does not exist!"
            logging.error(error_message)
            raise FileNotFoundError(error_message)
        # get ssh_private_key_passphrase from config
        ssh_private_key_passphrase = self.__config.get(
            "ssh_private_key_passphrase", None)
        # check if ssh_private_key_passphrase is valid
        if not isinstance(ssh_private_key_passphrase, str):
            error_message = f"ssh_private_key_passphrase {ssh_private_key_passphrase} is not a string!"
            logging.error(error_message)
            raise TypeError(error_message)
        # get listener_threshold from config
        listener_threshold = self.__config.get(
            "listener_threshold", 3)
        # check if listener_threshold is valid
        if not isinstance(listener_threshold, int):
            error_message = f"listener_threshold {listener_threshold} is not an integer!"
            logging.error(error_message)
            raise TypeError(error_message)
        if listener_threshold < 1:
            error_message = f"listener_threshold {listener_threshold} is less than 1!"
            logging.error(error_message)
            raise ValueError(error_message)
        # get key from key_path file
        with open(key_path, "r") as key_file:
            # create keypair from key
            self.__key = Keypair.create_from_mnemonic(key_file.read())
        # create a blake3 hash of the chain_spec_path file
        self.__chain_spec_hash = self._file_hash(chain_spec_path)
        # set ssh_private_key_path
        self.__ssh_private_key_path = ssh_private_key_path
        # set ssh_private_key_passphrase
        self.__ssh_private_key_passphrase = ssh_private_key_passphrase
        # set listener_threshold
        self.__listener_threshold = listener_threshold
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
        connected_message = f"\n\n\nConnected to {self.__chain.name} {self.__chain_spec_hash} as Committer {self.__key.ss58_address}!\n\n\n"
        logging.info(f"{'*' * 100}\n{connected_message}{'*' * 100}")

        self._is_downloading = False
        self._is_querying = False
        self._queryables = {}

    ############################## CONFIG LOGIC ##############################

    def __get_config(self) -> dict:
        if self.__config_path is None:
            return {}
        with open(self.__config_path, "r") as config_file:
            return json.load(config_file)

    ############################## DOWNLOAD STATE-LOGIC ##############################

    def __start_downloading(self):
        self._is_downloading = True

    def __stop_downloading(self):
        self.__topic_id = None
        self.__kuris = None
        self.__download_location_path = None
        self._queryables = {}
        self._is_downloading = False

    ############################## LISTENER-QUERY STATE-LOGIC ##############################

    def __start_querying(self):
        self._is_querying = True

    def __stop_querying(self):
        self._is_querying = False

    ############################## HTTPS MIMICRY ##############################

    def __prepare_payload(self, payload: dict) -> dict:
        return {
            "payload": payload,
        }

    def __api_call(self, host: str, method: str, payload: dict) -> dict:
        uri = f"/{method}"
        response = requests.post(
            url=f"http://{host}{uri}",
            json=self.__prepare_payload(payload),
        )
        return response.json()

    ############################## QUERY FUNCTONS ##############################

    def __query_listener(self, listener_ip_address: str) -> None:
        payload = {
            "topic_id": self.__topic_id,
            "kuris": self.__kuris,
            "chain_spec_hash": self.__chain_spec_hash,
            "sender": self.__key.ss58_address
        }
        response = self.__api_call(
            host=listener_ip_address,
            method="state",
            payload=payload,
        )
        logging.info(f"response: {response}")
        # check if response is valid
        if not isinstance(response, dict):
            logging.error(f"response {response} is not a dict!")
            raise TypeError
        if "errors" not in response:
            logging.error(f"response {response} does not have an errors key!")
            raise KeyError
        if "data" not in response:
            logging.error(f"response {response} does not have a data key!")
            raise KeyError
        # check if response["errors"] is valid
        if not isinstance(response["errors"], list):
            logging.error(
                f"response[errors] {response['errors']} is not a list!")
            raise TypeError
        # check if response["data"] is valid
        if not isinstance(response["data"], dict):
            logging.error(f"response[data] {response['data']} is not a dict!")
            raise TypeError
        logging.info(f"self._queryables: {self._queryables}")
        if response["errors"] == []:
            for kuri, found in response["data"].items():
                logging.info(f"kuri: {kuri}")
                logging.info(f"found: {found}")
                if found is True:
                    if listener_ip_address not in self._queryables:
                        self._queryables[listener_ip_address] = [kuri]
                    else:
                        self._queryables[listener_ip_address].append(
                            kuri)
        logging.info(f"self._queryables: {self._queryables}")

    def __query_listeners(self, listener_ip_addresses: list) -> None:
        # verify that the listener_ip_addresses are valid
        for listener_ip_address in listener_ip_addresses:
            if not self._is_valid_ip_address(listener_ip_address):
                logging.error(
                    f"listener_ip_address {listener_ip_address} is not a valid IP address!")
                raise ValueError
        # query the listeners
        self.__start_querying()
        for listener_ip_address in listener_ip_addresses:
            self.__query_listener(listener_ip_address)
        self.__stop_querying()

    ############################## INPUT VERIFICATION FOR DOWNLOAD FUNCTONS ##############################

    def __verify_topic_id(self, topic_id: int) -> None:
        logging.info(f"topic_id: {topic_id}")
        logging.info(f"type(topic_id): {type(topic_id)}")
        if not isinstance(topic_id, int):
            logging.error(f"topic_id {topic_id} is not an integer!")
            raise TypeError
        if topic_id < 0:
            logging.error(f"topic_id {topic_id} is less than 0!")
            raise ValueError

    def __verify_kuris(self, kuris: list) -> None:
        if not isinstance(kuris, list):
            logging.error(f"kuris {kuris} is not a list!")
            raise TypeError
        for kuri in kuris:
            if not isinstance(kuri, str):
                logging.error(f"kuri {kuri} is not a string!")
                raise TypeError

    def __verify_download_location_path(self, download_location_path: str) -> None:
        if not isinstance(download_location_path, str):
            logging.error(
                f"download_location_path {download_location_path} is not a string!")
            raise TypeError
        if not os.path.exists(download_location_path):
            logging.error(
                f"download_location_path {download_location_path} does not exist!")
            raise FileNotFoundError

    ############################## DOWNLOAD FUNCTONS ##############################

    def __download_files_from_listener(self, listener_with_queryables: list) -> None:
        listener_ip_address = listener_with_queryables[0]
        queryables = listener_with_queryables[1]
        # request for the files to be downloaded from the listener
        response = self.__api_call(
            host=listener_ip_address,
            method="syn",
            payload={
                "topic_id": self.__topic_id,
                "kuris": queryables,
                "chain_spec_hash": self.__chain_spec_hash,
                "sender": self.__key.ss58_address
            },
        )
        # check if response is valid
        if not isinstance(response, dict):
            logging.error(f"response {response} is not a dict!")
            raise TypeError
        if "errors" not in response:
            logging.error(
                f"response {response} does not have an errors key!")
            raise KeyError
        if "synack" not in response:
            logging.error(
                f"response {response} does not have a synack key!")
            raise KeyError
        # check if response["errors"] is valid
        if not isinstance(response["errors"], list):
            logging.error(
                f"response[errors] {response['errors']} is not a list!")
            raise TypeError
        # check if response["synack"] is valid
        if not isinstance(response["synack"], bool):
            logging.error(
                f"response[synack] {response['synack']} is not a bool!")
            raise TypeError
        # check if response["errors"] is empty
        if response["errors"] != []:
            logging.error(
                f"response[errors] {response['errors']} is not empty!")
            raise ValueError
        # check if response["synack"] is True
        if response["synack"] is not True:
            logging.error(
                f"response[synack] {response['synack']} is not True!")
            raise ValueError
        # connect to the listener and download the files
        # setup the ssh client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=listener_ip_address, username="reader",
                           pkey=paramiko.RSAKey.from_private_key_file(
                               self.__ssh_private_key_path, password=self.__ssh_private_key_passphrase))
        # setup the sftp client
        sftp_client = ssh_client.open_sftp()
        # download all the files from the /home/.metarium/outbox
        sftp_client.chdir("/home/.metarium/outbox")
        for file in sftp_client.listdir():
            sftp_client.get(file, f"{self.__download_location_path}/{file}")
        # close the sftp client
        sftp_client.close()
        # close the ssh client
        ssh_client.close()
        logging.info(
            f"all files successfully downloaded from IP address {listener_ip_address}!")
        # make an "ack" request to the listener
        response = self.__api_call(
            host=listener_ip_address,
            method="ack",
            payload={
                "sender": self.__key.ss58_address
            },
        )
        # check if response is valid
        if not isinstance(response, dict):
            logging.error(f"response {response} is not a dict!")
            raise TypeError
        if "ackack" not in response:
            logging.error(
                f"response {response} does not have a ackack key!")
            raise KeyError
        # check if response["ackack"] is valid
        if not isinstance(response["ackack"], bool):
            logging.error(
                f"response[ackack] {response['ackack']} is not a bool!")
            raise TypeError
        # check if response["ackack"] is True
        if response["ackack"] is not True:
            logging.error(
                f"response[ackack] {response['ackack']} is not True!")
            raise ValueError
        logging.info(
            f"successfully made an ack request to IP address {listener_ip_address}!")

    @wait_while_querying
    def __download_files(self) -> None:
        logging.info("downloading files...")
        logging.info("getting the listeners with the most queryables...")
        # get the listeners with the most queryables in descending order
        listeners_with_most_queryables = sorted(
            self._queryables.items(), key=lambda x: len(x[1]), reverse=True)
        # remove the listeners with repeated queryables
        for listener_with_most_queryables in listeners_with_most_queryables:
            listener_ip_address = listener_with_most_queryables[0]
            queryables = listener_with_most_queryables[1]
            for other_listener_with_most_queryables in listeners_with_most_queryables:
                other_listener_ip_address = other_listener_with_most_queryables[0]
                other_queryables = other_listener_with_most_queryables[1]
                if listener_ip_address != other_listener_ip_address:
                    for queryable in queryables:
                        if queryable in other_queryables:
                            other_queryables.remove(queryable)
        # remove the listeners with no queryables
        listeners_with_most_queryables = [
            listener_with_most_queryables for listener_with_most_queryables in listeners_with_most_queryables if listener_with_most_queryables[1] != []]
        logging.info(
            f"listeners with the most queryables: {listeners_with_most_queryables}")
        # download the files
        for listener_with_queryables in listeners_with_most_queryables:
            self.__download_files_from_listener(listener_with_queryables)

    @wait_while_downloading
    def download(self, topic_id: int = None, kuris: list = None,
                 download_location_path: str = None) -> None:
        # check if topic_id is valid
        self.__verify_topic_id(topic_id)
        # check if kuris is valid
        self.__verify_kuris(kuris)
        # check if download_location_path is valid
        self.__verify_download_location_path(download_location_path)
        # set topic_id
        self.__topic_id = topic_id
        # set kuris
        self.__kuris = kuris
        # set download_location_path
        self.__download_location_path = download_location_path
        # start downloading
        self.__start_downloading()
        # get the topic from the chain
        topic_from_chain = self.__topic_from_chain(self.__topic_id)
        # get the listeners from the topic
        listeners = topic_from_chain.get("listener_nodes", [])
        # get listeners with a valid IP address
        valid_listeners = []
        # get the node info from the chain
        for listener in listeners:
            node_info = self.__node_info_from_chain(listener)
            ip_address = node_info.get("ip_address", None)
            ssh_pub_key = node_info.get("ssh_pub_key", None)
            if ip_address is not None and self._is_valid_ip_address(ip_address):
                valid_listeners.append({
                    "node": listener,
                    "ip_address": ip_address,
                    "ssh_pub_key": ssh_pub_key
                })
        # check if there are enough valid listeners
        if len(valid_listeners) < self.__listener_threshold:
            # if there are not enough valid listeners, raise a warning
            logging.warning(
                f"Only {len(valid_listeners)} valid listeners for topic {self.__topic_id}. Threshold is {self.__listener_threshold}")
        # upload the file to the listeners
        self.__query_listeners([listener["ip_address"]
                                for listener in valid_listeners])
        # process the queryables
        self.__download_files()
        # stop downloading
        self.__stop_downloading()

    ############################## CHAIN QUERYING ##############################

    def __topic_from_chain(self, topic: int):
        # query the chain for the topic
        topic = self.__chain.query(
            module="Metarium", storage_function="Topics", params=[topic])

        topic = topic.serialize()

        if topic == None:
            topic = {}

        return topic

    def __node_info_from_chain(self, node: str):
        # query the chain for the node
        node = self.__chain.query(
            module="Metarium", storage_function="NodeInfoMap", params=[node])

        node = node.serialize()
        if node == None:
            node = {}

        return node

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

    def _is_valid_ssh_pub_key(self, ssh_pub_key: str = None) -> bool:
        # check if ssh_pub_key is valid
        if not isinstance(ssh_pub_key, str):
            logging.error(f"ssh_pub_key {ssh_pub_key} is not a string!")
            raise TypeError
        # check if ssh_pub_key is valid
        ssh = SSHKey(ssh_pub_key, strict=True)
        try:
            ssh.parse()
        except InvalidKeyError as err:
            return False
        except NotImplementedError as err:
            return False
        return True
