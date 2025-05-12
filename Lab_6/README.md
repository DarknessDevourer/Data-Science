Lab 6: Linear Regression with NumPy & Gradient Descent

Overview
In this lab you will:

Generate synthetic 2D data around a known line y = kx + b using NumPy.

Implement the analytical Ordinary Least Squares (OLS) solution for linear regression.

Compare your OLS estimates to NumPy’s built-in np.polyfit.

Implement batch gradient descent to fit the same linear model.

Visualize and compare the regression lines and the loss-vs-iteration curve.

Objectives

Reinforce working with NumPy arrays and basic statistics.

Derive and code the OLS formulas for slope and intercept.

Understand and implement a simple gradient descent optimizer.

Compare analytical and iterative approaches to fitting a line.

Interpret convergence behavior via the Mean Squared Error (MSE) plot.

Prerequisites

Python 3.6 or newer

NumPy

Matplotlib

Jupyter Notebook or JupyterLab
Install the required packages by running:
pip install numpy matplotlib jupyter

Files
lab_6.ipynb — Jupyter notebook containing all code, plots, and commentary.
Лабораторна робота 6.pdf — PDF statement of the assignment (Ukrainian).

Notebook Structure

Data Generation
• Fix random seed for reproducibility
• Define true parameters (true_k, true_b) and generate noisy observations

Task 1: OLS Implementation
• Compute k̂ and b̂ via closed-form formulas
• Compare with np.polyfit(x, y, 1)
• Plot data points, true line, OLS fit, and polyfit line

Task 2: Gradient Descent
• Initialize parameters and hyperparameters (learning_rate, n_iter)
• Update slope and intercept using batch gradient descent
• Plot the fitted line on the original data
• Plot MSE vs. iteration count to inspect convergence

Conclusions
• Summarize numerical results and convergence behavior
• Discuss differences between analytical and iterative solutions

How to Run

Clone or download the project folder.

In the project directory, launch Jupyter with:
jupyter notebook lab_6.ipynb

Execute cells in order, reviewing code outputs and plots.

Expected Results

OLS and np.polyfit should produce virtually identical slope and intercept estimates.

Gradient descent will converge to the same solution, showing a rapid drop in MSE followed by asymptotic behavior.

The loss-vs-iterations plot illustrates convergence speed and helps tune hyperparameters.
