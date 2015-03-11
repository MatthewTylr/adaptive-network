#!/usr/bin/python3
"""
Main script for the testing of an adapitive network able to close the most
appropriate routes based on situational awareness.

Usage: main.py <configuration file> <additional flags>
"""
# Title: main.py
# Author: Matthew Taylor (matthewtylr@gmail.com)
# Version: 0.2.2
# Version Description:
# Working Adaptive and PRER Methods Based on Betweenness.

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
import collections

def chance(x):
    chance_set = [0]*100
    chance_add = int(numpy.ceil(x*100))
    chance_num = numpy.floor(random.sample(range(100),chance_add))
    for a in range(0,chance_add):
        apply_num = int(chance_num[a])
        chance_set[apply_num] = 1
    chance_return_num = numpy.floor(numpy.random.uniform(0,100,1))
    chance_return = chance_set[int(chance_return_num)]
    if x == 1:
        chance_return = 1
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
    parser.add_argument("--run", help="Runs Algorithm",
                                action="store_true")
    parser.add_argument("--prermode", help="Mode for initial edge removal.",
                                action="store_true")
    parser.add_argument("--debug", help="Output Calculations",
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
    discovery = int(config['restrictions']['discovery'])
    prer = float(config['prersettings']['prer'])

    # Create Network------------------------------------------------------------

    net = nx.watts_strogatz_graph(spop+ipop+rpop,connectivity,rewiring)

    if args.display:
        nx.draw(net)
        plt.show()

    # Add Network Attributes ---------------------------------------------------

    # Seed Network with Susceptible
    for a in net.nodes():
        net.node[a]['state'] = 'S'
        net.node[a]['count'] = 0
    # If Infectious is Greater than 1
    sample = numpy.floor(numpy.random.uniform(0,(spop+ipop+rpop),(ipop)))
    for a in sample:
        net.node[a]['state'] = 'I'

    # Pre-Run Edge Removal
    if args.prermode:
        total_edge_count = len(net.edges())
        edge_betweenness = nx.edge_current_flow_betweenness_centrality(net)
        edge_betweenness_sort = sorted(edge_betweenness.items(), key=operator.itemgetter(1), reverse = True)
        # Remove Those Edges!
        for a in range(0,int(numpy.floor(total_edge_count*prer))):
            net.remove_edge(edge_betweenness_sort[a][0][0],edge_betweenness_sort[a][0][1])

    # Create Data File ---------------------------------------------------------

    current_time = strftime("%Y-%m-%d-%H-%M-%S", localtime())
    data_file = open("SIR_{0}.csv".format(current_time),"w")
    data_file.write("timestep, s, u, i, r, mbet\n")

    # Simulation----------------------------------------------------------------

    for a in range(0,time):

        # PRER MODE EDGE EVALUATION

        if args.prermode:

            print("Evaluating Edge Betweenness")

            mean_bet = 0
            edge_betweenness = nx.edge_current_flow_betweenness_centrality(net)

            for c in edge_betweenness:
                mean_bet += edge_betweenness[c]

            mean_bet = mean_bet/len(net.nodes())

        # Individuals Become Infectious (Unknown)

        for b in net.nodes():

            if net.node[b]['state'] == 'U' or net.node[b]['state'] == 'I':
                neighbors = net.neighbors(b)

                for d in range(0,len(neighbors)):
                    specific_neighbor = neighbors[d]
                    get_sick = chance(beta)

                    if net.node[specific_neighbor]['state'] == 'S' and get_sick == 1:
                        net.node[specific_neighbor]['state'] = 'U'

            # Infectious Recover

            if net.node[b]['state'] == 'U' or net.node[b]['state'] == 'I':
                recover = chance(gamma)

                if recover == 1:
                    net.node[b]['state'] = 'R'

        for b in net.nodes():

            if net.node[b]['state'] == 'U':
                net.node[b]['count'] += 1

            # Individuals are Recognized as Infectious

            if net.node[b]['state'] == 'U' and net.node[b]['count'] >= discovery:
                net.node[b]['state'] = 'I'

        # Algorithm --------------------------------------------------------------------------------

        if args.run:

            # Lists for Targets
            target_inf = []
            target_nei = []
            target_edges = []

            # Build Info List
            for c in net.nodes():

                # INF + Neighbors
                if net.node[c]['state'] == 'I':
                    target_inf.append(c)
                    target_nei.append(net.neighbors(c))

            target_edges = net.edges(target_inf)

            if restrict == 0:
                net.remove_edges_from(target_edges)

            else:

                print("Running Algorithm")

                # Calculate Edge Betweenness
                edge_betweenness = nx.edge_betweenness_centrality(net)

                # Create Mean Betweenness Counter

                mean_bet = 0

                # Create a Dictionary of Metrics
                edge_dict = {}

                for d in edge_betweenness:

                    target_edge_pos_id = 0

                    mean_bet += edge_betweenness[d]

                    for e in target_edges:
                        if d == e:
                            target_edge_pos_id = 1

                    if target_edge_pos_id == 1:
                        edge_dict[d] = 1, edge_betweenness[d]
                    else:
                        edge_dict[d] = 0, edge_betweenness[d]



                # Sort Dictionary
                edge_dict_sort = sorted(edge_dict.items(), key=operator.itemgetter(1), reverse = True)

                # Calculate Mean Betweenness

                mean_bet = mean_bet/len(net.nodes())

                # Remove Edges
                for d in range(0,restrict):
                    net.remove_edge(edge_dict_sort[d][0][0],edge_dict_sort[d][0][1])



        # ------------------------------------------------------------------------------------------

        # Count and Display
        num_s = 0
        num_u = 0
        num_i = 0
        num_r = 0

        for b in net.nodes():
            state = net.node[b]['state']

            if state == 'S':
                num_s += 1

            if state == 'U':
                num_u += 1

            if state == 'I':
                num_i += 1

            if state == 'R':
                num_r += 1

        print("Timestep = {0}, S = {1}, U = {2}, I = {3}, R = {4}, MBET = {5}".format(a,num_s,num_u,num_i,num_r,mean_bet))

        if args.debug:
            print("TEI =",len(target_edges),"TEITE% =",len(target_edges)/len(net.edges()))

        # Commit Data For Timestep to Dataset
        timeset_data = "{0}, {1}, {2}, {3}, {4}, {5}".format(a, num_s, num_u, num_i, num_r, mean_bet)
        data_file.write(timeset_data + "\n")

        if num_u == 0 and num_i == 0:
            break

if __name__ == "__main__":
    main()
