from pygrfnn.network import Model, make_connections
from pygrfnn.oscillator import Zparam
from pygrfnn.grfnn import GrFNN
from pygrfnn.utils import timed

import numpy as np


# load onset signal
# odf = np.loadtxt('sampleOnsets/rumba.onset.txt')
odf = np.loadtxt('sampleOnsets/bossa.onset.txt')
fs_odf = odf[0]
odf = odf[1:]*0.5   # this factor is relevant (but annoying)
t_odf = np.arange(0, odf.size)
t_odf = t_odf/fs_odf


# create a pair of GrFNNs
params1 = Zparam(0, -1.0, -0.25, 0, 0, .5)
params2 = Zparam(0.03, 1.0, -1.0, 0, 0, .5)

center_freq = 2.0
half_range =  2.5
oscs_per_octave = 64

layer1 = GrFNN(params1,
              fc=center_freq,
              octaves_per_side=half_range,
              oscs_per_octave=oscs_per_octave)

layer2 = GrFNN(params2,
              fc=center_freq,
              octaves_per_side=half_range,
              oscs_per_octave=oscs_per_octave)


# define connectivities

# internal connectivity
rels = [1./3., 1./2., 1., 2., 3.]
internal_conns1 = make_connections(layer1, layer1, 0.6, 0.1, harmonics=rels,
                                   complex_kernel=True, self_connect=False)

internal_conns2 = make_connections(layer2, layer2, 0.5, 0.1, harmonics=rels,
                                   complex_kernel=True, self_connect=False)


# inter layer connectivity
affConn = make_connections(layer1, layer2, 0.75, 0.1, harmonics=[1],
                           complex_kernel=False, self_connect=True)

effConn = make_connections(layer2, layer1, -0.75, .4, harmonics=[1],
                           complex_kernel=True, self_connect=False)


# create the model
net = Model()
net.add_layer(layer1)
net.add_layer(layer2, visible=False)

# add connectivity
internal_conns1 = net.connect_layers(layer1, layer1, internal_conns1)
internal_conns2 = net.connect_layers(layer2, layer2, internal_conns2)
affConn = net.connect_layers(layer1, layer2, affConn)
effConn = net.connect_layers(layer2, layer1, effConn)


# run the model
@timed
def run():
  net.run(odf, t_odf, 1.0/fs_odf)

run()


# visualize outputs
TF = layer2.TF
f = layer2.f
T = 1.0/f

plot_onset_signal = False
plot_conns = True
plot_tf_output = True

if plot_onset_signal:
    import matplotlib.pyplot as plt
    plt.plot(t_odf, odf)
    plt.show()

if plot_conns:
    from pygrfnn.vis import plot_connections
    plot_connections(effConn)

if plot_tf_output:
    # from pygrfnn.vis import tf_simple
    # tf_simple(TF, t_odf, T, odf, np.abs)
    # tf_simple(TF, t_odf, T, None, np.abs)
    from pygrfnn.vis import tf_detail
    tf_detail(TF, t_odf, T, np.max(t_odf), odf, np.abs)


