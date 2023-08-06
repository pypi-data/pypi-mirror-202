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
import numpy as np

from openrl.envs.common import make
from openrl.modules.common import PPONet as Net
from openrl.runners.common import PPOAgent as Agent


def train_agent(env: str):
    render_model = "rgb_array"
    env_num = 9
    env = make(env, render_mode=render_model, env_num=env_num, asynchronous=True)
    # 创建 神经网络
    net = Net(env)

    # 初始化训练器
    agent = Agent(net, use_wandb=False)
    # 开始训练
    agent.train(total_time_steps=20000)

    agent.set_env(env)
    obs, info = env.reset()
    done = False
    step = 0
    total_reward = 0
    while not np.any(done):
        # 智能体根据 observation 预测下一个动作
        action, _ = agent.act(obs, deterministic=True)
        obs, r, done, info = env.step(action)
        total_reward += np.mean(r)
        step += 1
    print(f"Total reward: {total_reward}")

    env.close()
