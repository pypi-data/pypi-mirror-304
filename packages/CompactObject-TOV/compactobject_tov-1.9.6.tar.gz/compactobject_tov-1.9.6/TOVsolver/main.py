# Python packages
import numpy as np
import math
from scipy.interpolate import UnivariateSpline
from scipy.constants import pi
from scipy.integrate import odeint, ode
from matplotlib import pyplot
from scipy import optimize
from itertools import repeat
import csv


# Import files
import TOVsolver.solver_code as TOV_solver
import TOVsolver.EoS_import as EoS_import
import TOVsolver.speed_of_sound as speed_of_sound

# Global Variables
def OutputMR(input_file='',density=[],pressure=[]):

    """Outputs the mass, radius, and tidal deformability
    Args:
        file_name (string, optional): string. CSV file to be opened.
        density (array, optional): numpy 1Darray. Passed into a check function and returned if valid.
        pressure (array, optional): numpy 1Darray. Passed into a check function and returned if valid.

    Returns:
        MR (tuple): tuple with mass, radius.
    """

    c = 3e10
    G = 6.67428e-8
    Msun = 1.989e33

    dyncm2_to_MeVfm3 = 1./(1.6022e33)
    gcm3_to_MeVfm3 = 1./(1.7827e12)
    oneoverfm_MeV = 197.33
    #############This is something we need to change, like the input for this EOS import should
    ############# be one file contatining Whole EOS. that first column is density and second is pressure
    energy_density, pressure = EoS_import.EOS_import(input_file,density,pressure)
    ############# Lets the user only input the EOS file path, then this EOS_import should have file
    ############# as input. and the outputMR should have a file as input too?
    
    Radius = []
    Mass = []
    
    density = np.logspace(14.3, 15.6, 50)
#This following step is to make a dicision whether the EOS ingredients is always increase. We can do that outsie of this main to the 
#EOS import.
#if   all(x<y for x, y in zip(eps_total_poly[:], eps_total_poly[[1:])) and all(x<y for x, y in zip(pres_total_poly[j][:], pres_total_poly[j][1:])):
    for i in range(len(density)):
        try:
            Radius.append(TOV_solver.solveTOV(density[i], energy_density, pressure)[1])
            Mass.append(TOV_solver.solveTOV(density[i], energy_density, pressure)[0])
    #This is sentense is for avoiding the outflow of the result, like when solveTOV blow up because of ill EOS, we need to stop
        except OverflowError as e:
            #print("This EOS is ill-defined to reach an infinity result, that is not phyiscal, No Mass radius will be generated.")
            break
    MR = np.vstack((Radius, Mass)).T
    #print("Mass Radius file will be generated and stored as  2-d array. The first column is Radius, second one is mass")
    
    return MR

def OutputMRT(input_file='',density=[],pressure=[]):

    """Outputs the mass, radius, and tidal deformability
    Args:
        file_name (string, optional): string. CSV file to be opened.
        density (array, optional): numpy 1Darray. Passed into a check function and returned if valid.
        pressure (array, optional): numpy 1Darray. Passed into a check function and returned if valid.

    Returns:
        MRT (tuple): tuple with mass, radius, and tidal deformability. 
    """

    c = 3e10
    G = 6.67428e-8
    Msun = 1.989e33

    dyncm2_to_MeVfm3 = 1./(1.6022e33)
    gcm3_to_MeVfm3 = 1./(1.7827e12)
    oneoverfm_MeV = 197.33
    #############This is something we need to change, like the input for this EOS import should
    ############# be one file contatining Whole EOS. that first column is density and second is pressure
    energy_density, pressure = EoS_import.EOS_import(input_file,density,pressure)
    ############# Lets the user only input the EOS file path, then this EOS_import should have file
    ############# as input. and the outputMR should have a file as input too?
    
    Radius = []
    Mass = []
    tidal = [] 
    density = np.logspace(14.3, 15.6, 50)
#This following step is to make a dicision whether the EOS ingredients is always increase. We can do that outsie of this main to the 
#EOS import.
#if   all(x<y for x, y in zip(eps_total_poly[:], eps_total_poly[[1:])) and all(x<y for x, y in zip(pres_total_poly[j][:], pres_total_poly[j][1:])):
    for i in range(len(density)):
        try:
            Radius.append(TOV_solver.solveTOV_tidal(density[i], energy_density, pressure)[1])
            Mass.append(TOV_solver.solveTOV_tidal(density[i], energy_density, pressure)[0])
            tidal.append(TOV_solver.solveTOV_tidal(density[i], energy_density, pressure)[2])
    #This is sentense is for avoiding the outflow of the result, like when solveTOV blow up because of ill EOS, we need to stop
        except OverflowError as e:
            #print("This EOS is ill-defined to reach an infinity result, that is not phyiscal, No Mass radius will be generated.")
            break
    MRT = np.vstack((Radius, Mass,tidal)).T
    #print("Mass Radius and tidal will be generated as the 3-d array. The first column is Radius, second one is mass,last is tidal")

    return MRT

def OutputC_s(input_file='',density=[],pressure=[]):

    """Calls function to open csv (if needed) and check equation of state validity.
        Then calls function to calculate speed of sound.

    Args:
        file_name (string, optional): string. CSV file to be opened.
        density (array, optional): numpy 1Darray. Passed into a check function and returned if valid.
        pressure (array, optional): numpy 1Darray. Passed into a check function and returned if valid.

    Returns:
        C_s (array): numpy 1D array. List of speeds of sound.
    """

    energy_density, pressure = EoS_import.EOS_import(input_file,density,pressure)
    C_s = speed_of_sound.speed_of_sound_calc(energy_density, pressure)
    return C_s

def OutputMRpoint(central_density,energy_density,pressure):

    """Outputs the mass, radius, and tidal deformability (single point)
    Args:
        central_density (float): central density that we want to compute
        density (array, optional): numpy 1Darray. Density of EoS
        pressure (array, optional): numpy 1Darray. pressure of EoS

    Returns:
        MR (tuple): tuple with mass, radius.
    """

    c = 3e10
    G = 6.67428e-8
    Msun = 1.989e33

    dyncm2_to_MeVfm3 = 1./(1.6022e33)
    gcm3_to_MeVfm3 = 1./(1.7827e12)
    oneoverfm_MeV = 197.33
    
    Radius = []
    Mass = []
    
#This following step is to make a dicision whether the EOS ingredients is always increase. We can do that outsie of this main to the 
#EOS import.
#if   all(x<y for x, y in zip(eps_total_poly[:], eps_total_poly[[1:])) and all(x<y for x, y in zip(pres_total_poly[j][:], pres_total_poly[j][1:])):
    try:
        Radius.append(TOV_solver.solveTOV(central_density, energy_density, pressure)[1])
        Mass.append(TOV_solver.solveTOV(central_density, energy_density, pressure)[0])
    #This is sentense is for avoiding the outflow of the result, like when solveTOV blow up because of ill EOS, we need to stop
    except OverflowError as e:
        print("This EOS is ill-defined to reach an infinity result, that is not phyiscal, No Mass radius will be generated.")
    MR = np.vstack((Radius, Mass)).T
    
    return MR

def OutputMRTpoint(central_density,energy_density,pressure):

    """Outputs the mass, radius, and tidal deformability (single point)
    Args:
        central_density (float): central density that we want to compute
        density (array, optional): numpy 1Darray. Density of EoS
        pressure (array, optional): numpy 1Darray. pressure of EoS

    Returns:
        MRT (tuple): tuple with mass, radius and tidal.
    """

    c = 3e10
    G = 6.67428e-8
    Msun = 1.989e33

    dyncm2_to_MeVfm3 = 1./(1.6022e33)
    gcm3_to_MeVfm3 = 1./(1.7827e12)
    oneoverfm_MeV = 197.33
    
    Radius = []
    Mass = []
    tidal = [] 
#This following step is to make a dicision whether the EOS ingredients is always increase. We can do that outsie of this main to the 
#EOS import.
#if   all(x<y for x, y in zip(eps_total_poly[:], eps_total_poly[[1:])) and all(x<y for x, y in zip(pres_total_poly[j][:], pres_total_poly[j][1:])):
    try:
        Radius.append(TOV_solver.solveTOV_tidal(central_density, energy_density, pressure)[1])
        Mass.append(TOV_solver.solveTOV_tidal(central_density, energy_density, pressure)[0])
        tidal.append(TOV_solver.solveTOV_tidal(central_density, energy_density, pressure)[2])
    #This is sentense is for avoiding the outflow of the result, like when solveTOV blow up because of ill EOS, we need to stop
    except OverflowError as e:
        print("This EOS is ill-defined to reach an infinity result, that is not phyiscal, No Mass radius will be generated.")
    MRT = np.vstack((Radius, Mass,tidal)).T
        
    return MRT

