#!/usr/bin/env python
"""
Generate draft reconstruction using the RAST annotated genome and modelseedpy. 
No gap-filling is perfrormed. 
The default gram-positive or gram-negative biomass function is used. 

Usage:
./gem_recon_modelseed.py data/gem_steps_ouput/S_infantis.faa Salmonella_infantis_MRS_16_01939 s_infantis_md_basebf_no_gf.sbml

Notes
Remember that "SId does not include Unicode character codes; the identifiers are plain text." meaning you cannot use characters such as "/", "-" in the model id
"""
import os, sys
from modelseedpy import MSBuilder, MSGenome
import cobra

repo_basepath = "/".join( os.path.dirname(os.path.abspath(__file__)) .split("/")[:-1])
genome_annotation = os.path.join(repo_basepath, sys.argv[1])
modelId = sys.argv[2]


msGenome = MSGenome.from_fasta(genome_annotation, split=' ')

model = MSBuilder.build_metabolic_model(model_id = modelId, 
                                        genome = msGenome, 
                                        index= "0", 
                                        classic_biomass = True, 
                                        gapfill_model = False, 
                                        gapfill_media = None, 
                                        annotate_with_rast = True, 
                                        allow_all_non_grp_reactions = True)

modelname = os.path.join(repo_basepath, "results/models/", sys.argv[3])

print("~~~~")
print(model.id)
print("~~~")
cobra.io.write_sbml_model(cobra_model = model, filename = modelname)

