from dataclasses import dataclass


@dataclass
class CacheStats(object):
    # TODO: we only consider tlb and dcache for now, when we add support for others we can incorporate them here

    # Average dcache dynamic and leakage power.
    system_datapath_dcache_average_pwr: float
    system_datapath_dcache_dynamic_pwr: float  # Average dcache dynamic power.
    system_datapath_dcache_leakage_pwr: float  # Average dcache leakage power.
    system_datapath_dcache_area: float  # dcache area.
    system_datapath_tlb_average_pwr: float  # Average tlb dynamic and leakage power.
    system_datapath_tlb_dynamic_pwr: float  # Average tlb dynamic power.
    system_datapath_tlb_leakage_pwr: float  # Average tlb leakage power.
    system_datapath_tlb_area: float  # tlb area.
