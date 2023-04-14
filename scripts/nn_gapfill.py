#!/usr/bin/env python 

import dnngior
import cobra
from pathlib import Path
import os, sys

logfile    = open("log", "w")

base_path  = "/".join(os.path.abspath(__file__).split("/")[:-2])
draftModel = os.path.join(base_path, 'S_infantis_mvl3A.sbml')

# CASE 1: Gapfill draft reaconstruction with complete media
# ----------------------------------------------------------

# Gapfill
gapfill            = dnngior.Gapfill(draftModel, medium = None, objectiveName = 'bio1')

# Export gapfilled model
gf_model_compl_med = gapfill.gapfilledModel.copy()
modelname = os.path.join(base_path, "S_infantis_gf_complMed.sbml")
cobra.io.write_sbml_model(cobra_model = gf_model_compl_med, filename = modelname)

print("NN gapfilling added {} new readctions".format(len(gapfill.added_reactions)))
print("The NN gapfilled model, comes with {} reactions and {} metabolites".format(len(gf_model_compl_med.metabolites), len(gf_model_compl_med.reactions)))

logfile.write("\nGapfill using a complete medium and the default biomass function\n\n")
logfile.write("NN gapfilling added {} new readctions".format(len(gapfill.added_reactions)))

# Keep track of what was added
for reaction in gf_model_compl_med.reactions:
    if reaction.id in gapfill.added_reactions:
        logfile.write(reaction.id + "\t" + reaction.build_reaction_string() + "\n")
        for compound in reaction.metabolites:
            logfile.write(compound.id + "\n")

        logfile.write("\n~~~~\n")


logfile.write("\n\n------------------------------------------------\n\n")


# CASE 2: Gapfill draft reaconstruction with mvl3A + yeast extract media and the default biomass function
# ---------------------------------------------------------------------------------------------------------

mvl3_media_file = os.path.join(base_path, 'data/media/mvl3A_medium.csv')

# Import media 
mvl3A = {}
with open(mvl3_media_file) as f:
    f.readline()
    for line in f:
        a = line.strip().split('\t')
        mvl3A['EX_' + a[0] + '_e0'] = {'lower_bound':-1, 'upper_bound':1, 'metabolites':{a[0]+'_e0':-1.0}}


# Gapfill using mvl3A with yeast extract
gapfill_mvl3A = dnngior.Gapfill(draftModel, medium = mvl3A, objectiveName = 'bio1')

# # Make a copy of the gapfilled model
gf_model_mvl3A_med = gapfill_mvl3A.gapfilledModel.copy()

# and export it to a new sbml file
modelname = os.path.join(base_path, "S_infantis_gf_mvl3A.sbml")
cobra.io.write_sbml_model(cobra_model = gf_model_mvl3A_med, filename = modelname)

print("NN gapfilling added {} new readctions".format(len(gapfill_mvl3A.added_reactions)))
print("The NN gapfilled model, comes with {} reactions and {} metabolites".format(len(gf_model_mvl3A_med.metabolites), len(gf_model_mvl3A_med.reactions)))

logfile.write("\nGapfill using the mvl3-A medium with yeast extract and the default biomass function\n\n")
logfile.write("NN gapfilling added {} new readctions".format(len(gapfill_mvl3A.added_reactions)))


# Keep track of what was added
for reaction in gf_model_mvl3A_med.reactions:
    if reaction.id in gapfill_mvl3A.added_reactions:
        logfile.write(reaction.id + "\t" + reaction.build_reaction_string() + "\n")
        for compound in reaction.metabolites:
            logfile.write(compound.id + "\n")

        logfile.write("\n~~~~\n")

