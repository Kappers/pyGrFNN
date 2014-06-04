.. pyGFNN documentation master file, created by
   sphinx-quickstart on Tue May 13 19:30:43 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyGrFNN documentation
=====================

**pyGFNN** is a pure Python implementation of a Gradient Frequency Neural
Network (GFNN), introduced by Large, Almonte and Velasco in

   Edward W. Large, Felix V. Almonte, and Marc J. Velasco.
   *A canonical model for gradient frequency neural networks.*
   **Physica D: Nonlinear Phenomena**, 239(12):905-911, 2010.

These networks can be used to compute a time-frequency representation (TFR) of
an input signal (e.g. audio or an onset signal). Unlike other TFRs, GFNNs can
generate energy at frequencies not present in the input signal via mode-locking.
This property allows them to show behaviors similar to ones documented in music
perception literature, making them good candidates for computational models of
human perception.


The code is loosely based on the *Nonlinear Time-Frequency Transformation
Workbench* (unpublished), Matlab code obtained from Marc Velasco on early 2014.
Compared to that code, this code base is incomplete, as I'm primarily interested
in rhythm processing. That said, the package has been designed to be easily
extended.

.. Contents:


LICENCE
-------

TBD


Examples
========

1. A single layer (single GFNN) model responding to an external stimulus

.. literalinclude:: ../testSingleGFNN.py
   :language: python
   :emphasize-lines: 18-22,25-28,32,35
   :linenos:


2. A double layer model responding to an external stimulus. One layer is visible
(i.e. received the stimulus directly) and the other one is hidden. They are
connected via afferent and efferent connections

.. literalinclude:: ../testDoubleGFNN.py
   :language: python
   :emphasize-lines: 19-20,26-34,40-45,49-53,57-59,62-65,69-73
   :linenos:




Modules
=======

.. toctree::
   :hidden:

   self

.. toctree::
   :maxdepth: 2

   oscillator
   gfnn
   network
   vis
   defines
   utils


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

