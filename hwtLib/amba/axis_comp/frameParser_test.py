#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from hwt.hdl.constants import Time
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.stream import HStream
from hwt.hdl.types.struct import HStruct
from hwt.interfaces.structIntf import StructIntf
from hwt.pyUtils.testUtils import TestMatrix
from hwt.simulator.simTestCase import SimTestCase
from hwtLib.amba.axis import packAxiSFrame, \
    unpackAxiSFrame, axis_recieve_bytes
from hwtLib.amba.axis_comp.frameForge_test import unionOfStructs, unionSimple
from hwtLib.amba.axis_comp.frameParser import AxiS_frameParser
from hwtLib.types.ctypes import uint64_t, uint16_t, uint32_t
from pycocotb.constants import CLK_PERIOD


structManyInts = HStruct(
    (uint64_t, "i0"),
    (uint64_t, None),  # dummy word
    (uint64_t, "i1"),
    (uint64_t, None),
    (uint16_t, "i2"),
    (uint16_t, "i3"),
    (uint32_t, "i4"),  # 3 items in one word

    (uint32_t, None),
    (uint64_t, "i5"),  # this word is split on two bus words
    (uint32_t, None),

    (uint64_t, None),
    (uint64_t, None),
    (uint64_t, None),
    (uint64_t, "i6"),
    (uint64_t, "i7"),
)

MAGIC = 14
ref0_structManyInts = {
    "i0": MAGIC + 1,
    "i1": MAGIC + 2,
    "i2": MAGIC + 3,
    "i3": MAGIC + 4,
    "i4": MAGIC + 5,
    "i5": MAGIC + 6,
    "i6": MAGIC + 7,
    "i7": MAGIC + 8,
}
ref1_structManyInts = {
    "i0": MAGIC + 10,
    "i1": MAGIC + 20,
    "i2": MAGIC + 30,
    "i3": MAGIC + 40,
    "i4": MAGIC + 50,
    "i5": MAGIC + 60,
    "i6": MAGIC + 70,
    "i7": MAGIC + 80,
}


ref_unionOfStructs0 = (
    "frameA", {
        "itemA0": MAGIC + 1,
        "itemA1": MAGIC + 2,
    },
)

ref_unionOfStructs1 = (
    "frameA", {
        "itemA0": MAGIC + 10,
        "itemA1": MAGIC + 20,
    },
)

ref_unionOfStructs2 = (
    "frameB", {
        "itemB0": MAGIC + 3,
        "itemB1": MAGIC + 4,
        "itemB2": MAGIC + 5,
        "itemB3": MAGIC + 6,
    }
)

ref_unionOfStructs3 = (
    "frameB", {
        "itemB0": MAGIC + 30,
        "itemB1": MAGIC + 40,
        "itemB2": MAGIC + 50,
        "itemB3": MAGIC + 60,
    }
)


ref_unionSimple0 = ("a", MAGIC + 1)
ref_unionSimple1 = ("a", MAGIC + 10)
ref_unionSimple2 = ("b", MAGIC + 2)
ref_unionSimple3 = ("b", MAGIC + 20)


TEST_DW = [
    15, 16, 32, 51, 64,
    128, 512
]
RAND_FLAGS = [
    False,
    True
]


testMatrix = TestMatrix(TEST_DW, RAND_FLAGS)


class AxiS_frameParserTC(SimTestCase):

    def setDown(self):
        self.rtl_simulator_cls = None
        super(AxiS_frameParserTC, self).setDown()

    def randomizeIntf(self, intf):
        if isinstance(intf, StructIntf):
            for _intf in intf._interfaces:
                self.randomizeIntf(_intf)
        else:
            self.randomize(intf)

    def mySetUp(self, dataWidth, structTemplate, randomize=False,
                use_strb=False, use_keep=False):
        u = AxiS_frameParser(structTemplate)
        u.USE_STRB = use_strb
        u.USE_KEEP = use_keep
        u.DATA_WIDTH = dataWidth
        if self.DEFAULT_BUILD_DIR is not None:
            # because otherwise files gets mixed in parralel test execution
            unique_name = "%s_%s_dw%d_r%d" % (self.getTestName(),
                                              u._getDefaultName(),
                                              dataWidth,
                                              randomize)
            build_dir = os.path.join(self.DEFAULT_BUILD_DIR,
                                     self.getTestName() + unique_name)
        else:
            unique_name = None
            build_dir = None
        self.compileSimAndStart(u, unique_name=unique_name,
                                build_dir=build_dir)
        # because we want to prevent resuing of this class in TestCase.setUp()
        self.__class__.rtl_simulator_cls = None
        if randomize:
            self.randomizeIntf(u.dataIn)
            self.randomizeIntf(u.dataOut)
        return u

    def test_packAxiSFrame(self):
        t = structManyInts
        for DW in TEST_DW:
            d1 = t.from_py(ref0_structManyInts)
            f = list(packAxiSFrame(DW, d1))
            d2 = unpackAxiSFrame(t, f, lambda x: x[0])

            for k in ref0_structManyInts.keys():
                self.assertEqual(getattr(d1, k), getattr(d2, k), (DW, k))

    def runMatrixSim(self, time, dataWidth, randomize):
        unique_name = self.getTestName() + ("_dw%d_r%d" % (dataWidth, randomize))
        self.runSim(time, name="tmp/" + unique_name + ".vcd")

    @testMatrix
    def test_structManyInts_nop(self, dataWidth, randomize):
        u = self.mySetUp(dataWidth, structManyInts, randomize)

        self.runMatrixSim(30 * CLK_PERIOD, dataWidth, randomize)
        for intf in u.dataOut._interfaces:
            self.assertEmpty(intf._ag.data)

    @testMatrix
    def test_structManyInts_2x(self, dataWidth, randomize):
        t = structManyInts
        u = self.mySetUp(dataWidth, t, randomize)

        u.dataIn._ag.data.extend(packAxiSFrame(
            dataWidth, t.from_py(ref0_structManyInts)))
        u.dataIn._ag.data.extend(packAxiSFrame(
            dataWidth, t.from_py(ref1_structManyInts)))

        if randomize:
            # {DW: t}
            ts = {
                15: 300,
                16: 240,
                32: 300,
                51: 160,
                64: 160,
                128: 110,
                512: 90,
            }
            t = ts[dataWidth] * CLK_PERIOD
        else:
            t = ((8 * 64) / dataWidth) * 8 * CLK_PERIOD
        self.runMatrixSim(t, dataWidth, randomize)

        for intf in u.dataOut._interfaces:
            n = intf._name
            d = [ref0_structManyInts[n], ref1_structManyInts[n]]
            self.assertValSequenceEqual(intf._ag.data, d, n)

    @testMatrix
    def test_unionOfStructs_nop(self, dataWidth, randomize):
        t = unionOfStructs
        u = self.mySetUp(dataWidth, t, randomize)
        t = 15 * CLK_PERIOD

        self.runMatrixSim(t, dataWidth, randomize)
        for i in [u.dataOut.frameA, u.dataOut.frameB]:
            for intf in i._interfaces:
                self.assertEmpty(intf._ag.data)

    @testMatrix
    def test_unionOfStructs_noSel(self, dataWidth, randomize):
        t = unionOfStructs
        u = self.mySetUp(dataWidth, t, randomize)

        for d in [ref_unionOfStructs0, ref_unionOfStructs2]:
            u.dataIn._ag.data.extend(packAxiSFrame(dataWidth, t.from_py(d)))

        t = 15 * CLK_PERIOD
        self.runMatrixSim(t, dataWidth, randomize)

        for i in [u.dataOut.frameA, u.dataOut.frameB]:
            for intf in i._interfaces:
                self.assertEmpty(intf._ag.data)

    @testMatrix
    def test_unionOfStructs(self, dataWidth, randomize):
        t = unionOfStructs
        u = self.mySetUp(dataWidth, t, randomize)

        for d in [ref_unionOfStructs0, ref_unionOfStructs2,
                  ref_unionOfStructs1, ref_unionOfStructs3]:
            u.dataIn._ag.data.extend(packAxiSFrame(dataWidth, t.from_py(d)))
        u.dataOut._select._ag.data.extend([0, 1, 0, 1])

        if randomize:
            # {DW: t}
            ts = {
                15: 200,
                16: 280,
                32: 200,
                51: 90,
                64: 100,
                128: 130,
                512: 50,
            }
            t = ts[dataWidth] * CLK_PERIOD
        else:
            t = 50 * CLK_PERIOD
        self.runMatrixSim(t, dataWidth, randomize)

        for i in [u.dataOut.frameA, u.dataOut.frameB]:
            if i._name == "frameA":
                v0 = ref_unionOfStructs0[1]
                v1 = ref_unionOfStructs1[1]
            else:
                v0 = ref_unionOfStructs2[1]
                v1 = ref_unionOfStructs3[1]

            for intf in i._interfaces:
                n = intf._name
                vals = v0[n], v1[n]
                self.assertValSequenceEqual(intf._ag.data, vals, (i._name, n))

    @testMatrix
    def test_simpleUnion(self, dataWidth, randomize):
        t = unionSimple
        u = self.mySetUp(dataWidth, t, randomize)

        for d in [ref_unionSimple0, ref_unionSimple2,
                  ref_unionSimple1, ref_unionSimple3]:
            u.dataIn._ag.data.extend(packAxiSFrame(dataWidth, t.from_py(d)))
        u.dataOut._select._ag.data.extend([0, 1, 0, 1])

        t = 300 * Time.ns
        if randomize:
            # {DW: t}
            ts = {
                15: 80,
                16: 55,
                32: 85,
                51: 45,
                64: 70,
                128: 20,
                512: 65,
            }
            t = ts[dataWidth] * 2 * CLK_PERIOD
        self.runMatrixSim(t, dataWidth, randomize)

        for i in [u.dataOut.a, u.dataOut.b]:
            if i._name == "a":
                v0 = ref_unionSimple0[1]
                v1 = ref_unionSimple1[1]
            else:
                v0 = ref_unionSimple2[1]
                v1 = ref_unionSimple3[1]

            self.assertValSequenceEqual(i._ag.data, [v0, v1], i._name)

    def runMatrixSim2(self, t, dataWidth, frame_len, randomize):
        unique_name = self.getTestName() + (
            "_dw%d_len%d_r%d" % (dataWidth, frame_len, randomize))
        self.runSim(t * CLK_PERIOD, name="tmp/" + unique_name + ".vcd")

    @TestMatrix([8, 16, 32], [1, 2, 5], [False, True])
    def test_const_size_stream(self, dataWidth, frame_len, randomize):
        T = HStruct(
            (HStream(Bits(8), frame_len=frame_len), "frame0"),
            (uint16_t, "footer"),
        )
        u = self.mySetUp(dataWidth, T, randomize, use_strb=True)
        u.dataIn._ag.data.extend(
            packAxiSFrame(dataWidth,
                          T.from_py({"frame0": [i + 1 for i in range(frame_len)],
                                     "footer": 2}),
                          withStrb=True,
                          )
            )
        t = 20
        if randomize:
            t *= 3

        self.runMatrixSim2(t, dataWidth, frame_len, randomize)
        off, f = axis_recieve_bytes(u.dataOut.frame0)
        self.assertEqual(off, 0)
        self.assertValSequenceEqual(f, [i + 1 for i in range(frame_len)])
        self.assertValSequenceEqual(u.dataOut.footer._ag.data, [2])

    # @TestMatrix([8, 16, 32], [1, 2, 5], [False, True])
    # def test_stream_and_footer(self, dataWidth, frame_len, randomize):
    #     T = HStruct(
    #         (HStream(Bits(8)), "frame0"),
    #         (uint16_t, "footer"),
    #     )
    #     u = self.mySetUp(dataWidth, T, randomize, use_strb=True)
    #     u.dataIn._ag.data.extend(
    #         packAxiSFrame(dataWidth,
    #                       T.from_py({"frame0": [i + 1 for i in range(frame_len)],
    #                                  "footer": 2}),
    #                       withStrb=True,
    #                       )
    #         )
    #     t = 20
    #     if randomize:
    #         t *= 3
    # 
    #     self.runMatrixSim2(t, dataWidth, frame_len, randomize)
    # 
    #     off, f = axis_recieve_bytes(u.dataOut.frame0)
    #     self.assertEqual(off, 0)
    #     self.assertValSequenceEqual(f, [i + 1 for i in range(frame_len)])
    #     self.assertValSequenceEqual(u.dataOut.footer._ag.data, [2])


if __name__ == "__main__":
    import unittest
    suite = unittest.TestSuite()
    # suite.addTest(AxiS_frameParserTC('test_simpleUnion'))
    suite.addTest(unittest.makeSuite(AxiS_frameParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
