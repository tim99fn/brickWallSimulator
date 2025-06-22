## Brick Laying Simulation
This Python script simulates the laying of bricks for a wall, supporting different bond patterns and visualizing the process directly in your terminal. It generates a laying order based on a greedy strategy, determining which bricks become "layable" as others are placed.

For a more interactive and visual experience of the brick laying process, you can visit the online simulator built with HTML, CSS, and JavaScript. The underlying brick-laying logic (how bricks are positioned and their support dependencies) is identical to this Python script, offering a consistent simulation experience in a graphical interface.

HTML Simulator Link: [https://tim99fn.github.io/brickWallSimulator/]


### Features
Supported Brick Bond Patterns:
stretcher: Simulates a standard stretcher bond pattern.
english_cross: Simulates an English Cross bond pattern.
Terminal-Based Visualization: Watch the wall being built brick by brick in your terminal, with different characters representing laid bricks.
Greedy Laying Strategy: The script intelligently determines the optimal next "stride" of bricks to lay, prioritizing efficiency.
### How to Run
Save the Script: Save the provided Python code as a .py file (e.g., brick_simulator.py).

Open Terminal: Navigate to the directory where you saved the script using your terminal or command prompt.

Run with Flags: Execute the script using python followed by the script name and the desired flags:

Bash
python brick_simulator.py [OPTIONS]
### Available Options:

--bond [stretcher|english_cross]: Specifies the type of brick bond to simulate.
Default: stretcher
Example: --bond english_cross
--width_mm [value]: Sets the width of the wall in millimeters.
Default: 2300 (for stretcher bond)
Important Note for English Cross Bond: For the english_cross bond, a width of 2080 mm is specifically recommended. This width ensures the wall has "straight edges" (a consistent pattern without awkward partial bricks at the ends of courses), similar to a standard assignment setup for this bond. While other widths can be used, 2080 mm provides an aesthetically complete and mathematically convenient wall for the English Cross pattern in this simulation.
