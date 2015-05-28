import os
from lxml import etree
from anansi.comms import TCPClient
from time import sleep
from ConfigParser import ConfigParser
from anansi.logging_db import MolongloLoggingDataBase as LogDB
from anansi import exit_funcs

config_path = os.environ["ANANSI_CONFIG"]
config = ConfigParser()
config.read(os.path.join(config_path,"anansi.cfg"))
STATUS_IP = config.get("IPAddresses","status_ip")
STATUS_PORT = config.getint("IPAddresses","status_port")

def is_on_target(xml):
    return bool(xml.find("overview").find("on_target").text)


client = TCPClient(STATUS_IP,STATUS_PORT)
client.send("234353534")
xml = client.receive()
xml = etree.fromstring(xml)
print etree.tostring(xml,pretty_print=True)