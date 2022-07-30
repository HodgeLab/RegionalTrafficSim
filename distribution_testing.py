# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 11:36:04 2022

@author: antho
"""

import numpy as np
from scipy.stats import truncnorm
from scipy.stats import genhyperbolic
import matplotlib.pyplot as plt

# First set where averages align with centerpoint:
a = -3.6
b = np.inf
func_norm = 79.84
func_sd = 11.77
trunk = truncnorm.rvs(a, b, loc=func_norm, scale=func_sd, size=10000)
tk_avg = np.average(trunk)
print("Work-Trip Average (Uniform): ", tk_avg)
x_array = np.arange(30.5, 200, 0.3)
y_pdf = truncnorm.pdf(x_array, a, b, loc = func_norm, scale = func_sd)
plt.plot(x_array, y_pdf)
plt.show()

# HYPERBOLIC Testing
#Home-based loc
func_norm = 79.84
hyp_trunk = genhyperbolic.rvs(2, 0.75, 0, loc=func_norm, scale=func_sd, size=10000)
ht_avg = np.average(hyp_trunk)
print("Home-Trip Average (Hyper): ", ht_avg)
hyp_pdf = genhyperbolic.pdf(x_array, 2, 0.75, 0, loc = func_norm, scale = func_sd)
plt.plot(x_array, hyp_pdf)
plt.show()

# Work-based loc
func_norm = 72.87
hyp_trunk = genhyperbolic.rvs(2, 0.75, 0, loc=func_norm, scale=func_sd, size=10000)
ht_avg = np.average(hyp_trunk)
print("Work-Trip Average (Hyper): ", ht_avg)
hyp_pdf = genhyperbolic.pdf(x_array, 2, 0.75, 0, loc = func_norm, scale = func_sd)
plt.plot(x_array, hyp_pdf)
plt.show()

# Meal-based loc
func_norm = 126.01
hyp_trunk = genhyperbolic.rvs(2, 0.75, 0, loc=func_norm, scale=func_sd, size=10000)
ht_avg = np.average(hyp_trunk)
print("Meal-Trip Average (Hyper): ", ht_avg)
hyp_pdf = genhyperbolic.pdf(x_array, 2, 0.75, 0, loc = func_norm, scale = func_sd)
plt.plot(x_array, hyp_pdf)
plt.show()
# Compared to smaller "scale" parameter
func_sd = 5
hyp_trunk = genhyperbolic.rvs(2, 0.75, 0, loc=func_norm, scale=func_sd, size=10000)
ht_avg = np.average(hyp_trunk)
print("Meal-Trip Average (Hyper): ", ht_avg)
hyp_pdf = genhyperbolic.pdf(x_array, 2, 0.75, 0, loc = func_norm, scale = func_sd)
plt.plot(x_array, hyp_pdf)
plt.show()


# Low-value testing
func_norm = 0.31
func_sd = .2
x2_array = np.arange(0, 0.5, 0.003)
hyp_trunk = genhyperbolic.rvs(1, 1, 0, loc=func_norm, scale=func_sd, size=1000)
ht_avg = np.average(hyp_trunk)
print("Meal-Trip Average (Hyper): ", ht_avg)
hyp_pdf = genhyperbolic.pdf(x2_array, 1, 1, 0, loc=func_norm, scale=func_sd)
plt.plot(x2_array, hyp_pdf)
plt.show()