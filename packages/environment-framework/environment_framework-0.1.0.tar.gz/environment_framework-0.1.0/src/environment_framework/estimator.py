from typing import Any, Protocol


class Estimator(Protocol):
    def estimate(self, estimated: Any) -> float:
        """
        Estimates the current reward based on a estimated object.

        Parameters
        ----------
        estimated: Any
            Object to take the estimation from.

        Returns
        -------
        reward : float
            Current reward
        """
