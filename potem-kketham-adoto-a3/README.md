# a3

## Part-1 Part of Speech Tagging (POS):

The assignment task for this part is to find the part of speech given the word. This problem can be solved in three different ways. Here, in this assigment we tried to implement simplified approach (Naive Bayes), Hidden Markov Model (HMM) and MCMC Gibbs sampling. In this assignment there are 12 possible POS which are
['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']

### Step1: Training:
In the training phase, we maintained the matrix of transition probabilites which means what is probability of getting next POS given the current POS. For this we counted the number of times we observe POS_i+1 when we get POS_i. 

transition_probability = (count of (POS_i-1 and POS_i) / count of POS_i-1) <br />

Next we mainted the emission probability table which stores the probabiltiy of observing the word for given POS.

emission_probability = (count of word_i labelled as POS_i )/ (count of POS_i)

Next we maintained marginal probability matrix. Here I have written matrix but we implemeted with dictionary.

marginal_probability = (count of POS_i) / (total_no_words)

We maintained list of probability of starting and ending the sentence with each POS.

probability of sentence starting with given POS = (count of POS in 0 position) / (count of sentences in training data)

probability of sentence ending with given POS = (count of POS in last position in each sentence )/ (count of sentences in training data)

### step2: Methods

#### 1) Simplified (Naive Bayes):

For labelling the words with possible part of speech, we calculated the emission probability for a 
given word for each part of speech and then found maximum emission prbaility and label (POS) associated with it. 

P(s| W) = max(P(W|s_i)) where i = 0 to total unique POS

####  2) Viterbi Algorithm:

We followed the following steps for implementing viterbi algorithm

 #calculating the initial probability for step1
 - for each word as w: <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; v(w, 1) = empty list of length of total unique POS <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; for each POS as p <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; v(w, 1, p) <- probability of starting the sentence with p * emission probability of word given p for first step <br />
     
  - for each word or step i in a sentence starting from second position as w: <br />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       temp = empty list <br />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       backtracking = empty list <br />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       for each POS: <br />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;              temp = append(v(w, i-1, p_j_i-1) * transtition probability from POS_i-1 to POS_i * emission probability P(W | POS_1)) <br />
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                    where j is all possible POS in step i-1. <br />
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       v(w, i) = max(temp) <br />
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       backtracking = append(path from POS_i-1 to POS_i that has max(temp) value <br />
  
  - loop through reversed backtracking list to find find path from last word to first word <br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - there can be multiples paths to last word so we started backtracking from  <br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; the path that lead us from second last word to last word with maximum v(w, last-1) value.<br />
  - this path is the list of most probable POS for given words
  - Based on the lables and sentence we calculate the posterior probability for each POS:
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;P(s|W) = P(W|s)*P(s) / P(W) <br />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;total MAP (posteriori) probability = sum of all P(s|W) for each word <br />
      
  Choics and issues: <br />
  We encountered different problems while implementing this algorithm. There we words in testing set which were not presen in training set. For those words we assigned the emission probability of 1 for each POS. This seems have an effect of further choice of POS down the graph in algorithm. Also we had the problem of zero transition, emission probability for some of the words which made our whole probability to zero. Hence we assigned a small value of 1e-6 to zero probabiltites. <br />
  We also saw few single word sentences in testing which had to handled separately. <br />
  
 ####  3) MCMC Gibbs Sampling Algorithm:
 
 We tried to implement the Gibbs sampling for the complex Bayes Net using following algorithm:
 
 - iterations = 10000
 - sample = for random initial choices of POS for each word in sentence
 - samples = list of sample
 - probability_pos = [] (POS related with probailites)
 - for each iteration:
 -&nbsp;&nbsp;&nbsp; for each POS or i in first sample: <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; prob_dist (probability_distribution_for_each POS) = empty list <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if it is first POS: <br />
 
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; probability =  (transition probability from first POS_1 to second POS_2 ) *   (emission probability P(W_1 | POS_1) * marginal probability of POS_1 </br>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   prob_dist = append( probability ) <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if it is last sentence: <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  probability = (emission probabiity from P(W_last | POS_last) * <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (transition probability from second last POS _last-1 to POS_last 
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  prob_dist = append(probability) <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  if not last and first POS: <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; probability = (transition probability from previous POS to current POS) * (transition from current POS to next POS) * ( emission probability from current POS to word) <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; prob_dist = append(probability) <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; normalise the prob_dist: divide each element of prob_dist by sum of all element of prob_dist <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; new_pos = sample from prob_dist for i position of POS <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sample[i] = new_pos <br />
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; samples.append(sample) <br />
 -most probable labels for words list = empty list <br />
 - for each word: <br />
 &nbsp;&nbsp;&nbsp;&nbsp; count the occurance of corresponding POS in samples and get the POS for max count <br />
 &nbsp;&nbsp;&nbsp;&nbsp; most probable labels for words list = append(POS with max count) <br />
 -return  most probable labels for words list  <br />
   
  Issues: <br /><br />
  We constantly got the issue of 0 probability for this algorithm. We changed the 0 probailite to 1e-6. Afterwards the probailites were changing and the the choice from the prob_distribution was giving us different values but the count at the end was always dominated by noun. Hence, we could not figure out what was going on. All the codes have been commented in for MCMC section in the file.
  
### step3: Testing
<br />
We got the following results which is quite low.
For bc.test.tiny  <br /> <br />


![](/potem-kketham-adoto-a3/part1/test_2.png)

<br /> <br />
For bc.test data

![](/potem-kketham-adoto-a3/part1/test_1.png)

In our case, simple model seems to be doing better than HMM. Surely there seems to be some problem with our approach.


Part-2 Mountain Finding:



The assignment task for this part was to predict the ridge in the given test photograph, We were supposed to use three different approaches to find the horizon/ridge of the landmark in the given photograph this is like a feature that can be later used to find the location of a photograph according to the assignment. The assignment can be divided into four parts. One preprocessing part and three different approaches.
Pre-Processing Part:
The image has been read using the PIL module and later the image has been passed through a Sobel filter which is generally used for edge detection. The Sobel filter is essentially a discrete differentiation operator. It returns an approximate gradient of the image at a specific pixel. The features returned project the image with their edge strength.

Approach-1: We are supposed to use Bayes net to estimate the most consistent ridgeline in the whole image, We have implemented the above using the argmax function available in the numpy we can estimate the ridge from the whole image by finding out the most vibrant edge, which is what the algorithm seems to do.
Issues with Bayes net approach: Bayes net does not account for the consistency of the edges and hence we are left with multiple discrete edges in the image if the landmark(mountain) has less edge strength, In the case of normal images it seems to work fine since the ridge is both consistent and not masked by background. 
Hidden Markov Model: Most systems in nature can be implemented using Hidden Markov models. Hidden Markov Model is essentially a connected graph with various states follow Markov Model, It is also worth noting that the states also have hidden states attached to them, which impact the decision the system takes. From hereby we shall refer to the Hidden Markov model as hmm. We have modelled the whole image into a hmm graph we used the edge strength graph computed earlier to model the system. We have also computed negative log probabilities to make the problem which is minimum one into maximum.

HMM formal terms:
Transition Probability:  This is essentially like weights present in the weighted graph where the weights are the probabilities, In our approaches, we used three different types of probabilities one if the pixel is present in the same row then we assign the highest probability since we need to detect consistency in the ridgeline. We used reduced probabilities in other cases.

Emission Probability: This is essentially like the summary of each state we implemented this by computing the probability of each pixel in the row given the gradient of the particular row, we normalized the probabilities.

Viterbi Implementation:  We implemented the top-down approach of Viterbi we initially calculate the emission probability and transition probability and add all of them up to get the solution, from there we backtracked to find the path of states which in this case corresponds to the ridge or the horizon.

Approach-3:
Human Input:
We used the same functions as above except we split the edge strength at the given column values and computed the ridges separately and added them up.
The blue line denotes the Bayes net output the red line denotes the HMM output and the green one denotes the Human input approaches.
Challenges faced and improvements:
 We were not able to calculate the ridge-line consistently for the images where the background features were dominant, This poses a good challenge one way to deal with this is to employ an optimizer to calculate the emission and transition probability, also there are a lot of alternatives for Sobel filter which can do a better job like canny edge detector. Sometimes HMM and Viterbi may not provide an optimal result, deep learning models and GAN’s might do a better job at this, also there are concepts like integrating Neural Networks and HMM which also can be used. Overall the assignment was a good exercise.

References:
Viterbi algorithm - Wikipedia
Algorithms - Valhalla
How to Split Image Into Multiple Pieces in Python - Stack Overflow
Seam carving - Wikipedia
Viterbi Implemetation and Human Input-https://github.com/srmanj/Artificial-Intelligence-geotagging-using-Viterbi/blob/master/mountain.py

## Part 3

### Problem formulation

Part 3's problem is comprised of a character-recognition problem. The idea is to train two models (a simple naive bayes and a more complex HMM) to predict the letters of a scanned document. We formulated this problem in two basic parts. First, we tackled the simple model, which entailed using the pixels from the training image as the "expert" image for the emissions probability. Then we tackled the HMM, where we used a training document of text to calculated initial state and transition probabilities to add to the emissions probabilities. Then using Viterbi inference, we could then predict the characters of the test image.

### Program Description

The program that we created takes in arguments for the training image, the English text training document, and the test image. The output of the program includes two predictions for the characters of the test image, one for the simple naive bayes and one for the HMM.

**Image Processing**

The image processing part of the code was provided by the skeleton code. This takes care of the processing of the images and provides a list of lists of black and white dots.

**Pixel Arrays**

One of the first parts of development included transforming the outputs of the image processing into a structure that we could easily work with and compare pixels of an image to another image's pixel. To do this, we took advantage of NumPys arrays, which allows for broadcasting for quick operations. So, we created some functions that transform the 2-d grid of black and white dots into 1-d NumPy arrays with 1's and 0s. 

**Calculating Probabilities**

Next, we developed functions that estimate probabilities from training data. One of these functions takes in the English text source and gathers the transition and initial state probabilities from the text data. The function loops through the text, and for every letter, it looks at the letter/character right after it, and then performs the calculations for how many times a letter transitions to another. In addition, another function we created takes the numpy arrays for test image and uses broadcasting to compare the pixels elementwise. We used this comparison to then calculate the emission probabilities from that operation.

**Simple Model Classification**

This function takes the training data arrays and the test data arrays and performs the array-comparison functions we created. We then used Naive Bayes classification to calculate the training letter that best-matched the test letter in the closest way. 

**HMM Classification**

The HMM Classification builds upon the simple model and uses Viterbi inference to predict the characters of the test image. Using the emissions probabilities, transition probabilities, and the initial state probabilities calculated from other functions, it performs Viterbi inference. It loops through the test image characters and then considers the probability of transitioning from one character to the next, for every possible character. So it starts with the first letter in test image, and multiplies the emissions probability for that character times the initial state probability for that character. Once all the calculations are done, it takes the arg max of those probabilities and stores the character and probability in a variable called "T minus 1," simulating the table that is stored for the Viterbi algorithm. Then for all of succeeding characters in the image, it calculates the product of T minus 1, emissions probability, and the transition probability. Then it stores the arg max and max value and repeats until all characters in the test image are classified.

### Discussion

During the development and testing, we made some observations as well as ran into some issues that causes issues with the program. First, we observed that the simple model only performs well with the cleaner images, which is no surprise. Because this model only considers the emissions probability, all it has to make decisions is the quality of the test images matching to the training data. In addition to that, we noticed that the simple model also can confuse letters that look like numbers or other characters. For example, it can confuse the letter "l" with the number 1, and so on.

The HMM model classification was a difficult task and it does not perform how we would like. We labored to try to fix the problem in several ways. First, we tried to introduce a penalty for letters that occurred extremely and disproportionately freqently, but that strategy didn't yield results. Next, we observed that certain words like "the" and "it" were skewing the transition probabilities due to the fact that these words were very frequent. In order to address this, we took out some stop words, like "the", from the corpus when we processed the text in our function. However, that didn't solve the problem either. Despite these problems with the performance, we did take away a greater understanding of the Viterbi algorithm and the intuition behind it. That is, the algorithm is balancing the emissions probability (i.e. how close the pixels match) vs. the transition probabilities (i.e. the statistical nature of the language gathered from the training text). If the transition probability is very strong for a few characters relative to all others, it will dominate the calculation, despite the emissions probability being relatively high.
