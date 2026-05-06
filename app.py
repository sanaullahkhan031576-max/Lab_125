import gradio as gr
import numpy as np
import matplotlib.pyplot as plt

def calculate_deflection(length, load, modulus, inertia):
    # Formulas for Simply Supported Beam (Center Load)
    # Max Deflection (delta) = (P * L^3) / (48 * E * I)
    
    # Convert units (assuming input is meters/Newtons/Pascals)
    E = modulus * 1e9  # GPa to Pa
    I = inertia * 1e-6 # cm^4 to m^4 (common student input)
    P = load           # N
    L = length         # m
    
    # Calculate Max Deflection
    delta_max = (P * (L**3)) / (48 * E * I)
    
    # Generate visualization
    x = np.linspace(0, L, 100)
    # Simple parabolic approximation for visualization
    y = - (P * x / (48 * E * I)) * (3 * L**2 - 4 * x**2) if any(x <= L/2) else 0 # Simplified
    
    # Create plot
    plt.figure(figsize=(8, 4))
    plt.plot([0, L], [0, 0], 'k--', label="Original Beam")
    # Conceptual deflection curve
    curve = - (delta_max * 16 / L**3) * (x**2 * (L - x)) # Visual approximation
    plt.plot(x, curve, 'b', label="Deflected Shape")
    plt.title("Beam Deflection Visualization")
    plt.xlabel("Length (m)")
    plt.ylabel("Deflection (m)")
    plt.legend()
    plt.grid(True)
    
    plot_path = "deflection_plot.png"
    plt.savefig(plot_path)
    plt.close()
    
    return round(delta_max * 1000, 4), plot_path # Return in mm and the image

# Gradio Interface
demo = gr.Interface(
    fn=calculate_deflection,
    inputs=[
        gr.Number(label="Beam Length (m)", value=2.0),
        gr.Number(label="Point Load at Center (N)", value=500),
        gr.Number(label="Young's Modulus (GPa)", value=210),
        gr.Number(label="Moment of Inertia (cm^4)", value=500),
    ],
    outputs=[
        gr.Number(label="Max Deflection (mm)"),
        gr.Image(label="Deflection Plot")
    ],
    title="MechLab: Beam Deflection Calculator",
    description="Calculate the maximum deflection of a simply supported beam with a central point load."
)

if __name__ == "__main__":
    demo.launch()
