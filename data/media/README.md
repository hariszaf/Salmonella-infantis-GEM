# Media compounds


Lines after 65 and up to 108 come from the yeas extract as described in Heinken et. *al.* (2013) - supplementary Table 8d. 

The last 2 lines (LipidA and Ubiquinone-8) are not part of the yeast extract. We examine if that can make things work.. 

> We observed that without LipidA `dnngior` gapfiller **fails**! Without the Ubiquinone compound, a gapfilled model is returned. 

From the literature (Müştak, İ.B., Yardımcı, H. [Construction and in vitro characterisation of aroΑ defective (aroΑΔ) mutant Salmonella Infantis](https://doi.org/10.1007/s00203-019-01694-0). *Arch Microbiol* 201, 1277–1284 (2019)), we see that:

*there was no difference between the recombinant strain and the wild-type strain in terms of movement characteristics. This result suggests that there may be a different mechanism in S. Infantis strains for regulation of flagella production.* 


------------------


The default biomass function comes with the following compounds:

```python
['cpd00010_c0', 'cpd11493_c0', 'cpd00003_c0', 'cpd00006_c0', 'cpd00205_c0', 'cpd00254_c0', 'cpd10516_c0', 'cpd00063_c0', 'cpd00099_c0', 'cpd00149_c0', 'cpd00058_c0', 'cpd00015_c0', 'cpd10515_c0', 'cpd00030_c0', 'cpd00048_c0', 'cpd00034_c0', 'cpd00016_c0', 'cpd00220_c0', 'cpd00017_c0', 'cpd00201_c0', 'cpd00087_c0', 'cpd00345_c0', 'cpd00042_c0', 'cpd00028_c0', 'cpd00557_c0', 'cpd00264_c0', 'cpd00118_c0', 'cpd00056_c0', 'cpd15560_c0', 'cpd15352_c0', 'cpd15500_c0', 'cpd00166_c0', 'cpd00104_c0', 'cpd00037_c0', 'cpd00050_c0', 'cpd15793_c0', 'cpd15540_c0', 'cpd15533_c0', 'cpd15432_c0', 'cpd02229_c0', 'cpd15665_c0', 'cpd00023_c0', 'cpd00001_c0', 'cpd00033_c0', 'cpd00035_c0', 'cpd00039_c0', 'cpd00041_c0', 'cpd00051_c0', 'cpd00053_c0', 'cpd00054_c0', 'cpd00060_c0', 'cpd00065_c0', 'cpd00066_c0', 'cpd00069_c0', 'cpd00084_c0', 'cpd00107_c0', 'cpd00119_c0', 'cpd00129_c0', 'cpd00132_c0', 'cpd00156_c0', 'cpd00161_c0', 'cpd00322_c0', 'cpd00115_c0', 'cpd00241_c0', 'cpd00356_c0', 'cpd00357_c0', 'cpd00002_c0', 'cpd00038_c0', 'cpd00052_c0', 'cpd00062_c0', 'cpd17041_c0', 'cpd17042_c0', 'cpd17043_c0', 'cpd12370_c0', 'cpd00009_c0', 'cpd01997_c0', 'cpd03422_c0', 'cpd15666_c0', 'cpd00012_c0', 'cpd00008_c0', 'cpd00067_c0', 'cpd11416_c0']
```


Instead of 
cpd15432	LipidA	0.001	-100	100
we now have 
cpd15489	inner core oligosaccharide lipid A	0.001	-100	100
