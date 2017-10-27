# -*- coding: utf-8 -*-
from random import choice, randint
import rpyc

class ZeusService(rpyc.Service):
    ALIASES = ["zeus", "zeze"]
    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass
    @classmethod
    def exposed_whoAmI(cls): # this is an exposed method
        return "I am Zeus! The God of Gods!"
    @classmethod
    def exposed_getTheBomb(cls, counter, godsHome):
        counter -= randint(0,counter)
        if (counter <= 0):
            print ("I Am Dead!")
        return [counter, choice(godsHome)]
    
if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ZeusService, port=18861)
    t.start()
