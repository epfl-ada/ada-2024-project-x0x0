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

In a globalized beer market, understanding consumer preferences is crucial for breweries and marketers. Our project aims to explore geographical biases in beer ratings by analyzing a comprehensive dataset from BeerAdvocate. We hypothesize that users exhibit a preference for beers from their own country over foreign ones, reflecting cultural identity and national pride. To validate this, we will perform statistical analyses and clustering techniques on user ratings from multiple countries, not just Germany. By first analyzing the dataset to identify the top countries in terms of beer production and user activity, we ensure a robust and representative study. Our findings could offer valuable insights into consumer behavior, helping breweries tailor their strategies for different markets and contributing to the academic discourse on cultural influences in consumption patterns..

## Research questions
- Looking at individual countries, who prefers their beer? Do locals have higher average ratings for their beer compared to outside reviewers? And do locals rate beers coming from outside countries lower than the local beers?

- Looking specifically at countries' neighbors, are certain rivalries between countries revealed? For example, will we see a German/Dutch rivalry?

- If we cluster beers by rating and country of origin, will we see the same trend where people from a country prefer their own beers?

- Looking deeper into preferences, does separating by beer style reveal a style specific bias, or do people remain globally biased? (for countries that don't have sig diff, can do style analysis to see if there is)


## Proposed additional dataset
