from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.serializer.formater import formatVhdl
from hdl_toolkit.synthesizer.codeOps import If
from hdl_toolkit.synthesizer.rtlLevel.netlist import RtlNetlist


if __name__ == "__main__":
    t = vecT(8)
    fsmT = Enum('fsmT', ['send0', 'send1'])
    
    n = RtlNetlist("simpleRegister")
    
    s_out = n.sig("s_out", t)
    s_in0 = n.sig("s_in0", t)
    s_in1 = n.sig("s_in1", t)    
    clk = n.sig("clk")
    syncRst = n.sig("rst")
    
    
    fsmSt = n.sig("fsmSt", fsmT, clk, syncRst, fsmT.send0)
    If(fsmSt._eq(fsmT.send0),
        s_out ** s_in0,
        fsmSt ** fsmT.send1,
    ).Else(
        s_out ** s_in1 ,
        fsmSt ** fsmT.send0
    )
    
    interf = [clk, syncRst, s_in0, s_in1, s_out]
    
    for o in n.synthesize(interf):
            print(formatVhdl(str(o)))

    
