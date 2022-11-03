# makePlots.py

import matplotlib.pyplot as plt
import tools

def plot(plot_dir, plot_name, inputs):
    for key in inputs:
        data = inputs[key]["data"]
        x_vals, y_vals = tools.getXYVals(data)
        plt.plot(x_vals, y_vals)
    output_name = "{0}/{1}.pdf".format(plot_dir, plot_name)
    plt.savefig(output_name)

def makePlots():
    print("Yeah baby, let's go!")
    plot_dir    = "plots"
    plot_name   = "TSlepSlep_Run2"
    
    inputs = {}
    inputs["ATLAS_TSlepSlep_Soft2l"] = {}
    inputs["ATLAS_TSlepSlep_Soft2l"]["csv"] = "data/HEPData-ins1767649-v5-Figure_16a_Observed.csv"
    
    for key in inputs:
        inputs[key]["data"] = tools.getData(inputs[key]["csv"]) 
        inputs[key]["data"] = tools.getCleanData(inputs[key]["data"])
    
    tools.makeDir(plot_dir)
    plot(plot_dir, plot_name, inputs)

def main():
    makePlots()

if __name__ == "__main__":
    main()

