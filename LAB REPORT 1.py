import streamlit as st
from collections import deque, defaultdict

# --- Define the directed graph (as per your question image) ---
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
            # Sort neighbors alphabetically
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

# --- Streamlit App Layout ---
st.title("🔍 Python Search Algorithms Visualization")
st.subheader("Breadth-First Search (BFS) and Depth-First Search (DFS)")

st.markdown("""
This app demonstrates **BFS** and **DFS** traversal on a directed graph with
alphabetical tie-breaking (i.e., visiting nodes alphabetically when multiple options exist).
""")

# Choose algorithm
algorithm = st.selectbox("Select Search Algorithm", ["Breadth-First Search (BFS)", "Depth-First Search (DFS)"])
start_node = st.selectbox("Select Starting Node", sorted(graph.keys()), index=1)

if st.button("Run Search"):
    if algorithm.startswith("Breadth"):
        path, levels = bfs(graph, start_node)
    else:
        path, levels = dfs(graph, start_node)

    # --- Display Results ---
    st.write(f"### Traversal Path:")
    st.success(" → ".join(path))

    st.write("### Node Levels:")
    for node in path:
        st.write(f"**{node}** : Level {levels[node]}")

    # --- Visualization (Optional Text Graph) ---
    st.write("---")
    st.write("### Graph Structure:")
    for node, edges in graph.items():
        st.write(f"**{node} → {', '.join(edges) if edges else '∅'}**")

st.info("Tip: BFS explores level by level, while DFS explores depth before breadth.")
