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
CMPUT 331 Assignment 8 Problem 2 Student Solution
March 2025
Author: <Your name here>
"""

from sys import flags
from a8p1 import vigenereKeySolver, decryptVigenere

def hackVigenere(ciphertext: str):
    """
    return a string containing the key to the cipher
    """
    bestKey = ''
    bestScore = -1

    for keylen in range(1, 11):
        keys = vigenereKeySolver(ciphertext, keylen)
        key = keys[0]

        plaintext = decryptVigenere(ciphertext, key)

        score = 0
        for ch in plaintext:
            if ch in "ETAOIN":
                score += 1

        if score > bestScore:
            bestScore = score
            bestKey = key

    return bestKey

def test():
    # hackVigenere Tests
    ciphertext = "ANNMTVOAZPQYYPGYEZQPFEXMUFITOCZISINELOSGMMOAETIKDQGSYXTUTKIYUSKWYXATLCBLGGHGLLWZPEYXKFELIEUNMKJMLRMPSEYIPPOHAVMCRMUQVKTAZKKXVSOOVIEHKKNUMHMFYOAVVMITACZDIZQESKLHARKAVEUTBKXSNMHUNGTNKRKIETEJBJQGGZFQNUNFDEGUU"
    key = hackVigenere(ciphertext)
    assert key == "MAGIC"

    ciphertext = "AQNRXXXSTNSKCEPUQRUETZWGLAQIOBFKUFMGWIFKSYARFJSFWSPVXHLEMVQXLSYFVDVMPFWTMVUSIVSQGVBMAREKEOWVACSGYXKDITYSKTEGLINCMMKLKDFRLLGNERZIUGITCWJVGHMPFEXLDIGGFXUEWJIHXXJVRHAWGFYMKMFVLBKAKEHHO"
    key = hackVigenere(ciphertext)
    assert key == "SECRET"

    ciphertext = "JDMJBQQHSEZNYAGVHDUJKCBQXPIOMUYPLEHQFWGVLRXWXZTKHWRUHKBUXPIGDCKFHBZKFZYWEQAVKCQXPVMMIKPMXRXEWFGCJDIIXQJKJKAGIPIOMRXWXZTKJUTZGEYOKFBLWPSSXLEJWVGQUOSUHLEPFFMFUNVVTBYJKZMUXARNBJBUSLZCJXETDFEIIJTGTPLVFMJDIIPFUJWTAMEHWKTPJOEXTGDSMCEUUOXZEJXWZVXLEQKYMGCAXFPYJYLKACIPEILKOLIKWMWXSLZFJWRVPRUHIMBQYKRUNPYJKTAPYOXDTQ"
    key = hackVigenere(ciphertext)
    assert key == "QWERTY"

if __name__ == "__main__":
    test()