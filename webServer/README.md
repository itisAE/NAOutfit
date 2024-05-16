# TOR: Optimized Version Using Mediapipe

This project is an optimized version that uses mediapipe. The original code can be found here. For more details on the documentation, please refer to this link.

## Added Functions

1. `calculateLung(lmList, bodyPartNum1, bodyPartNum2)`: This function takes as input an array of arrays of coordinates for each point (float), the starting point (int), and the ending point (int).

2. `mediaValori(misurazioniArto)`: This function takes as input an array of measurements (float) and returns the average of the values (float).

## How to Try the Program

Ensure that all libraries are installed. For mediapipe, if you are using Linux as your operating system, verify the possibility of setting up a virtual environment (venv) by following this guide. Run the following command from the terminal:

```bash
python3 webServer.py
