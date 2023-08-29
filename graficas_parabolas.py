import numpy as np
import matplotlib.pyplot as plt

# Given points
t_minus_7 = -7
t_plus_7 = 7
q_t_minus_7 = 0.85
q_t_plus_7 = 0.95

# Vertex point
t_vertex = 0
q_vertex = 1

# Set up the equations to solve for coefficients a, b, and c
A = np.array([
    [t_minus_7**2, t_minus_7, 1],
    [t_vertex**2, t_vertex, 1],
    [t_plus_7**2, t_plus_7, 1]
])

b = np.array([q_t_minus_7, q_vertex, q_t_plus_7])

# Solve the equations
coefficients = np.linalg.solve(A, b)
a, b, c = coefficients

# Quality function
def quality_function(t):
    return max(min(a * t**2 + b * t + c, 1), 0)

# Generate data for plotting
t_values = np.linspace(-10, 10, 400)
q_values = [quality_function(t) for t in t_values]
'''
# Plot the function
plt.plot(t_values, q_values, label='Quality Function')
plt.scatter([t_minus_7, t_plus_7], [q_t_minus_7, q_t_plus_7], color='red', label='Given Points')
plt.xlabel('t')
plt.ylabel('q[t]')
plt.title('Quality Function')
plt.legend()
plt.grid()
plt.show()'''


def calculate_parabola_coefficients(q_t_minus, q_t_plus):
    t_minus = -7
    t_plus = 7
    A = np.array([
        [t_minus**2, t_minus, 1],
        [0, 0, 1],
        [t_plus**2, t_plus, 1]
    ])
    
    b = np.array([q_t_minus, 1, q_t_plus])
    
    coefficients = np.linalg.solve(A, b)
    a, b, c = coefficients
    
    return a, b, c
# Calculate coefficients
a, b, c = calculate_parabola_coefficients(0.85, 0.95)

def calculate_optimal_day():

    # Generate a random day from a normal distribution with mean 0 and std 2
    optimal_day = np.random.normal(0, 2)


    return int(round(optimal_day))

def quality_function(a, b, c, t):
    return max(min(a * t**2 + b * t + c, 1), 0)

def evaluate_quality_at_optimal_day(t_optimal, q_t_minus, q_t_plus):
    a, b, c = calculate_parabola_coefficients(q_t_minus, q_t_plus)
    q_t_optimal = quality_function(a, b, c, t_optimal)
    return q_t_optimal
t = calculate_optimal_day()
t = 7
print(t)
q_t_optimal = evaluate_quality_at_optimal_day(t, 0.85, 0.95)
print("Quality at optimal day:", q_t_optimal)