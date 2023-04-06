#!/usr/bin/env python 

import dnngior
import cobra
from pathlib import Path
import os


base_path  = Path(os.getcwd()).parents[0]
draftModel = os.path.join(base_path, 'S_infantis_mvl3A.sbml')

gapfill            = dnngior.Gapfill(draftModel, medium = None, objectiveName = 'bio1')
gf_model_compl_med = gapfill.gapfilledModel.copy()

modelname = os.path.join(base_path, "S_infantis_mvl3A.sbml")

cobra.io.write_sbml_model(cobra_model = gf_model_compl_med, filename = modelname)


