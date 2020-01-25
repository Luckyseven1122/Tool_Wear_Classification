# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 15:09:34 2020

@author: aboumessouer
"""

relevance_dict = {
    "Perschmann_2020-01-06": {
        "relevant_processes_i": [3,5,9,11,15,17,21,25,26,31,32,36],
        "vollnut": [1,6,3,4,6,1,7,2,5,5,2,7],
    },
    "Perschmann_2020-01-07": {
        "relevant_processes_i": [3,4,9,13,17,21,23,27,31,35,39,44,48,52,56,60,64,68,72,76,80,84,88, 93,],
        "vollnut": [1,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,5,],
    },
    "Perschmann_2020-01-08": {
        "relevant_processes_i": [1,3,4,7,11,14,18,22,26,30,34,38,42,46,50,53,],
        "vollnut": [5,1,6,7,7,7,7,7,7,7,7,7,7,7,7,1],
    },
    "Perschmann_2020-01-09": {
        "relevant_processes_i": [3,5,9,11,16,20,24,26,30,34,38,42,46,50,52,53,55,59,62,65,],
        "vollnut": [1,6,3,4,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],
    },
    "Perschmann_2020-01-10": {
        "relevant_processes_i": [0,3,7,9,13,17,21,35,37,40,43,51,55],
        "vollnut": [7,7,7,7,7,7,2,1,6,7,7,7,7],
    },
    "Perschmann_2020-01-13": {
        "relevant_processes_i": [1,5,9,13,17,19,23,27,31,35,39,43,45,49,53,57,61,65,],
        "vollnut": [7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,3],
    },
    "Perschmann_2020-01-14": {"relevant_processes_i": [71,74,78], "vollnut": [1,6,3]
    },
    
    "Perschmann_2020-01-15": {
        "relevant_processes_i": [1,5,6,15,19,21,25,28,32,34,35,36,37,38,39,40,41,42,45,49,],
        "vollnut": [4,6,1,7,2,5,5,2,7,7,7,7,7,7,7,7,7,7,7,7],
    },
    
    "Perschmann_2020-01-16": {
        "relevant_processes_i": [1,5,9,13,17,21],
        "vollnut": [7,7,7,7,7,7],
    },
}

failure_index_dict = {
    "Perschmann_2020-01-06": [],
    "Perschmann_2020-01-07": [],
    "Perschmann_2020-01-08": [1, 53],
    "Perschmann_2020-01-09": [],
    "Perschmann_2020-01-10": [21],
    "Perschmann_2020-01-13": [65],
    "Perschmann_2020-01-14": [],
    "Perschmann_2020-01-15": [],
    "Perschmann_2020-01-16": [],
}