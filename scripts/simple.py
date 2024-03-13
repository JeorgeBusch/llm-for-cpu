import m5
from m5.objects import *

#scons build/X86/gem5.opt -j <num_cores> CC=<GCC_dir> CXX=<G++_dir> --ignore-style
#build/X86/gem5.opt --outdir=<output_dir> scripts/simple.py
#scons build/X86/gem5.opt -j 1 CC=/usr/bin/gcc-10 CXX=/usr/bin/g++-10 --ignore-style

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()
#obj.cpu.clk_domain = SrcClockDomain()
#obj.cpu.clk_domain.clock = '1GHz'
#obj.cpu.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]
#obj.cpu.mem_mode = 'timing'
#obj.cpu.mem_ranges = [AddrRange('512MB')]

system.cpu = TimingSimpleCPU()
#obj.cpu.cpu = TimingSimpleCPU()

system.membus = SystemXBar()
#obj.cpu.membus = SystemXBar()

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
#obj.cpu.cpu.icache_port = obj.cpu.membus.cpu_side_ports
#obj.cpu.cpu.dcache_port = obj.cpu.membus.cpu_side_ports

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
#obj.cpu.cpu.createInterruptController()
#obj.cpu.cpu.interrupts[0].pio = obj.cpu.membus.mem_side_ports
#obj.cpu.cpu.interrupts[0].int_requestor = obj.cpu.membus.cpu_side_ports
#obj.cpu.cpu.interrupts[0].int_responder = obj.cpu.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports
#obj.cpu.system_port = obj.cpu.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
#obj.cpu.mem_ctrl = MemCtrl()
#obj.cpu.mem_ctrl.dram = DDR3_1600_8x8()
#obj.cpu.mem_ctrl.dram.range = obj.cpu.mem_ranges[0]
#obj.cpu.mem_ctrl.port = obj.cpu.membus.mem_side_ports

binary = 'tests/test-progs/hello/bin/x86/linux/hello'
#binary = 'scripts/dist/hello/hello'
#binary = 'scripts/a.out'
#binary = 'scripts/embed_python/build/bert_sst'

# for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(binary)
#obj.cpu.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()
#obj.cpu.cpu.workload = process
#obj.cpu.cpu.createThreads()

root = Root(full_system = False, system = system)
#root = Root(full_system = False, system = obj.cpu)

root.obj = CheckObject(cpu = system.cpu)

m5.instantiate()



print("Beginning simulation!")
exit_event = None
while exit_event is None:
    exit_event = m5.simulate(1000000000000)
    m5.stats.dump()
    
    if exit_event.getCause() == "simulate() limit reached":
        exit_event = None

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))