# Simplifying Family Trees with Breadth-First Search
This project aims to simplify complex family relationships by identifying the most direct connections between an individual (Bob) and their relatives in a large, interconnected community. It utilizes a breadth-first search (BFS) algorithm to calculate the minimum number of parent-child steps required to connect Bob with each person in the community.

## Background
In this scenario, Bob lives in an isolated community on board a generation ship where everyone is related due to meticulous record-keeping over generations. He has constructed a complete family tree but seeks to simplify his understanding of these relationships by highlighting only the most direct paths between himself and other individuals.

## Overview
1. Family Tree Representation: The family tree is transformed into a graph where each person is represented as a node, and parent-child relationships are depicted as directed edges. For instance, if Alice is John's daughter, there would be an edge from John to Alice.

2. Breadth-First Search Implementation:
>> Starting Point: Begin with Bob as the central figure.
>> Queue Setup: Create a queue containing Bob and mark him as visited.
>> Distance Tracking: Use data structures like dictionaries or maps to keep track of how many steps it takes (i.e., distance) from Bob to reach each person.
The BFS algorithm works by exploring all nodes at one distance level before moving on to nodes at greater distances:

Start with Bob and explore his immediate relatives (parents and children).

Move outward in layers until all individuals have been reached.

Record the shortest path length for each person relative to Bob.

3. Marking Most Direct Relationships:
For individuals connected back to Bob via multiple equally short paths (i.e., multiple equally direct familial ties), select one path based on additional criteria or simply choose one arbitrarily.
>> Traverse this chosen path backward from that individual towards Bob.
>> Highlight these most direct connections by annotating them in the simplified tree—specifically by adding an asterisk (*) before names involved along this selected path.

## Purpose 
This approach simplifies understanding complex familial connections by focusing only on those that are most directly related according to your criteria. It helps create annotated cards for each person showing their closest relatives marked with asterisks (*), making it easier for users like Bob to quickly identify their nearest familial ties within large networks.


