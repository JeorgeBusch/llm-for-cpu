from gem5.utils.requires import requires
from gem5.components.boards.x86_board import X86Board
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (MESITwoLevelCacheHierarchy,)
from gem5.components.processors.simple_switchable_processor import SimpleSwitchableProcessor
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.coherence_protocol import CoherenceProtocol
from gem5.isas import ISA
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator
from gem5.simulate.exit_event import ExitEvent
from gem5.resources.resource import CustomDiskImageResource, AbstractResource
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.boards.x86_board_se import X86BoardSE
from gem5.components.processors.switchable_processor import SwitchableProcessor

requires(
    isa_required=ISA.X86,
    #coherence_protocol_required=CoherenceProtocol.MESI_TWO_LEVEL,
    kvm_required=False,
)
'''
cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
    num_l2_banks=1,
)
'''
cache_hierarchy = NoCache()

memory = SingleChannelDDR3_1600("3GiB")

processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.TIMING,
    switch_core_type=CPUTypes.TIMING,
    num_cores=2,
)

#processor = SimpleProcessor(cpu_type=CPUTypes.ATOMIC, num_cores=1)

board = X86BoardSE(#SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

#binary = AbstractResource(local_path="tools/bert.cpp/build/bin/hello")
#binary = AbstractResource(local_path="tools/bert.cpp/build/bin/main")
binary = Resource("x86-hello64-static")
board.set_se_binary_workload(binary)

'''
command = "echo 'This is running on Atomic CPU cores.';" \
        + "sleep 1;" \
        + "m5 exit;"

board.set_kernel_disk_workload(
    kernel=AbstractResource(local_path="images/vmlinux-6.0.7"),
    disk_image=AbstractResource(local_path="images/x86-ubuntu-18.04-img"),
    readfile_contents=command,
)
'''

simulator = Simulator(
    full_system=False,
    board=board,
)

simulator.run()