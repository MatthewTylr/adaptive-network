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
import networkx
import operator
import random
import sys
from scipy import stats
import time
import configparser

def main():
    
