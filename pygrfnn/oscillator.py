"""
Basic functions implementing a nonlinear neural oscillator, as described in

    Edward W. Large, Felix V. Almonte, and Marc J. Velasco.
    *A canonical model for gradient frequency neural networks.*
    **Physica D: Nonlinear Phenomena**, 239(12):905-911, 2010.


To Dos:
    - Implement variations of :math:`\dot{z}`

"""

import numpy as np

from utils import nl
from defines import TWO_PI

import logging
logger = logging.getLogger('pygrfnn.oscillator')


class Zparam(object):

    """Convenience class to encapsulate oscillator intrinsic parameters.

    Attributes:
         a: :class:`float` -- Dampening parameter :math:`\\alpha`
         b1: :class:`.COMPLEX` -- :math:`b_1 = \\beta_1 + j\\delta_1`
         b2: :class:`.COMPLEX` -- :math:`b_2 = \\beta_2 + j\\delta_2`
         e: :class:`float` -- Coupling strength :math:`\\varepsilon`

    """

    def __init__(self, alpha=0.0, beta1=-1.0, beta2=-0.25,
                 delta1=0.0, delta2=0.0, epsilon=1.0):
        """Constructor.

        Args:
            alpha (float): :math:`\\alpha` (defaults to: 0.0)
            beta1 (float): :math:`\\beta_1` (defaults to: -1.0)
            beta2 (float): :math:`\\beta_2` (defaults to: -0.25)
            delta1 (float): :math:`\\delta_1` (defaults to: 0.0)
            delta2 (float): :math:`\\delta_2` (defaults to: 0.0)
            epsilon (float): :math:`\\varepsilon` (defaults to: 1.0)

        """

        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.delta1 = delta1
        self.delta2 = delta2
        self.epsilon = epsilon

        self.a = alpha + 1j * TWO_PI  # frequency scaled, to better handle log-spacing
        self.b1 = beta1 + 1j * delta1
        self.b2 = beta2 + 1j * delta2
        self.e = epsilon
        self.sqe = np.sqrt(self.e)

    def __repr__(self):
        return  "Zparams: " \
                "alpha: {0:0.3g}, " \
                "b1: {1:0.3g}+{2:0.3g}j, " \
                "b2: {3:0.3g}+{4:0.3g}j, " \
                "e: {5:0.3g}".format(self.alpha, self.beta1, self.delta1,
                                           self.beta2, self.delta2, self.e)


def zdot(x, z, f, zp):
    """Dynamics of a neural oscillator.

    Implements the dynamical system described in equation 20 of the paper
    referenced above.

    .. math::

        \\tau_i\\dot{z} = z \\Bigg(\\alpha + j\\omega + b_1 |z|^2 +
            \\frac{b_2\\varepsilon |z|^4}{1-\\varepsilon |z|^2} \\Bigg) +
            \\frac{x}{1-\\sqrt{\\varepsilon} x} \\frac{1}{1-\\sqrt{\\varepsilon}
            \\bar{z}}

    where

    .. math::

        b_1 &= \\beta_1 + j \\delta_1 \\\\
        b_2 &= \\beta_2 + j \\delta_2 \\\\

    Args:
        x (:class:`numpy.array`): input signal
        z (:class:`numpy.array`): oscillator state
        f (:class:`numpy.array`): natural frequency of the oscillator
        zp (:class:`.Zparam`): oscillator parameters: :math:`\\alpha,
            \\beta_1, \\delta_1, \\beta_2, \\delta_2` and :math:`\\varepsilon`

    Returns:
         (:class:`numpy.array`): The evaluated time derivative (:math:`\\dot{z}`)

    Note:
        Can work with vectors (i.e. simultaneously compute multiple oscillators).
        In that case, ``x``, ``z``, and ``f`` must have the same shape.

    ToDo:
        Revise equations in the docs

    """

    lin = (zp.a) * f
    nl1 = zp.b1 * f * np.abs(z) ** 2
    nl2 = zp.b2 * f * zp.e * (np.abs(z) ** 4) / (1 - zp.e * np.abs(z) ** 2)
    return z * (lin + nl1 + nl2) + x
