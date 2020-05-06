## Zestifying Zillows Zestimates

Authors: Nick Joseph, Shay Altshue

Description: Calculating Zillow's "Zestimate" log error through cluster modeling.

## Problem Statement
------------
Zillow provides a “Zestimate”, which is an estimated property value.

Can we improve Zillow's ability to predict property values by identifying when Zillow's Zestimate will be good, and when it will be bad?

## Project Goals
------------
* Explore the data to identify areas where feature engineering can improve model accuracy
* Utilize clustering within the data to calclulate log error

## Project Organization 
------------
```
    ├── readme.md
    ├── main.ipynb
    ├── main.py
    ├── data
    │   ├── interim
    │   ├── processed
    │   └── raw            
    ├── models
    ├── notebooks
    ├── src
    │   ├── __init__.py    <- Makes src a Python module
    │   ├── acquire.py 
    │   ├── wrangle.py
    │   ├── explore.py
    │   └── model.py
    ├── references
    │   └── data_dictionary
    └── models
