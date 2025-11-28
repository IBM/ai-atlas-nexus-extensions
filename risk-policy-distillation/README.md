# Global Explanations for LLM-as-a-Judge

![](img/clove.png)
![](img/glove.png)

This repository contains code for paper: *Interpreting LLM-as-a-Judge Policies via
Verifiable Global Explanations*

Given an LLM-as-a-Judge solution, CLoVE algorithm can generate high-level, concept-based 
local explanations. Additionally, GloVE algorithm uses iterative selection, combination and merging of
local explanations to generate a global summary of LLM-as-a-Judge policy.

Follow the steps below to install the code, run experiments from the paper or run CLoVE and GloVE
on custom use cases.

## Installation

To create a conda environment with necessary requirements:

```{bash}
conda create -n glove python=3.12
conda activate glove
pip install .
```

## Running Paper Experiments

To run algorithms presented in this work, you need to start an Ollama server:

```{bash}
OLLAMA_HOST=127.0.0.1:11435 ollama serve
```

To run experiments presented in the paper run the following:

```{bash}
python examples/run_experiments.py
```


## Explaining LLM-as-a-Judge in a Custom Use Case

Additionally, the repository provides notebooks to generate policy explanations for custom
use cases. 


* To generate local explanations of LLM-as-a-Judge using CLoVE follow the notebook
[here](examples/notebooks/explaining_decisions_with_clove.ipynb).
* To run the full pipeline and generate  a global summary given a dataset and an LLM-as-a-Judge
refer to the notebook [here](examples/notebooks/full_explanation_pipeline.ipynb).
