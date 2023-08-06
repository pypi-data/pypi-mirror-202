from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Protocol, Tuple

from environment_framework.estimator import Estimator
from environment_framework.game import Game
from environment_framework.observer import Observer
from environment_framework.visualizer import Visualizer


@dataclass
class ObservationSpace:
    # TODO: Add doc
    type_: str
    shape: Tuple[int, ...]


@dataclass
class ActionSpace:
    # TODO: Add doc
    type_: str
    shape: int


class ILevel(Protocol):
    @property
    def done(self) -> bool:
        """
        Returns if the game in the level has reached the end state.

        Returns
        -------
            done: bool
                Game has reached its end state.
        """

    @property
    def observation_space(self) -> ObservationSpace:
        """
        Return the desciribtion of the observation space.

        Returns
        -------
            observation_space: ObservationSpace
                The observation space describtion.
        """

    @property
    def action_space(self) -> ActionSpace:
        """
        Return the desciribtion of the action space.

        Returns
        -------
            observation_space: ActionSpace
                The action space describtion.
        """

    def reset(self) -> None:
        """
        Reset the level.
        """

    def step(self, action: Any) -> Any:
        """
        Take a step in the level with a given action.

        Parameters
        ----------
            action: Any
                Object which describes the action.
        Returns
        -------
            state: Any
                The step in which is the level after the action.
        """

    def observe(self) -> List[float]:
        """
        Observes the level and returns an observation.

        Returns
        -------
            observation: List[float]
                Observation of the current level state.
        """

    def estimate(self, estimated: Any) -> float:
        """
        Estimates the level state and returns a estimation value.

        Returns
        -------
            estimation: float
                Estimated reward of the current level state.
        """

    def render(self) -> Any:
        """
        Renders the current level state into a visualisation.

        Returns
        -------
            visualisation: Any
                Rendered visualisation of the current level state.
        """


class Level(ABC):  # pylint: disable=too-many-instance-attributes
    """
    Manages the lifecycle of a game and its observer and estimator.
    Is used within the Simulator to step through a Simulation.
    """

    def __init__(self, game: Game, observer: Observer, estimator: Estimator, visualizer: Visualizer) -> None:
        """
        Parameters
        ----------
            game: Game
                The game in which the level takes place.
            observer: Observer
                The observer of the game.
            estimator: Estimator
                The estimator of the game.
            visualizer: Visualizer
                The visualizer of the game.
        """
        self._game = game
        self._observer = observer
        self._estimator = estimator
        self._visualizer = visualizer

    @property
    def done(self) -> bool:
        """
        Returns if the game in the level has reached the end state.

        Returns
        -------
            done: bool
                Game has reached its end state.
        """
        return self._game.done

    @property
    @abstractmethod
    def observation_space(self) -> ObservationSpace:
        """
        Return the desciribtion of the observation space.

        Returns
        -------
            observation_space: ObservationSpace
                The observation space describtion.
        """

    @property
    @abstractmethod
    def action_space(self) -> ActionSpace:
        """
        Return the desciribtion of the action space.

        Returns
        -------
            observation_space: ActionSpace
                The action space describtion.
        """

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the level.
        """

    @abstractmethod
    def step(self, action: Any) -> Any:
        """
        Take a step in the level with a given action.

        Parameters
        ----------
            action: Any
                Object which describes the action.
        Returns
        -------
            state: Any
                The step in which is the level after the action.
        """

    def observe(self) -> List[float]:
        """
        Observes the level and returns an observation.

        Returns
        -------
            observation: List[float]
                Observation of the current level state.
        """
        return self._observer.observe(None)

    def estimate(self, estimated: Any) -> float:
        """
        Estimates the level state and returns a estimation value.

        Returns
        -------
            estimation: float
                Estimated reward of the current level state.
        """
        return self._estimator.estimate(estimated)

    def render(self) -> Any:
        """
        Renders the current level state into a visualisation.

        Returns
        -------
            visualisation: Any
                Rendered visualisation of the current level state.
        """
        return self._visualizer.render(None)
