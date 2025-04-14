# Control Systems Program

## PHASE I : *Signal Flow Graphs*

This Draws the signal flow graph and computes the following :

- All forward loops.
- individual loops.
- Combinations of $n$ non-touching loops.
- Values of $Δ$ , $Δ_1$ , ..., $Δ_m$ , where $m$ is the number of forward paths.
- The system's overall transfer function $\frac{INPUT}{OUTPUT}$


## PHASE II : *Routh_Stability_Criterion*

#### Detects System Stability and solves for roots in RHS of s-plane:


$a_n s^n + a_{n-1} s^{n-1} + a_{n-2} s^{n-2} + ... + a_1 s + a_0 = 0$


### Routh Array Construction:

| Power | Column 1 | Column 2 | Column 3 | $\Large ...$  |
|:-----:|:--------:|:--------:|:--------:|:---:|
| $\Large s^n$ | $\Large a_n$ | $\Large a_{n-2}$ | $\Large a_{n-4}$ | $\Large ...$  |
| $\Large s^{n-1}$ | $\Large a_{n-1}$ | $\Large a_{n-3}$ | $\Large a_{n-5}$ | $\Large ...$  |
| $\Large s^{n-2}$ | $\Large b_1 = \frac{a_{n-1}\cdot a_{n-2} - a_{n}\cdot a_{n-3}}{a_{n-1}}$ | $\Large b_2 = \frac{a_{n-1}\cdot a_{n-4} - a_{n}\cdot a_{n-5}}{a_{n-1}}$ | $\Large ...$  | $\Large ...$  |
| $\Large s^{n-3}$ | $\Large c_1 = \frac{b_{1}\cdot a_{n-3} - a_{n-1}\cdot b_{2}}{b_{1}}$ | $\Large ...$ | $\Large ...$ | $\Large ...$  |
| $\Large \vdots$ | $\Large \vdots$ | $\Large \vdots$ | $\Large \vdots$ | $\Large \ddots$ |
| $\Large s^0$ | $\Large k$ | $\Large 0$ | $\Large 0$ | $\Large ...$  |

> The number of sign changes in the first column indicates the number of roots in the Right Half s-Plane


# Setup

## Requirements

The following packages are required:
- matplotlib (for LaTeX rendering)
- PyQt6 (for GUI)
- sympy (for symbolic mathematics)

Install using pip:
```bash
pip install matplotlib PyQt6 sympy
```
Install in Debian based (Ubuntu):
```
sudo apt install python3-matplotlib python3-pyqt6 python3-sympy
```

