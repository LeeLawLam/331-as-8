#!/usr/bin/env python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.1
# Copyright 2025 <<Insert your name here>>
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
# ---------------------------------------------------------------
"""
CMPUT 331 Assignment 8 Problem 1 Student Solution
March 2025
Author: <Your name here>
"""


from sys import flags
import re
import itertools


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

ENG_LETT_FREQ = {'E': 0.1270, 'T': 0.0906, 'A': 0.0817, 'O': 0.0751, 'I': 0.0697, 'N': 0.0675, 'S': 0.0633, 'H': 0.0609, 
                 'R': 0.0599,  'D': 0.0425, 'L': 0.0403, 'C': 0.0278, 'U': 0.0276, 'M': 0.0241, 'W': 0.0236, 'F': 0.0223, 
                 'G': 0.0202,  'Y': 0.0197, 'P': 0.0193, 'B': 0.0129, 'V': 0.0098, 'K': 0.0077, 'J': 0.0015, 'X': 0.0015, 
                 'Q': 0.0010,  'Z': 0.0007}

def getLetterFrequency(message: str):
    # Returns a dictionary of letter frequencies in the message
    # Divide each letter count by total number of letters in the message to get it's frequency
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 
                   'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 
                   'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 
                   'Y': 0, 'Z': 0}

    message = message.upper()
    total = 0

    for ch in message:
        if ch in LETTERS:
            letterCount[ch] += 1
            total += 1

    if total == 0:
        return letterCount

    for ch in LETTERS:
        letterCount[ch] /= total

    return letterCount

def getSubsequences(ciphertext: str, keylen: int):
    # This function takes in a ciphertext as a string and a key length as a int for its parameters
    # This function will return list of lists containing the characters in each subsequence
    subsequences = []

    for i in range(keylen):
        subsequence = []
        for j in range(i, len(ciphertext), keylen):
            subsequence.append(ciphertext[j])
        subsequences.append(subsequence)

    return subsequences

def calculateTopIMC(subsequence: str):
    # Given a string, this function will calculate and return a list containing all 26 keys and their IMC values
    # Return a list of tuples containing key, IMC pairs from largest IMC to smallest
    scores = []

    if isinstance(subsequence, list):
        subsequence = ''.join(subsequence)

    for key in LETTERS:
        decrypted = decryptVigenere(subsequence, key)
        freq = getLetterFrequency(decrypted)

        imc = 0
        for ch in LETTERS:
            imc += freq[ch] * ENG_LETT_FREQ[ch]

        scores.append((key, imc))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def decryptVigenere(ciphertext: str, key: str):
    # This function takes in a vigenere ciphertext and its key as the parameters
    # The decrypted message will be returned
    
    decryption = ''
    key = key.upper()
    keyIndex = 0

    for ch in ciphertext:
        if ch.upper() in LETTERS:
            cnum = LETTERS.find(ch.upper())
            knum = LETTERS.find(key[keyIndex % len(key)])
            pnum = (cnum - knum) % 26
            decryption += LETTERS[pnum]
            keyIndex += 1
        else:
            decryption += ch

    return decryption

def vigenereKeySolver(ciphertext: str, keylength: int):
    """
    return a list of the ten most likely keys
    """
    # Remove nonalphabetic characters in ciphertext
    ciphertext = re.compile('[^A-Z]').sub('',ciphertext.upper())


    subsequences = getSubsequences(ciphertext, keylength)

    topLetters = []
    for subsequence in subsequences:
        imcList = calculateTopIMC(subsequence)
        topLetters.append(imcList[:3])

    allKeys = []

    for combo in itertools.product(*topLetters):
        key = ''
        totalIMC = 0

        for letter, imc in combo:
            key += letter
            totalIMC += imc

        allKeys.append((key, totalIMC))

    allKeys.sort(key=lambda x: x[1], reverse=True)

    bestKeys = []
    for key, score in allKeys[:5]:
        bestKeys.append(key)

    return bestKeys

def test():

    # decrypt Vigenere test
    assert decryptVigenere("gijmskoxmmqnexrrvcoxfbicyrc", "key").lower() == 'welcometocmputthreethreeone'

    # getLetterFrequency test
    assert getLetterFrequency("BEEF")['B'] == 0.25

    # getSubsequences test
    assert getSubsequences("UNIVERSITY", 3) == [["U", "V", "S", "Y"], ["N", "E", "I"], ["I", "R", "T"]]

    # calculateTopIMC test
    assert calculateTopIMC("QQQABCQQQ")[0][0] == "M"

    # vigenereKeySolver Tests
    ciphertext = "QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECHOSNYXXLSPMYKVQXJTDCIOMEEXDQVSRXLRLKZHOV"
    best_keys = vigenereKeySolver(ciphertext, 5)
    assert best_keys[0] == "EVERY"

    ciphertext = "VYCFNWEBZGHKPWMMCIOGQDOSTKFTEOBPBDZGUFUWXBJVDXGONCWRTAGYMBXVGUCRBRGURWTHGEMJZVYRQTGCWXF"
    best_keys = vigenereKeySolver(ciphertext, 6)
    assert best_keys[0] == "CRYPTO"

if __name__ == "__main__":
    test()

