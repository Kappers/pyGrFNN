"""
Mimic Ed Large's GrFNN-Toobox1.0 example1.m

A one layer network driven with a sinusoidal input. Several parameter
sets are provided for experimentation with different types of intrinsic
oscillator dynamics.

"""

import sys
sys.path.append('../')  # needed to run the examples from within the package folder

import numpy as np
import matplotlib.pyplot as plt

from pygrfnn.network import Model, make_connections
from pygrfnn.oscillator import Zparam
from pygrfnn.grfnn import GrFNN
from pygrfnn.vis import plot_connections
from pygrfnn.vis import tf_detail


# GrFNN params

# params = Zparam(-1,  0,  0, 0, 0, 1)  # Linear
params = Zparam( 0, -1, -1, 0, 0, 1)  # Critical
# params = Zparam( 0, -1, -1, 1, 0, 1)  # Critical with detuning
# params = Zparam( 1, -1, -1, 0, 0, 1)  # Limit Cycle
# params = Zparam(-1, -3, -1, 0, 0, 1)  # Double Limit-cycle



# Stimulus:
# Complex sinusoid

sr = 40.0  # sample rate
dt = 1.0/sr
t = np.arange(0, 50, dt)
fc = 1.0  # frequency
A = 0.25  # amplitude
s = A * np.exp(1j * 2 * np.pi * fc * t)

# ramp signal linearly up/down
ramp_dur = 0.02  # in secs
ramp = np.arange(0, 1, dt / ramp_dur)
env = np.ones(s.shape, dtype=float)
env[0:len(ramp)] = ramp
env[-len(ramp):] = ramp[::-1]
# apply envelope
s = s * env

# plt.plot(t, np.real(s))



# Create a GrFNN layer

layer = GrFNN(params, fc=1,
              octaves_per_side=1,
              oscs_per_octave=99.5)

# print(layer)


# create the model and add the layer
model = Model()
model.add_layer(layer)


# run the model
model.run(s, t, dt)


TF = layer.TF
f = layer.f
T = 1.0 / f

tf_detail(TF, t, f, None, np.max(t), np.real(s), np.abs)
plt.show()