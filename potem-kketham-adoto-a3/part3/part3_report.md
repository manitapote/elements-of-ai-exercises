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


## Part 1

### Problem formulation

