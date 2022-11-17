# ArbBetting

Python based arbitrage finder for Australian betting.

## Setup

We recommend installing VSCode and Miniconda for use as IDE and environment manager:

- https://code.visualstudio.com/
- https://docs.conda.io/en/latest/miniconda.html

### You can set up your conda environment as follows:

Create new conda environment named "arbet":
`conda env create -f environment.yml`

Update conda environment:
`conda activate arbet`
`conda env update -f environment.yml --prune`

To generate odds data and calculate arbs:  
`python main.py`


## Git Help

Creates a new local branch, copying the current working branch:
`git branch branch_name`

Changes your local working branch:
`git checkout branch_name`

Pulls changes from master into your own branch:
`git pull origin master`

Push changes from local branch to corresponding remote branch:
`git add files_to_commit`
`git commit -m "commit_message"`
`git push`

Gets  metadata changes from Git (new branch info):
`git fetch`

Shows current working branch and modified files:
`git status`

Deletes local branch (after you merge to master with a pull request):
`git branch -D branch_name`

