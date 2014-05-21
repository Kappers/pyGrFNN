"""GFNN related code, as described in

Edward W. Large, Felix V. Almonte, and Marc J. Velasco.
A canonical model for gradient frequency neural networks.
Physica D: Nonlinear Phenomena, 239(12):905-911, 2010.
"""

import numpy as np
from network import make_connections
from defines import COMPLEX, FLOAT
from utils import f, nml
from functools import partial
from oscillator import zdot

class GFNN(object):
    """
    Gradient Frequency Neural Network

    Note:
        Currently only log-frequency spacing implemented

    Attributes:
        f (numpy.array): ordered array of oscillators' natural frequencies (in Hz)
        size (int): number of oscillators in the GFNN
        oscs_per_octave (int): number of oscillators in a single octave
        internal_conns (numpy.array): matrix of internal connections (rows index
            source and columns index destination)
        z (numpy.array): initial oscillators states
        x_1 (numpy.array): last processed input
        dzdt (function): parametrized oscillator differential equation


    """

    def __init__(self,
                 zparams,
                 fc=1.0,
                 octaves_per_side=2.0,
                 oscs_per_octave=64):
        """ GFNN constructor

        Args:
            zparams (:class:`.Zparam`): oscillator parameters
            fc (float): GFNN center frequency (in Hz.)
            octaves_per_side (float): number of octaves above (and below) fc
            oscs_per_octave (float): number of oscillators per octave

        """

        # array of oscillators' frequencies (in Hz)
        self.f = np.asarray(fc*np.logspace(-octaves_per_side,
                                           octaves_per_side,
                                           base=2.0,
                                           num=2*oscs_per_octave*octaves_per_side+1),
                            dtype=FLOAT)

        # total number of oscillator in the network
        self.size = self.f.size

        # oscillator parameters
        self.zparams = zparams

        # matrix of internal connections
        self.internal_conns = None

        # initial oscillators states
        self.z = 1e-10*(1+1j)*np.ones(self.f.shape, dtype=COMPLEX)

        # last processed input
        self.x_1 = 0

        # oscillator differential equation
        self.dzdt = partial(zdot, f=self.f, zparams=self.zparams)

        # number of oscillators per octave
        self.oscs_per_octave = oscs_per_octave


    def connect_internally(self,
                           relations=[1],
                           internal_strength=0.5,
                           internal_stdev=0.5,
                           complex_kernel=False):
        """ Creates internal connections

        Args:
            relations (list): list of connection relations to be established. For example,
                ``relations = [0.5, 1., 3.]`` will establish the following connections:
                :math:`f_{dest} == 0.5f_{src};\\quad f_{dest} == f_{src};\\quad f_{dest} == 3f_{src}`
            internal_strength (float): weight of the internal connection.
                If 0.0, not connections will be created
            internal_stdev (float): internal connections standard deviation.
                If *internal_strength==0.0*, this will be ignored.
            complex_kernel (bool): if *True*, the connections are complex numbers

        """
        if internal_strength > 0:
            self.internal_conns = internal_strength * \
                                  make_connections(self,
                                                   self,
                                                   relations,
                                                   internal_stdev,
                                                   complex_kernel=complex_kernel,
                                                   self_connect=False)


    def reset(self, x_1=0, z=None):
        """Resets the state of the GFNN

        Args:
            x_1 (:class:`.numpy.array`): previous (last) processed input
            z (:class:`.numpy.array`): current state of the oscillators.
                If None, they will be set to 1e-10*(1+1j)

        """
        self.x_1 = x_1;
        if z is None:
            self.z = 1e-10*(1+1j)*np.ones(self.f.shape, dtype=COMPLEX)
        else:
            self.z = z


    # def process_signal(self, input, t, dt):
    #     """Process an external input (stimulus)

    #     Runs the GFNN for an external input. It runs isolated, not as part of a network
    #     (doesn't consider other inputs such as efferent or afferent).

    #     Note:
    #         TODO: raise exception when shapes of **input** and **t** mismatch?

    #     Args:
    #         input (numpy complex array): input signal (stimulus)
    #         t (numpy float array): time vector (must have the same shape as *input*)
    #         dt (float): input signal's sample period (inverse of the sample rate)

    #     Returns:
    #         :class:`numpy.array` Time-frequency representation of the input signal.
    #             Rows index frequency and columns index time
    #     """

    #     def f(x, e):
    #         sq = np.sqrt(e)
    #         return x * nl(x, sq) * nl(np.conj(x), sq)

    #     def nml(x, m=0.4, g=1.0):
    #         # return m * np.tanh(g*x)
    #         eps = np.spacing(1)
    #         return m*np.tanh(g*(np.abs(x)+eps))*x/(np.abs(x)+eps)


    #     self.TF = np.zeros((self.f.size, input.size), dtype=COMPLEX)
    #     for (i, x_stim) in enumerate(input):
    #         # process external signal (stimulus)
    #         x = f(x_stim, self.zparams.e)
    #         # print "-"*20
    #         # print x

    #         if self.internal_conns is not None:
    #             # process internal signal (via internal connections)
    #             x_int = self.z.dot(self.internal_conns)
    #             x = x + f(nml(x_int), self.zparams.e)
    #         # print x


    #         self.process_time_step(dt, x)
    #         self.TF[:,i] = self.z

    #     return self.TF


    # def process_time_step(self, dt, x):
    #     """Process a single sample

    #     Given a processed input (combined stimulus, external and internal contributions),
    #     updates the GFNN state :attr:`.z`. It also updates the last processed input :attr:`.x_1`

    #     Note:
    #         The current implementation assumes as constant time-step size

    #     Args:
    #         dt (float): time step in seconds (sampling period)
    #         input (:class:`.numpy.array`): processed input

    #     """

    #     import pdb
    #     pdb.set_trace()

    #     self.z = RK4(x, self.x_1, self.z, dt, self.dzdt)    # integrate the diffeq
    #     self.x_1 = x    # store the computed input (will be used in the next time step as x_1)

    #     # z = RK4(x, self.x_1, self.z, dt, self.dzdt)    # integrate the diffeq
    #     # return (z, x)    # return z and the computed input (will be required in the next time step as x_1)


    def compute_input(self, z, external_conns, x_stim=0):
        """TODO: document properly

        external_conns is a list of tuples of the form (source_z, connection_matrix)
        """
        # compute overall input (external signal + internal connections + eff/aff connections)
        # For reference: input pre-processing from NLTFT
        # x = f(n.e, x_stim) + f(n.e, nml(x_aff)) + f(n.e, nml(x_int)) + f(n.e, nml(x_eff));

        # process external signal (stimulus)
        x = f(x_stim, self.zparams.e)

        # process internal connections
        if self.internal_conns is not None:
            # process internal signal (via internal connections)
            x_int = z.dot(self.internal_conns)
            # x_int = self.internal_conns.dot(z)
            x = x + f(nml(x_int), self.zparams.e)

        # process other external inputs (afferent / efferent)
        for (source_z, conns) in external_conns:
            x_ext = source_z.dot(conns)
            # x_ext = conns.dot(source_z)
            x = x + f(nml(x_ext), self.zparams.e)

        # import pdb
        # pdb.set_trace()

        return x


