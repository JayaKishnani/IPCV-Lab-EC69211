# -*- coding: utf-8 -*-
"""Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WIMZGG-mN1Ri7QgmH1Y6iGyF-plid0SX
"""

from math import ceil
from collections import Counter

pi = 3.1415

LUM = [
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 48, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
]

CHR = [
    [17, 18, 24, 47, 99, 99, 99, 99],
    [18, 21, 26, 66, 99, 99, 99, 99],
    [24, 26, 56, 99, 99, 99, 99, 99],
    [47, 66, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99]
]

def rgb2ycc(a):
    ans = [[[0]*3]*len(a[0])]*len(a)
    for i in range(len(a)):
        for j in range(len(a[0])):
            r = a[i][j][0]
            g = a[i][j][1]
            b = a[i][j][2]
            ans[i][j][0] = 0.299*r + 0.587*g + 0.114*b
            ans[i][j][1] = -0.169*r -0.331*g +0.5*b +128
            ans[i][j][2] = 0.5*r -0.419*g -0.081*b + 128
    return ans

def chromasub(a):
    ans = [[0]*len(a[0])]*len(a)
    ###using a 4:2:0 subsampling
    for i in range(int(len(a)/2)):
        for j in range(int(len(a[0])/2)):
            ans[2*i][2*j] = (a[2*i][2*j]+a[2*i+1][2*j] + a[2*i][2*j+1] + a[2*i+1][2*j+1])/4
            ans[2*i][2*j+1] = ans[2*i+1][2*j] = ans[2*i+1][2*j+1] = ans[2*i][2*j]
    return ans[::2]

def zeroCentral(a):
    for i in range(len(a)):
      for j in range(len(a[0])):
        a[i][j] -= 128
    return a

def lumtrans(a):
    ans = [[0]*len(a[0])]*len(a)
    for i in range(len(a)):
        for j in range(len(a[0])):
            ans[i][j] = round(a[i][j]/LUM[i][j])
    return ans

def chrtrans(a):
    ans = [[0]*len(a[0])]*len(a)
    for i in range(len(a)):
        for j in range(len(a[0])):
            ans[i][j] = round(a[i][j]/CHR[i][j])
    return ans

from math import sqrt, cos
def dct(a):
    ans = [[0]*8]*8
    for x in range(8):
        for y in range(8):
            sum = 0
            for i in range(8):
                for j in range(8):
                    li = 1
                    if(i == 0):
                        li = 1/sqrt(2)
                    lj = 1
                    if(j == 0):
                        lj = 1/sqrt(2)

                    sum += li*lj*cos(pi*x*(2*i+1)/16)*cos(pi*y*(2*j+1)/16)*a[i][j]
    return ans

def get_freq_dict(a):
    data = Counter(a)
    ans = {k: d / len(a) for k, d in data.items()}
    return ans

def get_lowprob(p):
    sorted_p = sorted(p.items(), key=lambda x: x[1])
    return sorted_p[0][0], sorted_p[1][0]

def serialize(a):
    hor = 0
    vert = 0
    i = 0
    ans = [0]*64

    while (vert < 8) and (hor < 8):
        if ((hor + vert) % 2) == 0:  # going up
            if vert == 0:
                ans[i] = a[vert][hor]  # first line
                if hor == 8:
                    vert += 1
                else:
                    hor += 1
                i += 1
            elif (hor == 7) and (vert < 8):  # last column
                ans[i] = a[vert][hor]
                vert += 1
                i += 1
            elif (vert > 0) and (hor < 7):  # all other cases
                ans[i] = a[vert][hor]
                vert -= 1
                hor += 1
                i += 1
        else:  # going down
            if (vert == 7) and (hor <= 7):  # last line
                ans[i] = a[vert][hor]
                hor += 1
                i += 1
            elif hor == 0:  # first column
                ans[i] = a[vert][hor]
                if vert == 7:
                    hor += 1
                else:
                    vert += 1
                i += 1
            elif (vert < 7) and (hor > 0):  # all other cases
                ans[i] = a[vert][hor]
                vert += 1
                hor -= 1
                i += 1
        if (vert == 7) and (hor == 7):  # bottom right element
            ans[i] = a[vert][hor]
            break
    return ans

def trim(a):
    trimmed = a.copy()
    while(len(trimmed) > 0 and trimmed[-1] == 0):
      trimmed.pop(-1)
    if len(trimmed) == 0:
        trimmed = [0]
    return trimmed

def run_length(a):
    ans = []
    cnt = 0
    eob = ("EOB",)

    for i in range(len(a)):
        for j in range(len(a[0])):
            trimmed = trim(a[i])
            if j == len(trimmed):
                ans.append(eob)
                break
            #initial component
            if i == 0 and j == 0:
                ans.append((int(trimmed[j]).bit_length(), trimmed[j]))
            #difference from previous components
            elif j == 0:
                diff = int(a[i][j] - a[i - 1][j])
                if diff != 0:
                    ans.append((diff.bit_length(), diff))
                else:
                    ans.append((1, diff))
                cnt = 0
            elif trimmed[j] == 0:
                cnt += 1
            else:
                ans.append((cnt, int(trimmed[j]).bit_length(), trimmed[j]))
                cnt = 0
        if not (ans[len(ans) - 1] == eob):
            ans.append(eob)
    return ans

def huff(p: dict) -> dict:
    if len(p) == 2:
        return dict(zip(p.keys(), ['0', '1']))

    #new subtree
    p_prime = p.copy()
    a1, a2 = get_lowprob(p)
    p1, p2 = p_prime.pop(a1), p_prime.pop(a2)
    p_prime[a1 + a2] = p1 + p2

    #recursive call
    c = huff(p_prime)
    ca1a2 = c.pop(a1 + a2)
    c[a1], c[a2] = ca1a2 + '0', ca1a2 + '1'

    return c



    ###############################Next part of code###########################################




import cv2 ##solely for the purpose of input and used for nothing else
imgOriginal = cv2.imread('plants.png', cv2.IMREAD_COLOR)

#############RGB TO YCbCr###############
img = rgb2ycc(imgOriginal.tolist())
width = len(img[0])
height = len(img)
y = [[0]*width]*height
for i in range(height):
  for j in range(width):
    y[i][j] = img[i][j][0]

cr = [[0]*width]*height
for i in range(height):
  for j in range(width):
    cr[i][j] = img[i][j][1]

cb = [[0]*width]*height
for i in range(height):
  for j in range(width):
    cb[i][j] = img[i][j][2]
# size of the image in bits before compression
prevBits = len(y) * len(y[0]) * 8 + len(cb) * len(cb[0]) * 8 + len(cr) * len(cr[0]) * 8
prevBits /= 16

##########CENTRALIZE #########################
y = zeroCentral(y)
cr = zeroCentral(cr)
cb = zeroCentral(cb)

######CHROMA DOWNSAMPLING ##############
crf = chromasub(cr)
cbf = chromasub(cb)

########PADDING###################################
yWidth, yLength = ceil(len(y[0]) / 8) * 8, ceil(len(y) / 8) * 8
yPadded = [[0]*yWidth]*yLength
for i in range(len(y)):
    for j in range(len(y[0])):
        yPadded[i][j] = y[i][j]

cWidth, cLength = ceil(len(cbf[0]) / 8) * 8, ceil(len(cbf) / 8) * 8
crPadded = [[0]*cWidth]*cLength
cbPadded = [[0]*cWidth]*cLength
for i in range(len(crf)):
    for j in range(len(crf[0])):
        crPadded[i][j] += crf[i][j]
        cbPadded[i][j] += cbf[i][j]

#############GETTING THE NUMBER OF BLOCKS FOR SPLITTING################
horY = int(yWidth / 8)
vertY = int(yLength / 8)
horC = int(cWidth / 8)
vertC = int(cLength / 8)

##################SERIALIZED VALUE CONTAINERS##########################
yser = []
crser = []
cbser = []

#################ITERATING ON EVERY 8X8 BLOCK###########################
for i in range(vertY):
    for j in range(horY):
        block = []
        for k in range(8*i, 8*i+8):
          block.append(yPadded[k][8*j:8*j+8])
        mdct = dct(block)
        quant = [[0]*8]*8
        for x in range(8):
          for y in range(8):
            quant[x][y] = round(mdct[x][y] / LUM[x][y])
        yser.append(serialize(quant))


for i in range(vertC):
    for j in range(horC):
        block = []
        for k in range(8*i, 8*i+8):
          block.append(crPadded[k][8*j:8*j+8])
        mdct = dct(block)
        for x in range(8):
          for y in range(8):
            quant[x][y] = round(mdct[x][y] / CHR[x][y])
        crser.append(serialize(quant))

        block = []
        for k in range(8*i, 8*i+8):
          block.append(cbPadded[k][8*j:8*j+8])
        mdct = dct(block)
        for x in range(8):
          for y in range(8):
            quant[x][y] = round(mdct[x][y] / CHR[x][y])
        cbser.append(serialize(quant))

############RUN LENGTH ENCODING -> HUFFMAN (ENTROPY CODING)########################
yrun = run_length(yser)
crrun = run_length(crser)
cbrun = run_length(cbser)

yfreq = get_freq_dict(yrun)
crfreq = get_freq_dict(crrun)
cbfreq = get_freq_dict(cbrun)

yhuff = huff(yfreq)
crhuff = huff(crfreq)
cbhuff = huff(cbfreq)

# calculate the number of bits to transmit for each channel
# and write them to an output file
file = open("CompressedImage_plants.bin", "w")
ytrans = str()
for value in yrun:
    ytrans += yhuff[value]

crtrans = str()
for value in crrun:
    crtrans += crhuff[value]

cbtrans = str()
for value in cbrun:
    cbtrans += cbhuff[value]

if file.writable():
    file.write(ytrans + "\n" + crtrans + "\n" + cbtrans)
file.close()

compBits = len(ytrans) + len(crtrans) + len(cbtrans)
print("Compression Ratio is " + str(round(prevBits / (compBits), 1)))