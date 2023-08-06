from copy import deepcopy
import pytest
import numpy as np
from numpy.testing import assert_allclose
import pylira
from pylira import LIRADeconvolver, LIRADeconvolverResult, LIRASignificanceEstimator
from pylira.data import (
    disk_source_gauss_psf,
    gauss_and_point_sources_gauss_psf,
    point_source_gauss_psf,
)


@pytest.fixture(scope="session")
def lira_result(tmpdir_factory):
    random_state = np.random.RandomState(836)
    data = point_source_gauss_psf(random_state=random_state)
    data["flux_init"] = data["flux"]

    alpha_init = 0.05 * np.ones(np.log2(data["counts"].shape[0]).astype(int))

    tmpdir = tmpdir_factory.mktemp("data")
    deconvolve = LIRADeconvolver(
        alpha_init=alpha_init,
        n_iter_max=1000,
        n_burn_in=10,
        filename_out=tmpdir / "image-trace.txt",
        filename_out_par=tmpdir / "parameter-trace.txt",
        fit_background_scale=True,
        random_state=np.random.RandomState(156),
    )
    return deconvolve.run(data=data)


def test_np_random_state():
    # test to check numpy random state is platform independent
    random_state = np.random.RandomState(1234)

    assert random_state.randint(0, 10) == 3
    assert random_state.randint(0, 10) == 6


def test_import_name():
    assert pylira.__name__ == "pylira"


def test_image_analysis():
    assert pylira.image_analysis is not None


def test_lira_deconvolver():
    deconvolve = LIRADeconvolver(alpha_init=np.array([1, 2, 3]))

    assert deconvolve.alpha_init.dtype == np.float64
    assert_allclose(deconvolve.alpha_init, [1.0, 2.0, 3.0])

    config = deconvolve.to_dict()

    assert_allclose(config["alpha_init"], [1, 2, 3])
    assert not config["fit_background_scale"]
    assert "alpha_init" in str(deconvolve)


def test_lira_deconvolver_run_point_source(lira_result):
    assert lira_result.config["random_seed"] == 1346985517

    assert_allclose(lira_result.posterior_mean_from_trace[16][16], 955.7, rtol=3e-2)

    assert lira_result.posterior_mean[16][16] > 700
    assert lira_result.parameter_trace["smoothingParam0"][-1] > 0
    assert "alpha_init" in lira_result.config

    # check total flux conservation
    assert_allclose(np.nansum(lira_result.posterior_mean), 985, atol=10)

    trace_par = lira_result.parameter_trace

    idx = slice(lira_result.n_burn_in, None)
    assert len(trace_par) == 1000
    assert_allclose(np.mean(trace_par["smoothingParam0"][idx]), 0.056, rtol=0.1)
    assert_allclose(np.mean(trace_par["smoothingParam1"][idx]), 0.060, rtol=0.1)
    assert_allclose(np.mean(trace_par["smoothingParam2"][idx]), 0.060, rtol=0.1)
    assert_allclose(np.mean(trace_par["smoothingParam3"][idx]), 0.062, rtol=0.1)
    assert_allclose(np.mean(trace_par["smoothingParam4"][idx]), 0.070, rtol=0.1)


def test_reduce_write_read(tmpdir, lira_result):
    filename = tmpdir / "reduced.fits"
    lira_result.reduce_to_mean_std().write(filename)

    reduced = LIRADeconvolverResult.read(filename)

    assert_allclose(
        lira_result.posterior_mean_from_trace, reduced.posterior_mean, rtol=1e-5
    )
    assert_allclose(
        lira_result.posterior_std_from_trace, reduced.posterior_std, rtol=1e-5
    )


@pytest.mark.xfail
# TODO: make LIRA work for extended sources...
def test_lira_deconvolver_run_disk_source(tmpdir):
    data = disk_source_gauss_psf()
    data["flux_init"] = data["flux"]

    alpha_init = 0.02 * np.ones(np.log2(data["counts"].shape[0]).astype(int))

    deconvolve = LIRADeconvolver(
        alpha_init=alpha_init,
        n_iter_max=1000,
        n_burn_in=100,
        ms_al_kap1=0,
        ms_al_kap2=1000,
        ms_al_kap3=10,
        filename_out=tmpdir / "image-trace.txt",
        filename_out_par=tmpdir / "parameter-trace.txt",
        fit_background_scale=True,
        random_state=np.random.RandomState(156),
    )
    result = deconvolve.run(data=data)

    assert result.config["random_seed"] == 1346985517

    assert_allclose(result.posterior_mean[16][16], 14.0, rtol=0.1)
    assert_allclose(result.posterior_mean[0][0], 0.0011, atol=0.1)

    # check total flux conservation
    # TODO: improve accuracy
    assert_allclose(np.nansum(result.posterior_mean), 1413, atol=10)

    assert result.parameter_trace["smoothingParam0"][-1] > 0
    assert "alpha_init" in result.config

    trace_par = result.parameter_trace
    assert len(trace_par) == 1000

    idx = slice(result.n_burn_in, None)
    assert_allclose(np.mean(trace_par["smoothingParam0"][idx]), 0.08, rtol=5e-2)
    assert_allclose(np.mean(trace_par["smoothingParam1"][idx]), 0.20, rtol=5e-2)
    assert_allclose(np.mean(trace_par["smoothingParam2"][idx]), 0.31, rtol=5e-2)
    assert_allclose(np.mean(trace_par["smoothingParam3"][idx]), 0.34, rtol=5e-2)


def test_lira_deconvolver_run_gauss_source(tmpdir):
    random_state = np.random.RandomState(836)
    data = gauss_and_point_sources_gauss_psf(random_state=random_state)
    data["flux_init"] = data["flux"]

    alpha_init = 0.1 * np.ones(np.log2(data["counts"].shape[0]).astype(int))

    deconvolve = LIRADeconvolver(
        alpha_init=alpha_init,
        n_iter_max=1000,
        n_burn_in=200,
        ms_al_kap1=0,
        ms_al_kap2=1000,
        ms_al_kap3=10,
        fit_background_scale=False,
        filename_out=tmpdir / "image-trace.txt",
        filename_out_par=tmpdir / "parameter-trace.txt",
        random_state=np.random.RandomState(156),
    )
    result = deconvolve.run(data=data)

    assert result.config["random_seed"] == 1346985517
    assert result.posterior_mean[16][16] > 0.2

    assert result.parameter_trace["smoothingParam0"][-1] > 0
    assert "alpha_init" in result.config

    assert_allclose(result.posterior_mean[0][0], 0.0011, atol=0.1)

    # check at point source positions
    assert_allclose(result.posterior_mean[16][26], 137.4, rtol=0.1)
    # assert_allclose(result.posterior_mean[16][6], 7.11, rtol=0.1)
    assert_allclose(result.posterior_mean[26][16], 1337.0, rtol=0.1)
    assert_allclose(result.posterior_mean[6][16], 323.9, rtol=0.1)
    assert_allclose(result.posterior_mean[0][0], 0, atol=0.1)

    # check total flux conservation
    # TODO: improve accuracy
    assert_allclose(np.nansum(result.posterior_mean), 3430, rtol=0.1)

    trace_par = result.parameter_trace

    assert len(trace_par) == 1000

    idx = slice(deconvolve.n_burn_in, None)
    assert_allclose(np.mean(trace_par["smoothingParam0"][idx]), 0.032, rtol=0.4)
    assert_allclose(np.mean(trace_par["smoothingParam1"][idx]), 0.08, rtol=0.4)
    assert_allclose(np.mean(trace_par["smoothingParam2"][idx]), 0.13, rtol=0.4)
    assert_allclose(np.mean(trace_par["smoothingParam3"][idx]), 0.23, rtol=0.4)
    assert_allclose(np.mean(trace_par["smoothingParam4"][idx]), 0.36, rtol=0.4)


def test_lira_deconvolver_result_write(tmpdir, lira_result):
    filename = tmpdir / "test.fits.gz"
    lira_result.write(filename)


def test_lira_deconvolver_result_read(tmpdir, lira_result):
    filename = tmpdir / "test.fits.gz"
    lira_result.write(filename)

    new_result = LIRADeconvolverResult.read(filename)

    assert_allclose(lira_result.config["alpha_init"], new_result.config["alpha_init"])
    assert_allclose(lira_result.posterior_mean, new_result.posterior_mean)

    assert lira_result.image_trace.shape == new_result.image_trace.shape


def test_lira_significance_estimator(lira_result):
    replica_res = [deepcopy(lira_result) for i in range(50)]
    random_state = np.random.RandomState(836)
    data = point_source_gauss_psf(random_state=random_state)

    test_labels = np.zeros(data["background"].shape)
    test_labels[15:18, 15:18] = 1

    sig_est = LIRASignificanceEstimator(lira_result, replica_res, test_labels)
    pvals, _, _, _, _ = sig_est.estimate_p_values(data)

    assert pvals["0.0"] == 0.99
    assert pvals["1.0"] == 0.99


def test_random_seed_same():
    random_state = np.random.RandomState(334)

    data = point_source_gauss_psf(random_state=random_state)

    data["flux_init"] = np.ones((32, 32))
    alpha_init = np.ones(5)

    deconvolve_1 = LIRADeconvolver(
        alpha_init=alpha_init,
        n_iter_max=10,
        n_burn_in=0,
        random_state=np.random.RandomState(334),
    )
    result_1 = deconvolve_1.run(data=data)

    deconvolve_2 = LIRADeconvolver(
        alpha_init=alpha_init,
        n_iter_max=10,
        n_burn_in=0,
        random_state=np.random.RandomState(334),
    )
    result_2 = deconvolve_2.run(data=data)

    assert result_1.config["random_seed"] == 1022788739
    assert result_2.config["random_seed"] == 1022788739

    assert_allclose(
        result_1.posterior_mean[0, 0], result_2.posterior_mean[0, 0], rtol=1e-5
    )


def test_random_seed_different():
    random_state = np.random.RandomState(334)

    data = point_source_gauss_psf(random_state=random_state)
    data["flux_init"] = np.ones((32, 32))
    alpha_init = np.ones(5)

    deconvolve_1 = LIRADeconvolver(
        alpha_init=alpha_init,
        n_iter_max=10,
        n_burn_in=0,
        random_state=np.random.RandomState(394),
    )
    result_1 = deconvolve_1.run(data=data)

    deconvolve_2 = LIRADeconvolver(
        alpha_init=alpha_init,
        n_iter_max=10,
        n_burn_in=0,
        random_state=np.random.RandomState(434),
    )
    result_2 = deconvolve_2.run(data=data)

    assert result_1.config["random_seed"] == 2187641588
    assert result_2.config["random_seed"] == 1518241554

    assert not np.allclose(result_1.posterior_mean[0, 0], result_2.posterior_mean[0, 0])
