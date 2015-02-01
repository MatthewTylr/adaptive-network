#!/usr/bin/python3
"""
Main script for the testing of an adapitive network able to close the most
appropriate routes based on situational awareness.

Usage: main.py <configuration file> <additional flags>
"""
# Title: main.py
# Author: Matthew Taylor (matthewtylr@gmail.com)
# Version: 0.1

# Load Appropriate Libraries ---------------------------------------------------

import copy
import csv
import math
import networkx as nx
import matplotlib.pyplot as plt
import operator
import random
import sys
from scipy import stats
import numpy
from time import strftime, localtime
import argparse
import configparser

# Description: Random Event Function
# I: Probability of Something Happening.
# O: Returns one if true, 0 is false.
def chance(x):
    chance_set = [0]*100
    chance_add = int(numpy.ceil(x*100))
    chance_num = numpy.floor(numpy.random.uniform(0,100,chance_add))
    for a in range(0,chance_add):
        apply_num = int(chance_num[a])
        chance_set[apply_num] = 1
    chance_return_num = numpy.floor(numpy.random.uniform(0,100,1))
    chance_return = chance_set[int(chance_return_num)]
    return chance_return

# Description: Main Function
def main():

    parser = argparse.ArgumentParser(description="Simulator Restrictions")
    parser.add_argument('configPath', metavar='config',
                        help="the path to the simulation configuration file.")
    parser.add_argument("--DC", help="Displays Calculations Made for Each Step",
                                action="store_true")
    parser.add_argument("--meta", help="Prints Node and Edge Info",
                                action="store_true")
    parser.add_argument("--display", help="Display Network Model",
                                action="store_true")
    args=parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.configPath)

    # Load Config --------------------------------------------------------------

    print("Loading Configuration File")
    time = int(config['simulation']['time'])
    connectivity = int(config['simulation']['connectivity'])
    rewiring = float(config['simulation']['rewiring'])
    beta = float(config['simulation']['beta'])
    gamma = float(config['simulation']['gamma'])
    spop = int(config['classes']['spop'])
    ipop = int(config['classes']['ipop'])
    rpop = int(config['classes']['rpop'])
    restrict = int(config['restrictions']['restrict'])
    delay = int(config['restrictions']['delay'])

    # Create Network------------------------------------------------------------

    net = nx.watts_strogatz_graph(spop+ipop+rpop,connectivity,rewiring)

    if args.display:
        nx.draw(net)
        plt.show()

    # Add Network Attributes ---------------------------------------------------

    # Seed Network with Susceptible
    for a in net.nodes():
        net.node[a]['state'] = 'S'
    # If Infectious is Greater than 1
    sample = numpy.floor(numpy.random.uniform(0,(spop+ipop+rpop),(ipop)))
    for a in sample:
        net.node[a]['state'] = 'I'

    # Create Data File ---------------------------------------------------------

    current_time = strftime("%Y-%m-%d-%H-%M-%S", localtime())
    data_file = open("SIR_{0}.csv".format(current_time),"w")
    data_file.write("timestep, s, i, r\n")

    # Simulation----------------------------------------------------------------

    for a in range(0,time):

        # Individuals Become Infectious

        for b in net.nodes():

            if net.node[b]['state'] == 'I':
                neighbors = net.neighbors(b)

                for d in range(0,len(neighbors)):
                    specific_neighbor = neighbors[d]
                    get_sick = chance(beta)

                    if net.node[specific_neighbor]['state'] == 'R':
                        get_sick = 0

                    if get_sick == 1:
                        net.node[specific_neighbor]['state'] = 'I'


        # Individuals Recover

        for b in net.nodes():

            if net.node[b]['state'] == 'I':
                recover = chance(gamma)

                if recover == 1:
                    net.node[b]['state'] = 'R'

        # Count and Display
        num_s = 0
        num_i = 0
        num_r = 0
        for b in net.nodes():
            state = net.node[b]['state']

            if state == 'S':
                num_s += 1

            if state == 'I':
                num_i += 1

            if state == 'R':
                num_r += 1

        print("Timestep = {0}, S = {1}, I = {2}, R = {3}".format(a,num_s,num_i,num_r))

        # Commit Data For Timestep to Dataset
        timeset_data = "{0}, {1}, {2}, {3}".format(a, num_s, num_i, num_r)
        data_file.write(timeset_data + "\n")


        if num_i == 0:
            break

if __name__ == "__main__":
    main()
