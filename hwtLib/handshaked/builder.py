#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtLib.abstract.streamBuilder import AbstractStreamBuilder
from hwtLib.handshaked.fifo import HandshakedFifo
from hwtLib.handshaked.fork import HandshakedFork
from hwtLib.handshaked.join import HandshakedJoin
from hwtLib.handshaked.demux import HandshakedDemux
from hwtLib.handshaked.reg import HandshakedReg
from hwtLib.handshaked.resizer import HandshakedResizer


#from hwtLib.handshaked.forkRegistered import HandshakedRegisteredFork
class HsBuilder(AbstractStreamBuilder):
    """
    Helper class which simplifies building of large stream paths 
    """
    JoinCls = HandshakedJoin
    FifoCls = HandshakedFifo
    ForkCls = HandshakedFork
    RegCls  = HandshakedReg
    DemuxCls  = HandshakedDemux
    ResizerCls = HandshakedResizer