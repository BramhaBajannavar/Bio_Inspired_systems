import random
import numpy as np

# Sample distance matrix between cities (symmetric)
distance_matrix = np.array([
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
])

num_cities = len(distance_matrix)
population_size = 6      # Number of candidate routes in each generation
generations = 100        # Number of generations to evolve
mutation_rate = 0.1      # Probability of mutation per individual

# Generate a random route (a permutation of cities)
def create_route():
    route = list(range(num_cities))
    random.shuffle(route)
    return route

# Create initial population of random routes
def initial_population():
    return [create_route() for _ in range(population_size)]

# Calculate total distance of a route
def route_distance(route):
    distance = 0
    for i in range(num_cities):
        from_city = route[i]
        to_city = route[(i + 1) % num_cities]  # Wrap around to first city
        distance += distance_matrix[from_city][to_city]
    return distance

# Fitness function (inverse of distance)
def fitness(route):
    return 1 / route_distance(route)

# Tournament selection: choose the best from a random subset
def selection(population):
    tournament_size = 3
    selected = []
    for _ in range(population_size):
        tournament = random.sample(population, tournament_size)
        tournament = sorted(tournament, key=lambda r: fitness(r), reverse=True)
        selected.append(tournament[0])
    return selected

# Ordered Crossover (OX) for producing valid children routes
def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(num_cities), 2))
    child = [None] * num_cities

    # Copy the selected slice from parent1 to child
    child[start:end+1] = parent1[start:end+1]

    # Fill remaining positions with cities from parent2 in order
    p2_index = 0
    for i in range(num_cities):
        if child[i] is None:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]
    return child

# Mutation by swapping two cities with a given probability
def mutate(route):
    if random.random() < mutation_rate:
        i, j = random.sample(range(num_cities), 2)
        route[i], route[j] = route[j], route[i]

# Main Genetic Algorithm loop
def genetic_algorithm():
    population = initial_population()
    best_route_ever = None
    best_distance_ever = float('inf')

    for gen in range(generations):
        # Selection step
        selected = selection(population)

        # Crossover and mutation to create next generation
        next_generation = []
        for i in range(0, population_size, 2):
            parent1 = selected[i]
            parent2 = selected[(i + 1) % population_size]

            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)

            mutate(child1)
            mutate(child2)

            next_generation.extend([child1, child2])

        # Keep population size fixed
        population = next_generation[:population_size]

        # Track best route in current generation
        current_best_route = min(population, key=route_distance)
        current_best_distance = route_distance(current_best_route)

        if current_best_distance < best_distance_ever:
            best_distance_ever = current_best_distance
            best_route_ever = current_best_route

        print(f"Generation {gen+1}: Best Distance = {current_best_distance:.2f}")

    return best_route_ever, best_distance_ever

# Run the algorithm and print results
best_route, best_distance = genetic_algorithm()
print("\nBest route found:", best_route)
print("Distance of best route:", best_distance)
