# Initialize Parameters
num_cities = 5                   # Number of cities
population_size = 10              # Number of candidate routes
generations = 50                  # Number of generations
mutation_rate = 0.1               # Probability of mutation per individual
crossover_rate = 0.8              # Crossover probability

# Sample Distance Matrix for 5 cities (symmetric)
distance_matrix = [
    [0, 2, 9, 10, 3], 
    [1, 0, 6, 4, 7], 
    [15, 7, 0, 8, 2], 
    [6, 3, 12, 0, 5], 
    [10, 8, 4, 9, 0]
]

# Initialize Population with Random Routes (permutations of cities)
def create_route():
    route = list(range(num_cities))  # [0, 1, 2, 3, 4]
    random.shuffle(route)  # Randomize order
    return route

# Initial population of random routes
def initial_population():
    return [create_route() for _ in range(population_size)]

# Calculate total distance of a route based on the distance matrix
def route_distance(route):
    distance = 0
    for i in range(len(route)):
        from_city = route[i]
        to_city = route[(i + 1) % num_cities]  # Wrap around to the first city
        distance += distance_matrix[from_city][to_city]
    return distance

# Fitness function (lower distance is better, hence we use inverse)
def fitness(route):
    return 1 / route_distance(route)

# Tournament Selection: Select the best individuals
def selection(population):
    selected = []
    for _ in range(population_size):
        tournament = random.sample(population, 3)  # Randomly select 3 routes
        tournament = sorted(tournament, key=lambda r: fitness(r), reverse=True)
        selected.append(tournament[0])  # Choose best of 3
    return selected

# Crossover using Partially Matched Crossover (PMX)
def crossover(parent1, parent2):
    if random.random() < crossover_rate:
        start, end = sorted(random.sample(range(num_cities), 2))
        child1 = [None] * num_cities
        child2 = [None] * num_cities

        # Copy the crossover section from both parents
        child1[start:end+1] = parent1[start:end+1]
        child2[start:end+1] = parent2[start:end+1]

        # Fill remaining positions
        for i in range(num_cities):
            if child1[i] is None:
                for gene in parent2:
                    if gene not in child1:
                        child1[i] = gene
                        break

            if child2[i] is None:
                for gene in parent1:
                    if gene not in child2:
                        child2[i] = gene
                        break

        return child1, child2
    return parent1, parent2

# Mutation: Swap two cities with a given probability
def mutate(route):
    if random.random() < mutation_rate:
        i, j = random.sample(range(num_cities), 2)
        route[i], route[j] = route[j], route[i]
    return route

# Main Genetic Algorithm Loop
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

            child1, child2 = crossover(parent1, parent2)
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

        print(f"Generation {gen + 1}: Best Distance = {current_best_distance:.2f}")

    return best_route_ever, best_distance_ever

# Run the algorithm and print results
best_route, best_distance = genetic_algorithm()
print("\nBest route found:", best_route)
print("Distance of best route:", best_distance)
