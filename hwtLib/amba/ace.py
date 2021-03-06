from hwt.interfaces.std import VectSignal, Signal
from hwt.synthesizer.param import Param
from hwtLib.amba.axi3Lite import Axi3Lite_bAgent
from hwtLib.amba.axi4 import Axi4, Axi4_addr
from hwtLib.amba.axi_intf_common import Axi_hs
from hwtSimApi.hdlSimulator import HdlSimulator
from ipCorePackager.constants import DIRECTION


class DOMAIN():
    NON_SHARABLE = 0
    INNER_SHARABLE = 1
    OUTER_SHARABLE = 2
    SYSTEM = 3


class CACHE():
    DEVICE = 0
    NON_CACHEABLE = 0b0011
    WRITE_THROUGH = 0b0111
    WRITE_BACK = 0b1011


class BAR():
    NORMAL = 0b00
    BARRIER = 0b01
    IGNORE = 0b10
    SYNCHRONIZATION = 0b11


class AR_MODE():

    class NO_SNOOP():

        class READ():
            NON = (BAR.NORMAL, DOMAIN.NON_SHARABLE, 0b0000)
            SYSTEM = (BAR.NORMAL, DOMAIN.SYSTEM, 0b0000)

    class COHERENT():

        class READ_ONCE():
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b0000)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b0000)

        class READ_SHARED():
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b0001)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b0001)

        class READ_CLEAN():
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b0010)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b0010)

        class READ_NOT_SHARED_DIRTY():
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b0011)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b0011)

        class READ_UNIQUE():
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b0111)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b0111)

        class CLEAN_UNIQUE():
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b1011)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b1011)

        class MAKE_UNIQUE():
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b1100)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b1100)

    class CACHE_MAINTENANCE():

        class CLEAN_SHARED():
            NON = (BAR.NORMAL, DOMAIN.NON_SHARABLE, 0b1000)
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b1000)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b1000)

        class CLEAN_INVALID():
            NON = (BAR.NORMAL, DOMAIN.NON_SHARABLE, 0b1001)
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b1001)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b1001)

        class MAKE_INVALID():
            NON = (BAR.NORMAL, DOMAIN.NON_SHARABLE, 0b1101)
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b1101)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b1101)

    class BARRIER():
        NON = (BAR.BARRIER, DOMAIN.NON_SHARABLE, 0b0000)
        INNER = (BAR.BARRIER, DOMAIN.INNER_SHARABLE, 0b0000)
        OUTER = (BAR.BARRIER, DOMAIN.OUTER_SHARABLE, 0b0000)
        SYSTEM = (BAR.BARRIER, DOMAIN.SYSTEM, 0b0000)

    class DVM():

        class COMPLETE():
            INNER = (BAR.NORMAL, DOMAIN.INNER_SHARABLE, 0b1110)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b1110)

        class MESSAGE():
            INNER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b1111)
            OUTER = (BAR.NORMAL, DOMAIN.OUTER_SHARABLE, 0b1111)


def setAceArMode(arbar, ardomain, arsnoop, transactionType):
    bar, dom, snoop = transactionType
    arbar(bar)
    ardomain(dom)
    arsnoop(snoop)


class Ace_addr(Axi4_addr):
    """
    .. hwt-autodoc::
    """

    def _declr(self):
        Axi4_addr._declr(self)
        self.domain = VectSignal(2)
        self.region = VectSignal(4)
        self.snoop = VectSignal(3)
        self.bar = VectSignal(2)


class AceSnoop_addr(Axi_hs):
    """
    .. hwt-autodoc::
    """

    def _config(self):
        self.SNOOP_ADDR_WIDTH = Param(32)

    def _declr(self):
        self.addr = VectSignal(self.SNOOP_ADDR_WIDTH)
        self.snoop = VectSignal(4)
        self.prot = VectSignal(3)
        Axi_hs._declr(self)


class AceSnoop_resp(Axi_hs):
    """
    .. hwt-autodoc::
    """

    def _declr(self):
        self.resp = VectSignal(4)
        Axi_hs._declr(self)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = Axi3Lite_bAgent(sim, self)


class AceSnoop_data(Axi_hs):
    """
    .. hwt-autodoc::
    """

    def _config(self):
        self.SNOOP_DATA_WIDTH = Param(32)

    def _declr(self):
        self.data = VectSignal(self.SNOOP_DATA_WIDTH)
        self.last = Signal()
        Axi_hs._declr(self)


class Ace(Axi4):
    """
    :ivar ac: Coherent address channel.
        snoop address input to the master
    :ivar cr: Coherent response channel.
        used by the master to signal the response to snoops to the interconnect
    :ivar cd: Coherent data channel.
        output from the master to transfer snoop data

    https://static.docs.arm.com/ihi0022/d/IHI0022D_amba_axi_protocol_spec.pdf

    .. hwt-autodoc::
    """
    AW_CLS = Ace_addr
    AR_CLS = Ace_addr

    def _config(self):
        Axi4._config(self)
        self.SNOOP_ADDR_WIDTH = Param(32)
        self.SNOOP_DATA_WIDTH = Param(32)

    def _declr(self):
        super(Ace, self)._declr()
        with self._paramsShared():
            self.ac = AceSnoop_addr(masterDir=DIRECTION.IN)
            self.cr = AceSnoop_resp()
            self.cd = AceSnoop_data()

    def _initSimAgent(self, sim: HdlSimulator):
        raise NotImplementedError()

    def _getIpCoreIntfClass(self):
        raise NotImplementedError()
