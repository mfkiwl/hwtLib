#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.hdlObjects.constants import Time, READ, WRITE, NOP
from hwtLib.abstract.discoverAddressSpace import AddressSpaceProbe
from hwtLib.amba.axiLite_comp.structEndpoint_test import AxiLiteStructEndpointTC, \
    AxiLiteStructEndpointArray, structTwoFieldsDense, structTwoFieldsDenseStart
from hwtLib.ipif.simMaster import IPFISimMaster
from hwtLib.ipif.structEndpoint import IpifStructEndpoint
from hwt.interfaces.std import BramPort_withoutClk
from hwtLib.ipif.intf import IPIF


def addrGetter(intf):
    if isinstance(intf, IPIF):
        return intf.bus2ip_addr
    elif isinstance(intf, BramPort_withoutClk):
        return intf.addr
    else:
        raise TypeError(intf)

class IPIFStructEndpointTC(AxiLiteStructEndpointTC):
    FIELD_ADDR = [0x0, 0x4]

    def mkRegisterMap(self, u):
        registerMap = AddressSpaceProbe(u.bus, addrGetter).discover()
        self.registerMap = registerMap
        self.regs = IPFISimMaster(u.bus, registerMap)

    def mySetUp(self, data_width=32):
        u = self.u = IpifStructEndpoint(self.STRUCT_TEMPLATE)

        self.DATA_WIDTH = data_width
        u.DATA_WIDTH.set(self.DATA_WIDTH)

        self.prepareUnit(self.u, onAfterToRtl=self.mkRegisterMap)
        return u

    def randomizeAll(self):
        pass

    def test_nop(self):
        u = self.mySetUp(32)

        self.randomizeAll()
        self.doSim(100 * Time.ns)

        self.assertEmpty(u.bus._ag.readed)
        self.assertIs(u.bus._ag.actual, NOP)
        self.assertEmpty(u.field0._ag.dout)
        self.assertEmpty(u.field1._ag.dout)

    def test_read(self):
        u = self.mySetUp(32)
        MAGIC = 100
        A = self.FIELD_ADDR
        u.bus._ag.requests.extend([(READ, A[0]),
                                   (READ, A[1]),
                                   (READ, A[0]),
                                   (READ, A[1])
                                   ])

        u.field0._ag.din.append(MAGIC)
        u.field1._ag.din.append(MAGIC + 1)

        self.randomizeAll()
        self.doSim(300 * Time.ns)

        self.assertValSequenceEqual(u.bus._ag.readed, [MAGIC,
                                                       MAGIC + 1,
                                                       MAGIC,
                                                       MAGIC + 1])

    def test_write(self):
        u = self.mySetUp(32)
        MAGIC = 100
        A = self.FIELD_ADDR
        u.bus._ag.requests.extend([
            (WRITE, A[0], MAGIC),
            (WRITE, A[1], MAGIC + 1),
            (WRITE, A[0], MAGIC + 2),
            (WRITE, A[1], MAGIC + 3)])

        self.randomizeAll()
        self.doSim(400 * Time.ns)

        self.assertValSequenceEqual(u.field0._ag.dout, [MAGIC,
                                                        MAGIC + 2
                                                        ])
        self.assertValSequenceEqual(u.field1._ag.dout, [MAGIC + 1,
                                                        MAGIC + 3
                                                        ])


class IPIFStructEndpointDenseTC(IPIFStructEndpointTC):
    STRUCT_TEMPLATE = structTwoFieldsDense
    FIELD_ADDR = [0x0, 0x8]
    

class IPIFStructEndpointStartTC(IPIFStructEndpointTC):
    STRUCT_TEMPLATE = structTwoFieldsDenseStart
    FIELD_ADDR = [0x4, 0x8]


class IPIFStructEndpointOffsetTC(IPIFStructEndpointTC):
    FIELD_ADDR = [0x4, 0x8]

    def mySetUp(self, data_width=32):
        u = self.u = IpifStructEndpoint(self.STRUCT_TEMPLATE, offset=0x4)

        self.DATA_WIDTH = data_width
        u.DATA_WIDTH.set(self.DATA_WIDTH)

        self.prepareUnit(self.u, onAfterToRtl=self.mkRegisterMap)
        return u

class IPIFStructEndpointArray(AxiLiteStructEndpointArray):
    FIELD_ADDR = [0x0, 0x10]
    mkRegisterMap = IPIFStructEndpointTC.mkRegisterMap
    mySetUp = IPIFStructEndpointTC.mySetUp

    def randomizeAll(self):
        pass


    def test_nop(self):
        u = self.mySetUp(32)
        MAGIC = 100

        for i in range(8):
            u.field0._ag.mem[i] = MAGIC + 1 + i
            u.field1._ag.mem[i] = 2 * MAGIC + 1 + i

        self.randomizeAll()
        self.doSim(100 * Time.ns)

        self.assertEmpty(u.bus._ag.readed)
        for i in range(8):
            self.assertValEqual(u.field0._ag.mem[i], MAGIC + 1 + i)
            self.assertValEqual(u.field1._ag.mem[i], 2 * MAGIC + 1 + i)

    def test_read(self):
        u = self.mySetUp(32)
        # u.bus._ag._debug(sys.stdout)
        regs = self.regs
        MAGIC = 100
        # u.bus._ag.requests.append(NOP)
        for i in range(4):
            u.field0._ag.mem[i] = MAGIC + i + 1
            u.field1._ag.mem[i] = 2 * MAGIC + i + 1
            regs.field0.read(i, None)
            regs.field1.read(i, None)

        self.randomizeAll()
        self.doSim(200 * Time.ns)

        self.assertValSequenceEqual(u.bus._ag.readed, [
            MAGIC + 1,
            2 * MAGIC + 1,
            MAGIC + 2,
            2 * MAGIC + 2,
            MAGIC + 3,
            2 * MAGIC + 3,
            MAGIC + 4,
            2 * MAGIC + 4,
            ])

    def test_write(self):
        u = self.mySetUp(32)
        regs = self.regs
        MAGIC = 100

        for i in range(4):
            u.field0._ag.mem[i] = None
            u.field1._ag.mem[i] = None
            regs.field0.write(i, MAGIC + i + 1)
            regs.field1.write(i, 2 * MAGIC + i + 1)

        self.randomizeAll()
        self.doSim(400 * Time.ns)

        self.assertEmpty(u.bus._ag.readed)
        for i in range(4):
            self.assertValEqual(u.field0._ag.mem[i], MAGIC + i + 1, "index=%d" % i)
            self.assertValEqual(u.field1._ag.mem[i], 2 * MAGIC + i + 1, "index=%d" % i)






if __name__ == "__main__":
    import unittest
    suite = unittest.TestSuite()

    # suite.addTest(IPIFStructEndpointArray('test_read'))
    suite.addTest(unittest.makeSuite(IPIFStructEndpointTC))
    suite.addTest(unittest.makeSuite(IPIFStructEndpointDenseTC))
    suite.addTest(unittest.makeSuite(IPIFStructEndpointStartTC))
    suite.addTest(unittest.makeSuite(IPIFStructEndpointOffsetTC))
    suite.addTest(unittest.makeSuite(IPIFStructEndpointArray))

    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)