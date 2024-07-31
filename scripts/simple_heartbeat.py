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
stat_labels = {"simInsts":"", "system.cpu.mmu.dtb.rdAccesses":"", "system.cpu.mmu.dtb.wrAccesses":"", 
                    "system.cpu.mmu.dtb.rdMisses":"", "system.cpu.mmu.dtb.wrMisses":"", "system.cpu.mmu.itb.rdAccesses":"", 
                    "system.cpu.mmu.itb.wrAccesses":"","system.cpu.mmu.itb.rdMisses":"", "system.cpu.mmu.itb.wrMisses":"" }
simd_integer_ops={"system.cpu.exec_context.thread_0.statExecutedInstType::SimdAdd":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdAddAcc":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdAlu":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdCmp":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdCvt":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdMisc":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdMult":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdMultAcc":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdShift":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdShiftAcc":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdDiv":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdSqrt":""}

simd_floating_ops={"system.cpu.exec_context.thread_0.statExecutedInstType::SimdFloatAdd":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdFloatAlu":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdFloatCmp":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdFloatCvt":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdFloatDiv":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdFloatMisc":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdFloatMult":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdFloatMultAcc":"",
                    "system.cpu.exec_context.thread_0.statExecutedInstType::SimdFloatSqrt":""}
num_ticks = 0
stat_interval = 50000000000000

while exit_event is None:
    exit_event = m5.simulate(stat_interval)
    num_ticks += stat_interval
    m5.stats.dump()
    file = open('/mnt/c/Users/aej45/Desktop/llm-for-cpu/output/main/stats.txt', 'r')
    stats = file.readlines()
    file.close()
    #m5.stats.reset()
    if exit_event.getCause() == "simulate() limit reached":
        print("\nTick", num_ticks, "Stats:")
        num_integer_ops = 0
        num_floating_ops = 0
        for stat in stats:
            stat = stat.strip()
            
            if any(label in stat for label in stat_labels.keys()):
                label = list(stat_labels.keys() & stat.split(" "))[0]
                stat_labels[label] = stat[len(label):stat.find("#")].strip()
                
            if any(label in stat for label in simd_integer_ops.keys()):
                label = list(simd_integer_ops.keys() & stat.split(" "))[0]
                simd_integer_ops[label] = stat[len(label):stat.find("#")-22].strip()
                num_integer_ops += int(stat[len(label):stat.find("#")-22].strip())
                
            if any(label in stat for label in simd_floating_ops.keys()):
                label = list(simd_floating_ops.keys() & stat.split(" "))[0]
                simd_floating_ops[label] = stat[len(label):stat.find("#")-22].strip()
                num_floating_ops += int(stat[len(label):stat.find("#")-22].strip())
        print("Simulated Instructions:", stat_labels["simInsts"])
        
        num_d_access = int(stat_labels["system.cpu.mmu.dtb.rdAccesses"]) + int(stat_labels["system.cpu.mmu.dtb.wrAccesses"])
        if num_d_access != 0:
            d_miss_rate = (int(stat_labels["system.cpu.mmu.dtb.rdMisses"]) + int(stat_labels["system.cpu.mmu.dtb.wrMisses"])) / num_d_access
        else:
            d_miss_rate = 0
        print("Data Accesses:", num_d_access)
        print("Data Miss Rate:", d_miss_rate)
        
        num_i_access = int(stat_labels["system.cpu.mmu.itb.rdAccesses"]) + int(stat_labels["system.cpu.mmu.itb.wrAccesses"])
        if num_i_access != 0:
            i_miss_rate = (int(stat_labels["system.cpu.mmu.itb.rdMisses"]) + int(stat_labels["system.cpu.mmu.itb.wrMisses"])) / num_i_access
        else:
            i_miss_rate = 0
        print("Instruction Accesses:", num_i_access)
        print("Instruction Miss Rate:", i_miss_rate)
        
        print("Integer SIMD Ops:", num_integer_ops)
        print("Floating Point SIMD Ops:", num_floating_ops, "\n")
                
        exit_event = None
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