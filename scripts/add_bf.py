#!/usr/bin/env python
import os, sys
import cobra
import pandas as pd
from dnngior.MSEED_compounds import Compounds
from dnngior.MSEED_reactions import Reactions

"""
This script replaces the default biomass function of a model with a curated one as described in the docs/biomassFromLiterature.xlsx file.

sheet_name: biomass_invivo > 1, BIOMASS_iRR1083_metals > 2

Usage
./add_bf.py in_model out_model 2

"""

if sys.argv[3] == "1":
    sheetName = "biomass_invivo"
elif sys.argv[3] == "2":
    sheetName = "BIOMASS_iRR1083_metals"


# Load the model we want to add the biomass function; that is the draft reconstruction returned by ModelSEEDpy
base_path = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])

# models_path = os.path.join(base_path, "results/models")
# model = cobra.io.read_sbml_model(os.path.join(models_path, sys.argv[1] )) # "S_infantis_md_init.sbml"
model = cobra.io.read_sbml_model(os.path.join(base_path, sys.argv[1] )) # "S_infantis_md_init.sbml"

# Load the biomass function as a dictionary with compounds as keys and stoichiometry as their values
df = pd.read_excel(os.path.join(base_path, 'docs/biomassFromLiterature.xlsx'), sheet_name = sheetName)
bf_stoichiometry = df.set_index('ModelSEED_id').to_dict()['Stoichiometry_in_ModelSEED']

# To add compounds on the model that are part of the b.f but not already on the model, use script from ModelSEED biochemistry (through the dnngior library) to parse all metabolite/reaction info
compounds_helper = Compounds()
compounds_dict = compounds_helper.loadCompounds()
compounds_helper.saveCompounds(compounds_dict)

# Add compounds that are part of the new b.f. but are not already part of the model, on the model
for compound in bf_stoichiometry.keys():
    if compound not in model.metabolites:
        compound_id, compound_compartment = compound.split("_")
        modelseed_metabolite = compounds_dict[compound_id]
        new_met = cobra.Metabolite(
                    compound,
                    name = modelseed_metabolite["name"],
                    compartment = compound_compartment
                )
        model.add_metabolites([new_met])


# Initiate a cobra.reaction object
new_biom_funct      = cobra.Reaction(sheetName)
new_biom_funct.name = sheetName 
new_biom_funct.lower_bound = 0. 
new_biom_funct.upper_bound = 1000

# Add the reaction object to the model
model.add_reaction(new_biom_funct)

# As all compounds included in the new b.f. are already added in the model (previous for loop), you can add directly the compounds to the reaction, which is also already part of the model
new_biom_funct.add_metabolites(bf_stoichiometry)

# Set the new b.f as the obj. function of the model
if sheetName == "biomass_invivo":
    model.objective = model.reactions.biomass_invivo
elif sheetName == "BIOMASS_iRR1083_metals":
    print("hello friend")
    model.objective = model.reactions.BIOMASS_iRR1083_metals

model.remove_reactions(["bio1"])

# Export the model
outfile = os.path.join(base_path, sys.argv[2])
cobra.io.write_sbml_model(model, filename = outfile)
