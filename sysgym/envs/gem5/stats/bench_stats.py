from dataclasses import dataclass


@dataclass
class SummaryStats:
    # main three objectives
    cycle: int
    total_area: int
    avg_power: float
    # fu power
    idle_fu_cycles: int
    avg_fu_power: float
    avg_fu_dynamic_power: float
    avg_fu_leakage_power: float
    # mem power
    avg_mem_power: float
    avg_mem_dynamic_power: float
    avg_mem_leakage_power: float
    # area
    fu_area: int
    mem_area: float
    num_registers: int

    #  ##################### OPTIONAL REPORTS #############
    # These can be zero, see:
    # https://github.com/harvard-acc/ALADDIN/blob/26786c6c4c25ac8c726b56b7ac87cf5579ff4794/common/BaseDatapath.cpp#L783

    num_single_precision_fp_multipliers: float = 0.0
    num_single_precision_fp_adders: float = 0.0
    num_double_precision_fp_multipliers: float = 0.0
    num_double_precision_fp_adders: float = 0.0
    num_trigonometric_units: float = 0.0
    num_bitwise_operators: float = 0.0
    num_multipliers: float = 0.0
    num_shifters: float = 0.0
