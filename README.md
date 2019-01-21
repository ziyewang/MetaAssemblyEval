# MetaAssemblyEval
Assessment of metagenomic assemblers based on hybrid reads of real and simulated metagenomic sequences.
This is an evaluation strategy for metagenomic assemblers based on hybrid reads of real and simulated metagenomic sequences. The statistics of the contigs are based on metagenomic assembly evaluation tool, metaQUAST[1].

## <a name="started"></a>Getting Started

We recommend using Anaconda to run MetaAssemblyEval. Download [here](https://www.continuum.io/downloads)

After installing Anaconda, fisrt obtain MetaAssemblyEval:

```sh
git clone https://github.com/ziyewang/MetaAssemblyEval
```
Create a Anaconda environment and activate it:

```sh
conda create -n metaAssemblyeval_env python=2
source activate metaAssemblyeval_env
```

Install the MetaAssemblyEval dependencies into this environment:

```sh
conda install quast 
Note: Bioconda is needed to install quast.
```

## <a name="preprocessing"></a>References

[1] Mikheenko A, Saveliev V, and Gurevich A. MetaQUAST: Evaluation of metagenome assemblies. Bioinformatics, 32:1088-1090, 2016.

[2] Holtgrewe M. Mason-A read simulator for second generation sequencing data. Technical Report, FU Berlin, 2010.

[3] Li D, Luo R, Liu CM, et al. MEGAHIT v1.0: A fast and scalable metagenome assembler driven by advanced methodologies and community practices. Methods, 102:3-11, 2016.

[4] Nurk S, Meleshko D, Korobeynikov A, et al. MetaSPAdes: A new versatile metagenomic assembler. Genome Res, 27:824-834, 2017.

[5] Peng Y, Leung HC, Yiu SM, et al. IDBA-UD: A de novo assembler for single-cell and metagenomic sequencing data with highly uneven depth. Bioinformatics, 28:1420-1428, 2012.

[6] Rozov R, Goldshlager G, Halperin E, et al. Faucet: streaming de novo assembly graph con-
struction. Bioinformatics, 34:147-154, 2018.

[7] Mohamadi H, Khan H, and Birol I. ntCard: a streaming algorithm for cardinality estimation
in genomics data. Bioinformatics, 33:1324-1330, 2017.
24
