# makePlots.py

import matplotlib.pyplot as plt
import tools

def plot(plot_dir, plot_name, inputs, info):
    output_name = "{0}/{1}.pdf".format(plot_dir, plot_name)
    
    title   = info["title"]
    x_label = info["x_label"]
    y_label = info["y_label"]

    fig, ax = plt.subplots(figsize=(6, 6))
    
    for key in inputs:
        label   = key.replace('_', ' ')
        data    = inputs[key]["data"]
        color   = inputs[key]["color"]
        x_vals, y_vals = tools.getXYVals(data)
        plt.plot(x_vals, y_vals, label=label, color=color)
    
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.savefig(output_name)

def makePlots():
    print("Yeah baby, let's go!")
    plot_dir    = "plots"
    plot_name   = "TSlepSlep_Limits"
    
    # TSlepSlep
    inputs = {}
    inputs["ATLAS_Soft_2l"] = {}
    inputs["ATLAS_Soft_2l"]["csv"]      = "data/HEPData-ins1767649-v5-Figure_16a_Observed.csv"
    inputs["ATLAS_Soft_2l"]["color"]    = "xkcd:cherry red"

    info = {}
    info["title"]   = "TSlepSlep Limits"
    info["x_label"] = "X"
    info["y_label"] = "Y"
    
    # load data from csv file
    for key in inputs:
        inputs[key]["data"] = tools.getData(inputs[key]["csv"]) 
        inputs[key]["data"] = tools.getCleanData(inputs[key]["data"])
    
    tools.makeDir(plot_dir)
    plot(plot_dir, plot_name, inputs, info)

def main():
    makePlots()

if __name__ == "__main__":
    main()

