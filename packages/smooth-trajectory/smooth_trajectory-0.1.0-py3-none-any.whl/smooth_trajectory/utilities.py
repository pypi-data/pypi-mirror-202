"""Utility function for rotations, screws, etc.

Functions
---------
to_homogeneous_coordinate()
from_homogenous_coordinate()
to_screw()
polynomial()

"""

import numpy as np
import numpy.linalg as la
from scipy.spatial.transform import Rotation
from typing import Tuple


def to_homogeneous_coordinate(position: np.ndarray, rotation: Rotation) -> np.ndarray:
    """Get the homogenous coordinate for a given position and rotation pair
    
    Attributes
    ----------
    position (np.ndarray): Position array
    rotation (Rotation): Rotation

    Returns
    -------
    np.ndarray: Homogeneous coordinate representation of the position and
                rotation pair

    """
    # Initialize the homogenous coordinate
    hc = np.eye(4)

    hc[0:3, 0:3] = rotation.as_matrix()
    hc[0:3, 3] = position

    return hc


def from_homogenous_coordinate(hc: np.ndarray) -> Tuple[np.ndarray, Rotation]:
    """Get the position and rotation pair from a given homogenous coordinate
    
    Arguments
    ---------
    hc (np.ndarray): Homogenous coordinate
    
    Returns
    (np.ndarray, Rotation): Position and rotation
    
    """
    
    return (hc[0:3, 3], Rotation.from_matrix(hc[0:3, 0:3]))


def to_screw(hc: np.ndarray) -> np.ndarray:
    return np.array([hc[0, 3], hc[1, 3], hc[2, 3], hc[2, 1], hc[0, 2], hc[1, 0]])


def polynomial(
    t_initial: float, t_final: float, order: int = 3
) -> np.polynomial.Polynomial:
    """Fit a smooting polynomial

    Fit a linear, cubib or quintic polynomial between the initial and final
    time values

    (order = 1) a0 + a1 * t
    (order = 3) a0 + a1 * t + a2 * t**2 + a3 * t**3
    (order = 5) a0 + a1 * t + a2 * t**2 + a3 * t**3 + a4 * t**4 + a5 * t**5

    Parameters
    ----------
    t_initial (float): Initial time value
    t_final (float): Final time value
    order (int)

    Returns
    -------
    (np.polynomial.Polynomial): Numpy polynomial constructed from the
                                coefficients calculated using the input

    """

    if order == 1:
        coef_matrix = np.array([[1.0, t_initial], [1.0, t_final]])

        val = np.array([0.0, 1.0])
    elif order == 3:
        coef_matrix = np.array(
            [
                [1.0, t_initial, t_initial**2, t_initial**3],
                [0.0, 1.0, 2.0 * t_initial, 3.0 * t_initial**2],
                [1.0, t_final, t_final**2, t_final**3],
                [0.0, 1.0, 2.0 * t_final, 3.0 * t_final**2],
            ]
        )

        val = np.array([0.0, 0.0, 1.0, 0.0])
    elif order == 5:
        coef_matrix = np.array(
            [
                [
                    1.0,
                    t_initial,
                    t_initial**2,
                    t_initial**3,
                    t_initial**4,
                    t_initial**5,
                ],
                [
                    0.0,
                    1.0,
                    2.0 * t_initial,
                    3.0 * t_initial**2,
                    4 * t_initial**3,
                    5 * t_initial**4,
                ],
                [
                    0.0,
                    0.0,
                    2.0,
                    6.0 * t_initial,
                    12.0 * t_initial**2,
                    20.0 * t_initial**3,
                ],
                [1.0, t_final, t_final**2, t_final**3, t_final**4, t_final**5],
                [
                    0.0,
                    1.0,
                    2.0 * t_final,
                    3.0 * t_final**2,
                    4.0 * t_final**3,
                    5.0 * t_final**4,
                ],
                [
                    0.0,
                    0.0,
                    2.0,
                    6.0 * t_final,
                    12.0 * t_final**2,
                    20.0 * t_final**3,
                ],
            ]
        )

        val = np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
    else:
        raise ValueError("The order should be 1, 3 or 5")

    # Calculate the coefficients of the smoothing polynomial using least squares
    coeffs = la.inv(coef_matrix) @ val

    return np.polynomial.Polynomial(coeffs)