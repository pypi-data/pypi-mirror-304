from scipy.optimize import leastsq
import numpy as np
from .models import *


def chi2(params, mag, mag_err, phase, model):
    """
    Computes a simple chi2 term = (x_model(phase_i) - x_i)/(sigma_i)
    for a given chosen model

    Parameters
    ----------
    params: 1D array
        Params for the chosen model, following whatever format it requires
    mag: 1D array
        Measured distance-corrected magnitudes
    mag_err: 1D array
        Magnitude uncertainity, must match shape of mag
    phase: 1D array
        Phase angles in radians, must match shape of mag
    model: callable
        One of the models from models.py, or any similarly structured implementation
    Returns
    --------
    array
        (square root of the) chi2 per component

    """
    pred = model(phase, params)
    return (mag - pred) / mag_err


def fit(mag, phase, mag_err, model, params=[0.1]):
    """
    Performs a simple least squares minimization for a chosen model using
    scipy leastsq
    Parameters
    ----------
    mag: 1D array
        Measured distance-corrected magnitudes
    mag_err: 1D array
        Magnitude uncertainity, must match shape of mag
    phase: 1D array
        Phase angles in radians, must match shape of mag
    model: callable
        One of the models from models.py, or any similarly structured implementation
    params: 1D array
        Params for the chosen model, following whatever format the model requires
    Returns
    -------
    leastsq solution object (see scipy documentation)
    """
    sol = leastsq(
        chi2, [mag[0]] + params, (mag, phase, mag_err, model), full_output=True
    )

    return sol


def fit_models(mag, magSigma, phaseAngle, tdist, rdist):
    """
    Convenience function to fit all of the implemented models for a given set of measurements
    Parameters
    ----------
    mag: 1D array
        Measured apparent magnitudes
    magSigma: 1D array
        Magnitude uncertainity, must match shape of mag
    phaseAngle: 1D array
        Phase angles in DEGREES, must match shape of mag
    tdist: 1D array
        Topocentric distance (in au), used to distance-correct the measured magnitude, must match shape of mag
    rdist: 1D array
        Heliocentric distance (in au), used to distance-correct the measured magnitude, must match shape of mag
    Returns
    -------
    dictionary of dictionaries with all the parameters and their respective uncertainties for all the chosen models
    """
    # correct the mag to 1AU distance
    dmag = -5.0 * np.log10(tdist * rdist)
    mag = mag + dmag

    # double check if this is needed
    phaseAngle = np.deg2rad(phaseAngle)

    # now we'll fit using each one of the HG, HG12 and HG1G2 models and store these in a dictionary of dictionaries
    solutions = {}

    # Let's do HG first
    sol_HG = fit(mag, phaseAngle, magSigma, model=HG_model)

    solutions["HG"] = {}

    solutions["HG"]["chi2"] = np.sum(sol_HG[2]["fvec"] ** 2)
    solutions["HG"]["H"] = sol_HG[0][0]
    solutions["HG"]["G"] = sol_HG[0][1]
    solutions["HG"]["H_err"] = np.sqrt(sol_HG[1][0, 0])
    solutions["HG"]["G_err"] = np.sqrt(sol_HG[1][1, 1])
    solutions["HG"]["cov"] = sol_HG[1]

    # now HG12
    sol_HG12 = fit(mag, phaseAngle, magSigma, model=HG12_model)

    solutions["HG12"] = {}

    solutions["HG12"]["chi2"] = np.sum(sol_HG12[2]["fvec"] ** 2)
    solutions["HG12"]["H"] = sol_HG12[0][0]
    solutions["HG12"]["G12"] = sol_HG12[0][1]
    solutions["HG12"]["H_err"] = np.sqrt(sol_HG12[1][0, 0])
    solutions["HG12"]["G12_err"] = np.sqrt(sol_HG12[1][1, 1])
    solutions["HG12"]["cov"] = sol_HG12[1]

    # HG12 Pentilla
    sol_HG12Pen = fit(mag, phaseAngle, magSigma, model=HG12star_model)

    solutions["HG12Pen"] = {}

    solutions["HG12Pen"]["chi2"] = np.sum(sol_HG12[2]["fvec"] ** 2)
    solutions["HG12Pen"]["H"] = sol_HG12[0][0]
    solutions["HG12Pen"]["G12"] = sol_HG12[0][1]
    solutions["HG12Pen"]["H_err"] = np.sqrt(sol_HG12[1][0, 0])
    solutions["HG12Pen"]["G12_err"] = np.sqrt(sol_HG12[1][1, 1])
    solutions["HG12Pen"]["cov"] = sol_HG12[1]

    # finally, HG1G2 - note this returns an extra parameter

    # now HG12, let's tell the code we need that extra parameter
    sol_HG1G2 = fit(mag, phaseAngle, magSigma, model=HG1G2_model, params=[0.1, 0.1])

    solutions["HG1G2"] = {}

    solutions["HG1G2"]["chi2"] = np.sum(sol_HG1G2[2]["fvec"] ** 2)
    solutions["HG1G2"]["H"] = sol_HG1G2[0][0]
    solutions["HG1G2"]["G1"] = sol_HG1G2[0][1]
    solutions["HG1G2"]["G2"] = sol_HG1G2[0][1]
    solutions["HG1G2"]["H_err"] = np.sqrt(sol_HG1G2[1][0, 0])
    solutions["HG1G2"]["G1_err"] = np.sqrt(sol_HG1G2[1][1, 1])
    solutions["HG1G2"]["G2_err"] = np.sqrt(sol_HG1G2[1][2, 2])

    solutions["HG1G2"]["cov"] = sol_HG1G2[1]

    return solutions
