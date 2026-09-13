# Mathematical Statistics

A collection of Python applications developed during university coursework in mathematical statistics. The repository contains two individual projects covering numerical and graphical representation of statistical data and hypothesis testing for probability distributions.

## Projects

### 1. Numerical and Graphical Representation of Statistical Data
**Project:** `numerical_characteristics`

Processes statistical samples and provides their numerical and graphical representation.

- **Discrete statistical distribution** — constructs a variation series with absolute and relative frequencies.
- **Grouped statistical distribution** — divides sample data into intervals and calculates grouped frequencies.
- **Descriptive statistics** — computes the mean, median, mode, range, variance, corrected sample variance, standard deviation, and coefficient of variation.
- **Statistical moments** — calculates initial and central moments, skewness, and excess kurtosis.
- **Empirical distribution function** — constructs the empirical CDF for discrete and grouped data.
- **Statistical visualization** — generates frequency polygons, relative-frequency polygons, histograms, and empirical distribution function plots.

### 2. Testing Hypotheses About the Probability Distribution of a Random Variable
**Project:** `hypothesis_testing`

Tests hypotheses about probability distributions using Pearson's chi-squared goodness-of-fit test.

- **Distribution parameter estimation** — estimates unknown parameters of theoretical distributions from statistical samples.
- **Expected frequency calculation** — calculates theoretical probabilities and expected frequencies for grouped intervals.
- **Class merging** — combines adjacent intervals when the conditions required for the chi-squared test are not satisfied.
- **Pearson's chi-squared test** — calculates the empirical χ² statistic, degrees of freedom, and critical value to evaluate the null hypothesis.
- **Distribution fitting** — tests normal and exponential distribution hypotheses for the provided samples.

## Features

- Processing of discrete and grouped statistical data.
- Numerical analysis and graphical representation of statistical samples.
- Text-file input and calculation reports written to output files.
- Modular organization separating statistical calculations, data processing, visualization, and input/output handling.
- Ukrainian console messages, plots, and reports.

## Technologies

Python · NumPy · SciPy · Matplotlib
