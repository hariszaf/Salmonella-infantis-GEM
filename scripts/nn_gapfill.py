#!/usr/bin/env python 
"""
Aim of this script is to gapfill a draft reconstruction. 
It assumes your reconstructions are under the /results/models folder of the GitHub repo
and any media under data/media/.

Usage:
./nn_gapfill.py draft_reconstr_filename gf_reconstr_filename <optional: name_of_obj_function> <optional: media_filename>

Examples:
* complete media and default obj. function
./nn_gapfill.py S_infantis_mvl3A.sbml.modelseedpy S_infantis_gf_complMed.sbml

* with media and another obj. function
./nn_gapfill.py modelseedpy_draft_invivo_bf.sbml modelseedpy_gf_mvl3_invivo.sbml biomass_invivo mvl3A_medium.csv
"""

# Load arguments
import argparse
import os, sys

parser = argparse.ArgumentParser(
    description='Gapfill a draft reconstruction using the dnngior library',
    usage='use "%(prog)s --help" for more information',
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument(
        '-i', '--draft-reconstruction', dest='draft_reconstruction', help="Reconstruction to gapfill", required=True, type=str
    )
parser.add_argument(
        '-o', '--gapfilled-recosntruction', dest='gapfilled_reconstruction', help="Gapfilled output reconstruction", required=True, type=str
    )
parser.add_argument(
        '-m', '--media', dest='media', help="Media to gapfill based on", required=False, type=str, default=None
    )
parser.add_argument(
        '-z', '--objective-function', dest='objective_function', help="Objective function to gapfill based on", required=False, type=str, default="bio1"
    )

args = parser.parse_args()

# Import libraries
import dnngior
import cobra


# Init the logfile
if os.path.exists("reactions_added.txt"):
    logfile    = open("reactions_added.txt", "a")
else:
    logfile    = open("reactions_added.txt", "w")

# Path where repo is located
base_path   = "/".join(os.path.abspath(__file__).split("/")[:-2])

# Load media if provided
if args.media is not None:

    media_file     = args.media # os.path.join(base_path, args.media)
    media = {}
    with open(media_file) as f:
        f.readline()
        for line in f:
            a = line.strip().split('\t')
            media['EX_' + a[0] + '_e0'] = {'lower_bound':-1, 'upper_bound':1, 'metabolites':{a[0]+'_e0':-1.0}}
else:
    media = None


# Gapfill
gapfill = dnngior.Gapfill(args.draft_reconstruction, medium = media, objectiveName = args.objective_function)

# Export gapfilled model
gf_model_compl_med = gapfill.gapfilledModel.copy()
gf_model_filename = os.path.join(base_path, args.gapfilled_reconstruction)
cobra.io.write_sbml_model(cobra_model = gf_model_compl_med, filename = gf_model_filename)

print("NN gapfilling added {} new readctions".format(len(gapfill.added_reactions)))
print("The NN gapfilled model, comes with {} reactions and {} metabolites".format(len(gf_model_compl_med.metabolites), len(gf_model_compl_med.reactions)))


logfile.write("Gapfill the model:" + args.draft_reconstruction.split("/")[-1] + "\n")
logfile.write("Gapfilled model:" + args.gapfilled_reconstruction.split("/")[-1] + "\n")
if args.media is None:
    logfile.write("Gapfill using a complete medium\n")
else:
    logfile.write("Gapfill using medium: " + args.media + "\n")

if args.objective_function == "bio1": 
    logfile.write("Gapfill using the default biomass function\n")
else:
    logfile.write("Gapfill using an alternative objective function: " + args.objective_function)

logfile.write("NN gapfilling added {} new readctions".format(len(gapfill.added_reactions)))


# Keep track of what was added
for reaction in gf_model_compl_med.reactions:
    if reaction.id in gapfill.added_reactions:
        logfile.write(reaction.id + "\t~~~\t" + reaction.build_reaction_string() + "\n")
        for compound in reaction.metabolites:
            logfile.write(compound.id + "\n")

        logfile.write("\n~~~~\n")


logfile.write("\n\n------------------------------------------------\n\n")

