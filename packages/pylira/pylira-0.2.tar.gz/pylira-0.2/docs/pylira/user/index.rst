**********
User Guide
**********

This is how to use Pylira:

.. code::

    from pylira import LIRADeconvolver
    from pylira.data import point_source_gauss_psf

    data = point_source_gauss_psf()
    data["flux_init"] = data["flux"]
    deconvolve = LIRADeconvolver(
        alpha_init=np.ones(np.log2(data["counts"].shape[0]).astype(int))
    )
    result = deconvolve.run(data=data)

The ``data`` object is a simple Pythin ``dict`` containing the following quantities:

===================== =================================================
Quantity              Definition
===================== =================================================
counts                2D Numpy array containing the counts image
psf                   2D Numpy array containing an image of the PSF
exposure (optional)   2D Numpy array containing the exposure image
background (optional) 2D Numpy array containing the background / baseline image
===================== =================================================

From these quantities the predicted number of counts is computed like:

.. math::

    N_{Pred} = \mathrm{PSF} \circledast (\mathcal{E} \cdot (F + B))

Where :math:`\mathcal{E}` is the exposure, :math:`F` the deconvovled
flux image, :math:`B` the background and :math:`PSF` the PSF image.


.. toctree::
   :maxdepth: 2
   :hidden:

   data
   tutorials/index

