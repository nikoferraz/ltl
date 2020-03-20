---
title: Mastery Logistics LTL Assignment
author: Nick Ferraz
ms.date: [03/20/2020]
description: A multiple knapsacks problem for LTL shipments.
---

## Installation

Clone with SSH: **git@github.com:nikoferraz/ltl.git**

OR

Clone with HTTPS: **https://github.com/nikoferraz/ltl.git**

OR 

[Download ZIP from repo](https://github.com/nikoferraz/ltl) --- don't forget to unzip the folder :-)

## Getting Started

You will need the following:

1. Python 3.6.3 or later. You can download it [from here](https://www.python.org/downloads/).
2. A command line tool/shell such as CMD or Terminal.

## Running Tests and the Assignment Code

1) From the command line, navigate to the ltl directory.
2) To run tests type "python test.py" in the shell.
3) To run the ltl assignment type "python ltl_assignment". This will run the code and print the result.

## Project Structure and Code


### The Project Tree

```
ltl/
├── ltl
│   └── __init__.py
├── ltl_assignment.py
├── README.md
└── test.py
```

* The ltl module contains the business logic.
* ltl_assignment.py imports the distribute_shipment method from the ltl module, and prints the result of calling the method using the shipments and trucks variables.
* test.py contains the unit tests for each of the three functions in the ltl modules.

### The Code

Below we will look at each of the function in the ltl module. First we will take a look at the function as a whole and, when appropriate, describe what it does, then look at each of the components step by step.

NOTE: The source code contains comments which are omitted here to avoid redundancy.

#### get_optimal_load(capacity, shipments)
    
This function takes an int *capacity* and and an list of ints *shipments* and returns an list of ints with the optimal shipments for the given capacity. It is an implementation of the classical knapsack problem.

```python
def get_optimal_load(capacity, shipments):
    combinations = [el for i in range(len(shipments), 0, -1) for el in itertools.combinations(shipments, i) if sum(el) <= capacity]
    maximum, index, result = 0, 0 , 0
    for combination in combinations:
        total = sum(combination)
        if total > maximum:
            maximum = total
            result = index
        index += 1
    return [] if combinations == [] else list(combinations[result])
```

1) The first line stores all possible non-repeat combinations of shipments that are less than or equal to the truck capacity.
2) Next we initialize all of our variables.
3) The for loop iterates through every combination and stores the index of the one that has a maximum sum of shipments.
4) In the last line, the return value will look to see if there is a valid combination, and if so return that, otherwise return an empty list.

#### remove_loaded(loaded, shipments)

This simple helper function takes an list of ints *loaded* and an list of ints *shipments* and returns a list containing all elements in shipments minus the elements in loaded.

```python
def remove_loaded(loaded, shipments):
    for load in loaded: shipments.remove(load) if load in shipments else None
    return shipments
```

#### distribute_shipments(trucks, shipments)

This function takes a list of integers *trucks*, containing the capacity for each truck, and a list of integers *shipments*, containing the required capacity for each shipment. It returns a two-dimensional list containing lists of integers that represent the optimal distribution of shipments for each truck in the order it was given. This is an implementation of the multiple knapsacks problem.


```python
def distribute_shipments(trucks, shipments):
    if trucks == [] or shipments == []:
        return [[]]
    shipments_cp = copy.copy(shipments)
    if len(trucks) == 1:
        return [get_optimal_load(trucks[0], shipments_cp)]
    optimal_shipment = []
    trucks_cp = copy.copy(trucks)
    truck_arrangements = list(itertools.permutations(trucks, len(trucks)))
    current_shipment = []
    index, maximum, capacity_filled = 0, 0, 0
    for arrangement in truck_arrangements:
        current_shipment.append([])
        capacity_filled = 0
        for truck in arrangement:  
            loaded = get_optimal_load(truck, shipments_cp)
            current_shipment[index].append((truck, loaded) )
            shipments_cp = remove_loaded(loaded, shipments_cp)
            capacity_filled += sum(loaded)
        if capacity_filled > maximum:
            maximum = capacity_filled
            optimal_shipment = current_shipment[index]
        index += 1
        shipments_cp = copy.copy(shipments)
    result = []
    for i in range(len(trucks)):
        for truck in optimal_shipment:    
            if truck[0] == trucks[i]:
                result.append(truck[1])
    return result
```
Let's go through this function step by step:

##### Lines 1-5

Rather than having an if-else block I chose to use two separate if statements. The first one is a simple optimization that catches empty lists and returns an empty nested list. The second if statement is also meant to optimize the code by avoiding unnecessary computation if all that is needed is to get the optimal shipments for a single truck.

Line 3, ```shipments_cp = copy.copy(shipments)```, is a necessary step if we want to avoid mutating the original data that was passed to our function, since Python passes variables by reference.

##### Lines 6-10

Lines 6 and 10 are just initializing variables. Line 7 uses the same idea as line 3, to avoid mutating data.

Line 8, however, does something more interesting:

```python
truck_arrangements = list(itertools.permutations(trucks, len(trucks)))
```
Here we are using itertools library permutations function to get every possible non-repeat combination of the trucks list. This will be critical later because it will allow us to find the optimal shipment configuration. If we took the trucks as they are passed in and we start to load the shipments, there is no guarantee that we would get the optimal distribution for all shipments. For instance, if we have a a truck with less capacity and a truck with higher capacity, depending on how many shipments we have and how large they are, we might need to load the truck with smaller capacity first to make sure we don't waste space.

##### Lines 11-23

Because we are solving for multiple trucks we need to run the **get_optimal_load** function for each truck in each possible order of trucks. Unfortunately this brute force method is not very efficient, but it's the best way to ensure that we have an optimal distribution of shipments. To get the optimal distribution we need to keep track of each possible distribution and specifically the one that uses the truck capacity to carry the most shipments. This is what we are doing in lines 19 through 21.

We could stop there and have the function return the optimal distribution for all shipments and trucks. However, since we had to iterate through all possible combinations of trucks it is quite possible that the optimal solution is not in the order which was passed to the function. One way around that is to keep track of shipment distribution for each truck capacity, which we do in line 16 when we create an tuple of the truck capacity and the list of optimal shipments for that truck:

```python 
current_shipment[index].append((truck, loaded) )
```

##### Lines 26-31

While it would be ok to have the function return a tuple using that structure we go one extra step to return the result as a list of shipments for each truck in the order that was given by the trucks argument:

```python
for i in range(len(trucks)):
        for truck in optimal_shipment:    
            if truck[0] == trucks[i]:
                result.append(truck[1])
    return result
```