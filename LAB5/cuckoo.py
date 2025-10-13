import random

# Helper Functions
def generate_random_tour(n):
    """Generate a random permutation of cities"""
    tour = list(range(n))
    random.shuffle(tour)
    return tour

def evaluate_tour(tour, dist_matrix):
    """Calculate total distance of a tour"""
    distance = 0
    for i in range(len(tour) - 1):
        distance += dist_matrix[tour[i]][tour[i + 1]]
    distance += dist_matrix[tour[-1]][tour[0]]  # Return to start
    return distance

def levy_flight(tour):
    """Apply discrete mutation to simulate Levy flight"""
    new_tour = tour[:]
    n = len(tour)

    move_type = random.choice(["swap", "reverse", "shuffle"])

    if move_type == "swap":
        i, j = random.sample(range(n), 2)
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

    elif move_type == "reverse":
        i, j = sorted(random.sample(range(n), 2))
        new_tour[i:j] = reversed(new_tour[i:j])

    elif move_type == "shuffle":
        i, j = sorted(random.sample(range(n), 2))
        segment = new_tour[i:j]
        random.shuffle(segment)
        new_tour[i:j] = segment

    return new_tour

def get_worst_indices(fitness, m):
    """Return indices of m worst solutions"""
    return sorted(range(len(fitness)), key=lambda x: fitness[x], reverse=True)[:m]

# Cuckoo Search Algorithm for TSP
def cuckoo_search_tsp(dist_matrix, num_nests=15, pa=0.25, max_iter=500):
    n = len(dist_matrix)

    # Initialization
    nests = [generate_random_tour(n) for _ in range(num_nests)]
    fitness = [evaluate_tour(tour, dist_matrix) for tour in nests]

    best_index = min(range(num_nests), key=lambda i: fitness[i])
    best_nest = nests[best_index]
    best_fitness = fitness[best_index]

    # Iterations
    for t in range(1, max_iter + 1):
        for i in range(num_nests):
            new_tour = levy_flight(nests[i])
            new_fitness = evaluate_tour(new_tour, dist_matrix)

            j = random.randint(0, num_nests - 1)
            if new_fitness < fitness[j]:
                nests[j] = new_tour
                fitness[j] = new_fitness

        # Abandon worst nests
        num_abandon = int(pa * num_nests)
        worst_indices = get_worst_indices(fitness, num_abandon)

        for k in worst_indices:
            nests[k] = generate_random_tour(n)
            fitness[k] = evaluate_tour(nests[k], dist_matrix)

        # Update best solution
        current_best_index = min(range(num_nests), key=lambda i: fitness[i])
        if fitness[current_best_index] < best_fitness:
            best_fitness = fitness[current_best_index]
            best_nest = nests[current_best_index]

        # Print progress for each iteration
        print(f"Iteration {t}: Best Distance = {best_fitness}, Best Tour = {[c + 1 for c in best_nest]}")

    return best_nest, best_fitness

# Main Program (User Input)
if __name__ == "__main__":
    n = int(input("Enter number of cities: "))

    print("Enter distance matrix (row by row):")
    dist_matrix = [list(map(int, input().split())) for _ in range(n)]

    num_nests = int(input("Enter number of nests (e.g., 20): "))
    pa = float(input("Enter discovery probability Pa (0 to 1, e.g., 0.25): "))
    max_iter = int(input("Enter maximum iterations (e.g., 1000): "))

    best_tour, best_distance = cuckoo_search_tsp(dist_matrix, num_nests=num_nests, pa=pa, max_iter=max_iter)

    print("\nFinal Best Tour:", [c + 1 for c in best_tour])
    print("Final Best Distance:", best_distance)
