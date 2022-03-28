import mplhep as hep
import matplotlib.pyplot as plt
import seaborn as sns


#functions to square and square-root something respectively
def square(list):
    return [i ** 2 for i in list]

def sqrt(list):
    return [i ** 0.5 for i in list]


#function to plot in the ATLAS style
def atlas_plotter(data, title, xlabel, ylabel = 'Count', color = 'blue', bins = 'auto', xlim_required = False, xlim = (-10, 10), ylim_required = False, ylim = (0, 1.5), save_plot = False, binwidth = None):
    # set plot style
    plt.style.use([hep.style.ATLAS,
                   {'font.sans-serif': ['Tex Gyre Heros']},  # use when helvetica isn't installed
                   {'errorbar.capsize': 5},
                   {'axes.labelsize': 23},
                   {'axes.labelpad': 23},
    ])

    plt.figure(figsize = (10, 7))
    plt.title(title)
    plt.xlabel(xlabel)
    if xlim_required:
        plt.xlim(xlim)
    if ylim_required:
        plt.ylim(ylim)
    sns.histplot(data, bins = bins, color = color, binwidth = binwidth)

    plt.show()
    if save_plot:
        save_path = title + '.png'
        plt.savefig(save_path)



#here we are going to make the variables to feed into histos
#deltaR_lt_pos is usually going to be deltaR_lt02_pos but it's whatever you set your deltaR_lt to be 
#var is the jet collection variable that you are going for (truth pt, reco pt etc etc)
def make_truth_matched_var(deltaR_lt_pos, var):
    truth_match_var = []
    for i in range(len(deltaR_lt_pos)):
        temp = []
        try:
            for j in deltaR_lt_pos[i]:
                if deltaR_lt_pos[i] != []:
                    temp.append(var[j[0], j[1]])
                else:
                    temp.append(-99)
        except:
            temp.append(-999)

        truth_match_var.append(temp)

    return truth_match_var

#function to produce data to be plotted (essentially flattening without creating a numpy array first)
def make_plot_data(truth_matched_var):
    data = []
    for i in range(len(truth_matched_var)):
        for j in truth_matched_var[i]:
            data.append(j)
    return data


#the main functions we want to run (the rest are just side girls, baby, it's all about you)
def jet_match(tree, truth_col, reco_col, deltaR_lim = 0.2):
#set the number of jets we want to loop over 
    num_jets = 4
#define our collection strings
    tru_e = truth_col + '_e'
    tru_pt = truth_col + '_pt'
    tru_phi = truth_col + '_phi'
    tru_eta = truth_col + '_eta'

    rec_pt = reco_col + '_pt'
    rec_phi = reco_col + '_phi'
    rec_eta = reco_col + '_eta'

#make arrays from those collections
    truth_col_e = tree.array(tru_e)
    truth_col_pt = tree.array(tru_pt)
    truth_col_phi = tree.array(tru_phi)
    truth_col_eta = tree.array(tru_eta)

    reco_col_pt = tree.array(rec_pt)
    reco_col_phi = tree.array(rec_phi)
    reco_col_eta = tree.array(rec_eta)

#make the deltaR and deltaR positions arrays
    deltaR_lt = []
    deltaR_lt_pos = []
    for event in range(len(reco_col_phi)):
        temp1 = []
        temp2 = []
        try:
            for jet in range(num_jets):
                for obj in range(len(truth_col_phi[event])):
                    delta_phi = truth_col_phi[event][obj] - reco_col_phi[event][jet]
                    delta_eta = truth_col_eta[event][obj] - reco_col_eta[event][jet]
                    
                    delta_phi_sqrd = delta_phi ** 2
                    delta_eta_sqrd = delta_eta ** 2

                    deltaR_sqrd = delta_phi_sqrd + delta_eta_sqrd
                    deltaR = deltaR_sqrd ** 0.5

                    deltaR_lim = deltaR_lim
                    if deltaR <= deltaR_lim:
                        temp1.append([jet, deltaR])
                        temp2.append([jet, event, obj])
                    else:
                        continue
            deltaR_lt.append(temp1)
            deltaR_lt_pos.append(temp2)
        except:
            deltaR_lt.append([-999, -999])
            deltaR_lt_pos.append([-999, -999, -999])

#number of matched per jet graph
    #save_plot = False
    num_deltaR_lt_1 = []
    num_deltaR_lt_2 = []
    num_deltaR_lt_3 = []
    num_deltaR_lt_4 = []
    for i in range(len(deltaR_lt)):
        temp1 = 0
        temp2 = 0
        temp3 = 0
        temp4 = 0
        try:
            for j in range(len(deltaR_lt[i])):
                if deltaR_lt[i][j][0] == 0:
                    temp1+=1
                elif deltaR_lt[i][j][0] == 1:
                    temp2+=1
                elif deltaR_lt[i][j][0] == 2:
                    temp3+=1
                elif deltaR_lt[i][j][0] == 3:
                    temp4+=1
                    
            num_deltaR_lt_1.append(temp1)
            num_deltaR_lt_2.append(temp2)
            num_deltaR_lt_3.append(temp3)
            num_deltaR_lt_4.append(temp4)
        except:
            continue

    return deltaR_lt, deltaR_lt_pos, num_deltaR_lt_1, num_deltaR_lt_2, num_deltaR_lt_3, num_deltaR_lt_4
