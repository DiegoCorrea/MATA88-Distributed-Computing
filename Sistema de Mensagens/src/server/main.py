import logging
import rpyc
import sys, os
sys.path.append('..')
from server import ServerService
from rpyc.utils.server import ThreadedServer

if __name__ == "__main__":
    os.system('cls||clear')
    logging.basicConfig(filename='log/server.log', filemode='w',level=logging.DEBUG)
    logging.info('*************** Iniciando Aplicacao ***************')
    t = ThreadedServer(ServerService, port=27000)
    t.start()
    logging.info('*************** Finalizando Aplicacao ***************')
