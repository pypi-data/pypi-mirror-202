#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2023 The OpenRL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""""""
from typing import Optional, Union, List, Callable, Iterable
import gymnasium as gym

from gymnasium import Env

import openrl

from openrl.envs.vec_env import (
    SyncVectorEnv,
    AsyncVectorEnv,
    VecMonitor,
)


def make(
    id: str,
    env_num: int = 1,
    asynchronous: bool = False,
    add_monitor: bool = True,
    render_mode: Optional[str] = None,
    **kwargs,
) -> Env:
    if render_mode in [None, "human", "rgb_array"]:
        convert_render_mode = render_mode
    elif render_mode in ["group_human", "group_rgb_array"]:
        # will display all the envs (when render_mode == "group_human")
        # or return all the envs' images (when render_mode == "group_rgb_array")
        convert_render_mode = "rgb_array"
    elif render_mode == "single_human":
        # will only display the first env
        convert_render_mode = [None] * (env_num - 1)
        convert_render_mode = ["human"] + convert_render_mode
        render_mode = None
    elif render_mode == "single_rgb_array":
        # env.render() will only return the first env's image
        convert_render_mode = [None] * (env_num - 1)
        convert_render_mode = ["rgb_array"] + convert_render_mode
    else:
        raise NotImplementedError(f"render_mode {render_mode} is not supported.")

    if id in gym.envs.registry.keys():
        from openrl.envs.gymnasium import make_gym_envs

        env_fns = make_gym_envs(
            id=id, env_num=env_num, render_mode=convert_render_mode, **kwargs
        )
    elif id in openrl.envs.mpe.all_envs:
        from openrl.envs.mpe import make_mpe_envs

        env_fns = make_mpe_envs(
            id=id, env_num=env_num, render_mode=convert_render_mode, **kwargs
        )
    else:
        raise NotImplementedError(f"env {id} is not supported.")

    if asynchronous:
        env = AsyncVectorEnv(env_fns, render_mode=render_mode)
    else:
        env = SyncVectorEnv(env_fns, render_mode=render_mode)

    if add_monitor:
        env = VecMonitor(env)

    return env


def build_envs(
    make,
    id: str,
    env_num: int = 1,
    render_mode: Optional[Union[str, List[str]]] = None,
    disable_env_checker: Optional[bool] = None,
    wrappers: Optional[Union[Callable[[Env], Env], List[Callable[[Env], Env]]]] = None,
    **kwargs,
) -> List[Callable[[], Env]]:
    def create_env(env_id: int) -> Callable[[], Env]:
        """Creates an environment that can enable or disable the environment checker."""
        # If the env_id > 0 then disable the environment checker otherwise use the parameter
        _disable_env_checker = True if env_id > 0 else disable_env_checker

        def _make_env() -> Env:
            if isinstance(render_mode, list):
                env_render_mode = render_mode[env_id]
            else:
                env_render_mode = render_mode

            env = make(
                id,
                render_mode=env_render_mode,
                disable_env_checker=_disable_env_checker,
                **kwargs,
            )
            if wrappers is not None:
                if callable(wrappers):
                    env = wrappers(env)
                elif isinstance(wrappers, Iterable) and all(
                    [callable(w) for w in wrappers]
                ):
                    for wrapper in wrappers:
                        env = wrapper(env)
                else:
                    raise NotImplementedError
            return env

        return _make_env

    env_fns = [create_env(env_id) for env_id in range(env_num)]
    return env_fns
