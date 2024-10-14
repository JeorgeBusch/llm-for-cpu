import os
import xlsxwriter

stats_path = 'output/default/'

stat_folders = os.listdir(stats_path)
stat_folders = [folder for folder in stat_folders if not '.' in folder]

instructions = []
d_miss_rate = []
i_miss_rate = []
num_integer_ops = []
num_floating_ops = []
i_num_accesses = []
d_num_accesses = []
ipc = []
i = 0
for stat_folder in stat_folders: 
    stat_labels = {"finalTicks":0, "simInsts":0, "system.switch_cpu.mmu.dtb.rdAccesses":0, "system.switch_cpu.mmu.dtb.wrAccesses":0, 
                        "system.switch_cpu.mmu.dtb.rdMisses":0, "system.switch_cpu.mmu.dtb.wrMisses":0, "system.switch_cpu.mmu.itb.rdAccesses":0, 
                        "system.switch_cpu.mmu.itb.wrAccesses":0,"system.switch_cpu.mmu.itb.rdMisses":0, "system.switch_cpu.mmu.itb.wrMisses":0, "system.switch_cpu.numCycles":0,
                        "system.switch_cpu.exec_context.thread_0.numInsts":0 }
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

    print(stat_folder)        
    file = open(stats_path + stat_folder + '/stats.txt', 'r')
    stats = file.readlines()
    file.close()
    
    integer_ops = 0
    floating_ops = 0
    for stat in stats:
        stat = stat.strip()
        
        if any(label in stat for label in stat_labels.keys()):
            label = list(set(stat_labels.keys()).intersection(set(stat.split(" "))))[0]
            stat_labels[label] += int(stat[len(label):stat.find("#")].strip())
            
        if any(label in stat for label in simd_integer_ops.keys()):
            #label = list(simd_integer_ops.keys() & stat.split(" "))[0]
            label = list(set(simd_integer_ops.keys()).intersection(set(stat.split(" "))))[0]
            simd_integer_ops[label] += int(stat[len(label):stat.find("#")-22].strip())
            integer_ops += int(stat[len(label):stat.find("#")-22].strip())
            
        if any(label in stat for label in simd_floating_ops.keys()):
            #label = list(simd_floating_ops.keys() & stat.split(" "))[0]
            label = list(set(simd_floating_ops.keys()).intersection(set(stat.split(" "))))[0]
            simd_floating_ops[label] += int(stat[len(label):stat.find("#")-22].strip())
            floating_ops += int(stat[len(label):stat.find("#")-22].strip())
    
    num_integer_ops.append(integer_ops)
    num_floating_ops.append(floating_ops)
    
    instructions.append(stat_labels["system.switch_cpu.exec_context.thread_0.numInsts"])
    print("Simulated Instructions:", instructions[i])
    
    num_d_access = int(stat_labels["system.switch_cpu.mmu.dtb.rdAccesses"]) + int(stat_labels["system.switch_cpu.mmu.dtb.wrAccesses"])
    if num_d_access != 0:
        d_miss_rate.append((int(stat_labels["system.switch_cpu.mmu.dtb.rdMisses"]) + int(stat_labels["system.switch_cpu.mmu.dtb.wrMisses"])) * 1000 / instructions[i])
    else:
        d_miss_rate.append(0)
    d_num_accesses.append(num_d_access)
    print("Data Accesses:", num_d_access)
    print("Data Miss Rate:", d_miss_rate[i])
    
    num_i_access = int(stat_labels["system.switch_cpu.mmu.itb.rdAccesses"]) + int(stat_labels["system.switch_cpu.mmu.itb.wrAccesses"])
    if num_i_access != 0:
        i_miss_rate.append((int(stat_labels["system.switch_cpu.mmu.itb.rdMisses"]) + int(stat_labels["system.switch_cpu.mmu.itb.wrMisses"])) * 1000 / instructions[i])
    else:
        i_miss_rate.append(0)
        
    i_num_accesses.append(num_i_access)
    print("Instruction Accesses:", num_i_access)
    print("Instruction Miss Rate:", i_miss_rate[i])
    
    print("Integer SIMD Ops:", num_integer_ops[i])
    print("Floating Point SIMD Ops:", num_floating_ops[i])
    
    ipc.append(float(stat_labels["system.switch_cpu.exec_context.thread_0.numInsts"]) / float(stat_labels["system.switch_cpu.numCycles"]))
    print("IPC:", ipc[i], "\n")
    i += 1

book = xlsxwriter.Workbook(stats_path + "stats.xlsx")
sheet = book.add_worksheet('Stats')
sheet.set_column(1, 1, len('Instructions'))
sheet.write(0, 1, 'Instructions')
sheet.set_column(2, 2, len('Data Miss Rate'))
sheet.write(0,2, 'Data Miss Rate')
sheet.set_column(3, 3, len('Instruction Miss Rate'))
sheet.write(0,3, 'Instruction Miss Rate')
sheet.write(0,4, 'IPC')

for i in range(len(ipc)):
    sheet.write(i+1, 0, "Layer " + str(i))
    sheet.write(i+1, 1, instructions[i])
    sheet.write(i+1,2, d_miss_rate[i])
    sheet.write(i+1,3, i_miss_rate[i])
    sheet.write(i+1,4, ipc[i])
    sheet.write(i+1,5, i_num_accesses[i])
    sheet.write(i+1,6, d_num_accesses[i])


instruction_chart = book.add_chart({"type": "column"})
instruction_chart.add_series(
    {
        "name": ["Stats", 0, 1],
        "categories": ["Stats", 1, 0, 7, 0],
        "values": ["Stats", 1, 1, 7, 1],
    }
)
instruction_chart.set_title({"name": "Instructions per Layer"})
instruction_chart.set_y_axis({"name": "Num Instructions"})
instruction_chart.set_x_axis({"name": "Layer"})
instruction_chart.set_style(11)
sheet.insert_chart("B9", instruction_chart, {"x_offset": 25, "y_offset": 10})

ipc_chart = book.add_chart({"type": "column"})
ipc_chart.add_series(
    {
        "name": ["Stats", 0, 4],
        "categories": ["Stats", 1, 0, 7, 0],
        "values": ["Stats", 1, 4, 7, 4],
    }
)
ipc_chart.set_title({"name": "IPC per Layer"})
ipc_chart.set_y_axis({"name": "IPC"})
ipc_chart.set_x_axis({"name": "Layer"})
ipc_chart.set_style(11)
sheet.insert_chart("B24", ipc_chart, {"x_offset": 25, "y_offset": 10})

dmiss_chart = book.add_chart({"type": "column"})
dmiss_chart.add_series(
    {
        "name": ["Stats", 0, 2],
        "categories": ["Stats", 1, 0, 7, 0],
        "values": ["Stats", 1, 2, 7, 2],
    }
)
dmiss_chart.set_title({"name": "Data MPKI per Layer"})
dmiss_chart.set_y_axis({"name": "Miss Rate"})
dmiss_chart.set_x_axis({"name": "Layer"})
dmiss_chart.set_style(11)
sheet.insert_chart("H2", dmiss_chart, {"x_offset": 25, "y_offset": 10})

daccess_chart = book.add_chart({"type": "column"})
daccess_chart.add_series(
    {
        "name": ["Stats", 0, 3],
        "categories": ["Stats", 1, 0, 7, 0],
        "values": ["Stats", 1, 6, 7, 6],
    }
)
daccess_chart.set_title({"name": "Data Access per Layer"})
daccess_chart.set_y_axis({"name": "Num Misses"})
daccess_chart.set_x_axis({"name": "Layer"})
daccess_chart.set_style(11)
sheet.insert_chart("H17", daccess_chart, {"x_offset": 25, "y_offset": 10})

imiss_chart = book.add_chart({"type": "column"})
imiss_chart.add_series(
    {
        "name": ["Stats", 0, 3],
        "categories": ["Stats", 1, 0, 7, 0],
        "values": ["Stats", 1, 3, 7, 3],
    }
)
imiss_chart.set_title({"name": "Instruction MPKI per Layer"})
imiss_chart.set_y_axis({"name": "Num Misses"})
imiss_chart.set_x_axis({"name": "Layer"})
imiss_chart.set_style(11)
sheet.insert_chart("P2", imiss_chart, {"x_offset": 25, "y_offset": 10})

iaccess_chart = book.add_chart({"type": "column"})
iaccess_chart.add_series(
    {
        "name": ["Stats", 0, 3],
        "categories": ["Stats", 1, 0, 7, 0],
        "values": ["Stats", 1, 5, 7, 5],
    }
)
iaccess_chart.set_title({"name": "Instruction Accesses per Layer"})
iaccess_chart.set_y_axis({"name": "Num Misses"})
iaccess_chart.set_x_axis({"name": "Layer"})
iaccess_chart.set_style(11)
sheet.insert_chart("P17", iaccess_chart, {"x_offset": 25, "y_offset": 10})


book.close()
