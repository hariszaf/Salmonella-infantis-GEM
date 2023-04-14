#!/usr/bin/env python

from modelseedpy import MSBuilder, MSGenome
import cobra


genome_s_i = MSGenome.from_fasta('S_infantis.faa', split=' ')

model = MSBuilder.build_metabolic_model(model_id = "S_infantis", 
                                        genome = genome_s_i, 
                                        index= "0", 
                                        classic_biomass = True, 
                                        gapfill_model = False, 
                                        gapfill_media = None, 
                                        annotate_with_rast = True, 
                                        allow_all_non_grp_reactions = True)

modelname = "S_infantis_modelseed_init.sbml"

cobra.io.write_sbml_model(cobra_model=model, filename=modelname)




