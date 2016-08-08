import unittest

from hdl_toolkit.hdlObjects.specialValues import WRITE, READ
from hdl_toolkit.simulator.agentConnector import autoAddAgents, valuesToInts
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.simulator.shortcuts import simUnitVcd
from hdl_toolkit.synthetisator.shortcuts import synthesised
from hwtLib.mem.lutRam import RAM64X1S
from hdl_toolkit.bitmask import Bitmask


def applyRequests(ram, requests):
    """
    request has to be tuple (WRITE, addr, data) or (READ, addr)
    data can be only 0 or 1 (because width of data port is 1)
    """
    for req in requests:
        m = req[0] 
        if  m == WRITE:
            data = req[2]
            assert data == 1 or data == 0
            ram.d._ag.data.append(data)
            ram.we._ag.data.append(1)
        elif m == READ:
            ram.we._ag.data.append(0)
        else:
            raise Exception("invalid mode %s" % (repr(req[0])))
        
        addr = req[1]
        # ram addr has 6 bits
        for i in range(6):
            addrbit = getattr(ram, "a%d" % i)
            addrBitval = Bitmask.select(addr, i)
            addrbit._ag.data.append(addrBitval)
    
    

class LutRamTC(unittest.TestCase):

    def test_writeAndRead(self):
        u = RAM64X1S()

        synthesised(u)
        procs = autoAddAgents(u)

        requests = [(WRITE, 0, 0), (WRITE, 1, 1),
                    (READ, 0), (READ, 1),
                    (READ, 2), (READ, 3), (READ, 2)] 
        applyRequests(u, requests)
        
        
        simUnitVcd(u, procs,
                   "tmp/lutRam_writeAndRead.vcd", time=80 * HdlSimulator.ns)
        self.assertSequenceEqual(valuesToInts(u.o._ag.data), [0, 0, 0, 1, 0, 0, 0, 0])

        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(TwoCntrsTC('test_withStops'))
    suite.addTest(unittest.makeSuite(LutRamTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)