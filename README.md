Automatically generate input files for Wannier90 software to construct Wannier tight-binding models; Generate projected electronic band structures from the PROCAR file; Plot projected density of states.

If you use our code for your research, please cite: https://doi.org/10.48550/arXiv.2506.03871

Code list:
Wannier_auto.py:  Automatically generate appropriate input file "wannier90.win" for the Wannier90 software. 

wannier90.win:  Input file template for the Wannier90 software.

projbands.py:  Automatically generate the projected band structure data and store it in the "pband_dir" directory.

sumofweightforpbands.py:  Calculate the projected band weights and generate figures to help users intuitively understand the distribution of the weights as well as the corresponding band index ranges.


Recommended directory structure: <img src="Directory structure.png" alt="Directory Structure" width="600"/>
If the project is deployed according to this directory structure, all ".py" programs can be run directly; otherwise, the file paths in the ".py" scripts need to be modified.
