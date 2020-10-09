# Activation Functions with BROJA's PID

BROJA-PID additions for [10.5281/zenodo.3885793](https://zenodo.org/record/3885793) PID results of different activation functions can be compared. 

---

Tested with:
```
Python 3.8.1
numpy 1.18
scipy 1.4  
matplotlib 3.1.3
jpype1 0.7.5
ecos 2.0.7.post1
IDTxl 1.1
```
To install the requirements above except IDTxl one could simply use ```pip install -r requirements.txt``` after getting the correct python version. IDTxl can be obtained from https://github.com/pwollstadt/IDTxl.

---

It's simple to run the code:
```
python main.py
```
The results will be saved as "classical_terms.png" and 3 png images of PID results for each activation function.

---


The fastest way to implement and investigate a [new/custom] activation function would be to replace one of the four activation functions in main.py. Probably that would be the fourth activation function (no context) and then renaming it in functions_X__R_C dictionary. To have all four and your activation function, first adjust the n_functions in params.py then put it in the main loop where result of the activation functions are calculated and finally add it to the functions_X__R_C dictionary.

---

[1] Bertschinger, N., Rauh, J., Olbrich, E., Jost, J., & Ay, N. (2014). Quantifying unique information. Entropy, 16(4), 2161–2183. https://doi.org/10.3390/e16042161

[2] Sepehr Mahmoudian. (2020). [Re] Measures for investigating the contextual modulation of information transmission. Rescience C, 6(3), #2. http://doi.org/10.5281/zenodo.3885793
