#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 03 17:30:00 2019

@author: camaramm

XDATA = temain_mod.temain(NPTS, NX, IDATA, VERBOSE)
  Computes the 41 process measurements and 11 manipulated variables given
    the disturbances time-series matrix.
  The

  Parameters
  ----------
  NPTS : int
    TOTAL NUMBER OF DATA POINTS THE SIMULATOR WILL CALCULATE.
    The simulator gives 1 point per second, which means 1 MIN = 60 POINTS.
    The simulator has a pre-defined sample frequency of 180 s, which means 3 MIN = 1 SAMPLE.
    The number of desired samples is implied in `idata`: idata.shape[0]
    So, the total number of data points is `NPTS = Nsamples*3*60`.
  NX : int
    NUMBER OF SAMPLED DATA POINTS.
  IDATA : 2d-array
    MATRIX OF DISTURBANCES TIME-SERIES (NX, 20)
  VERBOSE :
    VERBOSE FLAG (0 = VERBOSE, 1 = NO VERBOSE)

  Returns
  -------
  XDATA : DataFrame
    MATRIX OF PROCESS MEASUREMENTS AND MANIPULATED VARIABLES (NX, 52)
"""

# modules
import numpy as np
import pandas as pd
import temain_mod


class tep2py():

    def __init__(self, idata):
        if idata.shape[1] == 20:
            self.disturbance_matrix = idata
        else:
            raise ValueError('Matrix of disturbances do not have the appropriate dimension.'
                'It must be shape[1]==20')

        self._build_var_table()
        self._build_disturbance_table()


    def simulate(self):
        """
        Parameters
        ----------
        IDATA : 2d-array
        MATRIX OF DISTURBANCES TIME-SERIES (NX, 20)

        Returns
        -------
        XDATA : DataFrame
        MATRIX OF PROCESS MEASUREMENTS AND MANIPULATED VARIABLES (NX, 52)
        """
        idata = self.disturbance_matrix

        # simulated TEP data
        xdata = temain_mod.temain(
           np.asarray(60*3*idata.shape[0], dtype=np.integer),  
           idata.shape[0],  
           idata,  
          np.int(1)  
          ) 

        # column names
        names = ( 
                ["XMEAS({:})".format(i) for i in range(1,41+1)] 
                + ["XMV({:})".format(i) for i in range(1,11+1)] 
                )
        # index
        datetime = np.arange(0, 3*idata.shape[0] , 3, dtype='datetime64[m]')  

        # data as DataFrame
        xdata = pd.DataFrame(xdata, columns=names, index=datetime)

        self.process_data = xdata


    def _build_var_table(self):
        
        description = [
            'A Feed (stream 1)',
            'D Feed (stream 2)',
            'E Feed (stream 3)',
            'A and C Feed (stream 4)',
            'Recycle Flow (stream 8)',
            'Reactor Feed Rate (stream 6)',
            'Reactor Pressure',
            'Reactor Level',
            'Reactor Temperature',
            'Purge Rate (stream 9)',
            'Product Sep Temp',
            'Product Sep Level',
            'Prod Sep Pressure',
            'Prod Sep Underflow (stream 10)',
            'Stripper Level',
            'Stripper Pressure',
            'Stripper Underflow (stream 11)',
            'Stripper Temperature',
            'Stripper Steam Flow',
            'Compressor Work',
            'Reactor Cooling Water Outlet Temp',
            'Separator Cooling Water Outlet Temp',
            'Component A (stream 6)',
            'Component B (stream 6)',
            'Component C (stream 6)',
            'Component D (stream 6)',
            'Component E (stream 6)',
            'Component F (stream 6)',
            'Component A (stream 9)',
            'Component B (stream 9)',
            'Component C (stream 9)',
            'Component D (stream 9)',
            'Component E (stream 9)',
            'Component F (stream 9)',
            'Component G (stream 9)',
            'Component H (stream 9)',
            'Component D (stream 11)',
            'Component E (stream 11)',
            'Component F (stream 11)',
            'Component G (stream 11)',
            'Component H (stream 11)',
            'D Feed Flow (stream 2)',
            'E Feed Flow (stream 3)',
            'A Feed Flow (stream 1)',
            'A and C Feed Flow (stream 4)',
            'Compressor Recycle Valve',
            'Purge Valve (stream 9)',
            'Separator Pot Liquid Flow (stream 10)',
            'Stripper Liquid Product Flow (stream 11)',
            'Stripper Steam Valve',
            'Reactor Cooling Water Flow',
            'Condenser Cooling Water Flow',
            'Agitator Speed'
        ]

        unit = [
            'kscmh',
            'kg h-1',
            'kg h-1',
            'kscmh',
            'kscmh',
            'kscmh',
            'kPa',
            '%',
            'oC',
            'kscmh',
            'oC',
            '%',
            'kPa',
            'm3 h-1',
            '%',
            'kPa',
            'm3 h-1',
            'oC',
            'kg h-1',
            'kW',
            'oC',
            'oC',
            *['mole %' for i in range(19)],
            *['%' for i in range(12)]
        ]

        variable = (
            ["XMEAS({:})".format(i) for i in range(1,41+1)]
            + ["XMV({:})".format(i) for i in range(1,12+1)]
            )
        
        table = pd.DataFrame({
            'variable': variable,
            'description': description,
            'unit': unit
            })

        self.info_variable = table


    def _build_disturbance_table(self):

        disturbance = ["IDV({:})".format(i) for i in range(1,20+1)]

        description = [
            'A/C Feed Ratio, B Composition Constant (Stream 4) Step',
            'B Composition, A/C Ratio Constant (Stream 4) Step',
            'D Feed Temperature (Stream 2) Step',
            'Reactor Cooling Water Inlet Temperature Step',
            'Condenser Cooling Water Inlet Temperature Step',
            'A Feed Loss (Stream 1) Step',
            'C Header Pressure Loss - Reduced Availability (Stream 4) Step',
            'A, B, C Feed Composition (Stream 4) Random Variation',
            'D Feed Temperature (Stream 2) Random Variation',
            'C Feed Temperature (Stream 4) Random Variation',
            'Reactor Cooling Water Inlet Temperature Random Variation',
            'Condenser Cooling Water Inlet Temperature Random Variation',
            'Reaction Kinetics Slow Drift',
            'Reactor Cooling Water Valve Sticking',
            'Condenser Cooling Water Valve Sticking',
            'Unknown',
            'Unknown',
            'Unknown',
            'Unknown',
            'Unknown',
            ]

        table = pd.DataFrame({
            'disturbance': disturbance,
            'description': description
            })

        self.info_disturbance = table


def test_tep_in_py():
    # matrix of disturbances
    idata = np.zeros((5,20))
    tep = tep2py(idata)
    tep.simulate()
    print(tep.process_data)


if __name__ == '__main__':
    test_tep_in_py()
