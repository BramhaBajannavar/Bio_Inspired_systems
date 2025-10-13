import numpy as np
import time

# Parameters for the simulation
grid_size = 20  # Grid size (20x20) for better visibility in terminal
prob_tree = 0.6  # Probability of a tree being present in a cell
prob_fire_start = 0.01  # Probability that a tree catches fire initially
max_steps = 50  # Number of steps to simulate (feel free to adjust)
burn_prob = 0.2  # Probability that fire spreads to neighboring trees (slower spread)

# Initialize the forest grid
def initialize_forest(grid_size, prob_tree, prob_fire_start):
    forest = np.random.choice([0, 1], size=(grid_size, grid_size), p=[1 - prob_tree, prob_tree])
    # Add some fire at random locations
    fire_starts = np.random.choice([0, 2], size=(grid_size, grid_size), p=[1 - prob_fire_start, prob_fire_start])
    forest = np.where(fire_starts == 2, 2, forest)
    return forest

# Update function for the simulation
def update_forest(forest):
    new_forest = forest.copy()

    # For each tree (state 1) check if it can catch fire (spread from neighboring burning trees)
    for i in range(1, forest.shape[0] - 1):
        for j in range(1, forest.shape[1] - 1):
            if forest[i, j] == 1:  # Tree is present
                # Check neighboring cells
                neighbors = [forest[i-1, j], forest[i+1, j], forest[i, j-1], forest[i, j+1]]
                if 2 in neighbors and np.random.rand() < burn_prob:  # If fire is in the neighborhood
                    new_forest[i, j] = 2  # The tree catches fire

            elif forest[i, j] == 2:  # If the tree is burning, it burns out
                new_forest[i, j] = 0  # Burned out (empty cell)
    
    return new_forest

# Function to print the forest grid in terminal
def print_forest(forest):
    for row in forest:
        print(' '.join(['T' if x == 1 else 'F' if x == 2 else '.' for x in row]))
    print("\n")

# Initialize the forest
forest = initialize_forest(grid_size, prob_tree, prob_fire_start)

# Run the simulation and print output for each step
for step in range(max_steps):
    print(f"Step {step + 1}")
    print_forest(forest)
    
    # Update the forest for the next step
    forest = update_forest(forest)
    
    # Wait for a moment before showing the next step
    time.sleep(0.5)  # Adjust the sleep time for speed of simulation (in seconds)
