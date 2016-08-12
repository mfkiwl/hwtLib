from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.interfaces.std import Signal, VldSynced, HandshakeSync
from hdl_toolkit.interfaces.utils import addClkRstn, propagateClkRstn
from hdl_toolkit.synthesizer.codeOps import If, c
from hdl_toolkit.synthesizer.interfaceLevel.unit import Unit
from hdl_toolkit.synthesizer.param import Param
from hwtLib.mem.atomic.flipReg import FlipRegister


class FlipCntr(Unit):
    """
    Counter with FlipRegister which is form memory with atomic access
    
    interface doFilip drives switching of memories in flip register
    dataIn has higher priority than doIncr
    """
    def _config(self):
        self.DATA_WIDTH = Param(18)

    def _declr(self):
        with self._paramsShared():
            with self._asExtern():
                addClkRstn(self)
                self.doIncr = Signal()
                self.doFlip = HandshakeSync()
                self.dataIn = VldSynced()
                self.dataOut = Signal(dtype=vecT(self.DATA_WIDTH))
            self.cntr = FlipRegister()
    
    def flipHandler(self):
        c(1, self.doFlip.rd)
        
        flipSt = self._reg("flipState", defVal=0)
        If(self.doFlip.vld,
            c(~flipSt, flipSt)
        ).Else(
            flipSt._same()
        )
        c(flipSt, self.cntr.select_sig)
        
    
    def dataHanldler(self):
        cntr = self.cntr
        c(cntr.firstOut + 1 , cntr.firstIn.data)
        c(self.doIncr, cntr.firstIn.vld)
        
        c(self.dataIn, cntr.secondIn)
        c(cntr.secondOut, self.dataOut)
        
    
    def _impl(self):
        propagateClkRstn(self)
        self.flipHandler()
        self.dataHanldler()
        
if __name__ == "__main__":
    from hdl_toolkit.synthesizer.shortcuts import toRtl
    print(toRtl(FlipCntr()))
