#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from candphy.logs import log

#creating the def for plotting the signals wave
def plot_signal(signal_radio,Fs=99.9,Fc=3.1,NFFT=1024,
                style='science',xlabel='frequency (Mhz)',
                ylabel='Power Spectral Density (DB/Hz)',grid=True,show=True,
                filepath='signal_radio_plot.png',save=True,
                dpi=900):
    if type(signal_radio)==dict:
        if signal_radio['type'] == 'signal_radio':
            log("the signal is from the get_signal_radio!")
            log("getting data from this for the plot...")
            sr=signal_radio
            order = sr['order']
            log("creating plotting")
            fig,ax=plt.psd(sr['samples'],NFFT=sr['bytes'],
                          Fs=sr['freq_rate']/order,
                          Fc=sr['freq_center']/order)
    else:
        fig,ax = plt.psd(signal_radio,NFFT=NFFT,Fc=Fc,Fs=Fs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if grid:
        plt.grid()
    if save:
        plt.savefig(filepath,dpi=dpi)
    if show:
        plt.show()
    
    return plt