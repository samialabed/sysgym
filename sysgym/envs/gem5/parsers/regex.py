import re

FLOAT_NUM_PARSER = r"\d+.?\d*[e\+[0-9]+]?"
summary_file_regex = {
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
system_parser = re.compile(
    rf"^(\w+)\s+({FLOAT_NUM_PARSER})", flags=re.RegexFlag.MULTILINE
)
val_re = r"([\d+.?\d*[e\+[0-9]+]?|nan|inf)"
dis_func_re = r"::(\D\S+)"
key_re = r"^(\w+(?:\.\w+)+)"
performance_parser = re.compile(rf"{key_re}\s+{val_re}", flags=re.RegexFlag.MULTILINE)
