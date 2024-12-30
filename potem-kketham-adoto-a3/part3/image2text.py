#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: Andrew Doto, adoto
# Manita Pote, potem
# Karthikeya Kethamakka, kketham
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import numpy as np

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

def get_training_arrays(letters):
    arrays = {}
    for letter in letters.keys():
        arr = np.array([])
        for line in letters[letter]:
            arr = np.append(arr,np.array([1 if p == "*" else 0 for p in line]), axis = 0)
        arrays[letter] = arr
    
    return arrays

def get_test_array(letter):
    array = np.array([])
    for line in letter:
        array = np.append(array, np.array([1 if p == "*" else 0 for p in line]), axis = 0)
    
    return array

def get_class(train, test):
    train_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    probs = np.array([])
    for index, letter in enumerate(train.keys()):
        matches = (test == train[letter]).sum()
        mismatches = (CHARACTER_HEIGHT * CHARACTER_WIDTH) - (test == train[letter]).sum()
        probs = np.append(probs, .99 * (matches / (CHARACTER_HEIGHT * CHARACTER_WIDTH)) + 0)
        
    best_match_ix = np.argmax(probs)
    
    return train_letters[best_match_ix]

def simple_model(train_set, test_set):
    prediction = ""
    train_arrays = get_training_arrays(train_set)
    for l in test_set:
        test_array = get_test_array(l)
        best_match = get_class(train_arrays, test_array)[0]
        prediction += best_match
    
    return prediction

def read_data(fname):
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = [w for w in line.split()[0::2]]
        exemplars += data

    return exemplars

def read_data2(fname):
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = [w for w in line.split()]
        exemplars += data

    return exemplars

def get_probs(txt):
    train_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    sentences = []
    sentence = ""
    for word in txt:
        if word == ".":
            sentence = sentence.rstrip()
            sentence += word
            sentences.append(sentence)
            sentence = ""
        elif word == ',':
            sentence = sentence.rstrip()
            sentence += word + " "
        elif word == '``':
            sentence += word
        elif word == "''":
            sentence = sentence.rstrip()
            sentence += word + " "
        elif word in ['The', 'the', "It", 'it']:
            continue
        else:
            sentence += word + " "
    lstr = " ".join(sentences)
    
    #print(lstr[0:30])
    
    tr = {}
    letter_counts = {}
    for char in train_letters:
        transitions = []
        #for sentence in sentences:
        for index, letter in enumerate(lstr):
            if letter not in letter_counts.keys():
                letter_counts[letter] = 1
            letter_counts[letter] += 1
            if index + 1 == len(lstr):
                break
            if letter == char:
                transitions.append(lstr[index+1])
        
        trprobs = {}
        for letter in transitions:
            if letter not in trprobs.keys():
                trprobs[letter] = transitions.count(letter)/len(transitions)#/letter_counts[letter]
        tr[char] = trprobs
    
    init = {}
    initials = []
    for sentence in sentences:
        initials.append(sentence[0])
        
    for letter in initials:
        if letter not in init.keys():
            init[letter] = initials.count(letter) / len(initials)
    
    return tr, init, letter_counts

def get_test_arrays(letters):
    arrays = {}
    for letter in range(len(letters)):
        arr = np.array([])
        for line in letters[letter]:
            arr = np.append(arr,np.array([1 if p == "*" else 0 for p in line]), axis = 0)
        arrays[letter] = arr
    
    return arrays

def viterbi(train_arrays, test_arrays, tr, init):
    train_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    prediction = ""
    t_min1= ()

    for l in test_arrays:
        if l == 0:
            probs = np.array([])
            for letter in train_letters:
                pct_match = (test_arrays[0] == train_arrays[letter]).sum() / (CHARACTER_HEIGHT * CHARACTER_WIDTH)
                matches = (test_arrays[0] == train_arrays[letter]).sum()
                probs = np.append(probs, (.99 * pct_match*2) * init[letter] if letter in init.keys() else 1e-50)
                #probs = np.append(probs, matches * init[letter] if letter in init.keys() else 1e-50)
                #print("Letter: ", letter, "| Emission: ", (.98 * pct_match), "| Initial Prob: ", init[letter] if letter in init.keys() else 1e-100)
            
            pred_letter = train_letters[np.argmax(probs)]
            prediction += pred_letter
            t_min1 = (pred_letter, np.max(probs))
            #print(t_min1)
        else:    
            probs = np.array([])
            for letter in train_letters:
                pct_match = (test_arrays[l] == train_arrays[letter]).sum() / (CHARACTER_HEIGHT * CHARACTER_WIDTH)
                matches = (test_arrays[l] == train_arrays[letter]).sum()
                probs = np.append(probs, t_min1[1] * (.99 * pct_match*2) * tr[t_min1[0]][letter] if letter in tr[t_min1[0]].keys() else 1e-50)
                
            pred_letter = train_letters[np.argmax(probs)]
            prediction += pred_letter
            t_min1 = (pred_letter, np.max(probs))
            #print(t_min1)
    return prediction
    

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

simple_pred = simple_model(train_letters, test_letters)

train_arrays = get_training_arrays(train_letters)
test_arrays = get_test_arrays(test_letters)

tr, init, letter_counts = get_probs(read_data(train_txt_fname))

hmm_pred = viterbi(train_arrays, test_arrays, tr, init)

## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!

# The final two lines of your output should look something like this:
print("Simple: " + simple_pred)
print("   HMM: " + hmm_pred) 


