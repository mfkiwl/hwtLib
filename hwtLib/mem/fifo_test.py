#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from hwt.hdl.constants import Time
from hwt.simulator.agentConnector import agInts
from hwt.simulator.simTestCase import SimTestCase
from hwtLib.mem.fifo import Fifo


class FifoTC(SimTestCase):
    def setUp(self):
        u = self.u = Fifo()
        u.DATA_WIDTH.set(8)
        u.DEPTH.set(4)
        u.EXPORT_SIZE.set(True)
        self.prepareUnit(u)

    def getTime(self, wordCnt):
        return wordCnt * 10 * Time.ns

    def test_fifoSingleWord(self):
        u = self.u

        expected = [1]
        u.dataIn._ag.data.extend(expected)

        self.doSim(90 * Time.ns)

        collected = u.dataOut._ag.data

        self.assertValSequenceEqual(collected, expected)

    def test_fifoWritterDisable(self):
        u = self.u

        data = [1, 2, 3, 4]
        u.dataIn._ag.data.extend(data)
        u.dataIn._ag.enable = False

        self.doSim(self.getTime(8))

        self.assertValSequenceEqual(u.dataOut._ag.data, [])
        self.assertValSequenceEqual(u.dataIn._ag.data, data)

    def test_normalOp(self):
        u = self.u

        expected = list(range(4))
        u.dataIn._ag.data.extend(expected)

        self.doSim(self.getTime(9))

        self.assertValSequenceEqual(u.dataOut._ag.data, expected)

    def test_multiple(self):
        u = self.u
        u.dataOut._ag.enable = False

        def openOutput(s):
            yield s.wait(self.getTime(9))
            u.dataOut._ag.enable = True
        self.procs.append(openOutput)

        expected = list(range(2 * 8))
        u.dataIn._ag.data.extend(expected)

        self.doSim(self.getTime(26))

        collected = u.dataOut._ag.data
        if u.EXPORT_SIZE:
            self.assertValSequenceEqual(u.size._ag.data,
                [0, 0, 1, 2, 3, 4, 4, 4, 4, 4,
                 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0])

        self.assertValSequenceEqual(collected, expected)

    def test_tryMore(self):
        u = self.u

        u.dataIn._ag.data.extend([1, 2, 3, 4, 5, 6])
        u.dataOut._ag.enable = False

        self.doSim(self.getTime(12))

        collected = agInts(u.dataOut)

        self.assertValSequenceEqual(self.model.memory._val, [1, 2, 3, 4])
        self.assertValSequenceEqual(collected, [])
        self.assertValSequenceEqual(u.dataIn._ag.data, [5, 6])

    def test_tryMore2(self):
        u = self.u

        u.dataIn._ag.data.extend([1, 2, 3, 4, 5, 6, 7, 8])

        def closeOutput(s):
            yield s.wait(self.getTime(4))
            u.dataOut._ag.enable = False

        self.procs.append(closeOutput)
        self.doSim(self.getTime(15))

        collected = agInts(u.dataOut)

        self.assertValSequenceEqual(self.model.memory._val.val, [5, 6, 3, 4])
        self.assertSequenceEqual(collected, [1, 2])
        self.assertSequenceEqual(u.dataIn._ag.data, [7, 8])

    def test_doloop(self):
        u = self.u
        u.dataIn._ag.data.extend([1, 2, 3, 4, 5, 6])

        self.doSim(self.getTime(12))

        collected = agInts(u.dataOut)
        self.assertSequenceEqual([1, 2, 3, 4, 5, 6], collected)
        self.assertSequenceEqual([], u.dataIn._ag.data)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(FifoTC('test_normalOp'))
    suite.addTest(unittest.makeSuite(FifoTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
