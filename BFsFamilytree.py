from collections import deque

def build_family_graph(family_data):
    """Creates a graph representation of the family tree."""
    graph = {}
    
    for card in family_data:
        person = card["Name"]
        father = card.get("Father")
        mother = card.get("Mother")

        
        if person not in graph:
            graph[person] = set()
        
        if father and father != "Unknown":
            graph[person].add(father)
            graph.setdefault(father, set()).add(person)
        
        if mother and mother != "Unknown":
            graph[person].add(mother)
            graph.setdefault(mother, set()).add(person)
        
        for child in children:
            graph[person].add(child)
            graph.setdefault(child, set()).add(person)
    
    return graph

def bfs_shortest_paths(graph, start):
    """Finds the shortest direct relationships from the starting person to everyone else."""
    queue = deque([(start, None)])  # (current person, direct parent in shortest path)
    visited = {start: None}  # Stores direct connections in shortest paths
    
    while queue:
        person, parent = queue.popleft()
        for neighbor in graph[person]:
            if neighbor not in visited:
                visited[neighbor] = person
                queue.append((neighbor, person))
    
    return visited

def mark_simplified_family_tree(family_data, bob_name):
    """Marks the most direct relationships in Bob's family tree."""
    graph = build_family_graph(family_data)
    shortest_paths = bfs_shortest_paths(graph, bob_name)
    
    marked_family_data = []
    for card in family_data:
        person = card["Name"]
        father = card.get("Father")
        mother = card.get("Mother")
        children = card.get("Children", [])
        
        marked_father = f'*{father}' if father and shortest_paths.get(person) == father else father
        marked_mother = f'*{mother}' if mother and shortest_paths.get(person) == mother else mother
        marked_children = [f'*{child}' if shortest_paths.get(child) == person else child for child in children]
        
        marked_family_data.append({"Name": person, "Father": marked_father, "Mother": marked_mother, "Children": marked_children})
    
    return marked_family_data

# Example data: a small family tree
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

# Process and display the simplified family tree
marked_tree = mark_simplified_family_tree(data, "Bob")
for entry in marked_tree:
    print(entry)

