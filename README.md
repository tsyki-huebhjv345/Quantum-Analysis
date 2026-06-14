# Quantum-Analysis

A Python Aer-simulation project designed to explore and visualize quantum system probability under different vector parameters. The script utilizes quantum circuit simulation to map out efficiency and optimization factors across 4 data states.

# Overview

The main script (`Analysis-DV-Reconst-Send.py`) runs a data extraction across 19 probability intervals ranging from 0.05 to 0.95. By applying Y-axis quantum rotations (`ry` gates) based on Bloch sphere vector mathematics, the system maps out a total grid of 361 unique coordinate scenarios. 

Each scenario executes exactly **100,000 trials (shots)** on a quantum engine simulator to acquire data state probabilities.

# Structure

* **`Analysis-DV-Reconst-Send.py`**: The primary script contains quantum circuit setup, Aer-simulator iteration, Performance testing loops, and dashboard rendering.
* **`Library/`**: Dedicated folder holding auxiliary modules and standalone analytical scripts.

# Requirements

The code relies on the following framework requirements:
* **Python 3.10+**
* **Qiskit** & **Qiskit-Aer** (Local quantum hardware simulator engine)
* **NumPy** (Array mathematics)
* **Matplotlib** (Data visualization dashboarding)

To install all dependencies at once, run:
```bash
pip install qiskit qiskit-aer numpy matplotlib
```

# Process

1. **State Conversion**: An internal conversion function translates standard decimal fractions into Bloch sphere rotation angles (in radians).
2. **Grid Sweep**: The code loops through both Operational Factor K and Operational Factor L to test all possible combinations.
3. **Simulation**: A 2-qubit, 2-bit matrix records baseline metrics across four possible outcomes: `00`, `01`, `10`, and `11`.
4. **Performance Testing**: Tracking thresholds are checked in real-time to compute:
   * **Maximum Efficiency**: Peak probability of state `00` (system fully functional).
   * **Maximum Load Capacity**: Peak probability of state `11` (system completely saturated).
   * **Boundary States**: Critical regions where performance balances near a 50/50 distribution split.

# Visual

Upon finishing the processing loop, the application generates a 2x2 Matplotlib grid showing a scatter-dot visual distribution:
* **Chart 00 (Green)**: System Performance Density Map
* **Chart 01 (Orange)**: Primary Vector Distribution
* **Chart 10 (Blue)**: Secondary Vector Distribution
* **Chart 11 (Red)**: Peak System Saturation Map

The opaqueness (`alpha`) of individual data points shifts according to its calculated likelihood, allowing the user to instantly identify optimal operation zones.
*The Comments of the code are written in Polish due to the project being highschool assignment
