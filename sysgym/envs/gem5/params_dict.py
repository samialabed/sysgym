from typing import List

from sysgym.envs.params_dict_abc import EnvParamsDict


class Gem5ParamsDict(EnvParamsDict):
    """Helper methods that translate between env params and system params"""

    def as_sys(self) -> List[str]:
        # TODO: workaround dependency until we do a refactor for schema system
        opts = []

        for param in self._schema.parameters():
            val = self[param.name]
            if param.name == "cache_size":
                # Cache_size has to be x * cache_line_sz * cache_assoc
                val = val * self["cache_line_sz"] * self["cache_assoc"]
            elif param.name == "tlb_entries":
                # Note: tlb_entries has to be tlb_entries * tlb_assoc
                val = val * self["tlb_assoc"]

            opts.append(f"set {param.name} {val}")
        return opts
