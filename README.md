# ArbBetting

Python based arbitrage finder for betting.

## Setup

Download and use VSCode and Anaconda:

https://code.visualstudio.com/

https://www.anaconda.com/products/distribution

Create new conda environment:  
`conda create --name your_env python`

Install dependencies from environment.yml:  
`conda activate your_env`  
`conda env update --file environment.yml --prune`

Create folders in directory
`data`
`logs`

To generate combined odds data:  
`python total_odds.py`


## Git Help

Creates your own branch from your current branch:

`git branch name`


Changes your current branch:

`git checkout name`

Pulls changes from master into your own branch:

`git pull origin master`

Push changes from local onto your branch:

`git add .`

`git commit -m "message"`

`git push`

Gets all metadata changes from Git (new branch info):

`git fetch`

Look at current branch name and modified files

`git status`

Deleted the branch (after you merge with a pull request)

`git branch -D name`