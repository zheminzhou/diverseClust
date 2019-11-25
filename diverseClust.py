import os, sys, numpy as np, pandas as pd
import subprocess
import click
import configparser
import re, shutil
from collections import defaultdict

__SCRIPT__ = os.path.realpath(__file__)
__DIR__ = os.path.dirname(__SCRIPT__)

config = configparser.ConfigParser()
config.read(__SCRIPT__.rsplit('.', 1)[0] + '.ini')
config = dict(config['params'])

# run usearch for preclustering 99%
def precluster(prefix, query) :
    sys.stdout.write('Pre-clustering using usearch. Results in {0}.repr and {0}.uc\n'.format(prefix))
    subprocess.Popen('{usearch} -cluster_fast {0} -query_cov 0.99 -target_cov 0.99 -leftjust -rightjust -id 0.99 -centroids {1}.repr -uc {1}.uc'.format(query, prefix, **config).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
    
# run blastp to get pairwise matrix
def runBlastp(prefix) :
    sys.stdout.write('Running BLASTp to generate {0}.bsp\n'.format(prefix))
    subprocess.Popen('{makeblastdb} -in {0}.repr -dbtype prot'.format(prefix, **config).split(), stdout=subprocess.PIPE).wait()
    subprocess.Popen('{blastp} -task blastp-short -db {0}.repr -query {0}.repr -out {0}.bsp -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue score qlen slen" -evalue 0.1 -num_threads 10'.format(prefix, **config), shell=True).wait()
    
# convert blastp to links
def parseBlast(prefix, min_id, min_cov, min_cov2) :
    sys.stdout.write('Parsing BLASTp results into {0}.abc\n'.format(prefix))
    matrix = pd.read_csv('{0}.bsp'.format(prefix), sep='\t', header=None).values
    links = {}
    with open('{0}.abc'.format(prefix), 'w') as fout :    
        for part in matrix[matrix.T[2] >= min_id * 100] :
            if part[0] != part[1] :
                key = tuple(sorted([part[0], part[1]]))
                if key not in links :
                    c1, c2 = sorted([(part[7]-part[6]+1)/part[12], (part[9]-part[8]+1)/part[13]])
                    if c1 >= min_cov2 and c2 >= min_cov :
                        links[key] = c2
                        fout.write('{0}\t{1}\t{2}\n'.format(part[0], part[1], (c2-min_cov+0.0001)/(1-min_cov+0.0001)))

# get cluster using mcl
def runMCL(prefix, inflation) :
    sys.stdout.write('Running MCL to obtain clusters in {0}.mcl\n'.format(prefix))
    p = subprocess.Popen('{mcl} {0}.abc -I {1} --abc'.format(prefix, inflation, **config).split(), stderr=subprocess.PIPE, universal_newlines=True)
    output = re.findall(r'output is in (\S+)', p.communicate()[1])[0]
    shutil.move(output, '{0}.mcl'.format(prefix))
    
# extrapolate clusters to the whole dataset
def extrapolation(prefix) :
    cls = {}
    with open('{0}.mcl'.format(prefix)) as fin :
        for gid, line in enumerate(fin) :
            for p in line.strip().split('\t') :
                cls[p] = gid+1
    with open('{0}.uc'.format(prefix), 'r') as fin :
        for line in fin :
            if line.startswith('S\t') :
                part = line.strip().split('\t')
                if part[8] not in cls :
                    gid += 1
                    cls[part[8]] = gid+1
            elif line.startswith('H\t') :
                part = line.strip().split('\t')
                cls[part[8]] = cls[part[9]]
    with open('{0}.diverseClust'.format(prefix), 'w') as fout :
        for name, cls_id in sorted(cls.items(), key=lambda x:(x[1], x[0])) :
            fout.write('{0}\tdC_{1}\n'.format(name, cls_id))
    sys.stdout.write('Final outputs are saved in {0}.diverseClust\n'.format(prefix))

@click.command()
@click.option('-q', '--query', help='amino acid sequences to be clustered. Multi-FASTA format. REQUIRED.', required=True)
@click.option('-p', '--prefix', help='Prefix of outputs. [DEFAULT: same as query name]', default=None)
@click.option('-i', '--min_id', help='Minimal accepted identity in BLASTp [DEFAULT: 0.3]', default=0.3)
@click.option('-c', '--min_cov', help='Minimal alignment covereage to the smaller sequence in BLASTp [DEFAULT: 0.8]', default=0.8)
@click.option('--min_cov2', help='Minimal alignment covereage to the larger sequence in BLASTp [DEFAULT: 0.2]', default=0.2)
@click.option('-I', '--inflation', help='Inflation factor for MCL. [DEFAULT: 2.0]', default=2.0)
def main(query, prefix, min_id, min_cov, min_cov2, inflation) :
    if prefix == None :
        prefix = query
    # run usearch for preclustering 99%
    precluster(prefix, query)
    # run blastp to get pairwise matrix
    runBlastp(prefix)
    # convert blastp to links
    parseBlast(prefix, min_id, min_cov, min_cov2)
    # get cluster using mcl
    mcl_out = runMCL(prefix, inflation)
    # extrapolate clusters to the whole dataset
    extrapolation(prefix)


if __name__ == '__main__' :
    main()
    #parseBlast(fname, colId, minCut)
