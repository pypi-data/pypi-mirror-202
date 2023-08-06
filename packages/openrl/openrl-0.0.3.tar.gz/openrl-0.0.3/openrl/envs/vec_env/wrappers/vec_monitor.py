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
from typing import Any, Dict
import time

import numpy as np
from gymnasium.core import ActType

from openrl.envs.vec_env.base_venv import (
    BaseVecEnv,
)
from openrl.envs.vec_env.wrappers.base_wrapper import VecEnvWrapper


class VecInfo:
    def __init__(self, parallel_env_num, agent_num):
        self.parallel_env_num = parallel_env_num
        self.agent_num = agent_num

        self.infos = []
        self.rewards = []

        self.start_time = time.time()
        self.total_step = 0

    def statistics(self) -> Dict[str, Any]:
        # this function should be called each episode
        rewards = np.array(self.rewards)
        self.total_step += np.prod(rewards.shape[:2])
        rewards = rewards.transpose(2, 1, 0, 3)
        info_dict = {}
        ep_rewards = []
        for i in range(self.agent_num):
            agent_reward = rewards[i].mean(0).sum()
            ep_rewards.append(agent_reward)
            info_dict["agent_{}/episode_reward".format(i)] = agent_reward

        info_dict["FPS"] = int(self.total_step / (time.time() - self.start_time))
        info_dict["episode_reward"] = np.mean(ep_rewards)
        return info_dict

    def append(self, reward, info):
        assert reward.shape[:2] == (self.parallel_env_num, self.agent_num)
        self.infos.append(info)
        self.rewards.append(reward)

    def reset(self):
        self.infos = []
        self.rewards = []


class VecMonitor(VecEnvWrapper):
    def __init__(self, env: BaseVecEnv):
        super().__init__(env)
        self.vec_info = VecInfo(self.env.parallel_env_num, self.env.agent_num)

    @property
    def use_monitor(self):
        return True

    def step(self, action: ActType):
        returns = self.env.step(action)

        self.vec_info.append(reward=returns[1], info=returns[-1])

        return returns

    def statistics(self):
        # this function should be called each episode
        info_dict = self.vec_info.statistics()
        self.vec_info.reset()
        return info_dict
