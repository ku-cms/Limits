# makePlots.py

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import tools
import numpy as np

def plot(plot_dir, plot_name, inputs, info):
    output_name = "{0}/{1}.pdf".format(plot_dir, plot_name)
    
    title   = info["title"]
    x_label = info["x_label"]
    y_label = info["y_label"]
    x_lim   = info["x_lim"]
    y_lim   = info["y_lim"]

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
    
    legend_font_size = 10
    
    ax.legend(loc='upper right', prop={'size': legend_font_size})
    ax.set_title(title,     fontsize=20)
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

def makePlots():
    data_dir    = "data/TSlepSlep"
    plot_dir    = "plots"
    plot_name   = "TSlepSlep_Limits"
    
    # TSlepSlep
    inputs                                  = {}
    inputs["ATLAS_Soft_2l"]                 = {}
    inputs["ATLAS_Soft_2l"]["csv"]          = "{0}/HEPData-ins1767649-v5-Figure_16a_Observed.csv".format(data_dir)
    inputs["ATLAS_Soft_2l"]["label"]        = "ATLAS Soft 2l (Observed)"
    inputs["ATLAS_Soft_2l"]["color"]        = "xkcd:cherry red"
    inputs["ATLAS_Soft_2l"]["isDMvsM"]      = True
    inputs["ATLAS_Soft_2l"]["fillLeft"]     = False
    inputs["ATLAS_Soft_2l"]["flatten"]      = False
    inputs["ATLAS_2l"]                      = {}
    inputs["ATLAS_2l"]["csv"]               = "{0}/HEPData-ins1750597-v4-Exclusion_contour_Observed_3.csv".format(data_dir)
    inputs["ATLAS_2l"]["label"]             = "ATLAS 2l (Observed)"
    inputs["ATLAS_2l"]["color"]             = "xkcd:tangerine"
    inputs["ATLAS_2l"]["isDMvsM"]           = False
    inputs["ATLAS_2l"]["fillLeft"]          = False
    inputs["ATLAS_2l"]["flatten"]           = True
    inputs["CMS_Compressed"]                = {}
    inputs["CMS_Compressed"]["csv"]         = "{0}/KU_SUSY_TSlepSlep_Expected_Limit_DMvsM_v3p1.csv".format(data_dir)
    inputs["CMS_Compressed"]["label"]       = "CMS Compressed (Expected)"
    inputs["CMS_Compressed"]["color"]       = "xkcd:apple green"
    inputs["CMS_Compressed"]["isDMvsM"]     = True
    inputs["CMS_Compressed"]["fillLeft"]    = False
    inputs["CMS_Compressed"]["flatten"]     = False

    info = {}
    info["title"]   = "TSlepSlep Limits"
    info["x_label"] = r"$m \left(\tilde{\ell}_{\mathrm{L}/\mathrm{R}}\right)$ [GeV]"
    info["y_label"] = r"$\Delta m \left(\tilde{\ell}_{\mathrm{L}/\mathrm{R}}, \tilde{\chi}_{1}^{0}\right)$ [GeV]"
    info["x_lim"]   = [100.0, 400.0]
    info["y_lim"]   = [0.0,   100.0]
    #info["y_lim"]   = [0.0,   175.0]
    
    #info["x_lim"]   = [100.0, 600.0]
    #info["y_lim"]   = [0.0,   200.0]
    #info["x_lim"]   = [0.0, 800.0]
    #info["y_lim"]   = [0.0, 800.0]

    flatten_x_range = [0.0, 300.0]
    
    # load data from csv file
    for key in inputs:
        inputs[key]["data"] = tools.getData(inputs[key]["csv"]) 
        inputs[key]["data"] = tools.getCleanData(inputs[key]["data"])
        # convert to DM vs M data if needed
        if not inputs[key]["isDMvsM"]:
            inputs[key]["data"] = tools.getDMvsMData(inputs[key]["data"])
        # flatten: set y values to mean y value over a specified range
        if inputs[key]["flatten"]:
            inputs[key]["data"] = tools.getFlatData(inputs[key]["data"], flatten_x_range)
    
    tools.makeDir(plot_dir)
    plot(plot_dir, plot_name, inputs, info)

def main():
    makePlots()

if __name__ == "__main__":
    main()

