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
import io
import pathlib

from typing import Union, Dict, Tuple, Optional

import numpy as np
import torch
import gym

from openrl.runners.common.base_agent import BaseAgent
from openrl.runners.common.base_agent import SelfAgent

from openrl.drivers.onpolicy_driver import OnPolicyDriver as Driver
from openrl.algorithms.ppo import PPOAlgorithm as TrainAlgo
from openrl.buffers import NormalReplayBuffer as ReplayBuffer
from openrl.utils.logger import Logger
from openrl.buffers.utils.obs_data import ObsData
from openrl.utils.util import _t2n


class PPOAgent(BaseAgent):
    def __init__(
        self,
        net: Optional[torch.nn.Module] = None,
        env: Union[gym.Env, str] = None,
        run_dir: Optional[str] = None,
        env_num: Optional[int] = None,
        rank: int = 0,
        world_size: int = 1,
        use_wandb: bool = False,
        use_tensorboard: bool = False,
    ) -> None:
        self.net = net
        self._args = net.args
        self._use_wandb = use_wandb
        self._use_tensorboard = not use_wandb and use_tensorboard

        if env is not None:
            self._env = env
        elif hasattr(net, "env") and net.env is not None:
            self._env = net.env
        else:
            raise ValueError("env is None")

        if env_num is not None:
            self.env_num = env_num
        else:
            self.env_num = self._env.parallel_env_num

        self._args.n_rollout_threads = self.env_num
        self._args.learner_n_rollout_threads = self._args.n_rollout_threads

        self.rank = rank
        self.world_size = world_size

        self.client = None
        self.agent_num = self._env.agent_num
        if run_dir is None:
            self.run_dir = self._args.run_dir
        else:
            self.run_dir = run_dir

        if self.run_dir is None:
            assert (not self._use_wandb) and (not self._use_tensorboard), (
                "log_path must be set when using wandb or tensorboard."
                "Please set log_path in PPOAgent or in the config file or pass run_dir in the command line."
            )

        if self._args.experiment_name == "":
            self.exp_name = "ppo"
        else:
            self.exp_name = self._args.experiment_name

    def train(self: SelfAgent, total_time_steps: int) -> None:
        self._args.num_env_steps = total_time_steps

        self.config = {
            "args": self._args,
            "num_agents": self.agent_num,
            "run_dir": self.run_dir,
            "envs": self._env,
            "device": self.net.device,
        }

        trainer = TrainAlgo(
            args=self._args,
            init_module=self.net.module,
            device=self.net.device,
            agent_num=self.agent_num,
        )

        buffer = ReplayBuffer(
            self._args,
            self.agent_num,
            self._env.observation_space,
            self._env.action_space,
            data_client=None,
        )

        logger = Logger(
            args=self._args,
            project_name="PPOAgent",
            scenario_name=self._env.env_name,
            wandb_entity=self._args.wandb_entity,
            exp_name=self.exp_name,
            log_path=self.run_dir,
            use_wandb=self._use_wandb,
            use_tensorboard=self._use_tensorboard,
        )
        driver = Driver(
            config=self.config,
            trainer=trainer,
            buffer=buffer,
            client=self.client,
            rank=self.rank,
            world_size=self.world_size,
            logger=logger,
        )
        driver.run()

    def act(
        self,
        observation: Union[np.ndarray, Dict[str, np.ndarray]],
        deterministic: bool = False,
    ) -> Tuple[np.ndarray, Optional[Tuple[np.ndarray, ...]]]:
        assert self.net is not None, "net is None"
        observation = ObsData.prepare_input(observation)
        action, rnn_state = self.net.act(observation, deterministic=deterministic)

        action = np.array(np.split(_t2n(action), self.env_num))

        return action, rnn_state

    def set_env(
        self,
        env: Union[gym.Env, str] = None,
    ):
        self.net.reset()
        if env is not None:
            self._env = env
            self.env_num = env.parallel_env_num
        env.reset(seed=self._args.seed)

    def save(self, path: Union[str, pathlib.Path, io.BufferedIOBase]) -> None:
        pass
