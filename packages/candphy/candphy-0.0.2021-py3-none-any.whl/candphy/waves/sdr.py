#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from rtlsdr import *
import numpy as np

from candphy.logs import log

#def for get signal on the space signals on Mhz
def get_signal_radio(freq_center,freq_rate=3.1,
                     again=8,bytes=1024,bits_base=256):
    '''
    freq_center: the frequency central (Mhz) type: float
    freq_rate: the space of frequency's (Mhz) [1.4Mhz-3.1Mhz] type:float
    '''
    mhz = 1e6
    freq_rate*=mhz
    freq_center*=mhz
    init_freq = round(freq_center-(freq_rate/2),3)
    end_freq = round(freq_center+(freq_rate/2),3)
    log(f"init frequency: {init_freq}Mhz\nend frequency: {end_freq}Mhz")
    #initalizng the sdr
    log("initializing the sdr drive...")
    sdr = RtlSdr()
    
    log("configuring the sample rate...")
    sdr.sample_rate=(freq_rate)
    
    log("configuring the frequency center of samples...")
    sdr.center_freq=(freq_center)
    
    log("configuring the again...")
    sdr.again = again
    
    log("getting the samples using the bits and bytes as base as numpy array...")
    samples = np.array(sdr.read_samples(bits_base*bytes))
    log(f"size of samples signal: {samples.size} bits")
    
    res = {'freq_center':freq_center,
           'freq_rate':freq_rate,
           'bytes':bytes,
           'order':mhz,
           'size_signal':samples.size,
           'samples':samples,
           'type':'signal_radio'}
    
    return res
    
