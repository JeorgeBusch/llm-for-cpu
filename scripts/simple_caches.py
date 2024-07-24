import m5
from m5.objects import *
from caches import *
import argparse
import pandas as pd
from gem5.components.processors.simple_switchable_processor import SimpleSwitchableProcessor
from gem5.components.processors.cpu_types import CPUTypes

parser = argparse.ArgumentParser(description="Simple 2-level cache system.", epilog="Cache options may be found in src/mem/cache/Cache.py.\nReplacement options may be found in src/mem/cache/ReplacementPolicies.py")
parser.add_argument("--mem_size", help=f"Memory size. Default: 512MB.")
parser.add_argument("--l1i_size", help=f"L1 instruction cache size. Default: 16kB.")
parser.add_argument("--l1d_size", help=f"L1 data cache size. Default: 64kB.")
parser.add_argument("--l2_size", help=f"L2 cache size. Default: 256kB.")
parser.add_argument("--l1i_replpolicy", help=f"L1 instruction replacement policy. Default: LRURP")
parser.add_argument("--l1d_replpolicy", help=f"L1 data replacement policy. Default: LRURP")
parser.add_argument("--l2_replpolicy", help=f"L2 replacement policy. Default: LRURP")

options = parser.parse_args()

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

memSize = '512MB'
if options.mem_size:
    memSize = options.mem_size

system.mem_ranges = [AddrRange(memSize)]

system.cpu = AtomicSimpleCPU()
system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

system.membus = SystemXBar()
system.l2bus = L2XBar()
system.l2cache = L2Cache(options)

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)


system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports


binary = '/scratch/user/smb200007/research/llm-for-cpu/tools/bert.cpp/build/bin/main'

# for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

system.switch_cpu = TimingSimpleCPU(switched_out=True, cpu_id=0)

system.switch_cpu.workload = process
system.switch_cpu.createThreads()
switch_cpu_list = [(system.cpu, system.switch_cpu)]
switch_cpu_list2 = [(system.switch_cpu, system.cpu)]

root = Root(full_system = False, system = system)

m5.instantiate()


print("Beginning simulation!")
exit_event = None
switched = False

while exit_event is None:
    exit_event = m5.simulate()
    
    if exit_event.getCause() == "switchcpu":
        print("Switching CPU...")
        if not switched:
            m5.switchCpus(root.system, switch_cpu_list)
            switched = True
        else:
            m5.switchCpus(root.system, switch_cpu_list2)
            switched = False
        exit_event = None

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))