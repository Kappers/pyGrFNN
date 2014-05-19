"""
Basic functions implementing a nonlinear neural oscillator, as described in

Edward W. Large, Felix V. Almonte, and Marc J. Velasco.
A canonical model for gradient frequency neural networks.
Physica D: Nonlinear Phenomena, 239(12):905-911, 2010.


"""

import numpy as np
from utils import nl
from defines import TWO_PI

class Zparam(object):
    """
    Convenience class to encapsulate oscillator parameters.
    """

    def __init__(self, alpha=0.0, beta1=-1.0, delta1=0.0, beta2=-0.25, delta2=0.0, epsilon=1.0):
        """
        The constructor takes an optional list of named oscillator parameters:
        For example:
        ::

            params = Zparam(alpha=0.5,
                            beta1=-10.0,
                            beta2=-3.0,
                            delta1=0.0,
                            delta2=0.0,
                            epsilon=0.6)


        All parameters are optional (see default values in the class description)

        :param alpha: :math:`\\alpha` (defaults to: 0.0)
        :param beta1: :math:`\\beta_1` (defaults to: -1.0)
        :param beta2: :math:`\\beta_2` (defaults to: -0.25)
        :param delta1: :math:`\\delta_1` (defaults to: 0.0)
        :param delta2: :math:`\\delta_2` (defaults to: 0.0)
        :param epsilon: :math:`\\varepsilon` (defaults to: 1.0)

        :type alpha: float
        :type beta1: float
        :type beta2: float
        :type delta1: float
        :type delta2: float
        :type epsilon: float

        **Instance attributes**:
         - **a** (*float*) - Dampening parameter :math:`\\alpha`
         - **b1** (*complex*) - :math:`b_1 = \\beta_1 + j\\delta_1`
         - **b2** (*complex*) - :math:`b_2 = \\beta_2 + j\\delta_2`
         - **e** (*float*) - Coupling strength :math:`\\varepsilon`

        """

        self.a = alpha
        self.b1 = beta1 + 1j*delta1
        self.b2 = beta2 + 1j*delta2
        self.e = epsilon



def zdot(x, z, f, zparams):
    """
    Dynamics of a neural oscillator, as described in equation 15 of the paper referenced above.
    Can work with vectors (i.e. simultaneously compute different oscillators):

    .. math::

        \\dot{z} = z \\Bigg(\\alpha + j\\omega + b_1 |z|^2 + \\frac{b_2\\varepsilon |z|^4}{1-\\varepsilon |z|^2} \\Bigg) + \\frac{x}{1-\\sqrt{\\varepsilon} x} \\frac{1}{1-\\sqrt{\\varepsilon} \\bar{z}}

    where

    .. math::

        b_1 &= \\beta_1 + j \\delta_1 \\\\
        b_2 &= \\beta_2 + j \\delta_2 \\\\

    :param x: input signal
    :type x: complex numpy array
    :param z: oscillator state
    :type z: complex numpy array
    :param f: natural frequency of the oscillator
    :type f: numpy float array
    :param zparams: oscillator parameters: :math:`\\alpha, \\beta_1, \\delta_1,
                                                \\beta_2, \\delta_2` and :math:`\\varepsilon`
    :type zparams: Zparam

    :rtype: complex numpy array
    """

    lin = zparams.a + 1j*TWO_PI*f
    nonlin1 = zparams.b1*np.abs(z)**2
    nonlin2 = zparams.b2*zparams.e*np.abs(z)**4*nl(np.abs(z)**2, zparams.e)
    # RT = x*nl(x, np.sqrt(zparams.e))              # passive part of the Resonant Terms (RT)
    # RT = RT * nl(np.conj(z), np.sqrt(zparams.e))  # times the active part of RT
    RT = x * nl(np.conj(z), np.sqrt(zparams.e))     # Resonant Terms

    return z * (lin + nonlin1 + nonlin2) + RT




