#!/usr/bin/python python3

import os, subprocess as sub
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics
import hendrics
from pathlib import Path
from astropy.table import Table

obj_name = 'grs1915'

home = '/home/heasoft/tesis/repro-lc/'
folder = '/home/heasoft/tesis/repro-lc/'+obj_name+'/'

lisfile=sorted(os.listdir(folder))
os.chdir(folder)
obs_id=sorted(os.listdir())

for i in range(len(obs_id)):
    os.chdir(home)
    ob=folder+obs_id[i]
    os.chdir(ob)
    title=obs_id[i]

    events_str='nu'+obs_id[i]+'A01_cl.evt'
    calibrate_str='nu'+obs_id[i]+'A01_cl_nustar_fpma_ev.nc'
    lcurve_str=ob+'/nu'+obs_id[i]+'A01_cl_nustar_fpma_ev_calib.nc'

    sub.run(["HENreadevents", events_str])

    sub.run(["HENcalibrate", calibrate_str])

    os.mkdir('lcurve')
    lcurve=ob+'/lcurve/'
    os.chdir(lcurve)
    os.mkdir('4_6')
    os.mkdir('6_12')
    os.mkdir('12_25')
    lcurve_4_6=lcurve+'4_6/'
    lcurve_6_12=lcurve+'6_12/'
    lcurve_12_25=lcurve+'12_25/'
    os.chdir(ob)

    sub.run(["HENlcurve", lcurve_str, "-b", "1", "-e", "4", "6", "--gti-split", "--minlen", "800", "-d", lcurve_4_6])
    sub.run(["HENlcurve", lcurve_str, "-b", "1", "-e", "6", "12", "--gti-split", "--minlen", "800", "-d", lcurve_6_12])
    sub.run(["HENlcurve", lcurve_str, "-b", "1", "-e", "12", "25", "--gti-split", "--minlen", "800", "-d", lcurve_12_25])

    #sub.run(["HENlcurve", lcurve_str, "-b", "16", "-e", "4", "6", "--gti-split", "--minlen", "800", "-d", lcurve_4_6])
    #sub.run(["HENlcurve", lcurve_str, "-b", "16", "-e", "6", "12", "--gti-split", "--minlen", "800", "-d", lcurve_6_12])
    #sub.run(["HENlcurve", lcurve_str, "-b", "16", "-e", "12", "25", "--gti-split", "--minlen", "800", "-d", lcurve_12_25])

    #sub.run(["HENlcurve", lcurve_str, "-b", "-6.6", "-e", "4", "6", "--gti-split", "--minlen", "800", "-d", lcurve_4_6])
    #sub.run(["HENlcurve", lcurve_str, "-b", "-6.6", "-e", "6", "12", "--gti-split", "--minlen", "800", "-d", lcurve_6_12])
    #sub.run(["HENlcurve", lcurve_str, "-b", "-6.6", "-e", "12", "25", "--gti-split", "--minlen", "800", "-d", lcurve_12_25])

    os.mkdir('plot')
    plot=ob+'/plot/'
    os.chdir(plot)
    os.mkdir('4_6')
    os.mkdir('6_12')
    os.mkdir('12_25')
    plot_4_6=plot+'4_6/'
    plot_6_12=plot+'6_12/'
    plot_12_25=plot+'12_25/'

    list_lcurve_4_6=sorted(os.listdir(lcurve_4_6))
    list_lcurve_6_12=sorted(os.listdir(lcurve_6_12))
    list_lcurve_12_25=sorted(os.listdir(lcurve_12_25))

    for i in range(len(list_lcurve_4_6)):
        filename_lcurve_4_6=Path(list_lcurve_4_6[i]).stem
        filename_lcurve_6_12=Path(list_lcurve_6_12[i]).stem
        filename_lcurve_12_25=Path(list_lcurve_12_25[i]).stem

        sub.run(["HENplot", lcurve_4_6+list_lcurve_4_6[i], "-o", plot_4_6+filename_lcurve_4_6, "--noplot"])
        sub.run(["HENplot", lcurve_6_12+list_lcurve_6_12[i], "-o", plot_6_12+filename_lcurve_6_12, "--noplot"])
        sub.run(["HENplot", lcurve_12_25+list_lcurve_12_25[i], "-o", plot_12_25+filename_lcurve_12_25, "--noplot"])

    list_plot_4_6=sorted(os.listdir(plot_4_6))
    list_plot_6_12=sorted(os.listdir(plot_6_12))
    list_plot_12_25=sorted(os.listdir(plot_12_25))

    obs_id_rms = []
    rms_data = []
    mean_hr1_data = []
    mean_hr2_data = []

    for i in range(len(list_plot_4_6)):
        filename_plot_4_6=Path(list_plot_4_6[i]).stem

        A = pd.read_table(plot_4_6+list_plot_4_6[i], sep=" ", header=None).drop(columns=[2])
        B = pd.read_table(plot_6_12+list_plot_6_12[i], sep=" ", header=None).drop(columns=[2])
        C = pd.read_table(plot_12_25+list_plot_12_25[i], sep=" ", header=None).drop(columns=[2])

        time = pd.Series([], dtype='float64')
        hr1 = pd.Series([], dtype='float64')
        hr2 = pd.Series([], dtype='float64')
        total_lc = pd.Series([], dtype='float64')

        for i in range(len(A)):
            time[i] = A[0][i] - A[0][0]
            hr1[i] = B[1][i] / A[1][i]
            try:
                hr2[i] = C[1][i] / A[1][i]
            except Exception as e:
                print("-------STOP HERE-------")
                print(A.shape, B.shape, C.shape, hr2.size)
                raise Exception
            total_lc[i] = A[1][i] + B[1][i] + C[1][i]

        plot_data = pd.DataFrame()
        plot_data.insert(0,"time", time)
        plot_data.insert(1,"total_lc", total_lc)
        plot_data.insert(2,"hr1", hr1)
        plot_data.insert(3,"hr2", hr2)

        # Ambil obs_id dari nama file
        #obs_id_num_str = str(filename_plot_4_6)
        obs_id_num = str(filename_plot_4_6[2:13])
        obs_id_rms.append(obs_id_num)

        # Perhitungan statistik
        mean_hr1 = statistics.mean(plot_data['hr1'])
        mean_hr2 = statistics.mean(plot_data['hr2'])
        mean_hr1_data.append(mean_hr1)
        mean_hr2_data.append(mean_hr2)

        var = statistics.variance(plot_data['total_lc'])
        mean = statistics.mean(plot_data['total_lc'])
        rms = np.sqrt(var/(mean**2))
        rms_data.append(rms)

        #var = statistics.variance(plot_data['total_lc'])
        #mean = statistics.mean(plot_data['total_lc'])
        #rms = var/mean
        #rms_data.append(rms)

        # Plot grafik
        plt.plot(plot_data['hr2'],plot_data['hr1'], marker='.', linestyle='None', markersize=1, color='black')
        plt.xlim(0,1.3)
        plt.ylim(0,4)
        plt.ylabel('HR1')
        plt.xlabel('HR2')
        plt.title(title)
        plt.savefig(filename_plot_4_6+'_CD.jpeg', dpi=1200)
        plt.clf()

        plt.plot(plot_data['time'], plot_data['total_lc'], color='black')
        plt.ylim(0,500)
        plt.xlim(0,1200)
        plt.xlabel('Time (s)')
        plt.ylabel('Rate (cts/s)')
        plt.title(title)
        plt.savefig(filename_plot_4_6+'_LC.jpeg', dpi=1200)
        plt.clf()

        plt.plot(plot_data['hr2'], plot_data['total_lc'], marker='.', linestyle='None', markersize=1, color='black')
        plt.xlabel('HR2')
        plt.ylabel('Rate (cts/s)')
        plt.ylim(0,500)
        plt.xlim(0,1.3)
        plt.title(title)
        plt.savefig(filename_plot_4_6+'_HID.jpeg', dpi=1200)
        plt.clf()

    os.chdir(ob)
    stat = [obs_id_rms, rms_data, mean_hr1_data, mean_hr2_data]
    dict = {'obs_id_num': obs_id_rms, 'rms': rms_data, 'hr1' : mean_hr1_data, 'hr2' : mean_hr2_data}
    stat_data = pd.DataFrame(dict)

    stat_data.to_csv(title+'_statistik.csv')