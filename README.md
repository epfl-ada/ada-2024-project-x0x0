# Exploring Geographical Bias in Beer Ratings: ": Is Your State Swaying Your Sip?"

**Abstract**

Beer, the most common alcoholic beverage. Grabbing a beer has become one of the world’s favorite pastimes. It is a chance to get together amongst friends, decompress with colleagues after work. MAYBE ADD MORE
From America’s prohibition era to the current globalisation of the beer market, the choice of beer in a bar has never been so varied. The choice one makes when ordering a beer has never highlighted internal bias as much as now. 

The strong economic competition gives way to a cut-throat rivalry. Each brewery wants to sell more, be the best, especially if they sell beer in the same location. Can beers that come from far away compete with the regional preference people might have?
It’s a claim we hear all the time: regions boasting about having the “best” beer. But what if there’s more to it than just national pride? What if the state you call home influences how you taste beer? What if your national pride is ingrained in your beer preferences? In this investigation, we dive deep into the beer preferences of Americans. 

This lead us to our question at hand: Do people from different states have a bias for their own beers? To crack the case, we’ll begin by examining the geography of beer preferences through the lens of U.S. states. Inspired by the idea that people from certain regions of the world share similar food tastes, we’ll analyze regional beer preferences, comparing neighboring states and even the way different beer styles shape the ratings by state. Join us as we sift through the data to uncover hidden trends and discover the reasons behind these regional biases. Could the answers be hiding in plain sight? Let’s investigate and find out.


**Research questions**

-Do regions like the same kind of beer?

-Do we see significant differences between regions when comparing beer ratings?

-Looking at the state level, do we see more trends ? Does doing a sentiment analysis on the text reviews reveal similar trends ?

-Looking deeper into preferences, does separating by beer style reveal a style specific bias that could explain these differences in ratings? Could we find state specific trends on beer style prefereneces?

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

Our dataset is very large, in the millions of data points, making t-testing or equivalents meaningless, thus we decided to mainly go with using Cohen’s D which takes into consideration size effect

*Question 1:*

We define a region as a state and its neighbouring states. Within these regions, do the individual states like each other’s beer? To test this, we are comparing the distribution of the ratings of beers coming from each state to each other, and using Cohen’s D to test effect size. We are only comparing ratings when beers and users come from the region. We would hope to see that most regions have  low Cohen’s D so we can reject the notion that their distributions are significantly different. In this part we also aim to define regions of the US which are states that tend to rate beers more similarly.

*Question 2:*

Looking specifically at the custom ‘regions’ discovered in question 1, do we see differences between beer ratings? Do regions have higher average ratings for their beer compared to outside reviewers? Do regions rate beers coming from outside countries lower than local beers? To test this we use our previously constructed regions, and compare them with each other (Cohen’s D) to see if there are differences in the way they rate their own region’s beers, or coming from an outside region. We would like to see that regions prefer their own beer while disliking other regions' beer.

*Question 3:*

Looking at the state level, are these biases still present? Do locals have higher average ratings for their beer compared to outside reviewers? Do locals rate beers coming from outside countries lower than local beers? For this part, the analysis will be similar to region by region, except more granular, being state by state. We would like to see whether states prefer their own beer while disliking other regions' beer, maybe in a more extreme way.

*Question 4:*

Looking deeper into preferences, does separating by beer style reveal a style specific bias that could explain these differences? We’re doing this because maybe a bias that was hidden in a previous analysis will become more apparent when analyzed by style. Additionally, we might be able to explain certain biases. For example, if California is biased towards its own beers, and imagine they like a style of beer X and give it very high ratings, but, when we look at production through breweries, they are a state that produces a lot of this style. Therefore it would be more accurate to conclude that Californians simply prefer this style of beer.

Style preferences are masked by the general popularity of certain beer styles in the US such as American IPA and the Imperial Stout which made uncovering these preferences difficult. By clustering by considering most features such aroma, taste and appeance for each style of beer, could we uncover more style specific clusters?

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

Thomas + Enzo: code modularisation + file management

Question 1: Thomas- large scale Cohen's D analysis + custom region definitions

Question 2: Helene/Alexandra - custom region ratings exploration

Question 3: Iarantsoa / Alexandra - state by state specific rating bias exploration

Question 4a: Helene- preliminary beer style preference analysis

Question 4b: Enzo/ Iarantsoa- style specific parameters and cluster exploration

Question 5a: Iarantsoa - parameter selection

Question 5b: Alex - reviews clustering to explore any geographical links


