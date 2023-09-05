import tkinter as tk
from tkinter import ttk, Scrollbar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cairosvg

# Function to generate a simplified 2D electron orbital plot for hydrogen
def generate_electron_orbital():
    # Get input values (e.g., n, l, m)
    n = int(n_entry.get())
    l = int(l_entry.get())
    m = int(m_entry.get())
    
    # Define constants
    a0 = 1  # Bohr radius (simplified)
    r_max = 5 * a0  # Maximum radial distance (simplified)
    
    # Create radial and angular grids
    r_values = np.linspace(0, r_max, 500)
    theta_values = np.linspace(0, 2 * np.pi, 500)
    R, Theta = np.meshgrid(r_values, theta_values)
    
    # Calculate the radial part of the wavefunction
    R_nl = (2 / n) * np.sqrt((np.math.factorial(n - l - 1)) / (2 * n * np.math.factorial(n + l))) * (2 * r_values / n * a0) ** l * np.exp(-r_values / (n * a0)) * np.polyval(np.polyder(np.polyval(np.polyder(np.polyval(np.polyder(np.polyval(np.polyval(np.polyval(np.polyfit([0, 1, 2, 3, 4, 5], [1, -1, 1, -1, 1, -1, 1, -1], l), r_values / (n * a0)), l), l), m), l), m), l), m)
    
    # Calculate the angular part of the wavefunction
    Y_lm = np.sqrt((2 * l + 1) * np.math.factorial(l - m) / (4 * np.pi * np.math.factorial(l + m))) * np.exp(1j * m * Theta)
    
    # Combine the radial and angular parts
    Psi = R_nl * Y_lm
    
    # Create a new figure
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6), dpi=80)
    
    # Plot the probability density (squared magnitude of Psi)
    ax.pcolormesh(Theta, R, abs(Psi)**2, shading='auto')
    ax.set_title(f'Hydrogen Electron Orbital (n={n}, l={l}, m={m})')
    
    # Display the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, columnspan=2)
    
    # Create vertical and horizontal scrollbars
    v_scrollbar = Scrollbar(window, orient="vertical", command=canvas_widget.yview)
    h_scrollbar = Scrollbar(window, orient="horizontal", command=canvas_widget.xview)
    canvas_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Place the scrollbars
    v_scrollbar.grid(row=5, column=2, sticky="ns")
    h_scrollbar.grid(row=6, column=0, columnspan=2, sticky="ew")

    # Update the canvas's scroll region when the plot changes
    canvas_widget.bind("<Configure>", lambda e: canvas_widget.configure(scrollregion=canvas_widget.bbox("all")))

    # Save the Matplotlib figure as an SVG file
    svg_filename = f"electron_orbital_{n}_{l}_{m}.svg"
    plt.savefig(svg_filename, format="svg", bbox_inches="tight", dpi=80)
    plt.close()

    # Convert the SVG file to PDF (if needed)
    pdf_filename = f"electron_orbital_{n}_{l}_{m}.pdf"
    cairosvg.svg2pdf(url=svg_filename, write_to=pdf_filename)

    # Display a message
    result_label.config(text=f'Electron orbital plot saved as "{pdf_filename}"')


# Create the main window
window = tk.Tk()
window.title('Electron Orbital Visualization')

# Create and place labels and entry fields for input
n_label = ttk.Label(window, text='Principal Quantum Number (n):')
n_label.grid(row=0, column=0)
n_entry = ttk.Entry(window)
n_entry.grid(row=0, column=1)
n_entry.insert(0, '1')  # Default value for n

l_label = ttk.Label(window, text='Azimuthal Quantum Number (l):')
l_label.grid(row=1, column=0)
l_entry = ttk.Entry(window)
l_entry.grid(row=1, column=1)
l_entry.insert(0, '0')  # Default value for l

m_label = ttk.Label(window, text='Magnetic Quantum Number (m):')
m_label.grid(row=2, column=0)
m_entry = ttk.Entry(window)
m_entry.grid(row=2, column=1)
m_entry.insert(0, '0')  # Default value for m

generate_button = ttk.Button(window, text='Generate Electron Orbital Plot', command=generate_electron_orbital)
generate_button.grid(row=3, column=0, columnspan=2)

result_label = ttk.Label(window, text='')
result_label.grid(row=4, column=0, columnspan=2)

# Run the Tkinter main loop
window.mainloop()
