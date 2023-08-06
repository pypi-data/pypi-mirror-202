# MPE env fetched from https://github.com/marlbenchmark/on-policy/tree/main/onpolicy/envs/mpe
from gymnasium import Env
from typing import Optional, Union, List, Callable, Iterable
from openrl.envs.common import build_envs
from openrl.envs.mpe.mpe_env import make

all_envs = [
    "simple_spread",
]


def make_mpe_envs(
    id: str,
    env_num: int = 1,
    render_mode: Optional[Union[str, List[str]]] = None,
    **kwargs,
) -> List[Callable[[], Env]]:
    env_wrappers = []
    env_fns = build_envs(
        make=make,
        id=id,
        env_num=env_num,
        render_mode=render_mode,
        wrappers=env_wrappers,
        **kwargs,
    )
    return env_fns
