import functools
import logging
from collections import defaultdict
from dataclasses import asdict
from typing import Callable, Dict

import dacite

from sysgym.env_abc import EnvMetrics
from sysgym.param_dict import EnvParamsDict

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


def repeat_env(num_times: int):
    """Wrapper that allows repeating an execution multiple times and then average the
    environment results"""

    def decorator_repeat(
        func: Callable[[EnvParamsDict], EnvMetrics]
    ) -> Callable[[EnvParamsDict], EnvMetrics]:
        @functools.wraps(func)
        def wrapper_repeater(*args, **kwargs) -> EnvMetrics:
            avg_env_metrics = defaultdict(float)
            env_metrics = None
            for repetition_count in range(1, num_times + 1):
                LOG.info(
                    "Repeating the environment: %s/%s", repetition_count, num_times
                )
                env_metrics = func(*args, **kwargs)
                # nested dictionary
                env_measures_asdict = asdict(env_metrics)
                # TODO: seems inefficient? but even if we are using numpy/pandas we
                #  will still need to loop through the array to build it
                #  Vectorization might not be worth it especially since the repetition
                #  usually 3-5
                map_nested_dicts_modify(
                    mutable_ob=avg_env_metrics,
                    new_observations=env_measures_asdict,
                    func=lambda prev_avg, new_val: moving_avg_func(
                        prev_avg=prev_avg, new_val=new_val, n=repetition_count
                    ),
                )
            if not env_metrics:
                # TODO: use a more narrow exception
                raise Exception("Env metrics returned empty")

            env_measurements_avg = dacite.from_dict(
                data_class=type(env_metrics),
                data=avg_env_metrics,
                config=dacite.Config(check_types=False, strict=True),
            )
            return env_measurements_avg

        return wrapper_repeater

    return decorator_repeat
