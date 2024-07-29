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
    elif replName == "SHiPRP":
        return SHiPRP()
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
    if prefetchName == "BasePrefetcher":
        return BasePrefetcher()
    elif prefetchName == "MultiPrefetcher":
        return MultiPrefetcher()
    elif prefetchName == "QueuedPrefetcher":
        return QueuedPrefetcher()
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
    return BasePrefetcher()
    
class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    
    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass
    
    def connectCPU(self, cpu):
        # define this in base class
        raise NotImplementedError
        
    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports
    
    
class L1ICache(L1Cache):
    size = '16kB'
    
    def __init__(self, options=None):
        super(L1ICache, self).__init__(options)
        if not options:
            return
        if options.l1i_size:
            self.size = options.l1i_size
        if options.l1i_replpolicy:
            self.replacement_policy = replParser(options.l1i_replpolicy)
        if options.l1i_prefetcher:
            self.prefetcher = prefetchParser(options.l1i_prefetcher)
    
    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    size = '64kB'
    
    def __init__(self, options=None):
        super(L1DCache, self).__init__(options)
        if not options:
            return
        if options.l1d_size:
            self.size = options.l1d_size
        if options.l1d_replpolicy:
            self.replacement_policy = replParser(options.l1d_replpolicy)
        if options.l1d_prefetcher:
            self.prefetcher = prefetchParser(options.l1d_prefetcher)
    
    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port
    
class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    
    def __init__(self, options=None):
        super(L2Cache, self).__init__()
        if not options:
            return
        if options.l2_size:
            self.size = options.l2_size
        if options.l2_replpolicy:
            self.replacement_policy = replParser(options.l2_replpolicy)
        if options.l2_prefetcher:
            self.prefetcher = prefetchParser(options.l2_prefetcher)
    
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports
        
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports