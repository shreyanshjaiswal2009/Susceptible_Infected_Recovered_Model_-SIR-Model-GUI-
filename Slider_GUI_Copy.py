import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image, ImageTk
import matplotlib.text as mtext
from tkinter import messagebox


# Add the ggplot style
plt.style.use('ggplot')

def update_graph(event=None):
    global N, I0, Snot, beta, gamma, animation_running

    try:
        if animation_running[0]:
            return

        N = int(slider_N.get())
        I0 = int(slider_I0.get())
        Snot = int(slider_Snot.get())  # New Snot slider
        beta = round(float(slider_beta.get()), 2)  # Round to 2 decimal places

        # Ensure Snot + I0 = N
        Snot = min(Snot, N - I0)

        # Ensure that N is always greater than or equal to I0
        N = max(N, I0)

        if N < I0:
            return
        else:
            S0 = Snot  # Set initial susceptible population S0 as Snot
            t = np.linspace(0, 160, 160)
            y0 = S0, I0, 0
            ret = odeint(deriv, y0, t, args=(N, beta, gamma))
            S, I, R = ret.T

            # Clear the existing plot
            ax.cla()

            # Update the plot with new data and customize colors
            ax.plot(t, S / N, color='#1f77b4', alpha=0.8, lw=2, label='Susceptible')
            ax.plot(t, I / N, color='#ff7f0e', alpha=0.8, lw=2, label='Infected')
            ax.plot(t, R / N, color='#2ca02c', alpha=0.8, lw=2, label='Recovered with immunity')

            # Set plot labels and title
            ax.set_xlabel('Time / days')
            ax.set_ylabel('Ratio')
            ax.set_ylim(0, 1.2)
            ax.yaxis.set_tick_params(length=0)
            ax.xaxis.set_tick_params(length=0)
            ax.legend(loc='upper right', labels=['Susceptible', 'Infected', 'Recovered'])

            Rnot = beta / gamma
            Compare = ""
            if Rnot > 1:
                Compare = "> 1"
            elif Rnot < 1:
                Compare = "< 1"

            Rnotvalue = round(float(Rnot), 2)
            Title = f'N = {N}, I0 = {I0}, S0 = {Snot}, CR = {beta}, RR = {gamma}, Rnot ({Rnotvalue}) {Compare}'
            ax.set_title(Title)

                # Calculate dI/dt at t=0
            y0 = Snot, I0, 0
            dSdt, dIdt, dRdt = deriv(y0, 0, N, beta, gamma)

            # Create text to display disease spread type
            spread_type_text = "Disease spread type = "
            if dIdt < 0:
                spread_type_text += "Eradication"
            elif dIdt == 0:
                spread_type_text += "Endemic"
            else:
                spread_type_text += "Epidemic"

            # Add the text to the graph (position: upper left)
            text = mtext.Text(0.02, 0.95, spread_type_text, transform=ax.transAxes)
            ax.add_artist(text)


            # Redraw the canvas
            fig.canvas.draw()

    except Exception as e:
        stats_text.set(f"Error: {str(e)}")  # Display the error message in the statistics text

def clear_graph():
    global animation_running
    if not animation_running[0]:
        ax.cla()
        ax.set_title('')
        ax.set_xlabel('')
        ax.set_ylabel('')
        fig.canvas.draw()
        stats_text.set("")  # Clear statistics text

def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

def animation_speed_to_scale(speed):
    return int((speed - 0.5) * 10)

def scale_to_animation_speed(scale):
    return scale / 10 + 0.5

def animation_speed_to_interval(speed):
    # Convert animation speed (0.5x to 2.5x) to interval (delay in milliseconds)
    # Interval is the reciprocal of the animation speed (e.g., 0.5x -> 2000, 1.0x -> 1000, 2.5x -> 400)
    return int(1000 / speed)

def update_animation_speed(speed):
    global interval, animation_speed

    # Convert speed to interval (by multiplying by 10 and then dividing by 10)
    interval = animation_speed_to_interval(float(speed) * 10) / 10

    # Update the animation interval if the animation is currently running
    if animation_running[0]:
        animation.event_source.interval = interval

    animation_speed = float(speed)  # Update the animation_speed variable



def update_animation_speed(scale):
    global animation_speed
    animation_speed = scale_to_animation_speed(float(scale))
    if animation_running[0]:
        animation.event_source.interval = animation_speed_to_interval(animation_speed)



def reset_simulation():
    global N, I0, Snot, beta, animation_running, animation

    # Check if animation is running
    if animation_running[0]:
        messagebox.showinfo("Animation Running", "Cannot reset while animation is running.")
        return

    # Ask for confirmation before resetting
    confirmed = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the simulation?")
    if not confirmed:
        return

    # Disable the Reset button during reset
    reset_button.config(state=tk.DISABLED)

    # Reset simulation parameters to their initial values
    N = 0
    I0 = 0
    Snot = 0
    beta = 0.0
    animation_running = [False]

    # Reset sliders to zero
    slider_N.set(0)
    slider_I0.set(0)
    slider_Snot.set(0)
    slider_beta.set(0)

    # Clear the existing plot
    ax.cla()
    ax.set_title('')
    ax.set_xlabel('')
    ax.set_ylabel('')
    fig.canvas.draw()
    stats_text.set("")  # Clear statistics text

    # Re-enable the Reset button after reset
    reset_button.config(state=tk.NORMAL)


def simulate():
    global N, I0, Snot, beta, gamma, animation_running, animation, animation_speed, slider_speed

    try:
        if animation_running[0]:
            return

        N = int(slider_N.get())
        I0 = int(slider_I0.get())
        Snot = int(slider_Snot.get())  # New Snot slider
        beta = round(float(slider_beta.get()), 2)  # Round to 2 decimal places

        # Ensure Snot + I0 = N
        Snot = min(Snot, N - I0)

        # Ensure that N is always greater than or equal to I0
        N = max(N, I0)

        if N < I0:
            return
        else:
            S0 = Snot  # Set initial susceptible population S0 as Snot
            t = np.linspace(0, 160, 160)
            y0 = S0, I0, 0
            ret = odeint(deriv, y0, t, args=(N, beta, gamma))
            S, I, R = ret.T

            # Clear the existing plot
            ax.cla()

            # Set plot labels and title
            ax.set_xlabel('Time / days')
            ax.set_ylabel('Ratio')
            ax.set_ylim(0, 1.2)
            ax.yaxis.set_tick_params(length=0)
            ax.xaxis.set_tick_params(length=0)
            ax.legend(loc='upper right', labels=['Susceptible', 'Infected', 'Recovered'])

            Rnot = beta / gamma
            Compare = ""
            if Rnot > 1:
                Compare = "> 1"
            elif Rnot < 1:
                Compare = "< 1"

            Rnotvalue = round(float(Rnot), 2)
            Title = f'N = {N}, I0 = {I0}, S0 = {Snot}, CR = {beta}, RR = {gamma}, Rnot ({Rnotvalue}) {Compare}'
            ax.set_title(Title)

            # Calculate dI/dt at t=0
            dSdt, dIdt, dRdt = deriv(y0, 0, N, beta, gamma)

            # Create text to display disease spread type
            spread_type_text = "Disease spread type = "
            if dIdt < 0:
                spread_type_text += "Eradication"
            elif dIdt == 0:
                spread_type_text += "Endemic"
            else:
                spread_type_text += "Epidemic"

            # Add the text to the graph (position: upper left)
            text = mtext.Text(0.02, 0.95, spread_type_text, transform=ax.transAxes)
            ax.add_artist(text)

            # Create animation
            def update(frame):
                if not animation_running[0]:
                    return

                ax.plot(t[:frame], S[:frame] / N, color='#1f77b4', alpha=0.8, lw=2, label='Susceptible')
                ax.plot(t[:frame], I[:frame] / N, color='#ff7f0e', alpha=0.8, lw=2, label='Infected')
                ax.plot(t[:frame], R[:frame] / N, color='#2ca02c', alpha=0.8, lw=2, label='Recovered with immunity')

                if frame == len(t) - 1:
                    animation_running[0] = False

                # Update the disease spread type text during animation
                y0 = Snot, I0, 0
                dSdt, dIdt, dRdt = deriv(y0, t[frame], N, beta, gamma)
                spread_type_text = "Disease spread type = "
                if dIdt < 0:
                    spread_type_text += "Eradication"
                elif dIdt == 0:
                    spread_type_text += "Endemic"
                else:
                    spread_type_text += "Epidemic"
                text.set_text(spread_type_text)


            animation_running = [True]
            slider_speed.config(state=tk.DISABLED)  # Disable speed slider during animation

            original_interval = animation_speed_to_interval(animation_speed)
            interval = original_interval / 5

            animation = FuncAnimation(fig, update, frames=len(t), interval=interval, repeat=False)

            # Redraw the canvas
            fig.canvas.draw()

    except Exception as e:
        stats_text.set(f"Error: {str(e)}")  # Display the error message in the statistics text

def pause_animation():
    global animation_running

    if animation_running[0]:
        animation.event_source.stop()
        animation_running[0] = False
        slider_speed.config(state=tk.NORMAL)  # Re-enable the speed slider during pause

def resume_animation():
    global animation_running
    if not animation_running[0]:
        animation.event_source.start()
        animation_running[0] = True
        slider_speed.config(state=tk.DISABLED)  # Disable speed slider during animation
def show_credits_dialog():
    credits_text = "Made by Shreyansh (@shreyansh2009 on replit.com)"
    messagebox.showinfo("Credits", credits_text)
# Initialize variables
N = 0
I0 = 0
Snot = 0  # New variable for initial susceptible population (S0)
beta = 0.0
gamma = 0.1  # Fixed recovery rate
animation_running = [False]  # Added initialization for animation_running
animation_speed = 100  # Set animation speed to 66.67x (1.5x faster than 100x)
  # Initial animation speed (adjust as desired)

# Create the main window
root = tk.Tk()
root.title("SIR Simulation")

# Create a frame to hold the graph
graph_frame = ttk.Frame(root)
graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Create the figure and axes for the graph
fig, ax = plt.subplots(facecolor='w', figsize=(12, 7))
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)

# Create input boxes and buttons
input_frame = ttk.Frame(root)
input_frame.pack(padx=10, pady=(0, 10))

# Create a custom style for the buttons with black text
button_style = ttk.Style()
button_style.configure("Custom.TButton", font=("Arial", 12), foreground="black", background="#4CAF50")

# New Snot slider
label_Snot = ttk.Label(input_frame, text="Initial number of susceptible people (S0):")
label_Snot.grid(row=0, column=0, padx=5, pady=5, sticky="w")
slider_Snot = ttk.Scale(input_frame, from_=0, to=100000, length=200, orient="horizontal", command=update_graph)
slider_Snot.set(0)
slider_Snot.grid(row=0, column=1, padx=5, pady=5, sticky="w")

label_N = ttk.Label(input_frame, text="Total population (N):")
label_N.grid(row=1, column=0, padx=5, pady=5, sticky="w")
slider_N = ttk.Scale(input_frame, from_=0, to=100000, length=200, orient="horizontal", command=update_graph)
slider_N.set(0)
slider_N.grid(row=1, column=1, padx=5, pady=5, sticky="w")

label_I0 = ttk.Label(input_frame, text="Initial number of infected people (I0):")
label_I0.grid(row=2, column=0, padx=5, pady=5, sticky="w")
slider_I0 = ttk.Scale(input_frame, from_=0, to=5000, length=200, orient="horizontal", command=update_graph)
slider_I0.set(0)
slider_I0.grid(row=2, column=1, padx=5, pady=5, sticky="w")

label_beta = ttk.Label(input_frame, text="Contact rate (beta):")
label_beta.grid(row=3, column=0, padx=5, pady=5, sticky="w")
slider_beta = ttk.Scale(input_frame, from_=0, to=5, length=400, orient="horizontal", command=update_graph)
slider_beta.set(0)
slider_beta.grid(row=3, column=1, padx=5, pady=5, sticky="w")

simulate_button = ttk.Button(input_frame, text="Simulate", command=simulate, style="Custom.TButton")
simulate_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

pause_button = ttk.Button(input_frame, text="Pause", command=pause_animation, style="Custom.TButton")
pause_button.grid(row=0, column=3, padx=5, pady=5, sticky="w")

resume_button = ttk.Button(input_frame, text="Resume", command=resume_animation, style="Custom.TButton")
resume_button.grid(row=0, column=4, padx=5, pady=5, sticky="w")

reset_button = ttk.Button(input_frame, text="Reset Program", command=reset_simulation, style="Custom.TButton")
reset_button.grid(row=0, column=7, padx=5, pady=5, sticky="w")


clear_button = ttk.Button(input_frame, text="Clear Graph", command=clear_graph, style="Custom.TButton")
clear_button.grid(row=0, column=5, padx=5, pady=5, sticky="w")

# New slider for animation speed
speed_label = ttk.Label(input_frame, text="Animation Speed:")
speed_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")

# Set custom scaling range (5 to 25), which will be mapped to (0.5 to 2.5)
slider_speed = ttk.Scale(input_frame, from_=5, to=25, length=200, orient="horizontal", command=update_animation_speed)
slider_speed.set(animation_speed_to_scale(animation_speed))  # Adjust initial value based on the range (0.5 to 2.5)
slider_speed.grid(row=1, column=3, padx=5, pady=5, sticky="w")
slider_speed = ttk.Scale(input_frame, from_=5, to=25, length=200, orient="horizontal", command=update_animation_speed)



# Create a custom style for the "CREDITS" button
button_style = ttk.Style()
button_style.configure("Credits.TButton", font=("Arial", 10))

# Create the "CREDITS" button with the custom style
credits_button = ttk.Button(root, text="CREDITS", command=show_credits_dialog, style="Small.TButton")
credits_button.pack(side="bottom", padx=5, pady=5)


# ... (previous code)


# Create a custom style for the smaller button with black text
small_button_style = ttk.Style()
small_button_style.configure("Small.TButton", font=("Arial", 10), foreground="black")


# Create a label to display the statistics
stats_text = tk.StringVar()
stats_label = ttk.Label(input_frame, textvariable=stats_text, wraplength=400, justify="left", font=("Arial", 16, "bold"))
stats_label.grid(row=0, column=6, rowspan=2, padx=(50, 0), pady=5, sticky="n")

# Configure window resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Redraw the canvas after implementing the Reset button
fig.canvas.draw()


# Run the Tkinter event loop
root.mainloop()
