# makePlots.py

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import tools
import numpy as np

# Get color using index
def getColor(index):
    # version 1
    #colors = {
    #    1 : "xkcd:pinkish purple",
    #    2 : "xkcd:tangerine",
    #    3 : "xkcd:apple green",
    #    4 : "xkcd:bright blue",
    #    5 : "xkcd:light red"
    #}
    
    # version 2
    #colors = {
    #    1 : "xkcd:pale purple",
    #    2 : "xkcd:dusky rose",
    #    3 : "xkcd:soft green",
    #    4 : "xkcd:sky",
    #    5 : "xkcd:dusty pink"
    #}
    
    # version 3
    colors = {
        1 : "xkcd:pale purple",
        2 : "xkcd:pale yellow",
        3 : "xkcd:soft green",
        4 : "xkcd:sky",
        5 : "xkcd:dusty pink"
    }
    
    #colors = {
    #    1 : "xkcd:pinkish",
    #    2 : "xkcd:pale orange",
    #    3 : "xkcd:jade",
    #    4 : "xkcd:dark sky blue",
    #    5 : "xkcd:light red"
    #}
    
    #colors = {
    #    1 : "xkcd:light red",
    #    2 : "xkcd:light orange",
    #    3 : "xkcd:green",
    #    4 : "xkcd:azure",
    #    5 : "xkcd:lavender"
    #}
    return colors[index]

# Create plot
def plot(plot_dir, plot_name, input_list, inputs, info):
    output_name = "{0}/{1}.pdf".format(plot_dir, plot_name)
    
    title               = info["title"]
    proc_label          = info["proc_label"]
    x_label             = info["x_label"]
    y_label             = info["y_label"]
    proc_label_x_pos    = info["proc_label_x_pos"]
    proc_label_y_pos    = info["proc_label_y_pos"]
    x_lim               = info["x_lim"]
    y_lim               = info["y_lim"]
    legend_loc          = info["legend_loc"]
    legend_order        = info["legend_order"]
    # set alpha values
    #alpha_line          = 0.0
    #alpha_fill          = 1.0
    #alpha_line          = 1.0
    #alpha_fill          = 0.0
    #alpha_line          = 0.5 
    #alpha_fill          = 0.5 
    #alpha_line          = 1.0
    #alpha_fill          = 0.5 
    #alpha_line          = 0.0
    #alpha_fill          = 0.5 

    fig, ax = plt.subplots(figsize=(6, 6))

    print("Creating the plot '{0}'".format(title))
    
    for key in input_list:
        data        = inputs[key]["data"]
        label       = inputs[key]["label"]
        color       = inputs[key]["color"]
        line_style  = inputs[key]["line_style"]
        alpha_line  = inputs[key]["alpha_line"]
        alpha_fill  = inputs[key]["alpha_fill"]
        fillDown    = inputs[key]["fillDown"]
        fillLeft    = inputs[key]["fillLeft"]
        
        x_vals, y_vals = tools.getXYVals(data)
        
        plt.plot(x_vals, y_vals, label=label, color=color, linewidth=3, linestyle=line_style, alpha=alpha_line)
        
        # specify vertical limits for fill
        if fillDown:
            plt.fill_between(x_vals, y_lim[0], y_vals, color=color, alpha=alpha_fill)
        else:
            plt.fill_between(x_vals, y_vals, y_lim[1], color=color, alpha=alpha_fill)
        
        if fillLeft:
            x_min  = x_lim[0]
            x_max  = np.min(x_vals)
            x_fill = [x_min, x_max]
            plt.fill_between(x_fill, y_lim[0], y_lim[1], color=color, alpha=alpha_fill)
        
        print(" - Plotted '{0}'".format(key))
    
    # Enable dark mode!
    #plt.fill_between(x_lim, y_lim[0], y_lim[1], color="black", alpha=alpha_fill)
    
    # get coordinates for labels
    x_range = x_lim[1] - x_lim[0]
    y_range = y_lim[1] - y_lim[0]
    proc_label_x = x_lim[0] + proc_label_x_pos * x_range
    proc_label_y = y_lim[0] + proc_label_y_pos * y_range
    energy_label_x = x_lim[0] + 0.77 * x_range
    energy_label_y = y_lim[0] + 1.02 * y_range
    energy_label = r"$\sqrt{s} = 13$ TeV"
    label_font_size     = 12
    legend_font_size    = 8
    
    # label for center of mass energy
    ax.text(energy_label_x, energy_label_y, energy_label, fontsize=label_font_size)
    # label for process
    ax.text(proc_label_x, proc_label_y, proc_label, fontsize=label_font_size)
    
    # legend
    handles, labels = ax.get_legend_handles_labels()
    # set legend order
    handles_ordered = [handles[i] for i in legend_order]
    labels_ordered  = [labels[i]  for i in legend_order]
    legend = ax.legend(handles_ordered, labels_ordered, loc=legend_loc, framealpha=0.9, prop={'size': legend_font_size})
    
    # set alpha for legend entries
    for handle in legend.legendHandles:
        handle.set_alpha(1.0)
    
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
    ax.grid(color="black", linestyle="dotted")
    
    plt.savefig(output_name, bbox_inches='tight')

# Prepare to plot
def preparePlot(plot_dir, plot_name, input_list, inputs, info):
    title = info["title"]
    print("Preparing to plot '{0}'".format(title))
    
    # load data from csv file
    for key in input_list:
        inputs[key]["data"] = tools.getData(inputs[key]["csv"]) 
        inputs[key]["data"] = tools.getCleanData(inputs[key]["data"])
        # convert to DM vs M data if needed
        if not inputs[key]["isDMvsM"]:
            inputs[key]["data"] = tools.getDMvsMData(inputs[key]["data"])
        # smooth = 1: flat smoothing (set y values to mean y value over a specified range)
        if inputs[key]["smooth"] == 1:
            inputs[key]["data"] = tools.getFlatData(inputs[key]["data"], info["smooth_x_range"])
        # smooth = 2: linear smoothing (use x points based on given range and step size; set y values using linear fit of neighbors)
        if inputs[key]["smooth"] == 2:
            inputs[key]["data"] = tools.getLinearSmoothData(inputs[key]["data"], info["smooth_x_range"], info["smooth_step"])
    
    # plot
    tools.makeDir(plot_dir)
    plot(plot_dir, plot_name, input_list, inputs, info)

# Create plot for TSlepSlep
def makePlotTSlepSlep():
    data_dir    = "data/TSlepSlep"
    plot_dir    = "plots"
    plot_name   = "TSlepSlep_Limits"

    # input list:   define order when plotting
    # legend order: define order in legend
    
    #input_list = ["CMS_Preliminary", "ATLAS_Soft_2L", "ATLAS_2L", "CMS_2L"]
    #legend_order = [0, 1, 2, 3]
    
    input_list = ["ATLAS_Soft_2L", "ATLAS_2L", "CMS_2L", "CMS_Preliminary", "CMS_Preliminary_Up", "CMS_Preliminary_Down"]
    legend_order = [0, 1, 2, 3, 4, 5]

    #ku_susy_base_name = "TSlepSlep_contour_2022_11_08_dM_exp"
    ku_susy_base_name = "TSlepSlep_contour_2022_11_24_dM_exp"
    
    # TSlepSlep
    inputs                                          = {}
    inputs["ATLAS_Soft_2L"]                         = {}
    inputs["ATLAS_Soft_2L"]["csv"]                  = "{0}/HEPData-ins1767649-v5-Figure_16a_Observed.csv".format(data_dir)
    inputs["ATLAS_Soft_2L"]["label"]                = "ATLAS: Phys. Rev. D 101, 052005 (2020)"
    inputs["ATLAS_Soft_2L"]["color"]                = getColor(1)
    inputs["ATLAS_Soft_2L"]["line_style"]           = "-"
    inputs["ATLAS_Soft_2L"]["alpha_line"]           = 0.0
    inputs["ATLAS_Soft_2L"]["alpha_fill"]           = 0.5
    inputs["ATLAS_Soft_2L"]["isDMvsM"]              = True
    inputs["ATLAS_Soft_2L"]["fillDown"]             = True
    inputs["ATLAS_Soft_2L"]["fillLeft"]             = False
    inputs["ATLAS_Soft_2L"]["smooth"]               = 0
    inputs["ATLAS_2L"]                              = {}
    inputs["ATLAS_2L"]["csv"]                       = "{0}/HEPData-ins1750597-v4-Exclusion_contour_Observed_3.csv".format(data_dir)
    inputs["ATLAS_2L"]["label"]                     = "ATLAS: Eur. Phys. J. C 80, 123 (2020)"
    inputs["ATLAS_2L"]["color"]                     = getColor(2)
    inputs["ATLAS_2L"]["line_style"]                = "-"
    inputs["ATLAS_2L"]["alpha_line"]                = 0.0
    inputs["ATLAS_2L"]["alpha_fill"]                = 0.5
    inputs["ATLAS_2L"]["isDMvsM"]                   = False
    inputs["ATLAS_2L"]["fillDown"]                  = False
    inputs["ATLAS_2L"]["fillLeft"]                  = False
    inputs["ATLAS_2L"]["smooth"]                    = 0
    inputs["CMS_2L"]                                = {}
    inputs["CMS_2L"]["csv"]                         = "{0}/CMS_2L_TSlepSlep_Observed_Limit_MvsM_v1p1.csv".format(data_dir)
    inputs["CMS_2L"]["label"]                       = "CMS: J. High Energ. Phys. 2021, 123 (2021)"
    inputs["CMS_2L"]["color"]                       = getColor(4)
    inputs["CMS_2L"]["line_style"]                  = "-"
    inputs["CMS_2L"]["alpha_line"]                  = 0.0
    inputs["CMS_2L"]["alpha_fill"]                  = 0.5
    inputs["CMS_2L"]["isDMvsM"]                     = False
    inputs["CMS_2L"]["fillDown"]                    = False
    inputs["CMS_2L"]["fillLeft"]                    = False
    inputs["CMS_2L"]["smooth"]                      = 0
    inputs["CMS_Preliminary"]                       = {}
    #inputs["CMS_Preliminary"]["csv"]                = "{0}/KU_SUSY_TSlepSlep_Expected_Limit_DMvsM_v3p1.csv".format(data_dir)
    inputs["CMS_Preliminary"]["csv"]                = "{0}/{1}_central.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary"]["label"]              = "CMS Preliminary (Expected)"
    inputs["CMS_Preliminary"]["color"]              = getColor(3)
    inputs["CMS_Preliminary"]["line_style"]         = "-"
    inputs["CMS_Preliminary"]["alpha_line"]         = 1.0
    inputs["CMS_Preliminary"]["alpha_fill"]         = 0.5
    inputs["CMS_Preliminary"]["isDMvsM"]            = True
    inputs["CMS_Preliminary"]["fillDown"]           = True
    inputs["CMS_Preliminary"]["fillLeft"]           = False
    inputs["CMS_Preliminary"]["smooth"]             = 0
    inputs["CMS_Preliminary_Up"]                    = {}
    inputs["CMS_Preliminary_Up"]["csv"]             = "{0}/{1}_up.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary_Up"]["label"]           = "CMS Preliminary (Expected Up)"
    inputs["CMS_Preliminary_Up"]["color"]           = getColor(3)
    inputs["CMS_Preliminary_Up"]["line_style"]      = "--"
    inputs["CMS_Preliminary_Up"]["alpha_line"]      = 1.0
    inputs["CMS_Preliminary_Up"]["alpha_fill"]      = 0.0
    inputs["CMS_Preliminary_Up"]["isDMvsM"]         = True
    inputs["CMS_Preliminary_Up"]["fillDown"]        = True
    inputs["CMS_Preliminary_Up"]["fillLeft"]        = False
    inputs["CMS_Preliminary_Up"]["smooth"]          = 0
    inputs["CMS_Preliminary_Down"]                  = {}
    inputs["CMS_Preliminary_Down"]["csv"]           = "{0}/{1}_down.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary_Down"]["label"]         = "CMS Preliminary (Expected Down)"
    inputs["CMS_Preliminary_Down"]["color"]         = getColor(3)
    inputs["CMS_Preliminary_Down"]["line_style"]    = "--"
    inputs["CMS_Preliminary_Down"]["alpha_line"]    = 1.0
    inputs["CMS_Preliminary_Down"]["alpha_fill"]    = 0.0
    inputs["CMS_Preliminary_Down"]["isDMvsM"]       = True
    inputs["CMS_Preliminary_Down"]["fillDown"]      = True
    inputs["CMS_Preliminary_Down"]["fillLeft"]      = False
    inputs["CMS_Preliminary_Down"]["smooth"]        = 0

    info = {}
    info["title"]               = "TSlepSlep Limits"
    info["proc_label"]          = r"$p p \to \tilde{\ell}_{\mathrm{L/R}}^{+} \tilde{\ell}_{\mathrm{L/R}}^{-}$, $\tilde{\ell} \to \ell \tilde{\chi}_{1}^{0}$, $\ell \in [e, \mu]$"
    info["x_label"]             = r"$m \left(\tilde{\ell}_{\mathrm{L/R}}\right)$ [GeV]"
    info["y_label"]             = r"$\Delta m \left(\tilde{\ell}_{\mathrm{L/R}}, \tilde{\chi}_{1}^{0}\right)$ [GeV]"
    info["proc_label_x_pos"]    = 0.00  # process label x position as fraction in range [0.0, 1.0]
    info["proc_label_y_pos"]    = 1.02  # process label y position as fraction in range [0.0, 1.0]
    info["x_lim"]               = [90.0, 350.0]
    info["y_lim"]               = [3.0,  100.0]
    info["legend_loc"]          = "upper right"
    info["legend_order"]        = legend_order
    info["smooth_x_range"]      = [100,   300]  # x range over which to set y values to mean y value
    #info["smooth_step"]         = 100           # step size for linear smoothing
    #info["smooth_step"]         = 50            # step size for linear smoothing
    info["smooth_step"]         = 25            # step size for linear smoothing
    #info["smooth_step"]         = 20           # step size for linear smoothing
    #info["smooth_step"]         = 10           # step size for linear smoothing
    
    #info["x_lim"]               = [110.0, 300.0]
    #info["y_lim"]               = [0.0,   100.0]
    
    #info["x_lim"]   = [100.0, 400.0]
    #info["y_lim"]   = [0.0,   100.0]
    
    #info["x_lim"]   = [100.0, 400.0]
    #info["y_lim"]   = [0.0,   175.0]
    
    #info["x_lim"]   = [0.0, 400.0]
    #info["y_lim"]   = [0.0, 200.0]
    
    #info["x_lim"]   = [0.0, 800.0]
    #info["y_lim"]   = [0.0, 800.0]

    preparePlot(plot_dir, plot_name, input_list, inputs, info)

# Create plot for TChiWZ
def makePlotTChiWZ():
    data_dir    = "data/TChiWZ"
    plot_dir    = "plots"
    plot_name   = "TChiWZ_Limits"
    
    # input list:   define order when plotting
    # legend order: define order in legend
    
    #input_list = ["CMS_Preliminary", "CMS_2L_3L", "ATLAS_Soft_2L"]
    #legend_order = [2, 1, 0]
    
    input_list = ["ATLAS_Soft_2L", "CMS_2L_3L", "CMS_Preliminary", "CMS_Preliminary_Up", "CMS_Preliminary_Down"]
    legend_order = [0, 1, 2, 3, 4]
    
    #ku_susy_base_name = "TChiWZ_contour_2022_11_08_dM_exp"
    ku_susy_base_name = "TChiWZ_contour_2022_11_24_dM_exp"
    
    # TChiWZ
    inputs                                          = {}
    inputs["ATLAS_Soft_2L"]                         = {}
    inputs["ATLAS_Soft_2L"]["csv"]                  = "{0}/HEPData-ins1767649-v5-Figure_14b_Observed.csv".format(data_dir)
    inputs["ATLAS_Soft_2L"]["label"]                = "ATLAS: Phys. Rev. D 101, 052005 (2020)"
    inputs["ATLAS_Soft_2L"]["color"]                = getColor(1)
    inputs["ATLAS_Soft_2L"]["line_style"]           = "-"
    inputs["ATLAS_Soft_2L"]["alpha_line"]           = 0.0
    inputs["ATLAS_Soft_2L"]["alpha_fill"]           = 0.5
    inputs["ATLAS_Soft_2L"]["isDMvsM"]              = True
    inputs["ATLAS_Soft_2L"]["fillDown"]             = True
    inputs["ATLAS_Soft_2L"]["fillLeft"]             = False
    inputs["ATLAS_Soft_2L"]["smooth"]               = 0
    inputs["CMS_2L_3L"]                             = {}
    inputs["CMS_2L_3L"]["csv"]                      = "{0}/CMS_2L_3L_TChiWZ_Observed_Limit_DMvsM_v1p1.csv".format(data_dir)
    inputs["CMS_2L_3L"]["label"]                    = "CMS: J. High Energ. Phys. 2022, 91 (2022)"
    inputs["CMS_2L_3L"]["color"]                    = getColor(4)
    inputs["CMS_2L_3L"]["line_style"]               = "-"
    inputs["CMS_2L_3L"]["alpha_line"]               = 0.0
    inputs["CMS_2L_3L"]["alpha_fill"]               = 0.5
    inputs["CMS_2L_3L"]["isDMvsM"]                  = True
    inputs["CMS_2L_3L"]["fillDown"]                 = True
    inputs["CMS_2L_3L"]["fillLeft"]                 = False
    inputs["CMS_2L_3L"]["smooth"]                   = 0
    inputs["CMS_Preliminary"]                       = {}
    #inputs["CMS_Preliminary"]["csv"]                = "{0}/KU_SUSY_TChiWZ_Expected_Limit_DMvsM_v1p1.csv".format(data_dir)
    inputs["CMS_Preliminary"]["csv"]                = "{0}/{1}_central.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary"]["label"]              = "CMS Preliminary (Expected)"
    inputs["CMS_Preliminary"]["color"]              = getColor(3)
    inputs["CMS_Preliminary"]["line_style"]         = "-"
    inputs["CMS_Preliminary"]["alpha_line"]         = 1.0
    inputs["CMS_Preliminary"]["alpha_fill"]         = 0.5
    inputs["CMS_Preliminary"]["isDMvsM"]            = True
    inputs["CMS_Preliminary"]["fillDown"]           = True
    inputs["CMS_Preliminary"]["fillLeft"]           = False
    inputs["CMS_Preliminary"]["smooth"]             = 0
    inputs["CMS_Preliminary_Up"]                    = {}
    inputs["CMS_Preliminary_Up"]["csv"]             = "{0}/{1}_up.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary_Up"]["label"]           = "CMS Preliminary (Expected Up)"
    inputs["CMS_Preliminary_Up"]["color"]           = getColor(3)
    inputs["CMS_Preliminary_Up"]["line_style"]      = "--"
    inputs["CMS_Preliminary_Up"]["alpha_line"]      = 1.0
    inputs["CMS_Preliminary_Up"]["alpha_fill"]      = 0.0
    inputs["CMS_Preliminary_Up"]["isDMvsM"]         = True
    inputs["CMS_Preliminary_Up"]["fillDown"]        = True
    inputs["CMS_Preliminary_Up"]["fillLeft"]        = False
    inputs["CMS_Preliminary_Up"]["smooth"]          = 0
    inputs["CMS_Preliminary_Down"]                  = {}
    inputs["CMS_Preliminary_Down"]["csv"]           = "{0}/{1}_down.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary_Down"]["label"]         = "CMS Preliminary (Expected Down)"
    inputs["CMS_Preliminary_Down"]["color"]         = getColor(3)
    inputs["CMS_Preliminary_Down"]["line_style"]    = "--"
    inputs["CMS_Preliminary_Down"]["alpha_line"]    = 1.0
    inputs["CMS_Preliminary_Down"]["alpha_fill"]    = 0.0
    inputs["CMS_Preliminary_Down"]["isDMvsM"]       = True
    inputs["CMS_Preliminary_Down"]["fillDown"]      = True
    inputs["CMS_Preliminary_Down"]["fillLeft"]      = False
    inputs["CMS_Preliminary_Down"]["smooth"]        = 0
    
    info = {}
    info["title"]               = "TChiWZ Limits"
    info["proc_label"]          = r"$p p \to \tilde{\chi}_{2}^{0} \tilde{\chi}_{1}^{\pm}$ (Wino); $\tilde{\chi}_{2}^{0} \to Z^{*} \tilde{\chi}_{1}^{0}$, $\tilde{\chi}_{1}^{\pm} \to W^{*} \tilde{\chi}_{1}^{0}$"
    info["x_label"]             = r"$m \left(\tilde{\chi}_{2}^{0}\right)$ [GeV]" 
    info["y_label"]             = r"$\Delta m \left(\tilde{\chi}_{2}^{0}, \tilde{\chi}_{1}^{0}\right)$ [GeV]"
    info["proc_label_x_pos"]    = 0.00  # process label x position as fraction in range [0.0, 1.0]
    info["proc_label_y_pos"]    = 1.02  # process label y position as fraction in range [0.0, 1.0]
    info["x_lim"]               = [120.0, 400.0]
    info["y_lim"]               = [3.0,   50.0]
    info["legend_loc"]          = "upper left"
    info["legend_order"]        = legend_order
    
    #info["x_lim"]               = [120.0, 350.0]
    #info["y_lim"]               = [3.0,   50.0]
    
    #info["x_lim"]   = [0.0, 600.0]
    #info["y_lim"]   = [0.0, 50.0]
    
    #info["x_lim"]   = [100.0, 400.0]
    #info["y_lim"]   = [0.0,   100.0]
    
    #info["x_lim"]   = [0.0, 800.0]
    #info["y_lim"]   = [0.0, 800.0]
    
    preparePlot(plot_dir, plot_name, input_list, inputs, info)

# Create plot for T2ttC
def makePlotT2ttC():
    data_dir    = "data/T2ttC"
    plot_dir    = "plots"
    plot_name   = "T2ttC_Limits"
    
    # input list:   define order when plotting
    # legend order: define order in legend
    
    #input_list = ["CMS_Preliminary", "CMS_0L", "ATLAS_0L", "ATLAS_1L", "CMS_2L_3L"]
    #legend_order = [2, 3, 1, 4, 0]
    
    input_list = ["ATLAS_0L", "ATLAS_1L", "CMS_0L", "CMS_2L_3L", "CMS_Preliminary", "CMS_Preliminary_Up", "CMS_Preliminary_Down"]
    legend_order = [0, 1, 2, 3, 4, 5, 6]
    
    #ku_susy_base_name = "T2tt_contour_2022_11_08_dM_exp"
    ku_susy_base_name = "T2tt_contour_2022_11_24_dM_exp"
    
    # T2ttC
    inputs                                          = {}
    inputs["ATLAS_0L"]                              = {}
    inputs["ATLAS_0L"]["csv"]                       = "{0}/HEPData-ins1793461-v2-stop_obs.csv".format(data_dir)
    inputs["ATLAS_0L"]["label"]                     = "ATLAS: Eur. Phys. J. C 80, 737 (2020)"
    inputs["ATLAS_0L"]["color"]                     = getColor(1)
    inputs["ATLAS_0L"]["line_style"]                = "-"
    inputs["ATLAS_0L"]["alpha_line"]                = 0.0
    inputs["ATLAS_0L"]["alpha_fill"]                = 0.5
    inputs["ATLAS_0L"]["isDMvsM"]                   = False
    inputs["ATLAS_0L"]["fillDown"]                  = False
    inputs["ATLAS_0L"]["fillLeft"]                  = False
    inputs["ATLAS_0L"]["smooth"]                    = 0
    inputs["ATLAS_1L"]                              = {}
    inputs["ATLAS_1L"]["csv"]                       = "{0}/ATLAS_1L_T2ttC_Observed_Limit_DMvsM_v1p1.csv".format(data_dir)
    inputs["ATLAS_1L"]["label"]                     = "ATLAS: J. High Energ. Phys. 2021, 174 (2021)"
    inputs["ATLAS_1L"]["color"]                     = getColor(2)
    inputs["ATLAS_1L"]["line_style"]                = "-"
    inputs["ATLAS_1L"]["alpha_line"]                = 0.0
    inputs["ATLAS_1L"]["alpha_fill"]                = 0.5
    inputs["ATLAS_1L"]["isDMvsM"]                   = True
    inputs["ATLAS_1L"]["fillDown"]                  = False
    inputs["ATLAS_1L"]["fillLeft"]                  = False
    inputs["ATLAS_1L"]["smooth"]                    = 0
    inputs["CMS_0L"]                                = {}
    inputs["CMS_0L"]["csv"]                         = "{0}/HEPData-ins1849522-v1-Figure_09-a_Observed_Lines_v1p1.csv".format(data_dir)
    inputs["CMS_0L"]["label"]                       = "CMS: Phys. Rev. D 104, 052001 (2021)"
    inputs["CMS_0L"]["color"]                       = getColor(5)
    inputs["CMS_0L"]["line_style"]                  = "-"
    inputs["CMS_0L"]["alpha_line"]                  = 0.0
    inputs["CMS_0L"]["alpha_fill"]                  = 0.5
    inputs["CMS_0L"]["isDMvsM"]                     = True
    inputs["CMS_0L"]["fillDown"]                    = True
    inputs["CMS_0L"]["fillLeft"]                    = True
    inputs["CMS_0L"]["smooth"]                      = 0
    inputs["CMS_2L_3L"]                             = {}
    inputs["CMS_2L_3L"]["csv"]                      = "{0}/CMS_2L_3L_T2ttC_Observed_Limit_DMvsM_v1p1.csv".format(data_dir)
    inputs["CMS_2L_3L"]["label"]                    = "CMS: J. High Energ. Phys. 2022, 91 (2022)"
    inputs["CMS_2L_3L"]["color"]                    = getColor(4)
    inputs["CMS_2L_3L"]["line_style"]               = "-"
    inputs["CMS_2L_3L"]["alpha_line"]               = 0.0
    inputs["CMS_2L_3L"]["alpha_fill"]               = 0.5
    inputs["CMS_2L_3L"]["isDMvsM"]                  = True
    inputs["CMS_2L_3L"]["fillDown"]                 = False
    inputs["CMS_2L_3L"]["fillLeft"]                 = False
    inputs["CMS_2L_3L"]["smooth"]                   = 0
    inputs["CMS_Preliminary"]                       = {}
    #inputs["CMS_Preliminary"]["csv"]                = "{0}/KU_SUSY_T2ttC_Expected_Limit_DMvsM_v1p1.csv".format(data_dir)
    inputs["CMS_Preliminary"]["csv"]                = "{0}/{1}_central.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary"]["label"]              = "CMS Preliminary (Expected)"
    inputs["CMS_Preliminary"]["color"]              = getColor(3)
    inputs["CMS_Preliminary"]["line_style"]         = "-"
    inputs["CMS_Preliminary"]["alpha_line"]         = 1.0
    inputs["CMS_Preliminary"]["alpha_fill"]         = 0.5
    inputs["CMS_Preliminary"]["isDMvsM"]            = True
    inputs["CMS_Preliminary"]["fillDown"]           = True
    inputs["CMS_Preliminary"]["fillLeft"]           = False
    inputs["CMS_Preliminary"]["smooth"]             = 0
    inputs["CMS_Preliminary_Up"]                    = {}
    inputs["CMS_Preliminary_Up"]["csv"]             = "{0}/{1}_up.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary_Up"]["label"]           = "CMS Preliminary (Expected Up)"
    inputs["CMS_Preliminary_Up"]["color"]           = getColor(3)
    inputs["CMS_Preliminary_Up"]["line_style"]      = "--"
    inputs["CMS_Preliminary_Up"]["alpha_line"]      = 1.0
    inputs["CMS_Preliminary_Up"]["alpha_fill"]      = 0.0
    inputs["CMS_Preliminary_Up"]["isDMvsM"]         = True
    inputs["CMS_Preliminary_Up"]["fillDown"]        = True
    inputs["CMS_Preliminary_Up"]["fillLeft"]        = False
    inputs["CMS_Preliminary_Up"]["smooth"]          = 0
    inputs["CMS_Preliminary_Down"]                  = {}
    inputs["CMS_Preliminary_Down"]["csv"]           = "{0}/{1}_down.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary_Down"]["label"]         = "CMS Preliminary (Expected Down)"
    inputs["CMS_Preliminary_Down"]["color"]         = getColor(3)
    inputs["CMS_Preliminary_Down"]["line_style"]    = "--"
    inputs["CMS_Preliminary_Down"]["alpha_line"]    = 1.0
    inputs["CMS_Preliminary_Down"]["alpha_fill"]    = 0.0
    inputs["CMS_Preliminary_Down"]["isDMvsM"]       = True
    inputs["CMS_Preliminary_Down"]["fillDown"]      = True
    inputs["CMS_Preliminary_Down"]["fillLeft"]      = False
    inputs["CMS_Preliminary_Down"]["smooth"]        = 0
    
    info = {}
    info["title"]               = "T2ttC Limits"
    info["proc_label"]          = r"$p p \to \tilde{t} \bar{\tilde{t}}$; $\tilde{t} \to b f \bar{f}' \tilde{\chi}_{1}^{0}$"
    info["x_label"]             = r"$m \left(\tilde{t}\right)$ [GeV]" 
    info["y_label"]             = r"$\Delta m \left(\tilde{t}, \tilde{\chi}_{1}^{0}\right)$ [GeV]"
    info["proc_label_x_pos"]    = 0.00  # process label x position as fraction in range [0.0, 1.0]
    info["proc_label_y_pos"]    = 1.02  # process label y position as fraction in range [0.0, 1.0]
    info["x_lim"]               = [300.0, 900.0]
    info["y_lim"]               = [10.001, 80.0]
    info["legend_loc"]          = "upper left"
    info["legend_order"]        = legend_order
    
    #info["x_lim"]   = [200.0, 800.0]
    #info["y_lim"]   = [10.0,  210.0]
    
    #info["x_lim"]   = [300.0, 800.0]
    #info["y_lim"]   = [0.0,   250.0]
    
    #info["x_lim"]   = [0.0, 1000.0]
    #info["y_lim"]   = [0.0, 300.0]
    
    preparePlot(plot_dir, plot_name, input_list, inputs, info)

# Create plot for Higgsino
def makePlotHiggsino():
    data_dir    = "data/Higgsino"
    plot_dir    = "plots"
    plot_name   = "Higgsino_Limits"
    
    # input list:   define order when plotting
    # legend order: define order in legend
    
    input_list = ["CMS_2L_3L", "CMS_Preliminary", "CMS_Preliminary_Up", "CMS_Preliminary_Down"]
    legend_order = [0, 1, 2, 3]
    
    # TODO: Update KU SUSY results: use Higgsino limits instead of TChiWZ limits
    ku_susy_dir       = "data/TChiWZ"
    #ku_susy_base_name = "TChiWZ_contour_2022_11_08_dM_exp"
    ku_susy_base_name = "TChiWZ_contour_2022_11_24_dM_exp"
    
    # Higgsino
    inputs                                          = {}
    inputs["CMS_2L_3L"]                             = {}
    inputs["CMS_2L_3L"]["csv"]                      = "{0}/CMS_2L_3L_Higgsino_Observed_Limit_DMvsM_v1p1.csv".format(data_dir)
    inputs["CMS_2L_3L"]["label"]                    = "CMS: J. High Energ. Phys. 2022, 91 (2022)"
    inputs["CMS_2L_3L"]["color"]                    = getColor(4)
    inputs["CMS_2L_3L"]["line_style"]               = "-"
    inputs["CMS_2L_3L"]["alpha_line"]               = 0.0
    inputs["CMS_2L_3L"]["alpha_fill"]               = 0.5
    inputs["CMS_2L_3L"]["isDMvsM"]                  = True
    inputs["CMS_2L_3L"]["fillDown"]                 = True
    inputs["CMS_2L_3L"]["fillLeft"]                 = False
    inputs["CMS_2L_3L"]["smooth"]                   = 0
    inputs["CMS_Preliminary"]                       = {}
    #inputs["CMS_Preliminary"]["csv"]                = "{0}/KU_SUSY_TChiWZ_Expected_Limit_DMvsM_v1p1.csv".format(data_dir)
    #inputs["CMS_Preliminary"]["csv"]                = "{0}/{1}_central.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary"]["csv"]                = "{0}/{1}_central.csv".format(ku_susy_dir, ku_susy_base_name)
    inputs["CMS_Preliminary"]["label"]              = "CMS Preliminary (Expected)"
    inputs["CMS_Preliminary"]["color"]              = getColor(3)
    inputs["CMS_Preliminary"]["line_style"]         = "-"
    inputs["CMS_Preliminary"]["alpha_line"]         = 1.0
    inputs["CMS_Preliminary"]["alpha_fill"]         = 0.5
    inputs["CMS_Preliminary"]["isDMvsM"]            = True
    inputs["CMS_Preliminary"]["fillDown"]           = True
    inputs["CMS_Preliminary"]["fillLeft"]           = False
    inputs["CMS_Preliminary"]["smooth"]             = 0
    inputs["CMS_Preliminary_Up"]                    = {}
    #inputs["CMS_Preliminary_Up"]["csv"]             = "{0}/{1}_up.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary_Up"]["csv"]             = "{0}/{1}_up.csv".format(ku_susy_dir, ku_susy_base_name)
    inputs["CMS_Preliminary_Up"]["label"]           = "CMS Preliminary (Expected Up)"
    inputs["CMS_Preliminary_Up"]["color"]           = getColor(3)
    inputs["CMS_Preliminary_Up"]["line_style"]      = "--"
    inputs["CMS_Preliminary_Up"]["alpha_line"]      = 1.0
    inputs["CMS_Preliminary_Up"]["alpha_fill"]      = 0.0
    inputs["CMS_Preliminary_Up"]["isDMvsM"]         = True
    inputs["CMS_Preliminary_Up"]["fillDown"]        = True
    inputs["CMS_Preliminary_Up"]["fillLeft"]        = False
    inputs["CMS_Preliminary_Up"]["smooth"]          = 0
    inputs["CMS_Preliminary_Down"]                  = {}
    #inputs["CMS_Preliminary_Down"]["csv"]           = "{0}/{1}_down.csv".format(data_dir, ku_susy_base_name)
    inputs["CMS_Preliminary_Down"]["csv"]           = "{0}/{1}_down.csv".format(ku_susy_dir, ku_susy_base_name)
    inputs["CMS_Preliminary_Down"]["label"]         = "CMS Preliminary (Expected Down)"
    inputs["CMS_Preliminary_Down"]["color"]         = getColor(3)
    inputs["CMS_Preliminary_Down"]["line_style"]    = "--"
    inputs["CMS_Preliminary_Down"]["alpha_line"]    = 1.0
    inputs["CMS_Preliminary_Down"]["alpha_fill"]    = 0.0
    inputs["CMS_Preliminary_Down"]["isDMvsM"]       = True
    inputs["CMS_Preliminary_Down"]["fillDown"]      = True
    inputs["CMS_Preliminary_Down"]["fillLeft"]      = False
    inputs["CMS_Preliminary_Down"]["smooth"]        = 0
    
    info = {}
    info["title"]               = "Higgsino Limits"
    info["proc_label"]          = r"$p p \to \tilde{\chi}_{2}^{0} \tilde{\chi}_{1}^{\pm}, \tilde{\chi}_{2}^{0} \tilde{\chi}_{2}^{0}$, $m \left(\tilde{\chi}_{1}^{\pm}\right) = \left(m \left(\tilde{\chi}_{2}^{0}\right) + m \left(\tilde{\chi}_{1}^{0}\right)\right) / 2$"
    info["x_label"]             = r"$m \left(\tilde{\chi}_{2}^{0}\right)$ [GeV]" 
    info["y_label"]             = r"$\Delta m \left(\tilde{\chi}_{2}^{0}, \tilde{\chi}_{1}^{0}\right)$ [GeV]"
    info["proc_label_x_pos"]    = 0.00  # process label x position as fraction in range [0.0, 1.0]
    info["proc_label_y_pos"]    = 1.02  # process label y position as fraction in range [0.0, 1.0]
    info["x_lim"]               = [120.0, 400.0]
    info["y_lim"]               = [3.0,   50.0]
    info["legend_loc"]          = "upper left"
    info["legend_order"]        = legend_order
    
    preparePlot(plot_dir, plot_name, input_list, inputs, info)

def main():
    makePlotTSlepSlep()
    makePlotTChiWZ()
    makePlotT2ttC()
    makePlotHiggsino()

if __name__ == "__main__":
    main()

