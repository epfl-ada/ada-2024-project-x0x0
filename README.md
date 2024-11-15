# Your project name

This is a template repo for your project to help you organise and document your code better.
Please use this structure for your project and document the installation, usage and structure as below.

## Quickstart

```bash
# clone project
git clone <project link>
cd <project repo>

# [OPTIONAL] create conda environment
conda create -n <env_name> python=3.11 or ...
conda activate <env_name>


# install requirements
pip install -r pip_requirements.txt
```

### How to use the library

Tell us how the code is arranged, any explanations goes here.

## Project Structure

The directory structure of new project looks like this:

```
├── data                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

Readme.md file containing the detailed project proposal (up to 1000 words). Your README.md should contain:
    Title
    Abstract: A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?
    Research Questions: A list of research questions you would like to address during the project.
    Proposed additional datasets (if any): List the additional dataset(s) you want to use (if any), and some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible.
    Methods
    Proposed timeline
    Organization within the team: A list of internal milestones up until project Milestone P3.
    Questions for TAs (optional): Add here any questions you have for us related to the proposed project.
GitHub repository should be well structured and contain all the code for the initial analyses and data handling pipelines. For structure, please use this repository as a template
Notebook presenting the initial results to us. We will grade the correctness, quality of code, and quality of textual descriptions. There should be a single Jupyter notebook containing the main results. The implementation of the main logic should be contained in external scripts/modules that will be called from the notebook.

# Exploring Geographical Bias in Beer Ratings: Do Users Prefer Local Brews Over Foreign Ones?

We were inspired by the national pride of various countries that often claim that they are the “best” when it comes to the production of beers. In this article we are going to analyse the United States and see if we can quantify a bias that people from different states have for each other's beers. Does the state you are from influence your beer preferences, especially towards beers coming from your own state? More generally, by examining the data from two beer review websites, we aim to uncover links between a user's geographical location, and how they rate beers. Additionally, we will be trying to explain the bias in preference by looking at various factors, such comparing specifically neighbouring states, or analysing differences in beer style preferences. 


## Research questions

- Looking at individual states, who prefers their beer? Do locals have higher average ratings for their beer compared to outside reviewers? And do locals rate beers coming from outside countries lower than the local beers?
- Looking specifically at countries' neighbors, are certain rivalries between countries revealed? For example, will we see a German/Dutch rivalry?
- If we cluster beers by rating and country of origin, will we see the same trend where people from a country prefer their own beers?
- Looking deeper into preferences, does separating by beer style reveal a style specific bias, or do people remain globally biased? (for countries that don't have sig diff, can do style analysis to see if there is)

## Proposed additional dataset
**United States of America Geographical data**

* **Source**: https://state.1keydata.com/bordering-states-list.php
* **Usage**: Identify neighboring states for each selected state of the US to analyze regional influences


## Method

### Part 1: Cleaning up the dataset
**Step 1**: Exploring the data \
We started by carefully We started by carefully exploring the dataset, familiarizing ourselves with its structure and what was included in it.

**Step 2**: 
