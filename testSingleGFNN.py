import pygfnn.network as net
import pygfnn.oscillator as osc
import pygfnn.gfnn as gfnn
from pygfnn.utils import nextpow2

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt



plot_onset_signal = False
plot_internal_conns = False
plot_tf_output = True


# load onset signal
# odf = np.loadtxt('sampleOnsets/bossa.onset.txt')
odf = np.loadtxt('sampleOnsets/rumba.onset.txt')
fs_odf = odf[0]
odf = odf[1:]
t_odf = np.arange(0, odf.size)
t_odf = t_odf/fs_odf


# create single gfnn model

params = osc.Zparam(0, -0.25, -0.5, 0, 0, 1)

internal_strength = 0.6
internal_stdev = 0.5

center_freq = 2.0
half_range =  2
oscs_per_octave = 64

complex_kernel = True
layer = gfnn.GFNN(params,
                  fc=center_freq,
                  octaves_per_side=half_range,
                  oscs_per_octave=oscs_per_octave)

rels = [1./3., 1./2., 1., 2., 3.]
# rels = [1]
layer.connect_internally(relations=rels,
                         internal_strength=internal_strength,
                         internal_stdev=internal_stdev,
                         complex_kernel=complex_kernel)

net = net.Model()
net.add_layer(layer)


# plot internal conns (for the center frequency)
conn = layer.internal_conns[np.round(layer.f.size/2.0)]
f = layer.f
T = 1.0/f




# run the model

# temporary hack
# odf = np.insert(odf, 0, 0)
# odf = odf[:-1]

# seed = odf[0]
# seed_x = net.compute_input(layer, None, seed)
# odf = odf[1:]
# odf = np.insert(odf, -1, 0)
# layer.reset(x_1=seed_x)


net.process_signal(odf*0.5, t_odf, 1.0/fs_odf)
TF = layer.TF



# PLOTS

if plot_onset_signal:
    plt.plot(t_odf, odf)
    plt.show()



if plot_internal_conns:
    fig, (ax1, ax2) = plt.subplots(2,1,sharex=True)

    ax1.semilogx(layer.f, np.abs(conn))
    ax1b = ax1.twinx()
    ax1b.semilogx(layer.f, np.angle(conn), color='r')
    ax1b.set_xticks(2**np.arange(np.log2(nextpow2(np.min(layer.f))), 1+np.log2(nextpow2(np.max(layer.f)))))
    ax1b.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax1b.set_ylim([-np.pi, np.pi])
    ax1.axis('tight')


    ax2.semilogx(layer.f, np.real(conn))
    ax2b = ax2.twinx()
    ax2b.semilogx(layer.f, np.imag(conn), color='r')
    ax2b.set_xticks(2**np.arange(np.log2(nextpow2(np.min(layer.f))), 1+np.log2(nextpow2(np.max(layer.f)))))
    ax2b.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax2.axis('tight')

    plt.show()



if plot_tf_output:
    from pygfnn.vis import tf_simple, tf_detail
    # tf_simple(TF, t_odf, T, odf, np.abs)
    # tf_simple(TF, t_odf, T, None, np.abs)
    tf_detail(TF, t_odf, T, np.mean(t_odf), odf, np.abs)