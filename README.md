# Exploring Geographical Bias in Beer Ratings: ": Is Your State Swaying Your Sip?"

**Abstract**

Countries often claim that they have the “best” beer, in this article we are going to analyse the US and see if we can quantify a bias that people from different states have for each other's beers. Does the state you are from influence your beer preferences, especially towards beers coming from your own state? More generally, by examining the data from two beer review websites, we aim to uncover links between a user's geographical location, and how they rate beers. We were inspired by different regions of the world having similar food, so to try and find trends in beer data we’re going to start with a ‘regional’ analysis of states. Additionally, we will attempt to explain and find reasons for the bias in preference by looking at various factors, such comparing specifically neighbouring states, or analysing differences in beer style preferences.

**Research questions**

-Do regions like the same kind of beer?

-Do we see significant differences between regions when comparing beer ratings?

-Looking at the state level, are these biases still present?

-Looking deeper into preferences, does separating by beer style reveal a style specific bias that could explain these differences in ratings?

-If we cluster beers by rating and state of origin, will we see the same trend where people from a state prefer their own beers?

## Proposed Additional Datasets

Geographical Data: States’ bordering states

Source: https://state.1keydata.com/bordering-states-list.php

Usage: Group each state and its neighbors as a region and look if there is a difference in beer rating inside and between the regions. Therefore, we thought it useful to add an additional dataset classifying the state borders of each state. This dataset gives us the state name and all its neighbors.

## Methods

### Part 1: Cleaning up the dataset

*Step 1: Exploring the data*

We started by carefully exploring the dataset, familiarizing ourselves with its structure and what it contains.

*Step 2: Streamlining the dataset*

After considering what we would need for our project, we removed unnecessary data, and reformatted the files for ease of use.

*Step 3: Enrichment with additional datasets*

Adding additional geographical data (neighbours) to aid our analyses on geographical proximity of the different locations

Note: We are focussing on the US, as looking at BA data, the majority of it is US based data, and even in RB nearly a third of the data is US based. We still end up with dataframes millions of lines only, so we feel as though we have enough data for analysis. We will compare the results obtained in both datasets.

### Part 2: Is there bias and why is there bias?

Our dataset is very large, in the millions of data points, making t-testing or equivalents meaningless, thus we decided to mainly go with using Cohen’s D.

*Question 1:*

We define a region as a state and its neighbouring states. Within these regions, do the individual states like each other’s beer? To test this, we are comparing the distribution of the ratings of beers coming from each state to each other, and using Cohen’s D to test effect size. We are only comparing ratings when beers and users come from the region. We would hope to see that most regions have  low Cohen’s D so we can reject the notion that their distributions are significantly different.

*Question 2:*

Looking specifically at ‘regions’, do we see differences between beer ratings? Do regions have higher average ratings for their beer compared to outside reviewers?Do regions rate beers coming from outside countries lower than local beers? To test this we use our previously constructed regions, and compare them with each other (Cohen’s D) to see if there are differences in the way they rate their own region’s beers, or coming from an outside region. We would like to see that regions prefer their own beer while disliking other regions' beer.

*Question 3:*

Looking at the state level, are these biases still present? Do locals have higher average ratings for their beer compared to outside reviewers? Do locals rate beers coming from outside countries lower than local beers? For this part, the analysis will be similar to region by region, except more granular, being state by state. We would like to see whether states prefer their own beer while disliking other regions' beer, maybe in a more extreme way.

*Question 4:*

Looking deeper into preferences, does separating by beer style reveal a style specific bias that could explain these differences? We’re doing this because maybe a bias that was hidden in a previous analysis will become more apparent when analyzed by style. Additionally, we might be able to explain certain biases. For example, if California is biased towards its own beers, and imagine they like a style of beer X and give it very high ratings, but, when we look at production through breweries, they are a state that produces a lot of this style. Therefore it would be more accurate to conclude that Californians simply prefer this style of beer.

*Question 5:*

If we cluster beers by rating and state of origin, will we see the same trend where people from a state prefer their own beers? We would like to see similar trends as in questions 1-3, and we can recover similar biases, for example, for a cluster of California beers, do the high reviews originate from California?

## Proposed Timeline

17/11/24 Finish data Handling and Preprocessing & Initial Data Exploration

1/12/24 Finish Questions 1-5 Implementation

8/12/24 Finish final analyses

15/12/24 Write report

20/12/24 Milestone 3 Deadline

## Team organization

Enzo: Preprocessing pipeline and exploratory data

Iarantsoa/Thomas: Question 1

Helene/Alexandra: Question 2

Enzo/Alexandra: Question 3

Helene/Iarantsoa: Question 4

Thomas/Enzo: Question 5

## Questions for TAs

Clustering Approach: Do you have recommendations on the most suitable clustering algorithms given the nature of our data?

Are our questions suitably in depth based or should the analysis go even further?

Potential additional analysis

Does the diversity of beer offerings within a state affect user ratings and preferences?

* Objective: Assess whether states with a wider variety of beer styles receive different ratings compared to states with limited beer diversity.
* Hypothesis: A greater diversity of beers may lead to higher overall ratings due to increased exposure to different styles and tastes.
