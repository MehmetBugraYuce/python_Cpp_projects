--This README file is created using GPT 5.1-mini--
Pendulum Simulation — Interactive

Overview
- Interactive pendulum simulator using Matplotlib animation and sliders.
- Features: adjustable length `L` (m), gravity `g` (m/s^2), initial angle `θ₀` (rad), dummy mass slider, fading trail, gravity arrow, checkered background, period display, and Reset button.

Requirements
- Python 3.8+
- numpy
- scipy
- matplotlib

Quick setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install --upgrade pip
pip install numpy scipy matplotlib
```

Run
```powershell
python "pendulum.py"
```
Notes
- Use an interactive Matplotlib backend (TkAgg/Qt5Agg). If you see a headless warning, run without overriding `MPLBACKEND`.
- The `mass` slider is decorative (mass cancels out in the simple pendulum model used here).
- The `θ₀` slider is limited to ±1 rad; its displayed label shows degrees.

Exporting video (optional)
- Install `ffmpeg` and then you can add a line to `pendulum.py` to save the animation:
```python
ani.save('pendulum.mp4', writer='ffmpeg', fps=60)
```

Packaging to a Windows .exe
- Install PyInstaller and build:
```powershell
pip install pyinstaller
pyinstaller --onefile --windowed pendulum.py
```
- You may need to add Matplotlib data files or hidden imports; testing the generated exe without `--windowed` helps debug.

Advanced
- For large-angle period accuracy, replace the small-angle formula with an elliptic-integral based expression.
- To remove SciPy (if packaging size is a concern) a simple RK4 integrator can replace `odeint`.

File
- Main script: `pendulum.py`

License
- No license included. Use for personal/educational purposes.
