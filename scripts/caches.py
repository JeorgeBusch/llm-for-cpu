from m5.objects import Cache

# Check out src/mem/cache/Cache.py for the Cache class.
# Most of the functionality is in BaseCache found above the Cache class.
# To chance replacement polciies, modify replacement_policy and
# refer to src/mem/cache/replacement_policies/ReplacementPolicies.py

class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    
    def connectCPU(self, cpu):
        # define this in base class
        raise NotImplementedError
        
    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports
    
    
class L1ICache(L1Cache):
    size = '16kB'
    
    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    size = '64kB'
    
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
    
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports
        
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports