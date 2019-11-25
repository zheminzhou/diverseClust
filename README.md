# diverseClust
A simple script that can efficiently cluster divergent amino acid sequences based on the coverage of their alignments

# Requirements
* Python >= 3.5

* Install required Python packages
`
    pip install -r requirment.txt
`

* Install and link required 3rd party packages

1. ncbi-blast: ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/
2. mcl: https://github.com/JohannesBuchner/mcl
3. usearch: http://www.drive5.com/usearch/download.html (32-bit version is free for individual use)

ncbi-blast and mcl can also be installed using apt-get in ubuntu by:

````
    sudo apt-get update
    sudo apt-get install ncbi-blast+ mcl
````

# Usage:

Use
`
    python diverseClust.py --help
`

To get help page

# example:
Run
`
    python diverseClust.py -q examples/examples.fa
`
The expected output is:
`
    Pre-clustering using usearch. Results in examples/examples.fa.repr and examples/examples.fa.uc
    Running BLASTp to generate examples/examples.fa.bsp
    Parsing BLASTp results into examples/examples.fa.abc
    Running MCL to obtain clusters in examples/examples.fa.mcl
    Final outputs are saved in examples/examples.fa.diverseClust
`
