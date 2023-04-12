#!/usr/bin/env python 

import dnngior
import cobra
from pathlib import Path
import os


base_path  = "/".join(os.path.abspath(__file__).split("/")[:-2])
draftModel = os.path.join(base_path, 'S_infantis_mvl3A.sbml')

media_file = os.path.join(base_path, 'data/media/mvl3A_medium.csv')

mvl3A = {}
with open(media_file) as f:
    f.readline()
    for line in f:
        a = line.strip().split('\t')
        mvl3A['EX_' + a[0] + '_e0'] = {'lower_bound':-1, 'upper_bound':1, 'metabolites':{a[0]+'_e0':-1.0}}

gapfill            = dnngior.Gapfill(draftModel, medium = None, objectiveName = 'bio1')
gf_model_compl_med = gapfill.gapfilledModel.copy()

modelname = os.path.join(base_path, "S_infantis_mvl3A_gf.sbml")
cobra.io.write_sbml_model(cobra_model = gf_model_compl_med, filename = modelname)

print("NN gapfilling added {} new readctions".format(len(gapfill.added_reactions)))
print("The NN gapfilled model, comes with {} reactions and {} metabolites".format(len(gf_model_compl_med.metabolites), len(gf_model_compl_med.reactions)))
