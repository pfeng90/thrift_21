import sys, glob
sys.path.append('./gen-py')
import time

#from HelloService import HelloService
#from HelloService.HelloService import Processor

#from HelloService.ttypes import *

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from op.ttypes import PokerColor, Poker
from op.ReqService import Processor
import random
'''
class HelloServiceHandler:
    def __init__(self):
        self.log = {}
        print('create HelloServiceHandler')
    def func1(self):
        print('func1')
    def sayHello(self):
        #time.sleep(1)
        print("sayHello")
    def getData(self,input):
        return input + 'from server 1024'

class PokerColor(object):
    diamond = 0
    club = 1
    heart = 2
    spade = 3
class Poker(object):
    def __init__(self):
        self.v = 1
        self.t = PokerColor.diamond

    def __init__(self, v, t):
        self.v = v
        self.t = t

    def __add__(self, p):
        return self.v + p.v
    def __lt__(self, p):
        return self.v < p.v
    def __gt__(self, p):
        return self.v > p.v
'''
class OPHandler:
    def __init__(self): 
         self.pokers=[]
         self.cardsNum = 0
        #self.generatePokers()

    def generatePokers(self):
        self.pokers=[]        
        for i in range(14):
            for j in range(4):
                self.pokers.append(Poker(i, j))
        self.cardsNum = len(self.pokers)

    def randomOnePoker(self):
        index = random.randint(0, self.cardsNum)
        poker = self.pokers[index]
        del self.pokers[index]
        self.cardsNum -= 1
        return poker

    def login(self,name,pw):
        print('login with (name,pw) = (%s,%s)'%(name, pw))
        return True

    def startPlay(self):
        print('start play')
        self.generatePokers()

    def dealCards(self):
        print(dir(self))
        if self.cardsNum >=2 :
            one = self.randomOnePoker()
            two = self.randomOnePoker()
            return [one, two]
        print('dealCards')

    def askForCards(self):
        if self.cardsNum >= 1 :
            return self.randomOnePoker()
        print('askForCards')

class LogProcessor(Processor):
    def __init__(self, handler):
       super(LogProcessor, self).__init__(handler)

    def process(self, iprot, oprot):
        super(LogProcessor, self).process(iprot, oprot)
        print 'process end'
        print ('iprot.trans', iprot.trans)
        #print ('iprot.trans', iprot.trans.sock)
        

       
handler = OPHandler()
#processor = HelloService.Processor(handler)
processor = LogProcessor(handler)
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

print('starting the server')
server.serve()
print('server end')

