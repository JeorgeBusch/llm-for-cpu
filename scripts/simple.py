import m5
from m5.objects import *
import pandas as pd
from gem5.components.processors.simple_switchable_processor import SimpleSwitchableProcessor
from gem5.components.processors.cpu_types import CPUTypes

#scons build/X86/gem5.opt -j <num_cores> CC=<GCC_dir> CXX=<G++_dir> --ignore-style
#build/X86/gem5.opt --outdir=<output_dir> scripts/simple.py
#scons build/X86/gem5.opt -j 1 --ignore-style
# eval "$(/home/grads/a/averyjohnson/research/llm-for-cpu/tools/miniconda/bin/conda shell.bash hook)"

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

#system.mem_mode = 'atomic'
system.mem_ranges = [AddrRange('512MB')]

#detailed_cpu.createInterruptController()

system.cpu = AtomicSimpleCPU()
#system.switch_cpu = DetailedCPU()
#system.switch_cpu = [(atomic_cpu, timing_cpu)]

#system.cpu = TimingSimpleCPU()

system.membus = SystemXBar()

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports


system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

#binary = 'tests/test-progs/hello/bin/x86/linux/hello'
#binary = 'scripts/dist/hello/hello'
#binary = 'scripts/a.out'
#binary = 'scripts/embed_python/build/bert_sst'
binary = '/mnt/c/Users/aej45/Desktop/llm-for-cpu/tools/bert.cpp/build/bin/main'

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

#m5.seedRandom(int(1234567654321))

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

#exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))