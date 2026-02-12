A* Pathfinding Visualizer (pygame)

Overview

This small tool is a pygame-based A* pathfinding visualizer. It draws an R×C grid on a black background and lets you place a start, a goal, and obstacles, then visualize the A* search.

Requirements

- Python 3.10+ (your workspace includes a venv with pygame installed)
- pygame

Quick start

1. (Optional) Activate the included venv:
   - macOS / zsh: source pygame.venv/bin/activate
2. Install pygame if needed: pip install pygame
3. Run the script from this repository root:
   python Visual_A*.py

Command-line / interactive options

- --rows N and --cols M: set grid size when launching, e.g.:
  python Visual_A*.py --rows 40 --cols 50
- If you run without flags the program will prompt you for rows/cols at startup; press Enter to accept defaults.

Controls

- Left-click
  - First left-click you place the start node (green).
  - Second left-click you place the goal node (blue).
  - Subsequent left-clicks toggle obstacles (white).
  - Hold and drag with left button to paint obstacles.
- Right-click
  - Right-click a start/goal to remove it.
  - Hold and drag with right button to erase obstacles.
- Slider (bottom-left)
  - Drag the slider to control visualization speed. The mapping is: slider=1.0 -> fastest (0 ms delay), slider=0.0 -> slowest (~200 ms delay).
- Info mode (checkbox next to slider)
  - Click the checkbox to toggle info mode.
  - When enabled the algorithm prints numeric debug info to the terminal (g/h/f, open/closed sizes) and, if cells are large enough on screen, shows the values in each cell:
    - f centered, g top-left, h top-right (falls back to a single centered value for small cells).
- Space
  - Start the A* search visualization using the current slider speed and info mode.
- C
  - Clear the grid (removes start/goal/obstacles).

Notes and tips

- Grid sizing uses integer division to compute cell size; very large grids will produce very small cells where per-cell numeric labels are suppressed to avoid clutter.
- Info mode is intended for learning/debugging — it prints step-by-step numeric details to the terminal while the search runs.


