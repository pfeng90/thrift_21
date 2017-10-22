# -*- coding: utf-8 -*-
import sys
sys.path.append('./gen-py')
import time
#from HelloService import HelloService
#from HelloService.ttypes import *
from op import ReqService
from op.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

def showMenu():
    print(u'\t\t\t\t 1,开始')
    print(u'\t\t\t\t 2,发牌')
    print(u'\t\t\t\t 3,要牌')
    print(u'\t\t\t\t 4,结束')
    try:
        num = raw_input('choose:')
        choose = int(num)
        if choose and choose <=4 and choose >= 1:
            #print('user choose %d'% choose)
            return choose
        else:
            print('error input,choose again!\n\n')
            return showMenu()
    except Exception, e:
        print('error input,choose again!\n\n')
        return showMenu()
class HandPoker(object):
    def __init__(self):
        self.handPokers = []
        self.points = 0
    def add(self, poker):
        self.points = self.points + poker.v
        if self.points < 21:
            self.handPokers.append(poker)
            return True
        else:
            print('exceed 21 game over, points is ',self.points)
            return False
    def showHandPoker(self):
        for p in self.handPokers:
            print("p(%d,%d)"%(p.v, p.t))

def run():
    try:
        handpoker = None
        state = 0
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = ReqService.Client(protocol)
        #print(dir(client))
        transport.open()
        choose = showMenu()
        print('first chosoe %d'% choose)
        while(True):            
            if choose == 1 and state == 0:
                state = choose
                client.startPlay()
                handpoker = HandPoker()
                print('game start,next deal poker!')
            elif choose == 2:
                if state == 1:
                    state = choose
                    towPokers = client.dealCards()
                    print('deal cards finished!')
                    print(towPokers)
                    if handpoker:
                        for p in towPokers:
                            handpoker.add(p)
                        handpoker.showHandPoker()
                    else:
                        print('please first startPlay!')

            elif choose == 3 and state == 2:
                p = client.askForCards()
                print('server give one card ', p)
                if handpoker:
                    if(handpoker.add(p)):
                        handpoker.showHandPoker()
                    else:
                        handpoker.showHandPoker()
                        print('game over')
                        break
                else:
                    print('please first startPlay!')
            elif choose == 4:
                print('game over')
                break
                
            choose = showMenu()            
        '''
        print(client.login('pfeng','123456'))
        for i in range(1):
            print('ping()')
            client.startPlay()
            pokers = client.dealCards()
            print('pokers', pokers)
            poker = client.askForCards()
            print('poker', poker)
            #print(client.getData('client access'))
            #time.sleep(1)
        '''
        transport.close()
    except Thrift.TException, tx:
        print('exception:%s'% tx.message)

if __name__ == '__main__':
    #showMenu()
    run()
