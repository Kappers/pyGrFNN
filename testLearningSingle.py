"""
Script to test connectivity learning with a single layer network
"""

import matplotlib.pyplot as plt
import numpy as np

from pygrfnn.network import Model, make_connections
from pygrfnn.oscillator import Zparam
from pygrfnn.grfnn import GrFNN
from pygrfnn.vis import plot_connections
from pygrfnn.vis import tf_detail


# load onset signal
# odf = np.loadtxt('sampleOnsets/rumba.onset.txt')
odf = np.loadtxt('sampleOnsets/bossa.onset.txt')
fs_odf = odf[0]
odf = odf[1:] * 0.5   # this factor is relevant (but annoying)
t_odf = np.arange(0, odf.size)
t_odf = t_odf / fs_odf


# create single GrFNN
params = Zparam(0, -0.25, -0.5, 0, 0, 1)
layer = GrFNN(params,
              fc=2,
              octaves_per_side=2,
              oscs_per_octave=64)

# internal connectivity
internal_conns = make_connections(layer, layer, 0.0, 0.5,
                                  harmonics=[1. / 3., 1. / 2., 1., 2., 3.],
                                  complex_kernel=True,
                                  self_connect=False)


# create the model
model = Model()

# setup layers
model.add_layer(layer)

# add connectivity
conn = model.connect_layers(layer,
                            layer,
                            internal_conns,
                            learn=True,
                            d=0.001,
                            k=0.001)

# run the model
model.run(odf, t_odf, 1.0 / fs_odf)


# visualize results
TF = layer.TF
f = layer.f
T = 1.0 / f

plot_onset_signal = False
plot_conns = True
plot_tf_output = True

if plot_onset_signal:
    plt.plot(t_odf, odf)
    plt.show()

if plot_conns:
    plot_connections(conn, display_op=lambda x: np.log(np.abs(x)))
    plt.show()

if plot_tf_output:
    # from pygrfnn.vis import tf_simple
    # tf_simple(TF, t_odf, T, None, odf, np.abs)
    # tf_simple(TF, t_odf, T, None, None, np.abs)
    tf_detail(TF, t_odf, T, None, np.max(t_odf), odf, np.abs)
    plt.show()