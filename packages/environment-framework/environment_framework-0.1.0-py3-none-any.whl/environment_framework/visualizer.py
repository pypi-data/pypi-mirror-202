from typing import Any, Protocol


class Visualizer(Protocol):
    def render(self, visualized: Any) -> Any:
        """
        Renders the given visualizee to a visualisation.

        Parameters
        ----------
        visualizee: Any
            Object to visualise.

        Returns
        -------
        visualisation: Any
            The visualisation of the object.
        """
