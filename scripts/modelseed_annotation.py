#!/usr/bin/env python

import dnngior
import cobra
import os 

repo_parent_path  = '/'.join(os.getcwd().split("/")[:-1])
init_model = cobra.io.read_sbml_model("../S_infantis_mvl3A.sbml")

# dnngior makes use of modelseed classes and wraps them in a more suitable way
# we can add annottations from other resources (BiGG, KEGG etc) with the following
refined_model = dnngior.build_model.refine_model(gpfilledModel = init_model, draftModel = init_model)

modelname = os.path.join(repo_parent_path, "S_infantis_mvl3A.sbml")

cobra.io.write_sbml_model(cobra_model=refined_model, filename=modelname)

