# Albert Invent Data Science Library

[![MoleculeEngineering](https://circleci.com/gh/MoleculeEngineering/albert-ds/tree/main.svg?style=shield&circle-token=0ee8a888f4c69edf2bdf6d45e33b91435747abea)](https://app.circleci.com/pipelines/github/MoleculeEngineering/albert-ds)


The Albert Invent Data Science Library is a set of wrappers and helper functions which can be used to build data science applications on top of the albert platform. 

# Non-Python Dependencies

## Docker
If you want to use the docker image for doing development you will need to install the docker runtime (or docker desktop for windows/macos). If you are going to be running the docker image on an ubuntu system with a GPU you will need to additionally install the nvidia docker runtime -- instructions for which can be found at https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

# Getting Started
After installing the albert-ds package, you can setup your environment configuration by running the command `albert init` and following the prompts. Any credentials that you do not have (e.g. if you do not have data warehouse credentials) you can simply leave them blank. 

If you will be using clearML integrations then be sure to have your clearml pip install command ready as you will be prompted for it as part of the init process. If you have already setup clearml in your virtual environment prior to installing albert-ds then you can simply answer no to the prompt and it will leave your current configuration untouched.

# Running Unit Tests
NOTE: All the following commands should be run from within a virtual environment.

albert-ds utilizes pytest as its testing framework -- to run the full suite of unit tests use the helper script and the `ta` command:
```bash
$ ./al.sh ta
```

Alternatively if you want to run the tests in a fresh venv (i.e. test the build/install/unit test workflow) run the command `tb` -- This is useful for checking that you have correctly supplied all dependencies in the package setup.cfg. 

```bash
$ ./al.sh tb
```
Note that running the above command will look for lib-jwt-python at the relative path `../lib-jwt-python` if it is not located there it will attempt to clone the repo using ssh and will fail if you don't have your github ssh keys setup correct. 

# Package Installation 
Until we get a pypi package setup you will need to clone this repository and perform a pip install locally.

## Choosing an Install Environment
Depending on the application you may not need or want the full development stack associated with this library. You can therefore install different dependencies using the square bracket syntax e.g. `albert-ds[viz]` if you only want to install a certain set of dependencies. This is particularly useful if you are building out an application or microservice which only depends upon a subset of the full albert-ds library, and you do not want to install unused dependencies. 

If you specify no environment tag then you will just the get base code for albert-ds installed into your environment and most of it will not function without the required dependencies -- so be sure to choose one of the following stacks when installing the library. 

Note the use of quotes in the package install commands below e.g. `"albert-ds[dev]"` -- the quotes are required and you will get an error if you forget to include them.

## Full Development Stack
The full development stack can be installed using the `[dev]` or `[all]` tags. The development environment contains support for juptyerlab and all the associated ipython dependencies. It should not be installed in a deployed application
```bash
$ git clone git@github.com:MoleculeEngineering/albert-ds.git
$ pip install "albert-ds[torch]" # This needs to be run first for the [chem] dependency to work properly
$ pip install "albert-ds[dev]" #This should be run from within your python virtual environment
```


## Visualization Stack
The visualization stack includes only those dependencies which are needed to utilize the visualization components of the albert-ds library. It can be installed with the `[viz]` tag
```bash
$ git clone git@github.com:MoleculeEngineering/albert-ds.git
$ pip install "albert-ds[viz]" #This should be run from within your python virtual environment
```

## Metrics Stack
The metrics stack includes only those depenencies which are necessary to compute metrics (for example: if you have a microservice architecture and you are running lots of predictions and storing those in a database, you may want to have a microservice which is dedicated to computing performance/accuracy/etc... metrics and hence that service should not require any of the other stacks)
```bash
$ git clone git@github.com:MoleculeEngineering/albert-ds.git
$ pip install "albert-ds[metrics]" #This should be run from within your python virtual environment
```

## NLP Stack
The NLP Stack includes only those dependencies which are necessary to compute NLP transforms or embeddings, including helper functions for transforming or analyzing text data
```bash
$ git clone git@github.com:MoleculeEngineering/albert-ds.git
$ pip install "albert-ds[nlp]" #This should be run from within your python virtual environment
```

## Models Stack
The models stack includes all the dependencies necessary to build or run models. Installing the Models stack will also install the metrics stack
```bash
$ git clone git@github.com:MoleculeEngineering/albert-ds.git
$ pip install "albert-ds[models]" #This should be run from within your python virtual environment
```

## Chemistry Stack
The chemistry stacks includes all the dependencies needed to run the chemistry modeuls. 
```bash
$ git clone git@github.com:MoleculeEngineering/albert-ds.git
$ pip install "albert-ds[torch]" #This needs to happen first for the [chem] install to work correctly
$ pip install "albert-ds[chem]" 

# Using the Helper Script
Included in the repository is a helper script `al.sh` which contains a few simple helper scripts for building, publishing, etc... 
TODO: Include documentation here on the use of the helper script to build and publish the package to pypi.
