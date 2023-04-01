[![memote tested](https://img.shields.io/badge/memote-tested-blue.svg?style=plastic)](https://hariszaf.github.io/Salmonella-infantis-GEM)

# Salmonella-infantis-GEM

## Overall notes regarding `memote` and  CI-CD 

- The `build` will fail if the model stays the exact same. Thus, `merge` if and only if the `.sbml` file has changes. 


## Dependencies 

For the annotation: 
- `RASTtk`


For visualization: 
- `pafr` R libray

For alignment: 
- `minimap2`

For GEM reconstruction:

- `memote` 
- `modelseedpy` 
- `cobrapy`

KBase can be used to skip parts of CLI. 


## Regarding the assembly to be used 

We are using the publically available genome of the MRS-16/01939 strain of *S. infantis** [GCF_019918175.1](`https://www.ncbi.nlm.nih.gov/assembly/GCF_019918175.1/`).
Our strain carries a pESI-like plasmid. The sequence of the plasmid is also publically available ([CP047882](https://www.ncbi.nlm.nih.gov/nuccore/CP047882.1)).
The same strain can be also found without the plasmid; its genome is also available ([GCF_019918165.1](https://www.ncbi.nlm.nih.gov/assembly/GCF_019918165.1/))

Let's have a look at the lengths of the contigs present:

![contigs_lengths](docs/figures/contigs_lengths.png)

with NZ_JAHFWD010000014.1 being the longest contig. 


Using `minimap2` we first mapped the plasmid sequence (query; 1 sequence) against the contigs of the assembly (query; 202 contigs), as ideally the plasmid sequence should be part of one or two contigs: 

```bash
minimap2 CP047882.1_plasmid_s_i.fasta GCF_019918175.1_ASM1991817v1_genomic.fna > alignment.paf
```

By running the following chunk of code in R we get the figure below.

```R
library(pafr)
ali <- read_paf("alignment.paf")
# Drop low-quality, short or otherwise non-ideal alignments
prim_alignment <- filter_secondary_alignments(ali)

# order_by : 
# - 'Size': lines up query and target sequences from largest to smallest. 
# - 'qstart': keeps the query sequences ordered by size, but rearranges the targets by where they match to query sequences
# -  'provided', you need to provide a list to the function with two elements: the order of the query, and then target, sequences.

dotplot(prim_alignment, label_seqs=TRUE)
```

Apparently, only about the half of the plasmid seems to be present in our strain.

![minimap](docs/figures/plasmid_agains_contigs.png)


If we go the other way around and we map the contigs against the plasmid, we can extract the sequences from the contigs, mapping to plasmid sequences. 

![minimap_plasmid_as_target](docs/figures/contigs_against_plasmid.png)

Contigs on my assembly including plasmid parts as they appear on the plasmid sequence:

|  contig id         | length | start | end | 
|:------------------:|:------:|:-----|:----:|
| NZ_JAHFWD010000047.1* | 9,988  | 1 | 9,988 | 
| NZ_JAHFWD010000146.1  | 1,102  | 9,969 | 11,062 | 
| NZ_JAHFWD010000008.1  | 67,372 | 11,054 | 78,415| 
| NZ_JAHFWD010000033.1  |   544  | 78,189 |  78,721 |
| NZ_JAHFWD010000034.1  | 30,482 | 79,193 | 109,751 |
| NZ_JAHFWD010000013.1  | 32,217 | 109,738 | 141,946 |
| NZ_JAHFWD010000078.1  |  2,566 | 143,014 | 145,573 |
| NZ_JAHFWD010000097.1  | 10,374 | 145,563 |  155,930 |
| NZ_JAHFWD010000093.1  |  2,041 | 156,236 | 158,183 |
| NZ_JAHFWD010000168.1  |   283  | 158,168 | 158,440 |
| NZ_JAHFWD010000145.1  |   559  | 160,032 | 160,576 |
| NZ_JAHFWD010000166.1  |   584  | 179,196 | 179,762 |
| NZ_JAHFWD010000128.1  |   587  | 183,100 | 183,670 |
| NZ_JAHFWD010000154.1  |   553  | 196,005 | 196,543 |
| NZ_JAHFWD010000077.1  |  246   | 230,216 | 230,449 |
| NZ_JAHFWD010000073.1  |   264  | 230,460 | 230,711 |
| NZ_JAHFWD010000156.1  |    232 | 234,020 | 234,246 | 
| NZ_JAHFWD010000164.1  |   284  | 234,383 | 234,653 |
| NZ_JAHFWD010000179.1  |   269  | 240,692 | 240,954 |
| NZ_JAHFWD010000171.1  |   393  | 244,441 | 244,794 |
| NZ_JAHFWD010000163.1  |   396  | 245,521 | 245,914 |
| NZ_JAHFWD010000186.1  |   318  | 246,226 | 246,529 |
| NZ_JAHFWD010000172.1  |   540  | 248,300 | 248,819 |
| NZ_JAHFWD010000135.1  |   426  | 249,506 | 249,922 |
| NZ_JAHFWD010000120.1  |  2,232 | 257,464 | 259,683 |
| NZ_JAHFWD010000174.1  |   415  | 263,641 | 263,990 |
| NZ_JAHFWD010000047.1* | 14,305 | 270,727 | 285,075 | 


\* half of the contig matches in the start and the other half in the end of the plasmid |


Using the [Bakta](https://bakta.computational.bio) platform, we annotated the plasmid sequence (see [`s_infantis_plasmid_annotation.xlsx`](docs/s_infantis_plasmid_annotation.xlsx))
Comparing the coordinates we get which genes are present in the plasmid of our strain.



## GEM reconstuction steps 

1. RAST-annotate your assembly. One can go for that in the following ways: 
   - GUI approach: through [KBase](https://www.kbase.us) and more specifically by running the [`
Annotate Microbial Assembly with RASTtk - v1.073`](https://narrative.kbase.us/#appcatalog/app/RAST_SDK/annotate_contigset/release) tool.
   - CLI approach: using RASTtk which now is part of the Bacterial and Viral Bioinformatics Resource Center ([BV-BRC](https://www.bv-brc.org/docs/overview.html)) - [tutorial](https://www.bv-brc.org/docs/cli_tutorial/rasttk_getting_started.html). Also, [here](https://github.com/TheSEED/RASTtk-Distribution/releases/).

In our case, we used the second approach and we ran the [`rast_annotate.sh`](scripts/) script.

2. Use `ModelSeedPy` to get a draft reconstruction. **Attention:** no medium, no gapfilling is used at this step. The classic biomass is used! 

Apparently, no boundary reactions are included in this model. 

-------

## Note on metabolic models reconstructions and the SBML format

Glossary as presented in [Thiele and Palsson (2010)](https://doi.org/10.1038/nprot.2009.203):

- **Biochemical, Genetic and Genomic (BiGG) knowledge base** – A BiGG knowledge base is a genome-scale reconstruction, which incorporates in a structured manner genomic, proteomic, biochemical and physiological information of a particular organism or cell. 

- **Biomass reaction** – The biomass reaction lumps all known biomass precursors and their fractional distribution to a cell into one network reaction. 

- **Blocked reactions** – Network reactions that cannot carry any flux in any simulation condition are called blocked reactions. Generally, these blocked reactions are caused by missing links in the network. 

- **Dead-end metabolite** - A dead-end metabolite that is only produced or consumed in the network.

- **Demand reaction** – When the consumption reaction(s) of a metabolite is not known or outside the scope of the reconstruction it can be represented by this unbalanced, intracellular reaction (e.g., 1 A `-->`). 

- **Exchange reactions** - These reactions are unbalanced, extra-organism reactions that represent the supply to or removal of metabolites from the extra-organism “space”. (See Box 3). 

- **Extreme pathways (ExPa’s)**– ExPa’s are a unique and minimal set of flux vectors which lie at the edges of the bounded null space. 
Biochemically meaningful steady-state solutions can be obtained by nonnegative linear combination of ExPa’s. 

- **Futile cycles** – Stoichiometrically unbalanced cycles, which are associated with energy consumption. 

- **Gene-protein-reaction (GPR) association** – GPR association connect genes, proteins and reactions in a logical relationship (AND, OR). 

- **Genome-scale model (GEM)** – A GEM is derived from a GENRE, by converting it into a mathematical form (i.e., an in silico model) and by assessing computationally its phenotypic properties. 

- **Genome-scale network reconstruction (GENRE)** – A GENRE formed based on an organism-specific BiGG knowledge base. A GENRE is a collection biochemical transformation derived from the genome annotation and the bibliome of the target organism. A network GENRE is unique to an organism, as its genome is. 

<!-- - **Flux variability analysis (FVA)** – FVA is a frequently used computational tool for investigating more global capabilities under a given simulation condition (e.g., network redundancy). Therefore, every network reaction will be chosen as an objective function and the minimal and maximal possible flux value through the reaction is determined by minimizing and maximizing the objective function.  -->

- **Network gap** – A network gap is a missing reaction or function in the network, which can connect one or more dead-end metabolites with the remainder of the network. 

- **Objective function** – An objective function is a network reaction, or a linear combination of network reactions, for which is optimized in the linear programming problem. 

- **Sink reaction** – When the synthesis reaction(s) of a metabolite is not known or outside the scope of the reconstruction its discharge can be represented by this unbalanced, intracellular reaction (e.g., 1 A <-->) 

- **Reduced cost** - A parameter associated with linear programming. It can be used to investigate properties associated with the calculated optimal solution. Each network reaction has a reduced cost values associated, which represents the amount the objective value would increase if the flux through the reaction would be increased by one unit.
Note that by definition reduced costs values that can increase the objective value are negative numbers. 



Once the reconstruction is in a computer-readable format, the systems boundaries need to be defined. 
In particular, this means that for all metabolites that can be consumed or secreted by the target organism, a so-called **exchange reaction** needs to be added to the reconstruction. 
The exchange reactions can be employed in later simulation to define environmental conditions
(e.g., carbon source).

The exchange reactions represent the systems boundaries

The `_b` suffix on a compound, e.g. "M_cpd08636_b" stands for a boundary condition.
Thus it's coming with a `boundaryCondition="true"` flag.

This module uses various heuristics to decide whether a boundary reaction is an exchange, demand or sink reaction. It mostly orientates on the following paper:



exchange reactions for compounds with a special suffix  (i.e. the “_b” suffix that indicates boundary compounds).



---------

## Usage

All `memote` commands have extensive help descriptions.

1. For simple command line testing, check out `memote run -h`.
2. To generate a pretty report, check out `memote report snapshot -h`.

## Testing the Model with Continuous Integration

Currently, we can enable continuous model testing using Travis CI. All you have
to do is:

1. Create a [GitHub](https://github.com/) account.
2. Create an account at https://travis-ci.org using your GitHub account.
3. Run `memote online`.
4. A history report will be publicly visible at https://hariszaf.github.io/Salmonella-infantis-GEM.


---

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
