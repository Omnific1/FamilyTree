
#
# A little script to untangle a family tree.
# The goal is to take a bunch of family data and, starting from one person,
# figure out the most direct bloodline (parents, grandparents, etc.) for everyone.
# It uses a graph and a classic Breadth-First Search (BFS) to find the shortest paths.
#

from collections import deque
import json

def build_family_graph(family_data):
    """
    Turns our list of family data into a proper graph.

    Think of it like a social network map. Each person is a 'node', and we draw
    a line connecting them to their parents and children. We use an "undirected"
    graph because the relationship between a parent and child goes both ways.
    """
    graph = {}
    for card in family_data:
        person = card["Name"]
        # This is a handy way to make sure a person exists in our graph,
        # creating an empty spot for their connections if they're new.
        graph.setdefault(person, set())

        # Connect the person to their parents.
        for parent_type in ["Father", "Mother"]:
            parent = card.get(parent_type)
            # Make sure the parent exists and isn't just "Unknown".
            if parent and parent != "Unknown":
                # It's a two-way street: the person is connected to the parent,
                # and the parent is connected to the person.
                graph[person].add(parent)
                graph.setdefault(parent, set()).add(person)

        # Now, do the same for their children.
        for child in card.get("Children", []):
            graph[person].add(child)
            graph.setdefault(child, set()).add(person)

    return graph

def find_shortest_path_tree(graph, start_node):
    """
    This is the core of our logic: a Breadth-First Search (BFS).

    Starting from one person, it explores the graph layer by layer to find the
    shortest path to everyone else. The result is a 'predecessor' map, which
    is basically a breadcrumb trail. For any person, it tells you which person
    came just before them on the shortest path from the start_node.
    """
    # If the starting person isn't even in our graph, we can't do much.
    if start_node not in graph:
        return {}

    # The queue holds the people we still need to visit. We start with just our main person.
    queue = deque([start_node])
    
    # This dictionary will store our breadcrumb trail.
    # The starting person has no predecessor, so we mark it as None.
    predecessors = {start_node: None}

    while queue:
        # Grab the next person from the front of the line.
        current_person = queue.popleft()
        
        # Look at all their direct connections (neighbors).
        for neighbor in graph[current_person]:
            # If we haven't found a path to this neighbor yet, this must be the shortest one!
            if neighbor not in predecessors:
                # So, we record that we got to the 'neighbor' from the 'current_person'.
                predecessors[neighbor] = current_person
                # And add the neighbor to the back of the line to be processed later.
                queue.append(neighbor)

    return predecessors

def mark_direct_lineage(family_data, start_person_name):
    """
    Puts it all together to mark up our family tree.

    It builds the graph, finds the shortest paths from our starting person,
    and then goes through the original data, putting a '*' next to any
    relationship that's part of that direct lineage.
    """
    graph = build_family_graph(family_data)
    predecessors = find_shortest_path_tree(graph, start_person_name)
    
    if not predecessors:
        print(f"Warning: Starting person '{start_person_name}' not found in data.")
        return family_data

    marked_family_data = []
    for card in family_data:
        person = card["Name"]
        # It's good practice to work on a copy, so we don't accidentally
        # change the list while we're looping over it.
        new_card = card.copy()

        # --- The Key Logic ---
        # A relationship between Person A and Person B is "direct" if A is the
        # predecessor of B in our shortest-path tree, OR if B is the predecessor of A.
        # We have to check both directions to catch the whole path.

        # Check and mark the father relationship.
        father = card.get("Father")
        if father and (predecessors.get(person) == father or predecessors.get(father) == person):
            new_card["Father"] = f'*{father}'

        # Check and mark the mother relationship.
        mother = card.get("Mother")
        if mother and (predecessors.get(person) == mother or predecessors.get(mother) == person):
            new_card["Mother"] = f'*{mother}'

        # Go through the children and mark them if they're on the direct path.
        marked_children = []
        for child in card.get("Children", []):
            if predecessors.get(child) == person or predecessors.get(person) == child:
                marked_children.append(f'*{child}')
            else:
                marked_children.append(child)
        new_card["Children"] = marked_children

        marked_family_data.append(new_card)

    return marked_family_data

def main():
    """
    This is where we run the whole thing.
    """
    # Here's our sample family data. It's a bit tangled.
    data = [
        {"Name": "Alice", "Father": "Arlo", "Mother": "Madeline", "Children": []},
        {"Name": "Bob", "Father": "Charlie", "Mother": "Eve", "Children": []},
        {"Name": "Eve", "Father": "Oliver", "Mother": "Aurora", "Children": ["Bob"]},
        {"Name": "Charlie", "Father": "Jack", "Mother": "Luna", "Children": ["Bob"]},
        {"Name": "Madeline", "Father": "Jack", "Mother": "Aurora", "Children": ["Alice"]},
        {"Name": "Arlo", "Father": "Oscar", "Mother": "Isla", "Children": ["Alice"]},
        {"Name": "Oliver", "Father": "Hugo", "Mother": "Rose", "Children": ["Eve"]},
        {"Name": "Luna", "Father": "Oscar", "Mother": "Isla", "Children": ["Charlie"]},
        {"Name": "Aurora", "Father": "Hugo", "Mother": "Rose", "Children": ["Eve", "Madeline"]},
        {"Name": "Jack", "Father": "Oscar", "Mother": "Rose", "Children": ["Charlie", "Madeline"]},
        {"Name": "Hugo", "Father": "Unknown", "Mother": "Unknown", "Children": ["Oliver", "Aurora"]},
        {"Name": "Rose", "Father": "Unknown", "Mother": "Unknown", "Children": ["Oliver", "Aurora", "Jack"]},
        {"Name": "Isla", "Father": "Unknown", "Mother": "Unknown", "Children": ["Luna", "Arlo"]},
        {"Name": "Oscar", "Father": "Unknown", "Mother": "Unknown", "Children": ["Luna", "Jack", "Arlo"]}
    ]

    # Let's trace the family tree starting from "Bob".
    marked_tree = mark_direct_lineage(data, "Bob")
    
    # Using the json library to print this out makes it way easier to read.
    print(json.dumps(marked_tree, indent=4))


# This is a standard Python convention. It means the `main()` function
# will only run when you execute this file directly (e.g., `python family_tree.py`),
# not when you import it into another script.
if __name__ == "__main__":
    main()
