#!/usr/local/bin/python3
#
# Authors: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, April 2021
# The Viterbi and Human part of code were taken from https://github.com/srmanj/Artificial-Intelligence-geotagging-using-Viterbi/blob/master/mountain.py
# The Transission,Emission Probabilities and Naive Bayes aprroaches are my own implementation

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import numpy as np
import math


# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale, 0, filtered_y)
    return sqrt(filtered_y ** 2)


# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range(int(max(y - int(thickness / 2), 0)), int(min(y + int(thickness / 2), image.size[1] - 1))):
            image.putpixel((x, t), color)
    return image


# main program
#
(input_filename, gt_row, gt_col) = sys.argv[1:]
gt_row = int(gt_row)
gt_col = int(gt_col)

# load in image 
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))
# You'll need to add code here to figure out the results! For now,


# Approach 1-Bayes Net
bayes_ridge = np.argmax(edge_strength, axis=0)

# output answer
imageio.imwrite("output_simple.jpg", draw_edge(input_image, bayes_ridge, (0, 0, 255), 5))


# Approach 2- Viterbi Algorithm

# Transition Probability
def trans_prob_fun(edge_strength, row, col, State_prob):
    row_ed, col_ed = edge_strength.shape
    trans_prob = []
    i = 0
    while i < row_ed:
        if row == i:
            k = -np.log(0.75)
        elif row == i + 1 or row == i - 1:
            k = -np.log(0.375)
        elif row == i + 2 or row == i - 2:
            k = -np.log(0.1875)
        else:
            k = -np.log(0.1)
        trans_prob.append(State_prob[(i, col - 1)][0] + k)
        i = i + 1
    return trans_prob


row_ed, col_ed = edge_strength.shape
grad = 0
grad2 = 0
for i in range(row_ed):
    grad = grad + edge_strength[i][0]
for i in range(row_ed):
    for j in range(col_ed):
        grad2 = grad2 + edge_strength[i][j]

grad = grad2 / grad


# Emission Probability
def emi_prob_fun(edge_strength, row, col):
    est = math.log10(grad) - log10(10)
    k = (row_ed / np.round(est, 1))
    prob = 1 / int(row_ed - k)
    if row < int(k):
        return -np.log((edge_strength[row, col] / sum(edge_strength[:, col])))
    else:
        return -np.log((edge_strength[row, col] / sum(edge_strength[:, col])) * prob)


# Code from https://github.com/srmanj/Artificial-Intelligence-geotagging-using-Viterbi/blob/master/mountain.py starts Here

def Viterbi_probability(edge_strength, w):
    col_ed = edge_strength.shape[1]
    row_ed = edge_strength.shape[0]
    col_range = arange(1, col_ed)
    row_range = arange(0, row_ed)
    State_prob = {}
    i = 0
    while i < row_ed:
        State_prob[(i, 0)] = (w[i] * emi_prob_fun(edge_strength, i, 0), "")
        i = i + 1
    for c in col_range:
        for r in row_range:
            t_prob = trans_prob_fun(edge_strength, r, c, State_prob)
            e_prob = emi_prob_fun(edge_strength, r, c)
            prob_val = t_prob[np.argmin(t_prob)] + e_prob
            path = State_prob[(np.argmin(t_prob), c - 1)][1] + " " + str(
                np.argmin(t_prob))
            State_prob[(r, c)] = (prob_val, path)
    fin_col = []
    for i in row_range:
        fin_col.append(State_prob[(i, edge_strength.shape[1] - 1)][0])
    fin_path = np.argmin(fin_col)
    fin_path = State_prob[(fin_path, edge_strength.shape[1] - 1)][1].split(" ")
    start = 1
    fin_path = fin_path[start:]
    fin_path = [int(i) for i in fin_path]
    return fin_path


path_hmm = np.empty(row_ed)
z = -np.log(1 / row_ed)
path_hmm.fill(z)
hmm_path = Viterbi_probability(edge_strength, path_hmm)

# output
imageio.imwrite("output_hmm.jpg", draw_edge(input_image, hmm_path, (255, 0, 0), 5))


# Approach 3 Human-Input
def human_viterbi(edge_strength, gt_col, gt_row):
    p_1 = np.arange(0, gt_col)
    p_2 = np.arange(gt_col, col_ed)
    part_1 = edge_strength[:, p_1]
    part_2 = edge_strength[:, p_2]
    part_1 = flip(part_1, 1)
    human_line = np.empty(row_ed)
    human_line.fill(1)
    human_line[gt_row] = 1 / 100
    back = -1
    human_part1 = Viterbi_probability(part_1, human_line)[::back]
    human_part2 = Viterbi_probability(part_2, human_line)
    return human_part1[:back] + human_part2


human_final = human_viterbi(edge_strength, gt_col, gt_row)

imageio.imwrite("output_human.jpg", draw_edge(input_image, human_final, (0, 255, 0), 5))

# Code from https://github.com/srmanj/Artificial-Intelligence-geotagging-using-Viterbi/blob/master/mountain.py ends here
