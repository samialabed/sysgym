import re

E_NUM_REGEX = r"(?:e[\+\-][0-9]+)?"
FLOAT_NUM_PARSER = rf"\d+.?\d*{E_NUM_REGEX}"  # Support nums like e-35 and e+2
VALUE_REGEX = r"([\d+.?\d*[e\+[0-9]+]?|nan|inf)"
KEY_TO_VALUE_REGEX = r"^(\w+(?:\.\w+)+)"

SUMMARY_PARSERS = {
    "cycle": re.compile(r"(.*) cycles"),
    "avg_power": re.compile(r"(.*) mW"),
    "idle_fu_cycles": re.compile(r"(.*) cycles"),
    "avg_fu_cycles": re.compile(r"(.*) mW"),
    "avg_fu_power": re.compile(r"(.*) mW"),
    "avg_fu_dynamic_power": re.compile(r"(.*) mW"),
    "avg_fu_leakage_power": re.compile(r"(.*) mW"),
    "avg_mem_power": re.compile(r"(.*) mW"),
    "avg_mem_dynamic_power": re.compile(r"(.*) mW"),
    "avg_mem_leakage_power": re.compile(r"(.*) mW"),
    "total_area": re.compile(r"(.*) uM\^2"),
    "fu_area": re.compile(r"(.*) uM\^2"),
    "mem_area": re.compile(r"(.*) uM\^2"),
    "num_double_precision_fp_multipliers": re.compile(r"(.*)"),
    "num_double_precision_fp_adders": re.compile(r"(.*)"),
    "num_trigonometric_units": re.compile(r"(.*)"),
    "num_bitwise_operators": re.compile(r"(.*)"),
    "num_shifters": re.compile(r"(.*)"),
    "num_registers": re.compile(r"(.*)"),
}
SYSTEM_RES_PARSER = re.compile(
    rf"^(\w+)\s+({FLOAT_NUM_PARSER})", flags=re.RegexFlag.MULTILINE
)
PERFORMANCE_PARSER = re.compile(
    rf"{KEY_TO_VALUE_REGEX}\s+{VALUE_REGEX}", flags=re.RegexFlag.MULTILINE
)
CACHE_STATS_PARSER = re.compile(rf"(\S+) ({FLOAT_NUM_PARSER})")
