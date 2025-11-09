import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

# --- Define the directed graph (from your question image) ---
graph = {
    "A": [],
    "B": ["A", "C", "E", "G"],
    "C": ["D"],
    "D": ["B"],
    "E": ["H"],
    "F": [],
    "G": ["F"],
    "H": ["F"],
}

# --- BFS Implementation ---
def bfs(graph, start):
    visited = []
    queue = deque([(start, 0)])  # (node, level)
    levels = {start: 0}

    while queue:
        node, level = queue.popleft()
        if node not in visited:
            visited.append(node)
            levels[node] = level
            for neighbor in sorted(graph.get(node, [])):
                if neighbor not in visited:
                    queue.append((neighbor, level + 1))
    return visited, levels

# --- DFS Implementation ---
def dfs(graph, start, visited=None, levels=None, level=0):
    if visited is None:
        visited = []
    if levels is None:
        levels = {}

    visited.append(start)
    levels[start] = level

    for neighbor in sorted(graph.get(start, [])):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, levels, level + 1)
    return visited, levels

# --- Function to draw graph ---
def draw_graph(graph, path):
    G = nx.DiGraph()

    # Add nodes and edges
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G, seed=42)  # Position layout for consistent graph shape

    plt.figure(figsize=(7, 5))
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=["lightgreen" if node in path else "lightgray" for node in G.nodes()],
        node_size=1000,
        font_size=12,
        font_weight="bold",
        edge_color="gray",
        arrows=True,
        arrowsize=15
    )

    # Highlight traversal path with red edges
    edges_in_path = [(path[i], path[i+1]) for i in range(len(path)-1) if G.has_edge(path[i], path[i+1])]
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color="red", width=2.5)

    st.pyplot(plt.gcf())
    plt.close()

# --- Streamlit App Layout ---
st.title("🔍 Python Search Algorithms Visualization (BFS & DFS)")
st.subheader("Directed Graph Search with Visualization")

st.markdown("""
This app demonstrates **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** 
on a directed graph using alphabetical tie-breaking.
""")

# User input
algorithm = st.selectbox("Select Search Algorithm", ["Breadth-First Search (BFS)", "Depth-First Search (DFS)"])
start_node = st.selectbox("Select Starting Node", sorted(graph.keys()), index=1)

if st.button("Run Search"):
    if algorithm.startswith("Breadth"):
        path, levels = bfs(graph, start_node)
    else:
        path, levels = dfs(graph, start_node)

    # --- Show Results ---
    st.write(f"### Traversal Path:")
    st.success(" → ".join(path))

    st.write("### Node Levels:")
    for node in path:
        st.write(f"**{node}** : Level {levels[node]}")

    # --- Visualize Graph ---
    st.write("### Graph Visualization")
    draw_graph(graph, path)

    st.caption("🟩 Green = Visited nodes | 🔴 Red edges = Traversal order")

st.info("BFS explores level by level, while DFS explores depth before breadth.")
