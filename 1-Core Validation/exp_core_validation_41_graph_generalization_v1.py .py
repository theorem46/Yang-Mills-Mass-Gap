"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_41_graph_generalization_v1.py .py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 14 (Universal Embedding)
Theorem Support: "Admissibility on Arbitrary Relational Graphs"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    The ultimate test of geometric universality. Applies the Solved State
    algorithm to arbitrary graph topologies (not just grids).
    
    Tests Lines, Rings, Stars, Complete Graphs, Binary Trees, Ladders,
    Bipartite Graphs, and Small World networks. Convergence on all these
    structures proves RL is a theory of *Relational* geometry, independent
    of the background manifold.

ADVERSARIAL CONDITIONS:
    - Graphs:                  10 distinct graph classes
    - Logic:                   Median value of node + neighbors

PASS CRITERIA:
    1. Convergence:            Algorithm finds a stable configuration for every graph type.

USAGE:
    python3 exp_core_val_A10_graph_generalization.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

# ============================================================
# Utilities
# ============================================================


def median_list(vals):
    s = sorted(vals)
    return s[len(s) // 2]


def dicts_equal(a, b):
    if a.keys() != b.keys():
        return False
    for k in a:
        if a[k] != b[k]:
            return False
    return True


# ============================================================
# Solve on Graph
# ============================================================


def solved_step_graph(values, adj):
    D = {}
    for v in values:
        vals = [values[v]]
        for u in adj[v]:
            vals.append(values[u])
        D[v] = median_list(vals)
    return D


def solve_graph(values, adj, max_iter=400):
    cur = dict(values)
    for _ in range(max_iter):
        D = solved_step_graph(cur, adj)
        if dicts_equal(D, cur):
            return D
        cur = D
    return None


# ============================================================
# Graph Generators
# ============================================================


def line_graph(n):
    adj = {i: [] for i in range(n)}
    for i in range(n):
        if i > 0:
            adj[i].append(i - 1)
        if i < n - 1:
            adj[i].append(i + 1)
    vals = {i: i % 5 for i in range(n)}
    return vals, adj


def ring_graph(n):
    adj = {i: [(i - 1) % n, (i + 1) % n] for i in range(n)}
    vals = {i: (i * i) % 7 for i in range(n)}
    return vals, adj


def star_graph(n):
    adj = {0: [i for i in range(1, n)]}
    for i in range(1, n):
        adj[i] = [0]
    vals = {i: i for i in range(n)}
    return vals, adj


def complete_graph(n):
    adj = {i: [j for j in range(n) if j != i] for i in range(n)}
    vals = {i: (i + 3) % 11 for i in range(n)}
    return vals, adj


def binary_tree(n):
    adj = {i: [] for i in range(n)}
    for i in range(n):
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n:
            adj[i].append(l)
            adj[l].append(i)
        if r < n:
            adj[i].append(r)
            adj[r].append(i)
    vals = {i: i % 4 for i in range(n)}
    return vals, adj


def ladder_graph(n):
    adj = {}
    for i in range(2 * n):
        adj[i] = []
    for i in range(n):
        adj[i].append(i + n)
        adj[i + n].append(i)
        if i > 0:
            adj[i].append(i - 1)
            adj[i + n].append(i + n - 1)
        if i < n - 1:
            adj[i].append(i + 1)
            adj[i + n].append(i + n + 1)
    vals = {i: (i * i) % 9 for i in range(2 * n)}
    return vals, adj


def bipartite_graph(n):
    adj = {i: [] for i in range(2 * n)}
    for i in range(n):
        for j in range(n, 2 * n):
            adj[i].append(j)
            adj[j].append(i)
    vals = {i: i % 3 for i in range(2 * n)}
    return vals, adj


def grid_graph(n, m):
    adj = {}
    idx = lambda i, j: i * m + j
    for i in range(n):
        for j in range(m):
            v = idx(i, j)
            adj[v] = []
            if i > 0:
                adj[v].append(idx(i - 1, j))
            if i < n - 1:
                adj[v].append(idx(i + 1, j))
            if j > 0:
                adj[v].append(idx(i, j - 1))
            if j < m - 1:
                adj[v].append(idx(i, j + 1))
    vals = {v: (v * v) % 7 for v in adj}
    return vals, adj


def small_world(n):
    adj = {i: [(i - 1) % n, (i + 1) % n, (i + 5) % n] for i in range(n)}
    vals = {i: (i * 3) % 13 for i in range(n)}
    return vals, adj


def cycle_of_cliques(num_cliques=6, clique_size=10):
    adj = {}
    vals = {}
    idx = 0
    cliques = []
    for _ in range(num_cliques):
        nodes = []
        for _ in range(clique_size):
            adj[idx] = []
            vals[idx] = idx % 7
            nodes.append(idx)
            idx += 1
        cliques.append(nodes)
        for u in nodes:
            for v in nodes:
                if u != v:
                    adj[u].append(v)
    for i in range(num_cliques):
        a = cliques[i][0]
        b = cliques[(i + 1) % num_cliques][0]
        adj[a].append(b)
        adj[b].append(a)
    return vals, adj


# ============================================================
# Experiment
# ============================================================


def run_one(name, vals, adj):
    print("\n---", name, "---")
    D = solve_graph(vals, adj)
    if D is None:
        print("FAIL")
        return False
    print("PASS")
    return True


def run():
    ok = True
    ok &= run_one("Line", *line_graph(50))
    ok &= run_one("Ring", *ring_graph(50))
    ok &= run_one("Star", *star_graph(50))
    ok &= run_one("Complete", *complete_graph(40))
    ok &= run_one("BinaryTree", *binary_tree(63))
    ok &= run_one("Ladder", *ladder_graph(25))
    ok &= run_one("Bipartite", *bipartite_graph(20))
    ok &= run_one("GridGraph", *grid_graph(20, 20))
    ok &= run_one("SmallWorld", *small_world(60))
    ok &= run_one("CycleOfCliques", *cycle_of_cliques())

    if ok:
        print("\nOVERALL PASS")
    else:
        print("\nOVERALL FAIL")


# ============================================================

if __name__ == "__main__":
    run()
