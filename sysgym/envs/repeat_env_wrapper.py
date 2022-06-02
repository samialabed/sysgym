import functools
import logging
from collections import defaultdict
from dataclasses import asdict
from typing import Callable, Dict, Type

import dacite

from sysgym.envs.env_measure import EnvMeasurements
from sysgym.envs.params_dict_abc import EnvParamsDict

LOG = logging.getLogger("sysgym")


def moving_avg_func(prev_avg: float, new_val: float, n: int):
    prev_avg = prev_avg if prev_avg else 0.0
    new_val = new_val if new_val else 0.0

    return (prev_avg * (n - 1) + new_val) / n


def map_nested_dicts_modify(
    mutable_ob: Dict[str, any],
    new_observations: Dict[str, any],
    func: Callable[[any, any], any],
):
    for k, v in new_observations.items():
        if isinstance(v, Dict):
            if not mutable_ob.get(k):
                mutable_ob[k] = {}
            map_nested_dicts_modify(mutable_ob[k], v, func)
        else:
            mutable_ob[k] = func(mutable_ob.get(k), v)


def repeat_env(num_times: int, cls: Type[EnvMeasurements]):
    def decorator_repeat(
        func: Callable[[EnvParamsDict], EnvMeasurements]
    ) -> Callable[[EnvParamsDict], EnvMeasurements]:
        @functools.wraps(func)
        def wrapper_repeater(*args, **kwargs) -> EnvMeasurements:
            avg_env_measures = defaultdict(float)
            for repetition_count in range(1, num_times + 1):
                LOG.info(
                    "Repeating the environment: %s/%s", repetition_count, num_times
                )
                env_measures = func(*args, **kwargs)
                # nested dictionary
                env_measures_asdict = asdict(env_measures)
                # TODO: seems inefficient? but even if we are using numpy/pandas we
                #  will still need to loop through the array to build it
                #  Vectorization might not be worth it especially since the repetition
                #  usually 3-5
                map_nested_dicts_modify(
                    mutable_ob=avg_env_measures,
                    new_observations=env_measures_asdict,
                    func=lambda prev_avg, new_val: moving_avg_func(
                        prev_avg=prev_avg, new_val=new_val, n=repetition_count
                    ),
                )
            env_measurements_avg = dacite.from_dict(
                data_class=cls,
                data=avg_env_measures,
                config=dacite.Config(check_types=False, strict=True),
            )
            return env_measurements_avg

        return wrapper_repeater

    return decorator_repeat
