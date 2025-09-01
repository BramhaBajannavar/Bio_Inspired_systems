import numpy as np

# 1. DEFINE THE "MOUNTAIN RANGE" (FITNESS FUNCTION)
# The peak of this mountain is at (2, 3) with an altitude of 100.
def get_altitude(coords):
    """
    Calculates the altitude at a given (x, y) coordinate.
    This function creates a smooth peak we want to find.
    Higher values are better.
    """
    x, y = coords[0], coords[1]
    peak_x, peak_y = 2, 3
    # An inverted paraboloid: 100 - ((x-2)^2 + (y-3)^2)
    return 100 - np.power(x - peak_x, 2) - np.power(y - peak_y, 2)

# --- TAKE USER INPUT FOR SIMULATION PARAMETERS ---
print("--- ⛰️ Hiker Simulation Setup ---")
try:
    n_hikers = int(input("Enter the number of hikers in the group (default: 20): "))
except ValueError:
    print("Invalid input. Using 20 hikers.")
    n_hikers = 20

try:
    n_iterations = int(input("Enter the number of search iterations (default: 50): "))
except ValueError:
    print("Invalid input. Using 50 iterations.")
    n_iterations = 50
print("\n--- Starting The Hike ---")

# --- PSO ALGORITHM PARAMETERS ---
w = 0.5   # Inertia: tendency to keep walking in the same direction
c1 = 0.8  # Cognitive: trust in one's own memory
c2 = 0.9  # Social: trust in the group's best-found spot
bounds = [(-10, 10), (-10, 10)] # The boundaries of the map

# --- INITIALIZE THE HIKERS (PARTICLES) ---
# Each hiker's current coordinates (position)
positions = np.random.rand(n_hikers, 2) * 20 - 10
# Each hiker's current direction and speed (velocity)
velocities = np.random.rand(n_hikers, 2) * 0.1

# Each hiker remembers their personal best spot and its altitude
pbest_positions = np.copy(positions)
pbest_altitudes = np.array([get_altitude(p) for p in positions])

# The group knows the overall best spot found by any hiker
gbest_index = np.argmax(pbest_altitudes) # Note: argmax for maximization
gbest_position = pbest_positions[gbest_index]
gbest_altitude = pbest_altitudes[gbest_index]

# --- SETUP AND RUN THE SIMULATION ---
# Print a nice header for the output table
print(f"\n{'Iteration':<12} {'Highest Point Found':<25} {'Max Altitude':<15}")
print("-" * 55)

# Main loop where the search happens
for i in range(n_iterations):
    for j in range(n_hikers):
        
        # UPDATE EACH HIKER'S DIRECTION AND SPEED (VELOCITY)
        r1, r2 = np.random.rand(2)
        
        cognitive_pull = c1 * r1 * (pbest_positions[j] - positions[j])
        social_pull = c2 * r2 * (gbest_position - positions[j])
        velocities[j] = w * velocities[j] + cognitive_pull + social_pull
        
        # HIKER MOVES TO A NEW POSITION
        positions[j] = positions[j] + velocities[j]
        # Ensure hikers don't walk off the map
        positions[j] = np.clip(positions[j], bounds[0][0], bounds[0][1])
        
        # HIKER CHECKS THE ALTITUDE AT THE NEW SPOT
        current_altitude = get_altitude(positions[j])
        
        # UPDATE PERSONAL BEST IF THE NEW SPOT IS HIGHER
        if current_altitude > pbest_altitudes[j]: # Note: > for maximization
            pbest_positions[j] = positions[j]
            pbest_altitudes[j] = current_altitude
            
            # UPDATE GROUP'S BEST IF THIS HIKER FOUND A NEW HIGHEST POINT
            if current_altitude > gbest_altitude: # Note: > for maximization
                gbest_position = positions[j]
                gbest_altitude = current_altitude

    # --- SHOW PROPER OUTPUT FOR THIS ITERATION ---
    pos_str = f"[{gbest_position[0]:.4f}, {gbest_position[1]:.4f}]"
    print(f"{i+1:<12} {pos_str:<25} {gbest_altitude:<15.4f}")

# --- FINAL OUTPUT ---
print("\n" + "="*55)
print("Search Complete!")
print(f"The highest peak found by the hikers is at: {gbest_position}")
print(f"Maximum altitude reached: {gbest_altitude}")
print(f"(The actual peak is at [2.0, 3.0] with an altitude of 100.0)")10
]
