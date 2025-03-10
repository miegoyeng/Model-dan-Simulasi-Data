import numpy as np
import matplotlib.pyplot as plt

def generate_marbles(num_marbles, radius):
    return np.random.uniform(-radius, radius, num_marbles), np.random.uniform(-radius, radius, num_marbles)

def calculate_distances(x, y):
    return np.sqrt(x**2 + y**2)

def count_inside_circle(distances, radius):
    return np.sum(distances <= radius)

def estimate_pi(num_inside, num_marbles):
    return (num_inside / num_marbles) * 4, num_inside / num_marbles

def plot_simulation(num_marbles, radius, x, y, inside_circle, estimated_pi, probability):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)
    
    ax.add_patch(plt.Rectangle((-radius, -radius), 2*radius, 2*radius, fill=False, color='blue', linewidth=2))
    ax.add_patch(plt.Circle((0, 0), radius, fill=False, color='red', linewidth=2))
    
    ax.scatter(x[inside_circle], y[inside_circle], color='green', s=5, label='Inside Circle')
    ax.scatter(x[~inside_circle], y[~inside_circle], color='orange', s=5, label='Outside Circle')
    
    text_str = f"Inside: {np.sum(inside_circle)}\nOutside: {num_marbles - np.sum(inside_circle)}"
    ax.text(-radius, radius * 0.8, text_str, fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7))
    
    ax.legend()
    ax.set_title(f"Monte Carlo Simulation (N={num_marbles})\nEstimated π: {estimated_pi:.4f}, Probability: {probability:.4f}")
    plt.show()

def monte_carlo_marbles(num_marbles):
    radius = 0.5 
    x, y = generate_marbles(num_marbles, radius)
    distances = calculate_distances(x, y)
    num_inside = count_inside_circle(distances, radius)
    estimated_pi, probability = estimate_pi(num_inside, num_marbles)
    inside_circle = distances <= radius
    
    plot_simulation(num_marbles, radius, x, y, inside_circle, estimated_pi, probability)
    return estimated_pi, num_inside, num_marbles - num_inside, probability


num_marbles = 5000
estimated_pi, num_inside, num_outside, probability = monte_carlo_marbles(num_marbles)

print(f"Estimasi nilai pi: {estimated_pi}")
print(f"Jumlah kelereng dalam lingkaran: {num_inside}")
print(f"Jumlah kelereng di luar lingkaran: {num_outside}")
print(f"Probabilitas masuk dalam lingkaran: {probability}")