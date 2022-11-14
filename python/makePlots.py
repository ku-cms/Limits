# makePlots.py

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import tools
import numpy as np

# Create plot
def plot(plot_dir, plot_name, inputs, info):
    output_name = "{0}/{1}.pdf".format(plot_dir, plot_name)
    
    title               = info["title"]
    proc_label          = info["proc_label"]
    x_label             = info["x_label"]
    y_label             = info["y_label"]
    proc_label_x_pos    = info["proc_label_x_pos"]
    proc_label_y_pos    = info["proc_label_y_pos"]
    x_lim               = info["x_lim"]
    y_lim               = info["y_lim"]

    fig, ax = plt.subplots(figsize=(6, 6))

    print("Creating the plot '{0}'".format(title))
    
    for key in inputs:
        data        = inputs[key]["data"]
        label       = inputs[key]["label"]
        color       = inputs[key]["color"]
        fillLeft    = inputs[key]["fillLeft"]
        x_vals, y_vals = tools.getXYVals(data)
        plt.plot(x_vals, y_vals, label=label, color=color)
        plt.fill_between(x_vals, y_vals, y_lim[1], color=color, alpha=0.5)
        if fillLeft:
            x_min  = x_lim[0]
            x_max  = np.min(x_vals)
            x_fill = [x_min, x_max]
            plt.fill_between(x_fill, y_lim[0], y_lim[1], color=color, alpha=0.5)
        print(" - Plotted '{0}'".format(key))
    
    # Enable dark mode!
    #plt.fill_between(x_lim, y_lim[0], y_lim[1], color="black", alpha=0.5)
    
    # get coordinates for labels
    x_range = x_lim[1] - x_lim[0]
    y_range = y_lim[1] - y_lim[0]
    #proc_label_x = x_lim[0] + 0.50 * x_range
    #proc_label_y = y_lim[0] + 0.65 * y_range
    proc_label_x = x_lim[0] + proc_label_x_pos * x_range
    proc_label_y = y_lim[0] + proc_label_y_pos * y_range
    legend_font_size = 10
    
    ax.text(proc_label_x, proc_label_y, proc_label)
    ax.legend(loc='upper right', prop={'size': legend_font_size})
    #ax.set_title(title,     fontsize=20)
    ax.set_xlabel(x_label,  fontsize=16)
    ax.set_ylabel(y_label,  fontsize=16)
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(axis='both', which='both', bottom=True, top=True, left=True, right=True, direction="in")
    ax.tick_params(axis='both', which='major', labelsize=16, length=8)
    ax.tick_params(axis='both', which='minor', labelsize=8,  length=4)
    
    plt.savefig(output_name, bbox_inches='tight')

# Prepare to plot
def preparePlot(plot_dir, plot_name, inputs, info):
    title = info["title"]
    print("Preparing to plot '{0}'".format(title))
    
    # load data from csv file
    for key in inputs:
        inputs[key]["data"] = tools.getData(inputs[key]["csv"]) 
        inputs[key]["data"] = tools.getCleanData(inputs[key]["data"])
        # convert to DM vs M data if needed
        if not inputs[key]["isDMvsM"]:
            inputs[key]["data"] = tools.getDMvsMData(inputs[key]["data"])
        # flatten: set y values to mean y value over a specified range
        if inputs[key]["flatten"]:
            inputs[key]["data"] = tools.getFlatData(inputs[key]["data"], info["flatten_x_range"])
    
    # plot
    tools.makeDir(plot_dir)
    plot(plot_dir, plot_name, inputs, info)

# Create plot for TSlepSlep
def makePlotTSlepSlep():
    data_dir    = "data/TSlepSlep"
    plot_dir    = "plots"
    plot_name   = "TSlepSlep_Limits"
    
    # TSlepSlep
    inputs                                  = {}
    inputs["ATLAS_Soft_2L"]                 = {}
    inputs["ATLAS_Soft_2L"]["csv"]          = "{0}/HEPData-ins1767649-v5-Figure_16a_Observed.csv".format(data_dir)
    inputs["ATLAS_Soft_2L"]["label"]        = "ATLAS Soft 2L (Observed)"
    inputs["ATLAS_Soft_2L"]["color"]        = "xkcd:cherry red"
    inputs["ATLAS_Soft_2L"]["isDMvsM"]      = True
    inputs["ATLAS_Soft_2L"]["fillLeft"]     = False
    inputs["ATLAS_Soft_2L"]["flatten"]      = False
    inputs["ATLAS_2L"]                      = {}
    inputs["ATLAS_2L"]["csv"]               = "{0}/HEPData-ins1750597-v4-Exclusion_contour_Observed_3.csv".format(data_dir)
    inputs["ATLAS_2L"]["label"]             = "ATLAS 2L (Observed)"
    inputs["ATLAS_2L"]["color"]             = "xkcd:tangerine"
    inputs["ATLAS_2L"]["isDMvsM"]           = False
    inputs["ATLAS_2L"]["fillLeft"]          = False
    inputs["ATLAS_2L"]["flatten"]           = True
    inputs["CMS_Compressed"]                = {}
    inputs["CMS_Compressed"]["csv"]         = "{0}/KU_SUSY_TSlepSlep_Expected_Limit_DMvsM_v3p1.csv".format(data_dir)
    inputs["CMS_Compressed"]["label"]       = "CMS Compressed (Expected)"
    inputs["CMS_Compressed"]["color"]       = "xkcd:apple green"
    inputs["CMS_Compressed"]["isDMvsM"]     = True
    inputs["CMS_Compressed"]["fillLeft"]    = False
    inputs["CMS_Compressed"]["flatten"]     = False

    info = {}
    info["title"]               = "TSlepSlep Limits"
    info["proc_label"]          = r"$p p \to \tilde{\ell}_{\mathrm{L,R}}^{+} \tilde{\ell}_{\mathrm{L,R}}^{-}$, $\tilde{\ell} \to \ell \tilde{\chi}_{1}^{0}$, $\ell \in [e, \mu]$"
    info["x_label"]             = r"$m \left(\tilde{\ell}_{\mathrm{L,R}}\right)$ [GeV]"
    info["y_label"]             = r"$\Delta m \left(\tilde{\ell}_{\mathrm{L,R}}, \tilde{\chi}_{1}^{0}\right)$ [GeV]"
    info["proc_label_x_pos"]    = 0.50  # process label x position as fraction in range [0.0, 1.0]
    info["proc_label_y_pos"]    = 0.65  # process label y position as fraction in range [0.0, 1.0]
    info["x_lim"]               = [110.0, 300.0]
    info["y_lim"]               = [0.0,   100.0]
    info["flatten_x_range"]     = [0.0, 300.0]   # x range over which to set y values to mean y value
    
    #info["x_lim"]   = [100.0, 400.0]
    #info["y_lim"]   = [0.0,   100.0]
    
    #info["x_lim"]   = [100.0, 400.0]
    #info["y_lim"]   = [0.0,   175.0]
    
    #info["x_lim"]   = [100.0, 600.0]
    #info["y_lim"]   = [0.0,   200.0]
    
    #info["x_lim"]   = [0.0, 800.0]
    #info["y_lim"]   = [0.0, 800.0]

    preparePlot(plot_dir, plot_name, inputs, info)

# Create plot for TChiWZ
def makePlotTChiWZ():
    data_dir    = "data/TChiWZ"
    plot_dir    = "plots"
    plot_name   = "TChiWZ_Limits"
    
    # TChiWZ
    inputs                                  = {}
    inputs["ATLAS_Soft_2L"]                 = {}
    inputs["ATLAS_Soft_2L"]["csv"]          = "{0}/HEPData-ins1767649-v5-Figure_14b_Observed.csv".format(data_dir)
    inputs["ATLAS_Soft_2L"]["label"]        = "ATLAS Soft 2L (Observed)"
    inputs["ATLAS_Soft_2L"]["color"]        = "xkcd:cherry red"
    inputs["ATLAS_Soft_2L"]["isDMvsM"]      = True
    inputs["ATLAS_Soft_2L"]["fillLeft"]     = False
    inputs["ATLAS_Soft_2L"]["flatten"]      = False
    inputs["CMS_Compressed"]                = {}
    inputs["CMS_Compressed"]["csv"]         = "{0}/KU_SUSY_TChiWZ_Expected_Limit_DMvsM_v1p1.csv".format(data_dir)
    inputs["CMS_Compressed"]["label"]       = "CMS Compressed (Expected)"
    inputs["CMS_Compressed"]["color"]       = "xkcd:apple green"
    inputs["CMS_Compressed"]["isDMvsM"]     = True
    inputs["CMS_Compressed"]["fillLeft"]    = False
    inputs["CMS_Compressed"]["flatten"]     = False
    
    info = {}
    info["title"]               = "TChiWZ Limits"
    info["proc_label"]          = r"$p p \to \tilde{\chi}_{2}^{0} \tilde{\chi}_{1}^{\pm}$ (Wino); $\tilde{\chi}_{2}^{0} \to Z^{*} \tilde{\chi}_{1}^{0}$, $\tilde{\chi}_{1}^{\pm} \to W^{*} \tilde{\chi}_{1}^{0}$"
    info["x_label"]             = r"$m \left(\tilde{\chi}_{2}^{0}\right)$ [GeV]" 
    info["y_label"]             = r"$\Delta m \left(\tilde{\chi}_{2}^{0}, \tilde{\chi}_{1}^{0}\right)$ [GeV]"
    info["proc_label_x_pos"]    = 0.40  # process label x position as fraction in range [0.0, 1.0]
    info["proc_label_y_pos"]    = 0.75  # process label y position as fraction in range [0.0, 1.0]
    info["x_lim"]               = [120.0, 400.0]
    info["y_lim"]               = [3.0,   50.0]
    
    #info["x_lim"]   = [0.0, 600.0]
    #info["y_lim"]   = [0.0, 50.0]
    
    #info["x_lim"]   = [100.0, 400.0]
    #info["y_lim"]   = [0.0,   100.0]
    
    #info["x_lim"]   = [0.0, 800.0]
    #info["y_lim"]   = [0.0, 800.0]
    
    preparePlot(plot_dir, plot_name, inputs, info)

# Create plot for T2ttC
def makePlotT2ttC():
    data_dir    = "data/T2ttC"
    plot_dir    = "plots"
    plot_name   = "T2ttC_Limits"
    
    # T2ttC
    inputs                                  = {}
    inputs["ATLAS_0L"]                      = {}
    inputs["ATLAS_0L"]["csv"]               = "{0}/HEPData-ins1793461-v2-stop_obs.csv".format(data_dir)
    inputs["ATLAS_0L"]["label"]             = "ATLAS 0L (Observed)"
    inputs["ATLAS_0L"]["color"]             = "xkcd:cherry red"
    inputs["ATLAS_0L"]["isDMvsM"]           = False
    inputs["ATLAS_0L"]["fillLeft"]          = False
    inputs["ATLAS_0L"]["flatten"]           = False
    inputs["ATLAS_1L"]                      = {}
    inputs["ATLAS_1L"]["csv"]               = "{0}/ATLAS_1L_T2ttC_Observed_Limit_DMvsM_v1p1.csv".format(data_dir)
    inputs["ATLAS_1L"]["label"]             = "ATLAS 1L (Observed)"
    inputs["ATLAS_1L"]["color"]             = "xkcd:tangerine"
    inputs["ATLAS_1L"]["isDMvsM"]           = True
    inputs["ATLAS_1L"]["fillLeft"]          = False
    inputs["ATLAS_1L"]["flatten"]           = False
    inputs["CMS_Compressed"]                = {}
    inputs["CMS_Compressed"]["csv"]         = "{0}/KU_SUSY_T2ttC_Expected_Limit_DMvsM_v1p1.csv".format(data_dir)
    inputs["CMS_Compressed"]["label"]       = "CMS Compressed (Expected)"
    inputs["CMS_Compressed"]["color"]       = "xkcd:apple green"
    inputs["CMS_Compressed"]["isDMvsM"]     = True
    inputs["CMS_Compressed"]["fillLeft"]    = False
    inputs["CMS_Compressed"]["flatten"]     = False
    
    info = {}
    info["title"]               = "T2ttC Limits"
    info["proc_label"]          = "Process label."
    info["x_label"]             = r"$m \left(\tilde{t}_{1}\right)$ [GeV]" 
    info["y_label"]             = r"$\Delta m \left(\tilde{t}_{1}, \tilde{\chi}_{1}^{0}\right)$ [GeV]"
    info["proc_label_x_pos"]    = 0.50  # process label x position as fraction in range [0.0, 1.0]
    info["proc_label_y_pos"]    = 0.50  # process label y position as fraction in range [0.0, 1.0]
    info["x_lim"]               = [400.0, 1000.0]
    info["y_lim"]               = [10.0,  80.0]
    #info["x_lim"]   = [200.0, 800.0]
    #info["y_lim"]   = [10.0,  210.0]
    
    #info["x_lim"]   = [300.0, 800.0]
    #info["y_lim"]   = [0.0,   250.0]
    
    #info["x_lim"]   = [0.0, 1000.0]
    #info["y_lim"]   = [0.0, 300.0]
    
    preparePlot(plot_dir, plot_name, inputs, info)

def main():
    makePlotTSlepSlep()
    makePlotTChiWZ()
    makePlotT2ttC()

if __name__ == "__main__":
    main()

