## Part 2

**Problem Formulation**
For Part 2, the goal was to finish the code for the SebastianAutoPlayer, so that the program would play the game of Sebastian in such a way that gets the best score possible. This problem was unique in the sense that it is not a search problem, where states are explored via a search algorithm for a goal state. When we initially met to discuss the problem, we figured that the problem would involve expected value computations. Broadly, we figured that expected value calculations would be needed to "guide" decision-making for the algorithm. This approach was further clarified by the discussion video on games of chance, where Professor Crandall showed how he reasoned through a similar problem. That video was further inspiration for our approach. 

**Program Description**
To complete this task, we added functionality to the SebastianAutoPlayer file, per the instructions. Taking this problem step by step, the first function we added was a function that calculates the maximum score, given a set of dice. Using the Scorecard provided as a guide, the function refers to the categories and checks the criteria. The function returns the best score and the corresponding category, given the dice. In addition, the function also refers to the categories that were already recorded. By doing this, it only considers scores that are still "available," as categories can only be used once in the game. Next, we created a function that takes in the dice and a reroll strategy in the form of a list of booleans, and calculates the expected value of the reroll. The function considers all possible outcomes and calls the maximum score function we created. The function returns the expected value by totaling the scores and then multiplying by 1 over all outcomes, since all outcomes are equally likely. Finally, we created a function that considers all possible reroll strategies. This function takes in dice and the scorecard, and considers all possible reroll strategies and calls the expected value function we created. After all strategies are considered, it returns the strategy that had the highest expected value; the function also converts the strategy to a list of indexes for which dice to reroll from the boolean list. Once those functions were created, we implemented them into the first, second, and third roll methods of the AutoPlayer. The first and second roll use the function that finds the best strategy, and the third roll calls the max score function, which has the first element as the name of the category.

**Discussion**
In development we considered and came across a few interesting challenges. First, we noticed that our code needed to account for situations where the final roll didn't yield any score, i.e. the dice didn't meet any of the available categories. During testing, we noticed that this was happening towards the middle-late parts of the game. To adjust for this, we noticed that some categories were rare in occurrence as we were testing, like quintuplicatam. So in order to preserve categories that were higher in probability, we had the program choose to elect those lower probability categories earlier in order to preserve the other categories for more "assured" points in the later stages of the game. Secondly, we did some testing on trying to have the program calculate the probabilities differently based on how many rolls were left in that turn. After testing, we didn't find any discernable difference in mean performance, so we opted against that. And finally, we tested an option where the scoring function returned the total score of the roll, versus just the score of the best category. In other words, when given a strategy and dice, you have many outcomes. Each outcome is evaluated based on what categories it qualifies for. What we tried to do is to total up the scores for ALL categories that outcome qualifies for, not just the BEST category. We actually found that the performance dipped, so we changed it back to only consider the best score for that outcome.

Overall, this was a fun and interesting challenge. Thank you!

## Part 3

**Problem Formulation**
This problem can be abstracted as a text classification problem using Naïve Bayes classifier and Bag of Words both of which will be explained in detail in later parts of the file. Our task was to use these two approaches to classify given texts based on their labels. The dataset has already been separated into train and test data, In addition we were also given break down of data into labels, classes and text. Our job involves using them to train the model and later predict the result on the test data. The skeleton code also computes the accuracy of predictions.
Concepts used in the program:

1)	Bag of words: It is simply a data structure which keeps track of each word and its count. For our problem we implemented it using a 2D array, which has words and their respective counts.
2)	Naïve Bayes Classifier: We implemented Multinomial version of Naïve Bayes Classifier, which is more suitable for text classification problems.
3)	Logarithms: Often while dealing with text classification the probability values of each word are quite low and multiplying them will yield even more small values to avoid this, we use log and add them which should give similar value as a normal multiplication.
4)	 Pseudo-Count: We are maintaining pseudo count and adding it to count values to deal with zero-probabilities.
5)	Text-pre-processing: We are removing punctuations and converting all the upper cases to lower cases to make model more accurate.

**Program Description**
Initially we used Naïve Bayes classifier from scikit learn to understand the benchmark of the model, the model had in-built support to deal with low probabilities and zero probabilities. Then we made a generic model which would mimic the approach Multinomial Naïve Bayes classifier takes. Instead of coding for specific class our aim was to make program which could run any binary classification problem hence we wrote a generic code which involved using both Bag of words and Naïve Bayes approach. We achieved 85.30 percentage accuracy after performing text pre-processing and Laplace smoothing along with dealing with small probability values. Our program implements a Naïve Bayes class which has all the required functions.

pre-process string(str-data): This function performs text pre-processing and returns pre-processed string.
load_file(filename): This function is required to dealing with training and testing file.	
bag_of_words(text,index): This function iterates over given string and gives count of each word in the given string.
train(text,labels): This function trains the model, it computes Bag of words for each category and computes denominator, prior probabilities for each class.
prob(test_message): This function calculates posterior probabilities of the given testing data.
test(test_data): This function is used to calculate class labels for each word in the test data.
classifier(train_data,test_data): This function is used to send respective values to methods in the Naïve Bayes Class.

**References**:
Unfolding Naïve Bayes from Scratch ! | by Aisha Javed | Towards Data Science
https://towardsdatascience.com/unfolding-naïve-bayes-from-scratch-2e86dcae4b01


Sentiment Analysis using Bag of Words model | Olukunle Owolabi (tufts.edu)
https://sites.tufts.edu/olukunleowolabi/2020/02/13/sentiment-analysis-using-bag-of-words-model/

Enumerate() in Python - GeeksforGeeks
https://www.geeksforgeeks.org/enumerate-in-python/

Implementing a Naive Bayes classifier for text categorization in five steps | by Gustavo Chávez | Towards Data Science
https://towardsdatascience.com/implementing-a-naive-bayes-classifier-for-text-categorization-in-five-steps-f9192cdd54c3


Text Classification and Naive Bayes (stanford.edu)
https://web.stanford.edu/~jurafsky/slp3/slides/7_NB.pdf

All you need to know about text preprocessing for NLP and Machine Learning - KDnuggets
https://www.kdnuggets.com/2019/04/text-preprocessing-nlp-machine-learning.html
