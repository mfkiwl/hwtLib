#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.interfaces.utils import addClkRstn, propagateClkRstn
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit

from hwtLib.amba.axis import AxiStream
from hwtLib.examples.hierarchy.simpleSubunit2 import SimpleSubunit2TC
from hwtLib.examples.simple2withNonDirectIntConnection import Simple2withNonDirectIntConnection


class UnitToUnitConnection(Unit):
    """
    .. hwt-autodoc::
    """
    def _config(self):
        self.DATA_WIDTH = Param(8)
        self.USE_STRB = Param(True)

    def _declr(self):
        addClkRstn(self)
        with self._paramsShared():
            self.a0 = AxiStream()
            self.b0 = AxiStream()._m()

            self.u0 = Simple2withNonDirectIntConnection()
            self.u1 = Simple2withNonDirectIntConnection()

    def _impl(self):
        propagateClkRstn(self)
        self.u0.a(self.a0)
        self.u1.a(self.u0.c)
        self.b0(self.u1.c)


class UnitToUnitConnectionTC(SimpleSubunit2TC):

    @classmethod
    def setUpClass(cls):
        cls.u = UnitToUnitConnection()
        cls.compileSim(cls.u)

if __name__ == "__main__":
    from hwt.synthesizer.utils import to_rtl_str
    u = UnitToUnitConnection()
    print(to_rtl_str(u))
