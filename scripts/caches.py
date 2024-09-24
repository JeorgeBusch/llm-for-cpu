from m5.objects import Cache
from m5.objects.ReplacementPolicies import *
from m5.objects.Prefetcher import *

# Check out src/mem/cache/Cache.py for the Cache class.
# Most of the functionality is in BaseCache found above the Cache class.
# To chance replacement polciies, modify replacement_policy and
# refer to src/mem/cache/replacement_policies/ReplacementPolicies.py

def replParser(replName):
    if replName == "LRUP":
        return LRURP()
    elif replName == "DuelingRP":
        return DuelingRP()
    elif replName == "FIFORP":
        return FIFORP()
    elif replName == "SecondChanceRP":
        return SecondChanceRP()
    elif replName == "LFURP":
        return LFURP()
    elif replName == "BIPRP":
        return BIPRP()
    elif replName == "LIPRP":
        return LIPRP()
    elif replName == "MRURP":
        return MRURP()
    elif replName == "RandomRP":
        return RandomRP()
    elif replName == "BRRIPRP":
        return BRRIPRP()
    elif replName == "RRIPRP":
        return RRIPRP()
    elif replName == "DRRIPRP":
        return DRRIPRP()
    elif replName == "NRURP":
        return NRURP()
    elif replName == "SHiPMemRP":
        return SHiPMemRP()
    elif replName == "SHiPPCRP":
        return SHiPPCRP()
    elif replName == "TreePLRURP":
        return TreePLRURP()
    elif replName == "WeightedLRURP":
        return WeightedLRURP()
    return LRURP()
    
def prefetchParser(prefetchName):
    if prefetchName == "MultiPrefetcher":
        return MultiPrefetcher()
    elif prefetchName == "StridePrefetcherHashedSetAssociative":
        return StridePrefetcherHashedSetAssociative()
    elif prefetchName == "StridePrefetcher":
        return StridePrefetcher()
    elif prefetchName == "TaggedPrefetcher":
        return TaggedPrefetcher()
    elif prefetchName == "IndirectMemoryPrefetcher":
        return IndirectMemoryPrefetcher()
    elif prefetchName == "SignaturePathPrefetcher":
        return SignaturePathPrefetcher()
    elif prefetchName == "SignaturePathPrefetcherV2":
        return SignaturePathPrefetcherV2()
    elif prefetchName == "AccessMapPatternMatching":
        return AccessMapPatternMatching()
    elif prefetchName == "AMPMPrefetcher":
        return AMPMPrefetcher()
    elif prefetchName == "DeltaCorrelatingPredictionTables":
        return DeltaCorrelatingPredictionTables()
    elif prefetchName == "DCPTPrefetcher":
        return DCPTPrefetcher()
    elif prefetchName == "IrregularStreamBufferPrefetcher":
        return IrregularStreamBufferPrefetcher()
    elif prefetchName == "SlimAccessMapPatternMatching":
        return SlimAccessMapPatternMatching()
    elif prefetchName == "SlimDeltaCorrelatingPredictionTables":
        return SlimDeltaCorrelatingPredictionTables()
    elif prefetchName == "SlimAMPMPrefetcher":
        return SlimAMPMPrefetcher()
    elif prefetchName == "BOPPrefetcher":
        return BOPPrefetcher()
    elif prefetchName == "SBOOEPrefetcher":
        return SBOOEPrefetcher()
    elif prefetchName == "STeMSPrefetcher":
        return STeMSPrefetcher()
    elif prefetchName == "HWPProbeEventRetiredInsts":
        return HWPProbeEventRetiredInsts()
    elif prefetchName == "PIFPrefetcher":
        return PIFPrefetcher()
    return NULL
    
# Numbers for caches referenced from
# Customizing Cache Indexing through Entropy Estimation
# Numbers for embeded:
# https://www.arm.com/products/silicon-ip-cpu/cortex-a/cortex-a72
# Numbers for high:
# https://www.nas.nasa.gov/hecc/support/kb/cascade-lake-processors_579.html
# https://www.intel.com/content/www/us/en/products/sku/198652/intel-xeon-gold-6250-processor-35-75m-cache-3-90-ghz/specifications.html

    
class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 16
    tgts_per_mshr = 20
    
    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass
    
    def connectCPU(self, cpu):
        # define this in base class
        raise NotImplementedError
        
    def preset_config(self, preset):
        raise NotImplementedError
        
    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports
    
    
class L1ICache(L1Cache):
    size = '32kB'
    
    def preset_config(self, preset):
        if(preset == "medium"):
            self.size = '32kB'
            self.assoc = 2
            self.tag_latency = 2
            self.data_latency = 2
            self.response_latency = 2
            self.mshrs = 8
            self.tgts_per_mshr = 20
        if(preset == "embedded"):
            self.size = '32kB' # 48kB causes gem5 to crash
            self.assoc = 2
            self.tag_latency = 2
            self.data_latency = 2
            self.response_latency = 2
            self.mshrs = 8
            self.tgts_per_mshr = 20
        if(preset == "high"):
            self.size = '32kB'
            self.assoc = 2
            self.tag_latency = 2
            self.data_latency = 2
            self.response_latency = 2
            self.mshrs = 16
            self.tgts_per_mshr = 20
            pass
    
    def __init__(self, options=None):
        super(L1ICache, self).__init__(options)
        if not options:
            return
        if options.preset:
            self.preset_config(options.preset)
        if options.l1_replpolicy:
            self.replacement_policy = replParser(options.l1_replpolicy)
            
    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    size = '32kB'
    
    def preset_config(self, preset):
        if(preset == "medium"):
            self.size = '32kB'
            self.assoc = 2
            self.tag_latency = 2
            self.data_latency = 2
            self.response_latency = 2
            self.mshrs = 16
            self.tgts_per_mshr = 20
        if(preset == "embedded"):
            self.size = '32kB'
            self.assoc = 2
            self.tag_latency = 2
            self.data_latency = 2
            self.response_latency = 2
            self.mshrs = 16
            self.tgts_per_mshr = 20
        if(preset == "high"):
            self.size = '32kB'
            self.assoc = 2
            self.tag_latency = 2
            self.data_latency = 2
            self.response_latency = 2
            self.mshrs = 16
            self.tgts_per_mshr = 20
    
    def __init__(self, options=None):
        super(L1DCache, self).__init__(options)
        if not options:
            return
        if options.preset:
            self.preset_config(options.preset)
        if options.l1d_prefetcher:
            self.prefetcher = prefetchParser(options.l1d_prefetcher)
        if options.l1_replpolicy:
            self.replacement_policy = replParser(options.l1_replpolicy)
            
    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port
    
class L2Cache(Cache):
    size = '128kB'
    assoc = 4
    tag_latency = 8
    data_latency = 8
    response_latency = 8
    mshrs = 32
    tgts_per_mshr = 12
    
    def preset_config(self, preset):
        if(preset == "medium"):
            self.size = '512kB'
            self.assoc = 4
            self.tag_latency = 8
            self.data_latency = 8
            self.response_latency = 8
            self.mshrs = 32
            self.tgts_per_mshr = 12
        if(preset == "embedded"):
            self.size = '128kB'
            self.assoc = 4
            self.tag_latency = 8
            self.data_latency = 8
            self.response_latency = 8
            self.mshrs = 32
            self.tgts_per_mshr = 12
        if(preset == "high"):
            self.size = '1MB'
            self.assoc = 4
            self.tag_latency = 8
            self.data_latency = 8
            self.response_latency = 8
            self.mshrs = 32
            self.tgts_per_mshr = 12
    
    def __init__(self, options=None):
        super(L2Cache, self).__init__()
        if not options:
            return
        if options.preset:
            self.preset_config(options.preset)
        if options.l2_prefetcher:
            self.prefetcher = prefetchParser(options.l2_prefetcher)
        if options.l2_replpolicy:
            self.replacement_policy = replParser(options.l2_replpolicy)
    
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports
        
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
        
    def connectMemSideCache(self, cache):
        self.mem_side = cache.cpu_side
        
class L3Cache(Cache):
    size = '2MB'
    assoc = 16
    tag_latency = 32
    data_latency = 32
    response_latency = 32
    mshrs = 64
    tgts_per_mshr = 12
    
    def preset_config(self, preset):
        if(preset == "medium"):
            self.size = '1MB'
            self.assoc = 16
            self.tag_latency = 32
            self.data_latency = 32
            self.response_latency = 32
            self.mshrs = 64
            self.tgts_per_mshr = 12
        if(preset == "embedded"):
            pass
        if(preset == "high"):
            self.size = '2MB'
            self.assoc = 16
            self.tag_latency = 32
            self.data_latency = 32
            self.response_latency = 32
            self.mshrs = 64
            self.tgts_per_mshr = 12
            pass
    
    def __init__(self, options=None):
        super(L3Cache, self).__init__()
        if not options:
            return
        if options.preset:
            self.preset_config(options.preset)
        if options.l3_replpolicy:
            self.replacement_policy = replParser(options.l3_replpolicy)
            
    def connectCPUSideCache(self, cache):
        self.cpu_side = cache.mem_side
        
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
