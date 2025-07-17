import ROOT
import os
import array
import cmsstyle as CMS
import argparse
import numpy as np

def plot(plot_mode="both", max_files=1, var_index="all", log_scale=False, output_dir="plot_images_1", x_min=None, x_max=None):
    
    CMS.setCMSStyle()
    ROOT.gROOT.SetBatch(True) #to process multiple xrootd files

    #make a TChain to wrap the events from each file, then add those events
    events = ROOT.TChain("ntupliser/Events")
    for i in range(1, max_files + 1):
        path = f"root://cms-xrd-global.cern.ch//store/user/asahasra/EE_Par-FlatPt-1To300_PGun/Run3Scouting_Winter25_crabNano250704/250704_123742/0000/egScoutingP4_regress_train_{i}.root"
        events.Add(path)

    #go through the variables from the events and collect the list of the variables we need
    nevents = events.GetEntries()
    variables = events.GetListOfBranches()
    variable_names = []
    for i in range(variables.GetEntries()):
        variable = variables.At(i)
        name = variable.GetName()
        cname = variable.GetClassName()
        nleaves = variable.GetNleaves()

        #we don't need gen_pt, c_edep is an array, and we don't need vectors
        if name in ("gen_pt", "c_edep"):
            print(f"skipping variable {name}")
            continue
        if (cname and "vector" in cname) or (nleaves != 1):
            print(f"skipping variable {name}")
            continue

        variable_names.append(name)

    if var_index == "all":
        selected_vars = variable_names[:48]  #either all of them
    else:
        v_index = int(var_index) #or find the one that we need
        selected_vars = [variable_names[v_index - 1]]

    #every key in hold will be a variable name (pt, eta, etc) and every value will hold the data for that variable every event
    hold = {}
    for name in selected_vars:
        h = array.array('f', [0.0])
        hold[name] = h #one element array which will hold the value of the variable for each event
        #for each variable branch, when calling GetEntry(i), put the data for event i into the holding spot hold[name]
        events.SetBranchAddress(name, hold[name])

    gen_pt_h = array.array('f', [0.0])
    #for each gen_pt branch, when calling GetEntry(i), put the data for event i into the holding spot gen_pt_h
    events.SetBranchAddress("gen_pt", gen_pt_h)

    var_vector = {name: np.zeros(nevents, dtype=np.float32) for name in selected_vars}
    is_neg = np.zeros(nevents, dtype=bool)

    #for each event
    for i in range(nevents):

        events.GetEntry(i)
        #classify the electron as real or fake
        is_neg[i] = (gen_pt_h[0] == -50)
        for name in selected_vars:
            #add the value of that variable for this event into the variable vector
            var_vector[name][i] = hold[name][0]

        if i % 10000 == 0:
            print(f"loaded {i} entries")

    os.makedirs(output_dir, exist_ok=True)

    for name, values in var_vector.items():
        #find the minimum and maximum element of each value vector to set histogram bounds, then make histograms
        #or use inputed values
        min_val = float(x_min) if x_min is not None else float(min(values))
        print(min_val)
        max_val = float(x_max) if x_max is not None else float(max(values))
        print(max_val)
        if min_val == max_val:
            max_val = min_val + 1.0  # avoid hist range zero width
        scaled = (x_min is not None or x_max is not None)

        hneg = ROOT.TH1F(f"{name}_neg", f"{name} (gen_pt == -50)", 100, min_val, max_val)
        hpos = ROOT.TH1F(f"{name}_pos", f"{name} (gen_pt != -50)", 100, min_val, max_val)

        #fill values depending on if it's fake or not
        for i, v in enumerate(values):
            if is_neg[i]:
                hneg.Fill(v)
            else:
                hpos.Fill(v)

        #set bounds based on type of plot
        ymin = 0.1 if log_scale else 0.0

        if plot_mode == "neg":
            ymax = 1.2 * hneg.GetMaximum() if not log_scale else 10**(int(ROOT.TMath.Log10(hneg.GetMaximum())) + 1)
        elif plot_mode == "pos":
            ymax = 1.2 * hpos.GetMaximum() if not log_scale else 10**(int(ROOT.TMath.Log10(hpos.GetMaximum())) + 1)
        else:  # both
            maxmax = max(hneg.GetMaximum(), hpos.GetMaximum())
            ymax = 1.2 * maxmax if not log_scale else 10**(int(ROOT.TMath.Log10(maxmax)) + 1)

        yaxis_title = "Events/bin (log scale)" if log_scale else "Events/bin"

        #pretty plot stuff
        CMS.SetExtraText("Simulation Preliminary")
        CMS.SetLumi(None, run=None)
        CMS.SetEnergy(13.6)

        #make a plot of just the fake electrons
        if plot_mode == "neg":

            c = CMS.cmsCanvas("neg", min_val * 1.2, max_val * 1.2, ymin, ymax, name, yaxis_title, square=False, extraSpace=0.05, iPos=0)

            hneg.SetLineColor(ROOT.kRed)
            hneg.SetLineWidth(2)
            hneg.SetMarkerStyle(0)
            hneg.SetMarkerColor(ROOT.kRed)
            hneg.SetMinimum(ymin)

            c.SetLogy(1 if log_scale else 0)

            CMS.cmsObjectDraw(hneg, "HIST")

            frame = CMS.GetCmsCanvasHist(c)
            frame.GetYaxis().SetMaxDigits(2)
            ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
            frame.GetYaxis().SetTitleOffset(1)

            legend = CMS.cmsLeg(0.75, 0.75, 0.9, 0.9, textSize=0.03)
            CMS.addToLegend(legend, (hneg, "Fake electrons", "lp"))
            legend.Draw()

            suffix = "_log" if log_scale else ""
            scale_suffix = "_scaled" if scaled else ""
            c.SaveAs(f"{output_dir}/hist_{name}{scale_suffix}{suffix}.png")

        #make a plot of real electrons
        elif plot_mode == "pos":
            c = CMS.cmsCanvas("pos", min_val * 1.2, max_val * 1.2, ymin, ymax, name, yaxis_title, square=False, extraSpace=0.05, iPos=0)

            hpos.SetLineColor(ROOT.kBlue)
            hpos.SetLineWidth(2)
            hpos.SetMarkerStyle(0)
            hpos.SetMarkerColor(ROOT.kBlue)
            hpos.SetMinimum(ymin)

            c.SetLogy(1 if log_scale else 0)

            CMS.cmsObjectDraw(hpos, "HIST")

            frame = CMS.GetCmsCanvasHist(c)
            frame.GetYaxis().SetMaxDigits(2)
            ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
            frame.GetYaxis().SetTitleOffset(1)

            legend = CMS.cmsLeg(0.75, 0.75, 0.9, 0.9, textSize=0.03)
            CMS.addToLegend(legend, (hpos, "Real electrons", "lp"))
            legend.Draw()

            suffix = "_log" if log_scale else ""
            scale_suffix = "_scaled" if scaled else ""
            c.SaveAs(f"{output_dir}/hist_{name}{scale_suffix}{suffix}.png")

        else:  # both
            c = CMS.cmsCanvas("both", min_val * 1.2, max_val * 1.2, ymin, ymax, name, yaxis_title, square=False, extraSpace=0.05, iPos=0)

            hneg.SetLineColor(ROOT.kRed)
            hneg.SetLineWidth(2)
            hneg.SetMarkerStyle(0)
            hneg.SetMarkerColor(ROOT.kRed)
            hneg.SetMinimum(ymin)

            hpos.SetLineColor(ROOT.kBlue)
            hpos.SetLineWidth(2)
            hpos.SetMarkerStyle(0)
            hpos.SetMarkerColor(ROOT.kBlue)
            hpos.SetMinimum(ymin)

            c.SetLogy(1 if log_scale else 0)

            CMS.cmsObjectDraw(hneg, "HIST")
            CMS.cmsObjectDraw(hpos, "HIST SAME")

            frame = CMS.GetCmsCanvasHist(c)
            frame.GetYaxis().SetMaxDigits(2)
            ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
            frame.GetYaxis().SetTitleOffset(1)

            legend = CMS.cmsLeg(0.75, 0.75, 0.9, 0.9, textSize=0.03)
            CMS.addToLegend(legend, (hneg, "Fake electrons", "lp"))
            CMS.addToLegend(legend, (hpos, "Real electrons", "lp"))
            legend.Draw()

            suffix = "_log" if log_scale else ""
            scale_suffix = "_scaled" if scaled else ""
            c.SaveAs(f"{output_dir}/hist_{name}{scale_suffix}{suffix}.png")

        del hneg
        del hpos
        del c

    del events
    print("Plotting complete.")


if __name__ == "__main__":

    #all possible arguments
    parser = argparse.ArgumentParser(description="Plot histograms for electrons")
    parser.add_argument("--plotmode", choices=["neg", "pos", "both"], default="both",
                        help="Choose which histogram(s) to plot: neg, pos, or both (default: both)")
    parser.add_argument("--maxfiles", type=int, default=1,
                        help="Number of input files to load (default: 1)")
    parser.add_argument("--var", default="all",
                        help="Which variable to plot (1-48) or 'all' (default: all)")
    parser.add_argument("--log", action="store_true", default=False,
                        help="Plot y-axis on logarithmic scale")
    parser.add_argument("--output_dir", default="plot_images_1",
                    help="Output directory for saved plots (default: plot_images_1)")
    parser.add_argument("--x_min", type=float, default=None,
                    help="Minimum x-axis value (default: calculated from data)")
    parser.add_argument("--x_max", type=float, default=None,
                    help="Maximum x-axis value (default: calculated from data)")
    
    args = parser.parse_args()
    plot(plot_mode=args.plotmode, max_files=args.maxfiles, var_index=args.var, log_scale = args.log, output_dir=args.output_dir, x_min=args.x_min, x_max=args.x_max)
