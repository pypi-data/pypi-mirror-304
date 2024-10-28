from gymnasium.envs.registration import register

register(
    id="simiao-sumo-rl-v0",
    entry_point="gym_examples.envs:SUMOEnv",
)