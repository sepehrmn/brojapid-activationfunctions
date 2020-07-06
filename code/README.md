# Broja-PID measures for mahmoudian-2020-rescience

BROJA-PID additions for [10.5281/zenodo.3885793](https://zenodo.org/record/3885793)

Currently cleaning the repo and migrating from old PID estimator to a new one

---

Tested with:
```
Python 3.8.1
numpy 1.18
scipy 1.4  
matplotlib 3.1.3
jpype1
ecos
IDTxl 1.1
```
To install the requirements above one could simply use ```pip install -r requirements.txt``` after getting the correct python version. One can get IDTxl from https://github.com/pwollstadt/IDTxl

---

It's simple to run the code:
```
python main.py
```

---


The fastest way to implement and investigate a [new/custom] activation function would be to replace one of the four activation functions in main.py. Probably that would be the fourth activation function (no context) and then renaming it in functions_X__R_C dictionary. To have all four and your activation function, first adjust the n_functions in params.py then put it in the main loop where result of the activation functions are calculated and finally add it to the functions_X__R_C dictionary.
