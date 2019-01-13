# MetaAssemblyEval
Assessment of metagenomic assemblers based on hybrid reads of real and simulated metagenomic sequences.
This is an evaluation strategy for metagenomic assemblers based on hybrid reads of real and simulated metagenomic sequences. The obtain the statistics of the contigs are based on metagenomic assembly evaluation tool, metaQUAST[1].

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
conda install quast 
Note: Bioconda is needed to install quast
## <a name="preprocessing"></a>References

[1] 

[2]
