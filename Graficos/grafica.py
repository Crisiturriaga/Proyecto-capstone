import numpy as np
import matplotlib.pyplot as plt

# Given data
calidades = [
    [(-7, 0.85), (7, 0.95), 'C1'],
    [(-7, 0.92), (7, 0.93), 'C2'],
    [(-7, 0.91), (7, 0.87), 'C3'],
    [(-7, 0.95), (7, 0.95), 'C4'],
    [(-7, 0.85), (7, 0.85), 'C5'],
    [(-7, 0.93), (7, 0.94), 'C6']
]
mean = 0
std = 2

# Set up the equations to solve for coefficients a, b, and c
def calculate_coefficients(t_minus, t_plus, q_t_minus, q_t_plus):
    A = np.array([
        [t_minus**2, t_minus, 1],
        [0, 0, 1],
        [t_plus**2, t_plus, 1]
    ])

    b = np.array([q_t_minus, 1, q_t_plus])
    coefficients = np.linalg.solve(A, b)
    return coefficients

# Quality function
def quality_function(t, coefficients):
    a, b, c = coefficients
    return max(min(a * t**2 + b * t + c, 1), 0)

# Generate data for plotting
t_values = np.linspace(-7, 7, 400)

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Plot each quality function
for puntos in calidades:
    t_minus_7, q_t_minus_7 = puntos[0]
    t_plus_7, q_t_plus_7 = puntos[1]
    coefficients = calculate_coefficients(t_minus_7, t_plus_7, q_t_minus_7, q_t_plus_7)
    q_values = [quality_function(t, coefficients) for t in t_values]
    ax.plot(t_values, q_values, label=f'Distribución calidad {puntos[2]}')

# Set labels and title
ax.set_xlabel('t=Días')
ax.set_ylabel('q[t]=Calidad del día de cosecha t')
ax.set_title('Función de calidad de uvas')

# Set limits and grid
ax.set_xlim(-7, 7)
ax.set_ylim(0, 1.2)
ax.grid()

# Show legend
ax.legend()

# Show the plot
plt.show()

