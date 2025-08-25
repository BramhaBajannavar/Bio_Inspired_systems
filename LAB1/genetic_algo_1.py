import numpy as np

# Define the fitness function (we'll use the square of the chromosome value)
def fitness_function(chromosome):
    return int(chromosome, 2) ** 2  # Square of the integer value of the chromosome

# Genetic Algorithm Parameters
mutation_rate = 0.1
crossover_point = 3  # Random point in chromosome for crossover

# Initialize Population with user input
def initialize_population(population_size, initial_population=None):
    # If the user provides an initial population, use that. Otherwise, generate randomly.
    if initial_population is not None:
        return initial_population[:population_size]  # Slice to the desired population size
    else:
        # Generate random population if no initial chromosomes are provided
        chromosome_length = len(initial_population[0]) if initial_population else 5  # Default length if no input
        return [''.join(np.random.choice(['0', '1']) for _ in range(chromosome_length)) for _ in range(population_size)]

# Evaluate Fitness for each individual
def evaluate_population(population):
    fitness_values = [fitness_function(chromosome) for chromosome in population]
    return fitness_values

# Select Mating Pool based on Fitness
def select_mating_pool(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [f / total_fitness for f in fitness_values]
    mating_pool = np.random.choice(population, size=population_size, p=probabilities, replace=True)
    return mating_pool

# Crossover: Create offspring by crossing over parents
def crossover(parents):
    crossover_point = np.random.randint(1, len(parents[0]))
    child1 = parents[0][:crossover_point] + parents[1][crossover_point:]
    child2 = parents[1][:crossover_point] + parents[0][crossover_point:]
    return child1, child2

# Mutation: Flip bits in the chromosome based on mutation rate
def mutate(chromosome):
    mutated = ''.join(
        bit if np.random.rand() > mutation_rate else '1' if bit == '0' else '0' for bit in chromosome
    )
    return mutated

# Main Genetic Algorithm Loop
def genetic_algorithm(population_size, initial_population=None):
    population = initialize_population(population_size, initial_population)
    previous_best_fitness = -1  # Initialize the previous best fitness as a non-optimal value
    convergence_count = 0  # Track generations with no change in best fitness

    generations = 50  # Max number of generations to run the GA

    for generation in range(generations):
        # Evaluate Fitness for each individual in the population
        fitness_values = evaluate_population(population)
        best_fitness = max(fitness_values)
        
        # Convergence Check: If the best fitness hasn't changed for 2 generations, stop
        if best_fitness == previous_best_fitness:
            convergence_count += 1
        else:
            convergence_count = 0
        
        # Stop if convergence condition is met (no change in best fitness for 2 generations)
        if convergence_count >= 2:
            print(f"Convergence reached at generation {generation + 1}. Best fitness: {best_fitness}")
            break

        previous_best_fitness = best_fitness

        # Selection: Choose mating pool
        mating_pool = select_mating_pool(population, fitness_values)
        
        # Crossover and Mutation: Create new population
        new_population = []
        for i in range(0, population_size, 2):
            parents = np.random.choice(mating_pool, 2, replace=False)
            child1, child2 = crossover(parents)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))

        population = new_population

        # Track best fitness for the current generation
        print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

    # Final output: best solution found
    best_chromosome = population[fitness_values.index(best_fitness)]
    print(f"Best chromosome found: {best_chromosome} with fitness {best_fitness}")

# Example usage: You can specify initial population size and actual chromosomes
initial_population = ['01100', '11001', '10011', '00101']  # Example user input
population_size = 4  # Example population size (this can be any number)

# Run the Genetic Algorithm
genetic_algorithm(population_size, initial_population)
