stat_labels = {"simTicks":0, "simInsts":0, "system.switch_cpu.mmu.dtb.rdAccesses":0, "system.switch_cpu.mmu.dtb.wrAccesses":0, 
                    "system.switch_cpu.mmu.dtb.rdMisses":0, "system.switch_cpu.mmu.dtb.wrMisses":0, "system.switch_cpu.mmu.itb.rdAccesses":0, 
                    "system.switch_cpu.mmu.itb.wrAccesses":0,"system.switch_cpu.mmu.itb.rdMisses":0, "system.switch_cpu.mmu.itb.wrMisses":0, "system.switch_cpu.numCycles":0 }
simd_integer_ops={"system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdAdd":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdAddAcc":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdAlu":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdCmp":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdCvt":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdMisc":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdMult":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdMultAcc":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdShift":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdShiftAcc":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdDiv":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdSqrt":0}

simd_floating_ops={"system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdFloatAdd":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdFloatAlu":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdFloatCmp":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdFloatCvt":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdFloatDiv":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdFloatMisc":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdFloatMult":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdFloatMultAcc":0,
                    "system.switch_cpu.exec_context.thread_0.statExecutedInstType::SimdFloatSqrt":0}
                    
file = open('output/l1_sp/stats.txt', 'r')
stats = file.readlines()
file.close()

num_integer_ops = 0
num_floating_ops = 0
for stat in stats:
    stat = stat.strip()
    
    if any(label in stat for label in stat_labels.keys()):
        label = list(set(stat_labels.keys()).intersection(set(stat.split(" "))))[0]
        stat_labels[label] += int(stat[len(label):stat.find("#")].strip())
        
    if any(label in stat for label in simd_integer_ops.keys()):
        #label = list(simd_integer_ops.keys() & stat.split(" "))[0]
        label = list(set(simd_integer_ops.keys()).intersection(set(stat.split(" "))))[0]
        simd_integer_ops[label] += int(stat[len(label):stat.find("#")-22].strip())
        num_integer_ops += int(stat[len(label):stat.find("#")-22].strip())
        
    if any(label in stat for label in simd_floating_ops.keys()):
        #label = list(simd_floating_ops.keys() & stat.split(" "))[0]
        label = list(set(simd_floating_ops.keys()).intersection(set(stat.split(" "))))[0]
        simd_floating_ops[label] += int(stat[len(label):stat.find("#")-22].strip())
        num_floating_ops += int(stat[len(label):stat.find("#")-22].strip())

#print(stat_labels)
#print(simd_integer_ops)
#print(simd_floating_ops)

print("Simulated Instructions:", stat_labels["simInsts"])

num_d_access = int(stat_labels["system.switch_cpu.mmu.dtb.rdAccesses"]) + int(stat_labels["system.switch_cpu.mmu.dtb.wrAccesses"])
if num_d_access != 0:
    d_miss_rate = (int(stat_labels["system.switch_cpu.mmu.dtb.rdMisses"]) + int(stat_labels["system.switch_cpu.mmu.dtb.wrMisses"])) / num_d_access
else:
    d_miss_rate = 0
print("Data Accesses:", num_d_access)
print("Data Miss Rate:", d_miss_rate)

num_i_access = int(stat_labels["system.switch_cpu.mmu.itb.rdAccesses"]) + int(stat_labels["system.switch_cpu.mmu.itb.wrAccesses"])
if num_i_access != 0:
    i_miss_rate = (int(stat_labels["system.switch_cpu.mmu.itb.rdMisses"]) + int(stat_labels["system.switch_cpu.mmu.itb.wrMisses"])) / num_i_access
else:
    i_miss_rate = 0
print("Instruction Accesses:", num_i_access)
print("Instruction Miss Rate:", i_miss_rate)

print("Integer SIMD Ops:", num_integer_ops)
print("Floating Point SIMD Ops:", num_floating_ops, "\n")

print("IPC:", float(stat_labels["simInsts"])/float(stat_labels["system.switch_cpu.numCycles"]))