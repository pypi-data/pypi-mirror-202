"""Smooth trajectory generation

Create a trajectory using polynomial smoothing. There are three polynomial
smoothing methods implemented: linear (1st order), cubic (3rd order), and
quintic (5th order).

Functions
---------
_time_scaling()
screw_trajectory()
joint_trajectory()

"""

import numpy as np
import numpy.linalg as la
import scipy.linalg as sla
from .utilities import to_screw


def _time_scaling(t: float, poly: np.polynomial.Polynomial):
    """Time scaling for the trajectory

    Map a given time value in [t_initial, t_final] to [0, 1] interval

    Parameters
    ----------
    t (float): Time value to be evaluated
    polynomial (np.polynomial.Polynomial): Smoothing polynomial

    Returns
    -------
    float: Time value mapped to [0, 1] interval

    """

    return poly(t), poly.deriv()(t), poly.deriv(m=2)(t)


def screw_trajectory(
    t: float,
    poly: np.polynomial.Polynomial,
    initial_conf: np.array,
    final_conf: np.array,
) -> np.array:
    """Straight trajectory in SE(3)

    Create a straight line trajectory in SE(3)

    Parameters
    ----------
    t (float): Time value
    poly (np.polynomial.Polynomial): The smoothing polynomial for the time scaling
    initial_conf (np.ndarray): Initial configuration in SE(3)
    final_conf (np.ndarray): Final configuration in SE(3)

    Returns
    -------
    (np.ndarray): Configuration represented in SE(3) at time t

    TODO check the second return value (twist) and add to the docstring

    """

    # Map the given time to [0, 1] interval
    scaled_time, d_scaled_time, dd_scaled_time = _time_scaling(t, poly)

    log = sla.logm(la.inv(initial_conf) @ final_conf)

    X = initial_conf @ sla.expm(log * scaled_time)
    V = to_screw(initial_conf @ log @ la.inv(initial_conf) * d_scaled_time)

    return (X, V)


def joint_trajectory(
    t: float, poly: np.polynomial.Polynomial, initial_pos: float, final_pos: float
) -> float:
    """Straight trajectory in joint space

    Create a smooth straight line trajectory in Eucledean space

    Parameters
    ----------
    t (float): Time value
    poly (np.polynomial.Polynomial): The smoothing polynomial for the time scaling
    initial_pos (float): Initial position in Euclidean space
    final_pos (float): Final position in Euclidean space

    Returns
    -------
    (float): Position on the straight trajectory
    (float): Velocity on the straight trajectory

    """

    # Map the given time to [0, 1] interval
    scaled_time, d_scaled_time, dd_scaled_time = _time_scaling(t, poly)

    return (
        initial_pos + scaled_time * (final_pos - initial_pos),
        d_scaled_time * (final_pos - initial_pos),
        dd_scaled_time * (final_pos - initial_pos),
    )
