import os
import unittest

from hwt.serializer.hwt.serializer import HwtSerializer
from hwt.serializer.systemC.serializer import SystemCSerializer
from hwt.serializer.verilog.serializer import VerilogSerializer
from hwt.serializer.vhdl.serializer import Vhdl2008Serializer
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import to_rtl_str
from hwtLib.tests.statementTrees import StatementTreesTC


class BaseSerializationTC(unittest.TestCase):
    # file should be set on child class because we want the pats in tests
    # to be raltive to a current test case
    __FILE__ = None
    SERIALIZER_BY_EXT = {
        "v": VerilogSerializer,
        "vhd": Vhdl2008Serializer,
        "cpp": SystemCSerializer,
        "py": HwtSerializer,
    }

    def assert_serializes_as_file(self, u: Unit, file_name: str):
        ser = self.SERIALIZER_BY_EXT[file_name.split(".")[-1]]
        s = to_rtl_str(u, serializer_cls=ser)
        self.assert_same_as_file(s, file_name)

    def assert_same_as_file(self, s, file_name: str):
        assert self.__FILE__ is not None, "This should be set on child class"
        THIS_DIR = os.path.dirname(os.path.realpath(self.__FILE__))
        fn = os.path.join(THIS_DIR, file_name)
        # with open(fn, "w") as f:
        #     f.write(s)
        with open(fn) as f:
            ref_s = f.read()
        StatementTreesTC.strStructureCmp(self, s, ref_s)
