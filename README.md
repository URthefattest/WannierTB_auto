Capabilities: Automatically generate input files for Wannier90 software to construct Wannier tight-binding models; Generate projected electronic band structure from the PROCAR file; Plot projected band weights.


Code list:

Wannier_auto.py:  Automatically generate appropriate input file "wannier90.win" for the Wannier90 software to construct Wannier tight-binding models. 

wannier90.win:  Input file template for the Wannier90 software.

projbands.py:  Automatically generate the projected electronic band structure from the "PROCAR" file and store it in the "pband_dir" directory.

sumofweightforpbands.py:  Calculate the projected band weights and generate figures to provide an intuitive visualization of their distribution together with the corresponding band index ranges.


Recommended directory structure:

<img src="Directory Structure.png" alt="Directory Structure" width="800"/>

If the project is deployed according to this directory structure, all ".py" code can be run directly; otherwise, the file paths in the ".py" code need to be modified.

If you use our code for your research, please cite: https://doi.org/10.48550/arXiv.2506.03871


