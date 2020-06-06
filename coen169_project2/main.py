import csv
import math
import sys as Sys
import time
import numpy

import rec
from rec import Methods
from pearson_correlation import *
from cosine_similarity import *

ROWS = 200
COLS = 1000
HIGH = 5
TRAINER = [[0 for x in range(COLS)] for y in range(ROWS)]
RATINGS = [] 
PREDICTED_RATINGS = []

def start(method=None):
    global PREDICTED_RATINGS
    global RATINGS
    start = time.time()
    
    for index, rec in enumerate(RATINGS):
        rating = 0
        if rec[2] == 0:
            if method == Methods.cosine_sim:
                rating = cosine_sim(rec[0], rec[1]) 
            elif method == Methods.pearson:
                rating = pearson(rec[0], rec[1]) 
            elif method == Methods.p_iuf:
                rating = p_iuf(rec[0], rec[1]) 
            elif method == Methods.pearson_case:
                rating = pearson_case(rec[0], rec[1]) 
            elif method == Methods.item_cos:
                rating = item_cos(rec[0], rec[1]) 
            elif method == Methods.custom:
                rating = custom(rec[0], rec[1]) # userid, movieid
            PREDICTED_RATINGS.append(([rec[0]] + [rec[1]] + [rating]))

def main():
    global TRAINER
    global RATINGS
    global HIGH

    TRAINER = rec.reader("train.txt", "\t")

    response = 1
    while response != 0:
        option_text = """Choose test:
            (1)test5.txt
            (2)test10.txt
            (3)test20.txt
            (0) quit\n> """
        response = input(option_text)

        read_file = ""
        out_file = ""
        if response == '1':
            read_file = "test5.txt"
            HIGH = 5
            out_file = "result5.txt"
        elif response == '2':
            read_file = "test10.txt"
            HIGH = 10
            out_file = "result10.txt"
        elif response == '3':
            read_file = "test20.txt"
            HIGH = 20
            out_file = "result20.txt"
        elif response == '0':
            break
        else:
            print("Error")
            continue 

        del RATINGS[:]
        del PREDICTED_RATINGS[:]
        RATINGS = rec.reader(read_file, " ")

        option = 1
        while option != 0:
            algorithm_text = """Choose algorithm
            (1) cosine_similarity
            (2) pearson
            (3) p_iuf
            (4) p_case_mod
            (5) item_based_c
            (6) custom 
            (0) Quit\n>"""
            option = input(algorithm_text)
            print("Calculating...")
            method = Methods.cosine_similarity
            if option == '1':
                method = Methods.pearson
            elif option == '2':
                method = Methods.p_iuf
            elif option == '3':
                method = Methods.pearson_case_mod
            elif option == '4':
                method = Methods.cosine_similarity
            elif option == '5':
                method = Methods.item_based_c
            elif option == '6':
                method = Methods.custom
            elif option == '0': 
                break
            else:
                print("Error")
                continue 

            start(method)
            print("\nFinished. Check results in " + out_file)
            write_file(out_file, PREDICTED_RATINGS, " ")


if __name__ == '__main__':
    main()