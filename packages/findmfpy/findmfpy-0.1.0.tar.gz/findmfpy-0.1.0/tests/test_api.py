from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from findmfpy import pick_peaks, pick_peaks_diagnostic

SpectrumType = tuple[NDArray[np.float64], NDArray[np.float64]]


@pytest.fixture()
def signal_masses() -> list[float]:
    return [1020.0, 1050.0, 1100.0]


def _gauss_pdf(x: NDArray[np.float64], mu: float, sigma: float) -> NDArray[np.float64]:
    return np.exp(-((x - mu) ** 2) / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))


@pytest.fixture()
def profile_spectrum(signal_masses: list[float]) -> SpectrumType:
    mz_arr = np.linspace(1000, 1200, 5000)
    # generate a gaussian mixture of each of signael masses
    int_arr = np.zeros(mz_arr.shape)
    for mass in signal_masses:
        int_arr += _gauss_pdf(mz_arr, mass, 5.0) * 20.0
    return mz_arr, int_arr


def test_pick_peaks_when_defaults(profile_spectrum: SpectrumType) -> None:
    mz_arr, int_arr = profile_spectrum
    mz_peak, int_peak = pick_peaks(mz_arr, int_arr)
    assert set(np.round(mz_peak)) == {1020, 1050, 1100}
    assert len(mz_peak) == len(int_peak)


def test_pick_peaks_diagnostic_when_defaults(profile_spectrum: SpectrumType) -> None:
    mz_arr, int_arr = profile_spectrum
    mz_peak, int_peak, diagnostics = pick_peaks_diagnostic(mz_arr, int_arr)
    assert set(np.round(mz_peak)) == {1020, 1050, 1100}
    assert len(mz_peak) == len(int_peak)
    assert set(diagnostics.keys()) == {"resampled_mz_arr", "resampled_int_arr", "smoothed_int_arr"}
    assert len(diagnostics["resampled_mz_arr"]) == len(diagnostics["resampled_int_arr"])
    assert len(diagnostics["resampled_mz_arr"]) == len(diagnostics["smoothed_int_arr"])


if __name__ == "__main__":
    pytest.main()
