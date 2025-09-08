import numpy as np
import random

# ---------- PARAMETERS ----------
NUM_ANTS = 20
NUM_ITER = 100
ALPHA = 1     # influence of pheromone
BETA = 5      # influence of heuristic (1/cost)
RHO = 0.5     # evaporation rate
Q = 100       # pheromone deposit factor

# ---------- USER INPUT ----------
n = int(input("Enter number of routers (nodes): "))

print("\nEnter the network cost matrix (0 for no link, >0 for link cost):")
cost_matrix = []
for i in range(n):
    row = list(map(int, input().split()))
    cost_matrix.append(row)

cost_matrix = np.array(cost_matrix)
pheromone = np.ones((n, n))  # initial pheromone levels

src = int(input("\nEnter source router (0 to n-1): "))
dst = int(input("Enter destination router (0 to n-1): "))

# ---------- HELPER FUNCTIONS ----------
def path_cost(path):
    """Compute total cost of a path"""
    return sum(cost_matrix[path[i]][path[i+1]] for i in range(len(path)-1))

# ---------- MAIN ACO LOOP ----------
best_path = None
best_cost = float('inf')

for iteration in range(NUM_ITER):
    all_paths = []

    for ant in range(NUM_ANTS):
        current = src
        path = [current]
        visited = set([current])

        while current != dst:
            # Possible next hops
            neighbors = [j for j in range(n) if cost_matrix[current][j] > 0 and j not in visited]
            if not neighbors:  # Dead end
                break

            # Probabilities for neighbors
            probs = []
            for j in neighbors:
                tau = pheromone[current][j] ** ALPHA
                eta = (1 / cost_matrix[current][j]) ** BETA
                probs.append(tau * eta)

            probs = np.array(probs)
            probs /= probs.sum()

            # Choose next router
            next_router = random.choices(neighbors, weights=probs)[0]
            path.append(next_router)
            visited.add(next_router)
            current = next_router

        if path[-1] == dst:
            all_paths.append(path)
            cost = path_cost(path)
            if cost < best_cost:
                best_path, best_cost = path, cost

    # Evaporation
    pheromone *= (1 - RHO)

    # Deposit pheromone
    for path in all_paths:
        cost = path_cost(path)
        deposit = Q / cost
        for i in range(len(path)-1):
            a, b = path[i], path[i+1]
            pheromone[a][b] += deposit
            pheromone[b][a] += deposit  # assume undirected

print("\nBest path from router", src, "to", dst, ":", best_path)
print("Best path cost:", best_cost)
