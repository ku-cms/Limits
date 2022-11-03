# makePlots.py

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import tools

def plot(plot_dir, plot_name, inputs, info):
    output_name = "{0}/{1}.pdf".format(plot_dir, plot_name)
    
    title   = info["title"]
    x_label = info["x_label"]
    y_label = info["y_label"]
    x_lim   = info["x_lim"]
    y_lim   = info["y_lim"]

    fig, ax = plt.subplots(figsize=(6, 6))
    
    for key in inputs:
        data    = inputs[key]["data"]
        label   = inputs[key]["label"]
        color   = inputs[key]["color"]
        x_vals, y_vals = tools.getXYVals(data)
        plt.plot(x_vals, y_vals, label=label, color=color)
    
    legend_font_size = 12
    
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
    print("Yeah baby, let's go!")
    plot_dir    = "plots"
    plot_name   = "TSlepSlep_Limits"
    
    # TSlepSlep
    inputs = {}
    inputs["ATLAS_Soft_2l"]             = {}
    inputs["ATLAS_Soft_2l"]["csv"]      = "data/HEPData-ins1767649-v5-Figure_16a_Observed.csv"
    inputs["ATLAS_Soft_2l"]["label"]    = "ATLAS Soft 2l (Observed)"
    inputs["ATLAS_Soft_2l"]["color"]    = "xkcd:cherry red"
    inputs["ATLAS_Soft_2l"]["isMvsDM"]  = True
    inputs["ATLAS_2l"]                  = {}
    inputs["ATLAS_2l"]["csv"]           = "data/HEPData-ins1750597-v4-Exclusion_contour_Observed_3.csv"
    inputs["ATLAS_2l"]["label"]         = "ATLAS 2l (Observed)"
    inputs["ATLAS_2l"]["color"]         = "xkcd:tangerine"
    inputs["ATLAS_2l"]["isMvsDM"]       = False

    info = {}
    info["title"]   = "TSlepSlep Limits"
    info["x_label"] = r"$m \left(\tilde{\ell}\right)$ [GeV]"
    info["y_label"] = r"$\Delta m \left(\tilde{\ell}, \tilde{\chi}_{1}^{0}\right)$ [GeV]"
    info["x_lim"]   = [100.0, 600.0]
    info["y_lim"]   = [0.0,   200.0]
    
    # load data from csv file
    for key in inputs:
        inputs[key]["data"] = tools.getData(inputs[key]["csv"]) 
        inputs[key]["data"] = tools.getCleanData(inputs[key]["data"])
        # convert to MvsDM data if needed
        if not inputs[key]["isMvsDM"]:
            inputs[key]["data"] = tools.getDMData(inputs[key]["data"])
    
    tools.makeDir(plot_dir)
    plot(plot_dir, plot_name, inputs, info)

def main():
    makePlots()

if __name__ == "__main__":
    main()

