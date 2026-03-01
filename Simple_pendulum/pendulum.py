import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import CubicSpline
from matplotlib.collections import LineCollection
from matplotlib import cm
from matplotlib.colors import ListedColormap
from matplotlib.patches import FancyArrowPatch
from matplotlib.widgets import Slider, Button

#We need now to define our constants
g = 9.81 #as in m/s^2
L = 1.0  #as in meters

def pendulum_equation(state, t):
    theta, omega = state
    dtheta = omega
    domega = -(g / L) * np.sin(theta)
    return [dtheta, domega]

#Initial conditions (theta0 will be adjustable via slider)
theta0 = 0.5
omega0 = 0.0
# mass slider is dummy; mass does not affect simple pendulum without damping
mass_dummy = 1.0

#Time span (original coarse solution)
#This will be used to solve the ODE and then we will interpolate for smoothness
t = np.linspace(0, 10, 100)

#Solve the ODE on the coarse grid
solution = odeint(pendulum_equation, [theta0, omega0], t)

# Create a higher-resolution timebase for smooth animation
# Target fps: prefer 60, but ensure at least 50
fps_target = 60
fps = max(50, fps_target)
n_frames = int((t[-1] - t[0]) * fps) + 1
t_fine = np.linspace(t[0], t[-1], n_frames)

# Interpolate the solved angle onto the fine timebase (CubicSpline for smoothness)
try:
    cs = CubicSpline(t, solution[:, 0])
    theta_fine = cs(t_fine)
except Exception:
    # Fall back to linear interpolation if CubicSpline fails
    #This can happen if the solution has issues (e.g., NaNs)
    #So below line ensures we still get a resulti albeit a little less smooth
    theta_fine = np.interp(t_fine, t, solution[:, 0])

# Cartesian positions on the fine grid
x = L * np.sin(theta_fine)
y = -L * np.cos(theta_fine)

#----------------------------------------------------------------
#Below here is the code for the animation and interactive sliders
#Which is not our main concern
#Below part is %100 for visualization and done by GPT, so no more details from me
#----------------------------------------------------------------
#Setting up the visual figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-L*1.2, L*1.2)
ax.set_ylim(-L*1.2, L*1.2)
ax.set_aspect('equal')
# period text placeholder (will update when parameters change)
period_text = ax.text(0.95, 0.95, '', transform=ax.transAxes, ha='right', va='top', fontsize=10, bbox=dict(facecolor='white', alpha=0.7))
# Notebook-style checkered background (pale blue/white squares)
grid_spacing = 0.2 * L
x_edges = np.arange(-L*1.2, L*1.2 + grid_spacing, grid_spacing)
y_edges = np.arange(-L*1.2, L*1.2 + grid_spacing, grid_spacing)
nx = len(x_edges) - 1
ny = len(y_edges) - 1
cols = (np.add.outer(np.arange(ny), np.arange(nx)) % 2).astype(int)
cmap = ListedColormap(['#ffffff', '#e6f2ff'])
pc = ax.pcolormesh(x_edges, y_edges, cols, cmap=cmap, shading='auto', zorder=0)
# Left margin vertical line (light red)
v_margin_x = -L * 0.9
vline = ax.axvline(v_margin_x, color='#ffe6e6', linewidth=1.2, zorder=1)

line, = ax.plot([], [], 'o-', lw=2, zorder=4)

# Trail settings: length in seconds and computed number of frames
trail_seconds = 0.5  # trail lifetime in seconds (adjustable)
trail_length = max(2, int(trail_seconds * fps))

# Create a LineCollection for the fading trail (starts empty)
trail_lc = LineCollection([], linewidths=2)
trail_lc.set_zorder(3)
ax.add_collection(trail_lc)

# Gravity arrow (points downward from the bob) - shortened
arrow_length = 0.2 * L
arrow = FancyArrowPatch((0, 0), (0, -arrow_length), arrowstyle='->', mutation_scale=12, color='red')
ax.add_patch(arrow)

# Initialization for blitting
def init():
    line.set_data([], [])
    trail_lc.set_segments([])
    arrow.set_zorder(5)
    return line, trail_lc, arrow

# Update function for a single frame (draws the rod)
def update(frame):
    # Update pendulum rod
    thisx = [0, x[frame]]
    thisy = [0, y[frame]]
    line.set_data(thisx, thisy)

    # Build the fading trail from recent positions
    start = max(0, frame - trail_length + 1)
    xs = x[start:frame + 1]
    ys = y[start:frame + 1]

    segments = []
    colors = []
    if len(xs) > 1:
        points = list(zip(xs, ys))
        for i in range(len(points) - 1):
            segments.append([points[i], points[i + 1]])
        # Alpha increases towards the newest segment (older segments are more transparent)
        for i in range(len(segments)):
            alpha = (i + 1) / len(segments)
            colors.append((0.0, 0.0, 0.0, alpha))

    trail_lc.set_segments(segments)
    if colors:
        trail_lc.set_color(colors)
    else:
        trail_lc.set_color([])

    # Update gravity arrow anchored at bob, pointing downward
    start = (x[frame], y[frame])
    end = (x[frame], y[frame] - arrow_length)
    arrow.set_positions(start, end)

    return line, trail_lc, arrow

#Create the animation with the fine timebase and target fps
ani = animation.FuncAnimation(
    fig,
    update,
    frames=n_frames,
    init_func=init,
    interval=int(1000 / fps),
    blit=True,
)
# Initialize period display using default L and g
if g>0:
    period_text.set_text(f"T ≈ {2*np.pi*np.sqrt(L/g):.2f} s")
else:
    period_text.set_text('T = ∞')
# Add sliders for L, g, theta0 and mass dummy
plt.subplots_adjust(bottom=0.30)
ax_L = plt.axes([0.15, 0.18, 0.65, 0.03])
ax_g = plt.axes([0.15, 0.12, 0.65, 0.03])
ax_theta = plt.axes([0.15, 0.06, 0.65, 0.03])
ax_mass = plt.axes([0.15, 0.00, 0.65, 0.03])
sL = Slider(ax_L, 'L (m)', 0.1, 2.0, valinit=L)
sg = Slider(ax_g, 'g (m/s^2)', 0.1, 20.0, valinit=g)
stheta = Slider(ax_theta, 'θ₀ (deg)', -1.0, 1.0, valinit=theta0)  # range ±1 rad (~±57°)
smass = Slider(ax_mass, 'mass', 0.1, 10.0, valinit=mass_dummy)  # dummy

def update_params(val):
    global L, g, theta0, pc, vline, x, y, arrow_length, trail_lc
    L = sL.val
    g = sg.val
    theta0 = stheta.val
    # update slider label with degree equivalent
    deg = np.degrees(theta0)
    stheta.valtext.set_text(f"{deg:.1f}°")
    # mass slider has no effect, we just reference its value so it doesn't warn
    _ = smass.val

    # Recompute solution and interpolated positions
    solution = odeint(pendulum_equation, [theta0, omega0], t)
    try:
        cs = CubicSpline(t, solution[:, 0])
        theta_fine_local = cs(t_fine)
    except Exception:
        theta_fine_local = np.interp(t_fine, t, solution[:, 0])

    x = L * np.sin(theta_fine_local)
    y = -L * np.cos(theta_fine_local)

    # Update arrow length
    arrow_length = 0.2 * L

    # Update axes limits
    ax.set_xlim(-L*1.2, L*1.2)
    ax.set_ylim(-L*1.2, L*1.2)
    # compute and display period (small-angle approximation)
    if g>0:
        T = 2 * np.pi * np.sqrt(L / g)
        period_text.set_text(f"T ≈ {T:.2f} s")
    else:
        period_text.set_text('T = ∞')

    # Update checkered background
    try:
        pc.remove()
    except Exception:
        pass
    grid_spacing_local = 0.2 * L
    x_edges_local = np.arange(-L*1.2, L*1.2 + grid_spacing_local, grid_spacing_local)
    y_edges_local = np.arange(-L*1.2, L*1.2 + grid_spacing_local, grid_spacing_local)
    nx_local = len(x_edges_local) - 1
    ny_local = len(y_edges_local) - 1
    cols_local = (np.add.outer(np.arange(ny_local), np.arange(nx_local)) % 2).astype(int)
    pc = ax.pcolormesh(x_edges_local, y_edges_local, cols_local, cmap=cmap, shading='auto', zorder=0)

    # Update left margin
    try:
        vline.remove()
    except Exception:
        pass
    vline = ax.axvline(-L * 0.9, color='#ffe6e6', linewidth=1.2, zorder=1)

    # Clear trail
    trail_lc.set_segments([])

    fig.canvas.draw_idle()

sL.on_changed(update_params)
sg.on_changed(update_params)
stheta.on_changed(update_params)
# mass slider doesn't change dynamics, but we'll still hook it
smass.on_changed(lambda val: None)

# Pause animation while dragging sliders to avoid rendering artifacts
def _on_press(event):
    if event.inaxes in (sL.ax, sg.ax, stheta.ax, smass.ax):
        try:
            ani.event_source.stop()
        except Exception:
            pass

def _on_release(event):
    if event.inaxes in (sL.ax, sg.ax, stheta.ax, smass.ax):
        try:
            update_params(None)
            ani.event_source.start()
        except Exception:
            pass

cid_press = fig.canvas.mpl_connect('button_press_event', _on_press)
cid_release = fig.canvas.mpl_connect('button_release_event', _on_release)

# Reset button
ax_reset = plt.axes([0.87, 0.06, 0.08, 0.05])
btn_reset = Button(ax_reset, 'Reset')

def _reset(event):
    # reset sliders to initial values and clear trail
    sL.reset()
    sg.reset()
    stheta.reset()
    smass.reset()
    try:
        ani.event_source.stop()
    except Exception:
        pass
    update_params(None)
    trail_lc.set_segments([])
    # redraw initial frame
    init()
    fig.canvas.draw_idle()
    try:
        ani.event_source.start()
    except Exception:
        pass

btn_reset.on_clicked(_reset)

fig.suptitle('Pendulum Simulation', y=0.98)
plt.show()
