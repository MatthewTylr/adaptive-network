#!/usr/bin/python3
"""
Main script for the testing of an adapitive network able to close the most
appropriate routes based on situational awareness.

Usage: main.py <configuration file>
"""
# Title: main.py
# Author: Matthew Taylor (matthewtylr@gmail.com)
# Version: 0.1

# Load Appropriate Libraries
import copy
import csv
import math
import networkx as nx
import matplotlib.pyplot as plt
import operator
import random
import sys
from scipy import stats
import time
import argparse
import configparser

def main():

    parser = argparse.ArgumentParser(description="Simulator Restrictions")
    parser.add_argument('configPath', metavar='config',
                        help="the path to the simulation configuration file.")
    parser.add_argument("--DC", help="Displays Calculations Made for Each Step",
                                action="store_true")
    parser.add_argument("--meta", help="Prints Node and Edge Info", action="store_true")
    parser.add_argument("--display", help="Display Network Model", action="store_true")
    args=parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.configPath)

    # Load Config
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

    # Create Network
    net = nx.watts_strogatz_graph(spop+ipop+rpop,connectivity,rewiring)

    if args.display:
        nx.draw(net)
        plt.show()

    # Add Classes of Infection
    

if __name__ == "__main__":
    main()
