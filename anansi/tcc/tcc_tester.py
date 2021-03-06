from lxml import etree
from anansi.comms import TCPClient
from anansi import args
from anansi.config import build_config,config
from ConfigParser import ConfigParser
import sys
import os

if __name__ == "__main__":
    from anansi import args
    from anansi.config import config
    args.init()
    ANANSI_SERVER_IP = config.get("IPAddresses","tcc_ip")
    ANANSI_SERVER_PORT = config.getint("IPAddresses","tcc_port")

class TCCMessage(object):
    def __init__(self,user,comment=""):
        self.root = self._gen_element("tcc_request")
        self.user_info(user,comment)

    def __str__(self):
        return etree.tostring(self.root,encoding='ISO-8859-1')

    def __repr__(self):
        return etree.tostring(self.root,encoding='ISO-8859-1',pretty_print=True)

    def _gen_element(self,name,text=None,attributes=None):
        root = etree.Element(name)
        if attributes is not None:
            for key,val in attributes.items():
                root.attrib[key] = val
        if text is not None:
            root.text = text
        return root

    def server_command(self,command):
        elem = self._gen_element("server_command")
        elem.append(self._gen_element("command",text=command))
        self.root.append(elem)

    def user_info(self,username,comment):
        elem = self._gen_element("user_info")
        elem.append(self._gen_element("name",text=username))
        elem.append(self._gen_element("comment",text=comment))
        self.root.append(elem)

    def tcc_command(self,command):
        elem = self._gen_element("tcc_command")
        elem.append(self._gen_element("command",text=command))
        self.root.append(elem)

    def tcc_pointing(self,x,y,east_arm="enabled",west_arm="enabled",**attributes):
        elem = self._gen_element("tcc_command")
        elem.append(self._gen_element("command",text="point"))
        pointing = self._gen_element("pointing",attributes=attributes)
        pointing.append(self._gen_element("xcoord",text=str(x)))
        pointing.append(self._gen_element("ycoord",text=str(y)))
        arms = self._gen_element("arms")
        arms.append(self._gen_element("east",text=east_arm))
        arms.append(self._gen_element("west",text=west_arm))
        elem.append(pointing)
        elem.append(arms)
        self.root.append(elem)

class TCCUser(object):
    def __init__(self,ip=None,port=None):
        conf = config.tcc_server
        self.ip = conf.ip if ip is None else ip
        self.port = conf.port if port is None else port
        
    def send(self,msg,recv=True):
        client = TCPClient(self.ip,self.port,timeout=10.0)
        client.send(msg)
        if recv:
            response = client.receive()
        else:
            response = None
        del client
        return response

def shutdown():
    msg = TCCMessage("ebarr")
    msg.server_command("shutdown")
    print repr(msg)
    client = TCCUser()
    print client.send(str(msg))

def point(x,y,system="equatorial",tracking="on",east_arm="enabled",west_arm="enabled"):
    msg = TCCMessage("ebarr")
    msg.tcc_pointing(x,y,system=system,
                     tracking=tracking,
                     east_arm=east_arm,
                     west_arm=west_arm,
                     units="hhmmss")
    print repr(msg)
    client = TCCUser()
    print client.send(str(msg))

if __name__ == "__main__":
    shutdown()
