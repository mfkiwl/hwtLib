from hwt.simulator.simTestCase import SimTestCase
from hwtLib.amba.axi4_streamToMem import Axi4streamToMem
from hwtLib.abstract.discoverAddressSpace import AddressSpaceProbe
from hwtLib.amba.sim.axiMemSpaceMaster import AxiLiteMemSpaceMaster
from hwt.hdlObjects.constants import Time


class Axi4_streamToMemTC(SimTestCase):
    def setUp(self):
        SimTestCase.setUp(self)

        u = self.u = Axi4streamToMem()

        def mkRegisterMap(u):
            registerMap = AddressSpaceProbe(u.cntrlBus,
                                            lambda intf: intf.ar.addr)\
                                            .discover()
            self.regs = AxiLiteMemSpaceMaster(u.cntrlBus, registerMap)

        self.DATA_WIDTH = 32
        u.DATA_WIDTH.set(self.DATA_WIDTH)

        self.prepareUnit(self.u, onAfterToRtl=mkRegisterMap)

    def test_nop(self):
        u = self.u

        self.doSim(100 * Time.ns)

        self.assertEmpty(u.axi.ar._ag.data)
        self.assertEmpty(u.axi.aw._ag.data)
        self.assertEmpty(u.axi.w._ag.data)


if __name__ == "__main__":
    import unittest
    suite = unittest.TestSuite()
    # suite.addTest(Axi4_streamToMemTC('test_endstrbMultiFrame'))
    suite.addTest(unittest.makeSuite(Axi4_streamToMemTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)