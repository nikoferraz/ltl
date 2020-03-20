import itertools
import copy

# Takes a list of integers shipments and an int capacity and returns a list of shipments that best fit the given capacity.
def get_optimal_load(capacity, shipments):
    # Get all unique combinations of shipments that are less than or equal to the truck's capacity.
    combinations = [el for i in range(len(shipments), 0, -1) for el in itertools.combinations(shipments, i) if sum(el) <= capacity]
    maximum, index, result = 0, 0 , 0
    # Test each combination.
    for combination in combinations:
        total = sum(combination)
        if total > maximum:
            maximum = total
            result = index
        index += 1
    return [] if combinations == [] else list(combinations[result])

def remove_loaded(loaded, shipments):
    for load in loaded: shipments.remove(load) if load in shipments else None
    return shipments

def distribute_shipments(trucks, shipments):
    if trucks == []:
        return [[]]
    shipments_cp = copy.copy(shipments)
    if len(trucks) == 1:
        return [get_optimal_load(trucks[0], shipments_cp)]
    optimal_shipment = []
    trucks_cp = copy.copy(trucks)
    truck_arrangements = list(itertools.permutations(trucks, len(trucks))) # Get all possible arrangements of the trucks.
    truck_arrangements = [list(x) for x in truck_arrangements] # Convert to lists.
    current_shipment = []
    index = 0
    maximum = 0
    capacity_filled = 0
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
    # Sort the optimal_shipment to match the order of the original trucks list and return it.
    for i in range(len(trucks)):
        for truck in optimal_shipment:    
            if truck[0] == trucks[i]:
                result.append(truck[1])
    filled = [sum(capacity) for capacity in result]
    return result