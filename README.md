# Exploring Geographical Bias in Beer Taste in the US : Is your State swaying you Sip?

**Abstract**

Countries often claim that they have the “best” beer, we aim to analyse the US and see if we can quantify a bias that people from different states have for each other's beers. Does the state you are from influence your beer preferences, especially towards beers coming from your own state? More generally, by examining the data from the Beer Advocate beer review website, we aim to uncover links between a user's geographical location, and how they rate beers. We were inspired by different regions of the world having similar food, so to try and find trends in beer data we’re going to start with a ‘regional’ analysis of states. Additionally, we will attempt to explain and find reasons for the bias in preference by looking at various factors, such comparing specifically neighbouring states, or analysing differences in beer style preferences.


**Research questions**

- Do regions like the same kind of beer?

- Do we see significant differences between regions when comparing beer ratings?

- Looking at the state level, do we see more trends ? Does doing a sentiment analysis on the text reviews reveal similar trends ?

- Looking deeper into preferences, does separating by beer style reveal a style specific bias that could explain these differences in ratings? Could we find state specific trends on beer style prefereneces?

- Going the other way around, if we cluster beers by beer attributes and ratings, do we see regional bias? And do we see the same biases as before?

## Additional Dataset

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

Note: We are focussing on the US, as looking at BA data, the majority of it is US based data. We still end up with dataframes millions of lines only, so we feel as though we have enough data for analysis even by limiting our data to the US data in BA, we have enough data to make reasonable conclusions. 

### Part 2: Is there bias and why is there bias?

Our dataset is very large, in the millions of data points, making t-testing or equivalents meaningless, thus we decided to mainly go with using Cohen’s D which takes into consideration size effect

*Question 1:*

We define a region as a state and its neighbouring states. Within these regions, do the individual states like each other’s beer? To test this, we are comparing the distribution of the ratings of beers coming from each state to each other, and using Cohen’s D to test effect size. We are only comparing ratings when beers and users come from the region. We would hope to see that most regions have  low Cohen’s D so we can reject the notion that their distributions are significantly different. In this part we also aim to define regions of the US which are states that tend to rate beers more similarly.

*Question 2:*

Looking specifically at the custom ‘regions’ obtained in question 1, do we see differences between beer ratings? Do regions have higher average ratings for their beer compared to outside reviewers? Do regions rate beers coming from outside countries lower than local beers? To test this we use our previously constructed regions, and compare them with each other to see if there are differences in the way they rate their own region’s beers, or coming from an outside region. We would like to see that regions prefer their own beer while disliking other regions' beer.

*Question 3:*

Looking at the state level, are these biases still present? Do locals have higher average ratings for their beer compared to outside reviewers? Do locals rate beers coming from outside countries lower than local beers? For this part, the analysis will be similar to region by region, except more granular, being state by state. We would like to see whether states prefer their own beer while disliking other regions' beer, maybe in a more extreme way.

*Question 4:*

Looking deeper into preferences, does separating by beer style reveal a style specific bias that could explain these differences? We’re doing this because maybe a bias that was hidden in a previous analysis will become more apparent when analyzed by style. Additionally, we might be able to explain certain biases. For example, if California is biased towards its own beers, and imagine they like a style of beer X and give it very high ratings, but, when we look at production through breweries, they are a state that produces a lot of this style. Therefore it would be more accurate to conclude that Californians simply prefer this style of beer.

Style preferences are masked by the general popularity of certain beer styles in the US such as American IPA and the Imperial Stout which made uncovering these preferences difficult. By clustering by considering most features such aroma, taste and appeance for each style of beer, could we uncover more style specific clusters?

*Question 5:*

If we cluster all the US reviews based on a variety of parameters that allow us to distinguish between the beers in question, such as taste, aroma, appearance etc, are we able to find clusters that have geographical state dependencies? In the clusters that we are able to form, are there hidden patterns that reveal groupings of reviews originating from users of the same state in certain clusters? And are these these clusters geographically relavant?  



## Group organisation
Enzo: Preliminary data analysis and overall code pipline. Providing cleaned datasets for future analyis and data modularisation
Thomas : Data modularisation, geographical maps visulisation of create "custom regions"  
Helene: Beer style analysis and website repository organisation  
Alex: statistical method suggestions and reviews clustering  
Iarantsoa: Parameter/feature selection and graph analysis. Additional clustering analysis  


## Our data story
Below is the link to our website which will take you through the journey of our data story in more detail! <br>
Data story link: https://helenezablit.github.io/website-x0x0/ 
