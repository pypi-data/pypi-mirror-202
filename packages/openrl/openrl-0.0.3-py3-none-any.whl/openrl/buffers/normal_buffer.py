from .replay_data import ReplayData


class NormalReplayBuffer(object):
    def __init__(
        self, args, num_agents, obs_space, act_space, data_client, episode_length=None
    ):
        if episode_length is None:
            episode_length = args.episode_length
        self.data = ReplayData(
            args,
            num_agents,
            obs_space,
            act_space,
            data_client,
            episode_length,
        )

    def init_buffer(self, raw_obs, available_actions=None):
        self.data.init_buffer(raw_obs, available_actions)

    def insert(
        self,
        raw_obs,
        rnn_states,
        rnn_states_critic,
        actions,
        action_log_probs,
        value_preds,
        rewards,
        masks,
        bad_masks=None,
        active_masks=None,
        available_actions=None,
    ):
        self.data.insert(
            raw_obs,
            rnn_states,
            rnn_states_critic,
            actions,
            action_log_probs,
            value_preds,
            rewards,
            masks,
            bad_masks,
            active_masks,
            available_actions,
        )

    def after_update(self):
        self.data.after_update()

    def compute_returns(self, next_value, value_normalizer=None):
        self.data.compute_returns(next_value, value_normalizer)

    def feed_forward_generator(
        self,
        advantages,
        num_mini_batch=None,
        mini_batch_size=None,
        critic_obs_process_func=None,
    ):
        return self.data.feed_forward_generator(
            advantages,
            num_mini_batch,
            mini_batch_size,
            critic_obs_process_func=critic_obs_process_func,
        )

    def feed_forward_critic_obs_generator(
        self,
        advantages,
        num_mini_batch=None,
        mini_batch_size=None,
        critic_obs_process_func=None,
    ):
        # 只包含critic_obs和action
        return self.data.feed_forward_critic_obs_generator(
            advantages,
            num_mini_batch,
            mini_batch_size,
            critic_obs_process_func=critic_obs_process_func,
        )

    def naive_recurrent_generator(self, advantages, num_mini_batch):
        return self.data.naive_recurrent_generator(advantages, num_mini_batch)

    def recurrent_generator(self, advantages, num_mini_batch, data_chunk_length):
        return self.data.recurrent_generator(
            advantages, num_mini_batch, data_chunk_length
        )
