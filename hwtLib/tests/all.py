#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestLoader, TextTestRunner, TestSuite

from hwt.simulator.simTestCase import SingleUnitSimTestCase
from hwtLib.abstract.busEndpoint_test import BusEndpointTC
from hwtLib.abstract.frame_join_utils.test import FrameJoinUtilsTC
from hwtLib.abstract.streamAlignmentUtils_test import StreamJoiningUtilsTC
from hwtLib.abstract.template_configured_test import TemplateConfigured_TC
from hwtLib.amba.axiLite_comp.buff_test import AxiRegTC
from hwtLib.amba.axiLite_comp.endpoint_arr_test import \
    AxiLiteEndpointArrayTC, AxiLiteEndpointStructsInArrayTC
from hwtLib.amba.axiLite_comp.endpoint_fromInterfaces_test import \
    AxiLiteEndpoint_fromInterfaceTC, AxiLiteEndpoint_fromInterface_arr_TC
from hwtLib.amba.axiLite_comp.endpoint_struct_test import \
    AxiLiteEndpoint_arrayStruct_TC, AxiLiteEndpoint_struct_TC
from hwtLib.amba.axiLite_comp.endpoint_test import AxiLiteEndpointTCs
from hwtLib.amba.axiLite_comp.to_axi_test import AxiLite_to_Axi_TC
from hwtLib.amba.axi_comp.interconnect.matrixAddrCrossbar_test import\
    AxiInterconnectMatrixAddrCrossbar_TCs
from hwtLib.amba.axi_comp.interconnect.matrixCrossbar_test import \
    AxiInterconnectMatrixCrossbar_TCs
from hwtLib.amba.axi_comp.interconnect.matrixR_test import AxiInterconnectMatrixR_TCs
from hwtLib.amba.axi_comp.interconnect.matrixW_test import AxiInterconnectMatrixW_TCs
from hwtLib.amba.axi_comp.sim.ag_test import Axi_ag_TC
from hwtLib.amba.axi_comp.slave_timeout_test import AxiSlaveTimeoutTC
from hwtLib.amba.axi_comp.stream_to_mem_test import Axi4_streamToMemTC
from hwtLib.amba.axi_comp.tester_test import AxiTesterTC
from hwtLib.amba.axi_comp.to_axiLite_test import Axi_to_AxiLite_TC
from hwtLib.amba.axi_test import AxiTC
from hwtLib.amba.axis_comp.en_test import AxiS_en_TC
from hwtLib.amba.axis_comp.frameGen_test import AxisFrameGenTC
from hwtLib.amba.axis_comp.frame_deparser.test import AxiS_frameDeparser_TC
from hwtLib.amba.axis_comp.frame_join.test import AxiS_FrameJoin_TCs
from hwtLib.amba.axis_comp.frame_parser.footer_split_test import AxiS_footerSplitTC
from hwtLib.amba.axis_comp.frame_parser.test import AxiS_frameParserTC
from hwtLib.amba.axis_comp.measuringFifo_test import AxiS_measuringFifoTC
from hwtLib.amba.axis_comp.resizer_test import AxiS_resizer_TCs
from hwtLib.amba.axis_comp.storedBurst_test import AxiSStoredBurstTC
from hwtLib.amba.datapump.interconnect.rStrictOrder_test import \
    RStrictOrderInterconnectTC
from hwtLib.amba.datapump.interconnect.wStrictOrderComplex_test import \
    WStrictOrderInterconnectComplexTC
from hwtLib.amba.datapump.interconnect.wStrictOrder_test import \
    WStrictOrderInterconnectTC, WStrictOrderInterconnect2TC
from hwtLib.amba.datapump.r_test import Axi4_rDatapumpTC,\
    Axi3_rDatapumpTC
from hwtLib.amba.datapump.w_test import Axi4_wDatapumpTC, \
    Axi3_wDatapump_direct_TC, Axi3_wDatapump_small_splitting_TC
from hwtLib.avalon.endpoint_test import AvalonMmEndpointTCs
from hwtLib.avalon.mmAgent_test import AvalonMmAgentTC
from hwtLib.avalon.stAgent_test import AvalonStAgentTC
from hwtLib.clocking.cdc_test import CdcTC
from hwtLib.clocking.clkDivider import ClkDiv3TC
from hwtLib.examples.arithmetic.cntr_test import CntrTC, CntrResourceAnalysisTC
from hwtLib.examples.arithmetic.selfRefCntr_test import SelfRefCntrTC
from hwtLib.examples.arithmetic.twoCntrs_test import TwoCntrsTC
from hwtLib.examples.arithmetic.widthCasting import WidthCastingExampleTC
from hwtLib.examples.axi.simpleAxiRegs_test import SimpleAxiRegsTC
from hwtLib.examples.builders.ethAddrUpdater_test import EthAddrUpdaterTC
from hwtLib.examples.builders.handshakedBuilderSimple import \
    HandshakedBuilderSimpleTC
from hwtLib.examples.builders.hsBuilderSplit_test import HsBuilderSplit_TC
from hwtLib.examples.builders.pingResponder_test import PingResponderTC
from hwtLib.examples.emptyUnitWithSpi import EmptyUnitWithSpiTC
from hwtLib.examples.errors.errorsTestCase import ErrorsTC
from hwtLib.examples.hdlComments_test import HdlCommentsTC
from hwtLib.examples.hdlObjLists.listOfInterfaces0 import ListOfInterfacesSample0TC
from hwtLib.examples.hdlObjLists.listOfInterfaces1 import ListOfInterfacesSample1TC
from hwtLib.examples.hdlObjLists.listOfInterfaces2 import ListOfInterfacesSample2TC
from hwtLib.examples.hdlObjLists.listOfInterfaces3 import ListOfInterfacesSample3TC
from hwtLib.examples.hdlObjLists.listOfInterfaces4 import ListOfInterfacesSample4TC
from hwtLib.examples.hierarchy.hierarchySerialization_test import \
    HierarchySerializationTC
from hwtLib.examples.hierarchy.simpleSubunit2 import SimpleSubunit2TC
from hwtLib.examples.hierarchy.simpleSubunit3 import SimpleSubunit3TC
from hwtLib.examples.hierarchy.simpleSubunit_test import SimpleSubunitTC
from hwtLib.examples.hierarchy.unitToUnitConnection import \
    UnitToUnitConnectionTC
from hwtLib.examples.hierarchy.unitWrapper_test import UnitWrapperTC
from hwtLib.examples.mem.bram_wire import BramWireTC
from hwtLib.examples.mem.ram_test import RamResourcesTC, \
    SimpleAsyncRamTC, SimpleSyncRamTC
from hwtLib.examples.mem.reg_test import DRegTC, RegSerializationTC, \
    DoubleRRegTC, DReg_asyncRstTC
from hwtLib.examples.mem.rom_test import SimpleRomTC, SimpleSyncRomTC, \
    RomResourcesTC
from hwtLib.examples.operators.concat_test import ConcatTC
from hwtLib.examples.operators.indexing_test import IndexingTC
from hwtLib.examples.parametrization_test import ParametrizationTC
from hwtLib.examples.rtlLvl.rtlLvl_test import RtlLvlTC
from hwtLib.examples.showcase0_test import Showcase0TC
from hwtLib.examples.simple2withNonDirectIntConnection import \
    Simple2withNonDirectIntConnectionTC
from hwtLib.examples.simpleAxiStream_test import SimpleUnitAxiStream_TC
from hwtLib.examples.simpleWithNonDirectIntConncetion import \
    SimpleWithNonDirectIntConncetionTC
from hwtLib.examples.simpleWithParam import SimpleUnitWithParamTC
from hwtLib.examples.simple_test import SimpleTC
from hwtLib.examples.specialIntfTypes.intfWithArray import InterfaceWithArrayTypesTC
from hwtLib.examples.statements.constCondition import ConstConditionTC
from hwtLib.examples.statements.constDriver_test import ConstDriverTC
from hwtLib.examples.statements.forLoopCntrl_test import StaticForLoopCntrlTC
from hwtLib.examples.statements.fsm_test import FsmExampleTC, \
    HadrcodedFsmExampleTC, FsmSerializationTC
from hwtLib.examples.statements.ifStm_test import IfStmTC
from hwtLib.examples.statements.switchStm_test import SwitchStmTC
from hwtLib.examples.statements.vldMaskConflictsResolving_test import \
    VldMaskConflictsResolvingTC
from hwtLib.examples.timers import TimerTC
from hwtLib.handshaked.cdc_test import HandshakedCdc_slow_to_fast_TC,\
    HandshakedCdc_fast_to_slow_TC
from hwtLib.handshaked.fifoAsync_test import HsFifoAsyncTC
from hwtLib.handshaked.fifo_test import HsFifoTC
from hwtLib.handshaked.joinFair_test import HsJoinFair_2inputs_TC, \
    HsJoinFair_3inputs_TC
from hwtLib.handshaked.joinPrioritized_test import HsJoinPrioritizedTC, \
    HsJoinPrioritized_randomized_TC
from hwtLib.handshaked.ramAsHs_test import RamAsHs_TC
from hwtLib.handshaked.reg_test import HsRegL1D0TC, HsRegL2D1TC
from hwtLib.handshaked.resizer_test import HsResizerTC
from hwtLib.handshaked.splitCopy_test import HsSplitCopyTC, \
    HsSplitCopy_randomized_TC
from hwtLib.img.charToBitmap_test import CharToBitmapTC
from hwtLib.xilinx.ipif.axi4Lite_to_ipif_test import Axi4Lite_to_IpifTC
from hwtLib.xilinx.ipif.buff_test import IpifBuffTC
from hwtLib.xilinx.ipif.endpoint_test import IpifEndpointTC, \
    IpifEndpointDenseTC, IpifEndpointDenseStartTC, IpifEndpointArray
from hwtLib.xilinx.ipif.interconnectMatrix_test import IpifInterconnectMatrixTC
from hwtLib.logic.binToOneHot import BinToOneHotTC
from hwtLib.logic.bitonicSorter import BitonicSorterTC
from hwtLib.logic.cntrGray import GrayCntrTC
from hwtLib.logic.crcComb_test import CrcCombTC
from hwtLib.logic.crcUtils_test import CrcUtilsTC
from hwtLib.logic.crc_test import CrcTC
from hwtLib.logic.lsfr import LsfrTC
from hwtLib.logic.oneHotToBin_test import OneHotToBinTC
from hwtLib.mem.atomic.flipCntr_test import FlipCntrTC
from hwtLib.mem.atomic.flipRam_test import FlipRamTC
from hwtLib.mem.atomic.flipReg_test import FlipRegTC
from hwtLib.mem.bramEndpoint_test import BramPortEndpointTCs
from hwtLib.mem.cam_test import CamTC
from hwtLib.mem.cuckooHashTable_test import CuckooHashTableTC
from hwtLib.mem.fifoAsync_test import FifoAsyncTC
from hwtLib.mem.fifo_test import FifoWriterAgentTC, FifoReaderAgentTC, FifoTC
from hwtLib.mem.hashTableCore_test import HashTableCoreTC
from hwtLib.mem.lutRam_test import LutRamTC
from hwtLib.mem.ram_test import RamTC
from hwtLib.cesnet.mi32.axi4Lite_bridges_test import Mi32Axi4LiteBrigesTC
from hwtLib.cesnet.mi32.mi32agent_test import Mi32AgentTC
from hwtLib.cesnet.mi32.to_axi4Lite_test import Mi32_to_Axi4LiteTC
from hwtLib.peripheral.displays.hd44780.driver_test import Hd44780Driver8bTC
from hwtLib.peripheral.ethernet.rmii_adapter_test import RmiiAdapterTC
from hwtLib.peripheral.i2c.masterBitCntrl_test import I2CMasterBitCntrlTC
from hwtLib.peripheral.mdio.master_test import MdioMasterTC
from hwtLib.peripheral.segment7_test import Segment7TC
from hwtLib.peripheral.spi.master_test import SpiMasterTC
from hwtLib.peripheral.uart.rx_test import UartRxTC, UartRxBasicTC
from hwtLib.peripheral.uart.tx_rx_test import UartTxRxTC
from hwtLib.peripheral.uart.tx_test import UartTxTC
from hwtLib.structManipulators.arrayBuff_writer_test import ArrayBuff_writer_TC
from hwtLib.structManipulators.arrayItemGetter_test import ArrayItemGetterTC, \
    ArrayItemGetter2in1WordTC
from hwtLib.structManipulators.cLinkedListReader_test import \
    CLinkedListReaderTC
from hwtLib.structManipulators.cLinkedListWriter_test import \
    CLinkedListWriterTC
from hwtLib.structManipulators.mmu2pageLvl_test import MMU_2pageLvl_TC
from hwtLib.structManipulators.structReader_test import StructReaderTC
from hwtLib.structManipulators.structWriter_test import StructWriter_TC
from hwtLib.tests.fileUtils_test import FileUtilsTC
from hwtLib.tests.frameTmpl_test import FrameTmplTC
from hwtLib.tests.ipCorePackager_test import IpCorePackagerTC
from hwtLib.tests.rdSynced_agent_test import RdSynced_agent_TC
from hwtLib.tests.resourceAnalyzer_test import ResourceAnalyzer_TC
from hwtLib.tests.serializerModes_test import SerializerModes_TC
from hwtLib.tests.serializer_tmpVar_test import Serializer_tmpVar_TC
from hwtLib.tests.simulatorUtlls_test import SimulatorUtilsTC
from hwtLib.tests.statementTrees import StatementTreesTC
from hwtLib.tests.statementTreesInternal import StatementTreesInternalTC
from hwtLib.tests.statements import StatementsTC
from hwtLib.tests.synthesizer.interfaceLevel.interfaceSynthesizerTC import \
    InterfaceSynthesizerTC
from hwtLib.tests.synthesizer.interfaceLevel.subunitsSynthesisTC import \
    SubunitsSynthesisTC
from hwtLib.tests.synthesizer.rtlLevel.optimalizator import Expr2CondTC
from hwtLib.tests.synthesizer.rtlLevel.synthesis import BasicSynthesisTC, \
    StatementsConsystencyTC
from hwtLib.tests.transTmpl_test import TransTmpl_TC
from hwtLib.tests.types.bitsSlicing_test import BitsSlicingTC
from hwtLib.tests.types.hstructVal_test import HStructValTC
from hwtLib.tests.types.operators_test import OperatorTC
from hwtLib.tests.types.union_test import UnionTC
from hwtLib.tests.types.value_test import ValueTC
from hwtLib.tests.unionIntf_test import UnionIntfTC
from hwtLib.tests.vhdlSerializer_test import VhdlSerializer_TC
from hwtLib.xilinx.locallink.axis_conv_test import AxiS_localLinkConvTC


# from hwt.simulator.simTestCase import SimTestCase
def testSuiteFromTCs(*tcs):
    loader = TestLoader()
    for tc in tcs:
        if not issubclass(tc, SingleUnitSimTestCase):
            tc._multiprocess_can_split_ = True
    loadedTcs = [loader.loadTestsFromTestCase(tc) for tc in tcs
                 # if not issubclass(tc, SimTestCase)  # [debug] skip simulations
                 ]
    suite = TestSuite(loadedTcs)
    return suite


suite = testSuiteFromTCs(
    # basic tests
    FileUtilsTC,
    RtlLvlTC,
    HdlCommentsTC,
    InterfaceSynthesizerTC,
    SubunitsSynthesisTC,
    EmptyUnitWithSpiTC,
    Simple2withNonDirectIntConnectionTC,
    SimpleWithNonDirectIntConncetionTC,
    SimpleSubunit3TC,
    UnitToUnitConnectionTC,
    Expr2CondTC,
    OperatorTC,
    BitsSlicingTC,
    HStructValTC,
    ParametrizationTC,
    BasicSynthesisTC,
    StatementsConsystencyTC,
    ValueTC,
    StatementTreesInternalTC,
    StatementTreesTC,
    StatementsTC,
    ErrorsTC,
    StaticForLoopCntrlTC,
    SimpleUnitWithParamTC,
    SimpleSubunit2TC,
    HierarchySerializationTC,
    ListOfInterfacesSample0TC,
    ListOfInterfacesSample1TC,
    ListOfInterfacesSample2TC,
    ListOfInterfacesSample3TC,
    ListOfInterfacesSample4TC,
    FrameTmplTC,
    Showcase0TC,
    SimulatorUtilsTC,
    RdSynced_agent_TC,
    Segment7TC,
    SerializerModes_TC,
    Serializer_tmpVar_TC,
    TransTmpl_TC,
    UnionTC,
    UnionIntfTC,
    ResourceAnalyzer_TC,
    VhdlSerializer_TC,
    IfStmTC,
    SwitchStmTC,
    SimpleRomTC,
    SimpleSyncRomTC,
    RomResourcesTC,
    DRegTC,
    DoubleRRegTC,
    DReg_asyncRstTC,
    RegSerializationTC,
    CntrTC,
    CntrResourceAnalysisTC,
    ConstConditionTC,
    TemplateConfigured_TC,
    FrameJoinUtilsTC,

    # tests of simple units
    TimerTC,
    ConcatTC,
    VldMaskConflictsResolvingTC,
    ConstDriverTC,
    WidthCastingExampleTC,
    SimpleTC,
    SimpleSubunitTC,
    RamTC,
    BramWireTC,
    LutRamTC,
    FsmSerializationTC,
    FsmExampleTC,
    HadrcodedFsmExampleTC,
    OneHotToBinTC,
    BinToOneHotTC,
    GrayCntrTC,
    TwoCntrsTC,
    SelfRefCntrTC,
    IndexingTC,
    CdcTC,
    RamResourcesTC,
    SimpleAsyncRamTC,
    SimpleSyncRamTC,
    SimpleUnitAxiStream_TC,
    FifoWriterAgentTC,
    FifoReaderAgentTC,
    FifoTC,
    FifoAsyncTC,
    HsJoinPrioritizedTC,
    HsJoinPrioritized_randomized_TC,
    HsJoinFair_2inputs_TC,
    HsJoinFair_3inputs_TC,
    HandshakedCdc_slow_to_fast_TC,
    HandshakedCdc_fast_to_slow_TC,
    RamAsHs_TC,
    LsfrTC,
    ClkDiv3TC,
    BitonicSorterTC,
    InterfaceWithArrayTypesTC,

    FlipRegTC,
    FlipCntrTC,
    FlipRamTC,
    HsSplitCopyTC,
    HsSplitCopy_randomized_TC,
    HsFifoTC,
    HsFifoAsyncTC,
    HsRegL1D0TC,
    HsRegL2D1TC,
    HsResizerTC,
    HsBuilderSplit_TC,
    CamTC,
    UartTxTC,
    UartRxBasicTC,
    UartRxTC,
    UartTxRxTC,
    SpiMasterTC,
    I2CMasterBitCntrlTC,
    MdioMasterTC,
    Hd44780Driver8bTC,
    CrcUtilsTC,
    CrcCombTC,
    CrcTC,

    BusEndpointTC,

    *BramPortEndpointTCs,

    # avalon tests
    AvalonMmAgentTC,
    *AvalonMmEndpointTCs,
    AvalonStAgentTC,

    # axi tests
    SimpleAxiRegsTC,
    AxiTC,
    *AxiLiteEndpointTCs,
    AxiLiteEndpointArrayTC,
    AxiLiteEndpointStructsInArrayTC,
    AxiLiteEndpoint_struct_TC,
    AxiLiteEndpoint_arrayStruct_TC,
    AxiLiteEndpoint_fromInterfaceTC,
    AxiLiteEndpoint_fromInterface_arr_TC,
    AxiLite_to_Axi_TC,
    Axi_to_AxiLite_TC,
    AxiRegTC,
    AxiTesterTC,

    AxisFrameGenTC,
    Axi4_rDatapumpTC,
    Axi3_rDatapumpTC,
    Axi4_wDatapumpTC,
    Axi3_wDatapump_direct_TC,
    Axi3_wDatapump_small_splitting_TC,
    AxiSlaveTimeoutTC,
    AxiSStoredBurstTC,
    AxiS_en_TC,
    AxiS_measuringFifoTC,
    *AxiS_resizer_TCs,
    AxiS_frameDeparser_TC,
    AxiS_localLinkConvTC,
    AxiS_footerSplitTC,
    AxiS_frameParserTC,
    *AxiS_FrameJoin_TCs,
    HandshakedBuilderSimpleTC,
    EthAddrUpdaterTC,

    RStrictOrderInterconnectTC,
    WStrictOrderInterconnectTC,
    WStrictOrderInterconnect2TC,
    WStrictOrderInterconnectComplexTC,

    *AxiInterconnectMatrixAddrCrossbar_TCs,
    *AxiInterconnectMatrixCrossbar_TCs,
    *AxiInterconnectMatrixR_TCs,
    *AxiInterconnectMatrixW_TCs,

    Axi_ag_TC,
    Axi4_streamToMemTC,
    ArrayItemGetterTC,
    ArrayItemGetter2in1WordTC,
    ArrayBuff_writer_TC,
    CLinkedListReaderTC,
    CLinkedListWriterTC,
    MMU_2pageLvl_TC,
    StructWriter_TC,
    StructReaderTC,

    # ipif tests
    IpifEndpointTC,
    IpifEndpointDenseTC,
    IpifEndpointDenseStartTC,
    IpifEndpointArray,
    IpifBuffTC,
    Axi4Lite_to_IpifTC,
    IpifInterconnectMatrixTC,

    Mi32AgentTC,
    Mi32_to_Axi4LiteTC,
    Mi32Axi4LiteBrigesTC,

    # complex units tests
    UnitWrapperTC,
    IpCorePackagerTC,
    CharToBitmapTC,
    HashTableCoreTC,
    CuckooHashTableTC,
    PingResponderTC,

    RmiiAdapterTC,
    StreamJoiningUtilsTC,
)

if __name__ == '__main__':
    # runner = TextTestRunner(verbosity=2, failfast=True)
    runner = TextTestRunner(verbosity=2)

    try:
        from concurrencytest import ConcurrentTestSuite, fork_for_tests
        useParallerlTest = True
    except ImportError:
        # concurrencytest is not installed, use regular test runner
        useParallerlTest = False
    # useParallerlTest = False

    if useParallerlTest:
        # Run same tests across 4 processes
        concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests())
        runner.run(concurrent_suite)
    else:
        runner.run(suite)
