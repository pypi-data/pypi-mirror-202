from typing import Any, List, Protocol

from environment_framework.level import ActionSpace, ILevel, ObservationSpace


class Simulation(Protocol):
    """
    Describes the simulation of a Level.
    """

    level: ILevel
    level_settings: Any


class Simulator:  # pylint: disable = too-many-instance-attributes
    """
    Runs simulations on a Level.
    """

    # TODO: Add a proper state which is passed to the observe,estimate and render method.
    # TODO: Rename episodes to simulation.
    def __init__(self, simulation: Simulation, max_episode_steps: int = 100000) -> None:
        self.level = simulation.level
        self._max_episode_steps = max_episode_steps
        self.current_episodes_steps_done = 0
        self.episodes_done = 0
        self.steps_done = 0

    @property
    def action_space(self) -> ActionSpace:
        return self.level.action_space

    @property
    def observation_space(self) -> ObservationSpace:
        return self.level.observation_space

    @property
    def done(self) -> bool:
        """
        If the current simulation is finished.

        Returns
        -------
            done: bool
                Simulator is finished.
        """
        return self.level.done or (self.current_episodes_steps_done >= self._max_episode_steps)

    def clear_counter(self) -> None:
        """
        Clear the counters of the Simulator.
        """
        self.episodes_done = 0
        self.steps_done = 0
        self.current_episodes_steps_done = 0

    def reset(self) -> None:
        """
        Reset the Level and prepare for a new simulation.
        """
        self.level.reset()
        self.episodes_done += 1
        self.current_episodes_steps_done = 0

    def step(self, action: Any) -> Any:
        """
        Take a step in the Simulator through performing an action in the Level.

        Parameters
        ----------
            action: Any
                Action to take in the level.

        Returns
        -------
            taken_action: Any
                Returns the action taken in the Level.
        """
        self.current_episodes_steps_done += 1
        self.steps_done += 1
        return self.level.step(action)

    def observe(self) -> List[float]:
        """
        Observes the level and returns an observation.

        Returns
        -------
            observation: List[float]
                Observation of the current level state.
        """
        # TODO: pass state
        return self.level.observe()

    def estimate(self) -> float:
        """
        Estimates the level state and returns a estimation value.

        Returns
        -------
            estimation: float
                Estimated reward of the current level state.
        """
        # TODO: pass state
        return self.level.estimate(
            {
                "simulator": {
                    "curr_episode_step": self.current_episodes_steps_done,
                    "max_steps_per_episode": self._max_episode_steps,
                }
            }
        )

    def render(self) -> Any:
        """
        Renders the current level state into a visualisation.

        Returns
        -------
            visualisation: Any
                Rendered visualisation of the current level state.
        """
        # TODO: pass state
        return self.level.render()
