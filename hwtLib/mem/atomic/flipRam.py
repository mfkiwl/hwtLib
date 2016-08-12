from hdl_toolkit.interfaces.std import Signal, BramPort_withoutClk, Clk
from hdl_toolkit.interfaces.utils import propagateClk
from hdl_toolkit.synthesizer.codeOps import If, connect
from hdl_toolkit.synthesizer.interfaceLevel.unit import Unit
from hdl_toolkit.synthesizer.param import evalParam
from hwtLib.mem.ram import RamSingleClock


class FlipRam(Unit):
    """
    Switchable RAM, there are two memories and two sets of ports,
    Each set of ports is every time connected to opposite ram.
    By select you can choose between RAMs.
    
    This component is meant to be form of synchronization.
    Example first RAM is connected to first set of ports, writer performs actualizations on first RAM
    and reader reads data from second ram by second set of ports.
    
    Then select is set and access is flipped. Reader now has access to RAM 0 and writer to RAM 1.
    """
    def _config(self):
        RamSingleClock._config(self)

    def _declr(self):
        PORT_CNT = evalParam(self.PORT_CNT).val
        
        with self._paramsShared():
            with self._asExtern():
                self.clk = Clk()
                self.firstA = BramPort_withoutClk()
                self.secondA = BramPort_withoutClk()
                
                if PORT_CNT == 2:
                    self.firstB = BramPort_withoutClk()
                    self.secondB = BramPort_withoutClk()
                elif PORT_CNT >2:
                    raise NotImplementedError()
                
                self.select_sig = Signal()  
            
                
            self.ram0 = RamSingleClock()
            self.ram1 = RamSingleClock()

    def _impl(self):
        propagateClk(self)
        PORT_CNT = evalParam(self.PORT_CNT).val
        
        fa = self.firstA
        sa = self.secondA
        
        If(self.select_sig,
           connect(fa, self.ram0.a), 
           connect(sa, self.ram1.a)
        ).Else(
           connect(sa, self.ram0.a), 
           connect(fa, self.ram1.a)
        )
        if PORT_CNT == 2:
            fb = self.firstB
            sb = self.secondB
            If(self.select_sig,
               connect(fb, self.ram0.b), 
               connect(sb, self.ram1.b)
            ).Else(
               connect(sb, self.ram0.b),
               connect(fb, self.ram1.b)
            )
          
        
if __name__ == "__main__":
    from hdl_toolkit.synthesizer.shortcuts import toRtl
    print(toRtl(FlipRam))