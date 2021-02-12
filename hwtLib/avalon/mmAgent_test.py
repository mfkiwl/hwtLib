#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from hwt.interfaces.utils import addClkRstn
from hwt.simulator.simTestCase import SingleUnitSimTestCase
from hwt.synthesizer.unit import Unit
from hwtLib.avalon.mm import AvalonMM, RESP_OKAY
from hwtSimApi.constants import CLK_PERIOD
from hwt.hdl.constants import READ, WRITE
from pyMathBitPrecise.bit_utils import mask


class AvalonMmWire(Unit):

    def _declr(self):
        addClkRstn(self)
        self.dataIn = AvalonMM()
        self.dataOut = AvalonMM()._m()

    def _impl(self):
        self.dataOut(self.dataIn)


class AvalonMmAgentTC(SingleUnitSimTestCase):

    @classmethod
    def getUnit(cls):
        cls.u = AvalonMmWire()
        return cls.u

    def test_nop(self):
        u = self.u
        self.runSim(10 * CLK_PERIOD)

        self.assertEmpty(u.dataOut._ag.req)
        self.assertEmpty(u.dataOut._ag.wData)
        self.assertEmpty(u.dataIn._ag.rData)
        self.assertEmpty(u.dataIn._ag.wResp)

    def test_pass_data(self, N=8):
        assert N % 2 == 0, N
        u = self.u
        m = mask(u.dataIn.DATA_WIDTH // 8)

        # rw, address, burstCount
        inAddr = [
            (READ if (i % 2) == 0 else WRITE, 0x1 + i, 1)
            for i in range(N)
        ]
        u.dataIn._ag.req.extend(inAddr)
        # d, be
        inW = [
            (i + 1, m)
            for i in range(N // 2)
        ]
        u.dataIn._ag.wData.extend(inW)

        # readData, response
        inR = [
            (i + 1, RESP_OKAY)
            for i in range(N // 2)
        ]
        u.dataOut._ag.rData.extend(inR)
        inWResp = [RESP_OKAY for _ in range(N // 2)]
        u.dataOut._ag.wResp.extend(inWResp)

        t = N + 5
        self.runSim(t * CLK_PERIOD)

        ae = self.assertValSequenceEqual
        ae(u.dataOut._ag.req, inAddr)
        ae(u.dataOut._ag.wData, inW)
        ae(u.dataIn._ag.rData, inR)
        ae(u.dataIn._ag.wResp, inWResp)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(HsFifoTC('test_passdata'))
    suite.addTest(unittest.makeSuite(AvalonMmAgentTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
