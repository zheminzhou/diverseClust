# diverseClust
A simple script that can efficiently group divergent amino acid sequences into clusters based on the coverage of their alignments

# Requirements
1. **Python >= 3.5**

2. Install required Python packages
````
    pip install -r requirment.txt
````

3. Install required 3rd party packages

* **ncbi-blast**: ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/
* **mcl**: https://github.com/JohannesBuchner/mcl
* **usearch**: http://www.drive5.com/usearch/download.html (*32-bit version is free for individual use*)

**ncbi-blast** and **mcl** can also be installed using `apt-get` in ubuntu by:

````
    sudo apt-get update
    sudo apt-get install ncbi-blast+ mcl
````



4. Modify **"diverseClust.ini"** to link installed executable files. 

It reads:
````
   [params]
   usearch = /home/zhemin/software/usearch11.0.667_i86linux32
   makeblastdb = makeblastdb
   blastp = blastp
   mcl = mcl
````
at the moment. Change the values after the **"="** symbols to the actual links to the files.

# example:
Run
`````
    python diverseClust.py -q examples/examples.fa
`````
The expected output is:
`````
    Pre-clustering using usearch. Results in examples/examples.fa.repr and examples/examples.fa.uc
    Running BLASTp to generate examples/examples.fa.bsp
    Parsing BLASTp results into examples/examples.fa.abc
    Running MCL to obtain clusters in examples/examples.fa.mcl
    Final outputs are saved in examples/examples.fa.diverseClust
`````

# Usage:

Use
`
    python diverseClust.py --help
`

To get **help page**
````
Usage: diverseClust.py [OPTIONS]

Options:
  -q, --query TEXT       amino acid sequences to be clustered. Multi-FASTA
                         format. REQUIRED.  [required]
  -p, --prefix TEXT      Prefix of outputs. [DEFAULT: same as query name]
  -i, --min_id FLOAT     Minimal accepted identity in BLASTp [DEFAULT: 0.3]
  -c, --min_cov FLOAT    Minimal alignment covereage to the smaller sequence
                         in BLASTp [DEFAULT: 0.8]
  --min_cov2 FLOAT       Minimal alignment covereage to the larger sequence in
                         BLASTp [DEFAULT: 0.2]
  -I, --inflation FLOAT  Inflation factor for MCL. [DEFAULT: 2.0]
  --help                 Show this message and exit.
````

