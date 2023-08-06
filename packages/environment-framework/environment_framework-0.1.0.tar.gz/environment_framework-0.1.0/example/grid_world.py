# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:hydrogen
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Grid World example
#
# In this notebook we implement the GridWorld game with the `environment-framework` and use stable-baseliens3 to train a `DQN`-agent on it.

# %%
from enum import Enum
from random import randint
from typing import Any, List, Tuple

from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.dqn import DQN


import cv2
import numpy as np

from environment_framework.level import ActionSpace, Level, ObservationSpace
from environment_framework.gym import SimulatorFrameworkGym
from environment_framework.simulator import Simulator


# %% [markdown]
# ## Implement the `Game`


# %%
class Action(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3


class GridWorldGame:
    def __init__(self, size: int) -> None:
        self.size = size
        self.player_position = (0, 0)
        self.target_position = (0, 0)
        self.reset()

    @property
    def done(self) -> bool:
        return self.player_position == self.target_position

    def act(self, action: Action, **_: Any) -> None:
        if action == Action.UP:
            self.player_position = (self.player_position[0], self.player_position[1] - 1)
        if action == Action.DOWN:
            self.player_position = (self.player_position[0], self.player_position[1] + 1)
        if action == Action.RIGHT:
            self.player_position = (self.player_position[0] + 1, self.player_position[1])
        if action == Action.LEFT:
            self.player_position = (self.player_position[0] - 1, self.player_position[1])
        corrected_x = max(0, min(self.size - 1, self.player_position[0]))
        corrected_y = max(0, min(self.size - 1, self.player_position[1]))
        self.player_position = (corrected_x, corrected_y)

    def reset(self) -> None:
        def get_random_position() -> int:
            return randint(0, self.size - 1)

        self.player_position = (get_random_position(), get_random_position())
        self.target_position = (get_random_position(), get_random_position())
        if self.done:
            self.reset()


# %% [markdown]
# ## Implement the `Observer` and the `Estimator`


# %%
class GridWorldObserver:
    def __init__(self, game: GridWorldGame) -> None:
        self.game = game

    @property
    def shape(self) -> Tuple[int, ...]:
        return (4,)

    def observe(self, _: Any) -> List[float]:
        return [*self.game.player_position, *self.game.target_position]


class GridWorldEstimator:
    def __init__(self, game: GridWorldGame) -> None:
        self.game = game

    def estimate(self, _: Any) -> float:
        return -1 + float(self.game.done)


# %% [markdown]
# ## Add a nice little `Visualizer`


# %%
class GridWorldVisualizer:
    # We use BGR
    BLUE = [255, 0, 0]
    GREEN = [0, 255, 0]

    def __init__(self, game: GridWorldGame) -> None:
        self.game = game

    def render(self, _: Any) -> Any:
        frame = [[[0 for k in range(3)] for j in range(self.game.size)] for i in range(self.game.size)]
        frame[self.game.player_position[1]][self.game.player_position[0]] = self.BLUE
        frame[self.game.target_position[1]][self.game.target_position[0]] = self.GREEN
        return frame


# %% [markdown]
# ## Connect all together with a `Level`


# %%
class GridWorldLevel(Level):
    _game: GridWorldGame
    _observer: GridWorldObserver
    _estimator: GridWorldEstimator
    _visualizer: GridWorldVisualizer

    def __init__(
        self,
        game: GridWorldGame,
        observer: GridWorldObserver,
        estimator: GridWorldEstimator,
        visualizer: GridWorldVisualizer,
    ) -> None:
        super().__init__(game, observer, estimator, visualizer)

    def reset(self) -> None:
        self._game.reset()

    def step(self, action: Action) -> Any:
        if isinstance(action, np.int64):  # handle integer inputs
            action = Action(action)
        self._game.act(action)

    @property
    def action_space(self) -> ActionSpace:
        return ActionSpace("discrete", 4)

    @property
    def observation_space(self) -> ObservationSpace:
        return ObservationSpace("discrete", (4,))


class GridWorldSimulation:
    def __init__(self, level: GridWorldLevel) -> None:
        self.level = level
        self.level_settings = None


# %% [markdown]
# ## Look at a random selecting agent

# %%
game = GridWorldGame(7)
scale_factor = 10
level = GridWorldLevel(game, GridWorldObserver(game), GridWorldEstimator(game), GridWorldVisualizer(game))
simulator = Simulator(GridWorldSimulation(level))
while not simulator.done:
    action = Action(randint(0, 3))
    simulator.step(action)
    frame = np.array(simulator.render(), dtype=np.uint8)
    frame = cv2.resize(frame, (scale_factor * game.size, scale_factor * game.size), interpolation=cv2.INTER_AREA)
    cv2.imshow("GridWorld", frame)
    cv2.waitKey(33)
cv2.waitKey(500)
cv2.destroyAllWindows()

# %% [markdown]
# ## Use stable-baselines3 to train an DQN-agent in the environment

# %%
game = GridWorldGame(7)
level = GridWorldLevel(game, GridWorldObserver(game), GridWorldEstimator(game), GridWorldVisualizer(game))
simulator = Simulator(GridWorldSimulation(level))
env = SimulatorFrameworkGym(GridWorldSimulation(level), render_mode="rgb_array")

model = DQN("MlpPolicy", env)
model.learn(
    total_timesteps=int(2.5e5),
    progress_bar=True,
)

# %%
evaluate_policy(model, env, n_eval_episodes=10)

# %%
model.save("gridworld-dqn.zip")

# %%
game = GridWorldGame(7)
scale_factor = 20
level = GridWorldLevel(game, GridWorldObserver(game), GridWorldEstimator(game), GridWorldVisualizer(game))
simulator = Simulator(GridWorldSimulation(level))
env = SimulatorFrameworkGym(GridWorldSimulation(level), render_mode="rgb_array")

model = DQN.load("gridworld-dqn.zip", env=env)
vec_env = model.get_env()
obs = vec_env.reset()
for _ in range(50):
    obs = np.array(obs)
    action, _states = model.predict(obs)  # type: ignore
    obs, _, _, _ = vec_env.step(action)
    frame = np.array(vec_env.render(), dtype=np.uint8)
    frame = cv2.resize(frame, (scale_factor * game.size, scale_factor * game.size), interpolation=cv2.INTER_AREA)
    cv2.imshow("GridWorld", frame)
    cv2.waitKey(250)
cv2.waitKey(500)
cv2.destroyAllWindows()
