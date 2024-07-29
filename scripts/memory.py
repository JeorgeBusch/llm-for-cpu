from m5.objects import *

# Refer to src/mem/DRAMInterface.py

def configMemory(memName):
    if memName == "DDR3_1600_8x8":
        return DDR3_1600_8x8()
    elif memName == "HMC_2500_1x32":
        return HMC_2500_1x32()
    elif memName == "FIFORP":
        return FIFORP()
    elif memName == "DDR3_2133_8x8":
        return DDR3_2133_8x8()
    elif memName == "DDR4_2400_16x4":
        return DDR4_2400_16x4()
    elif memName == "DDR4_2400_8x8":
        return DDR4_2400_8x8()
    elif memName == "DDR4_2400_4x16":
        return DDR4_2400_4x16()
    elif memName == "LPDDR2_S4_1066_1x32":
        return LPDDR2_S4_1066_1x32()
    elif memName == "WideIO_200_1x128":
        return WideIO_200_1x128()
    elif memName == "LPDDR3_1600_1x32":
        return LPDDR3_1600_1x32()
    elif memName == "GDDR5_4000_2x32":
        return GDDR5_4000_2x32()
    elif memName == "HBM_1000_4H_1x128":
        return HBM_1000_4H_1x128()
    elif memName == "HBM_1000_4H_1x64":
        return HBM_1000_4H_1x64()
    elif memName == "LPDDR5_5500_1x16_BG_BL32":
        return LPDDR5_5500_1x16_BG_BL32()
    elif memName == "LPDDR5_5500_1x16_BG_BL16":
        return LPDDR5_5500_1x16_BG_BL16()
    elif memName == "LPDDR5_5500_1x16_8B_BL32":
        return LPDDR5_5500_1x16_8B_BL32()
    elif memName == "LPDDR5_5500_1x16_8B_BL32":
        return LPDDR5_5500_1x16_8B_BL32()
    elif memName == "LPDDR5_6400_1x16_BG_BL16":
        return LPDDR5_6400_1x16_BG_BL16()
    elif memName == "LPDDR5_6400_1x16_8B_BL32":
        return LPDDR5_6400_1x16_8B_BL32()
    return DDR3_1600_8x8()