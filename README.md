# brojapid-activationfunctions

BROJA Partial Information Decomposition (PID) analysis of neural activation functions.

This repository provides extensions to the BROJA-PID framework for investigating how different neural activation functions modulate contextual information transmission. It decomposes the information contributed by a driving input (**R**) and a contextual input (**C**) into unique, redundant, and synergistic components using the BROJA unique information measure.

This code accompanies the reproduction study:

> Sepehr Mahmoudian. (2020). [Re] Measures for investigating the contextual modulation of information transmission. *ReScience C*, 6(3), #2. [10.5281/zenodo.3885793](https://zenodo.org/record/3885793)

## Features

- **Four activation function modes**: additive, modulatory, both, and no-context
- **Classical information-theoretic terms**: mutual information, conditional mutual information
- **BROJA PID decomposition**: unique, redundant, and synergistic information
- **3D surface visualizations** of information measures across input magnitude ranges

## Installation

### Prerequisites

- Python 3.8+
- [IDTxl](https://github.com/pwollstadt/IDTxl) (for BROJA synergy solver via JPype/Tartu)

### Dependencies

```
numpy>=1.22.0
scipy>=1.10.0
matplotlib>=3.1.3
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install IDTxl separately (required for the Tartu synergy solver):

```bash
pip install idtxl
```

## Usage

```bash
python main.py
```

### Output

The script produces PNG visualizations in the project directory:

| File | Description |
|------|-------------|
| `classical_terms.png` | Classical mutual and conditional information terms |
| `pid_terms_additive.png` | PID decomposition — additive activation |
| `pid_terms_modulatory.png` | PID decomposition — modulatory activation |
| `pid_terms_both.png` | PID decomposition — combined activation |
| `pid_terms_nocontext.png` | PID decomposition — no-context baseline |

## Configuration

Edit `params.py` to adjust:

- `n_functions` — number of activation functions to analyze (default: 4)
- `increments` — resolution of the input magnitude grid (default: 0.1)
- `r_magnitudes` / `c_magnitudes` — range of driving/context input magnitudes
- `c__r` — context-to-response coupling parameter
- `firing_value` / `not_firing_value` — binary neuron output values

## Adding Custom Activation Functions

1. Replace one of the four functions in `main.py` (the `nocontext` function is a good candidate)
2. Rename it in `functions_X__R_C`
3. To add a fifth function alongside the existing four, increment `n_functions` in `params.py` and add the new function to the main computation loop

## Project Structure

```
brojapid-activationfunctions/
├── main.py          # Entry point — activation function definitions and PID computation
├── analysis.py      # Information-theoretic measures (MI, CMI, PID terms)
├── plotting.py      # 3D surface plot generation
├── params.py        # Configuration parameters
├── requirements.txt # Python dependencies
├── CITATION.cff     # Citation metadata
├── LICENSE          # MIT License
└── AUTHORS          # Author information
```

## References

1. Mahmoudian, S. (2020). [Re] Measures for investigating the contextual modulation of information transmission. *ReScience C*, 6(3), #2. [doi:10.5281/zenodo.3885793](https://doi.org/10.5281/zenodo.3885793)
2. Bertschinger, N., Rauh, J., Olbrich, E., Jost, J., & Ay, N. (2014). Quantifying unique information. *Entropy*, 16(4), 2161–2183. [doi:10.3390/e16042161](https://doi.org/10.3390/e16042161)
3. Wibral, M., Priesemann, V., & Lizier, J. T. (2017). Bits from brains for biologically inspired computing. *Frontiers in Robotics and AI*, 4, 14.

## Citation

If you use this code, please cite it using the metadata in [`CITATION.cff`](CITATION.cff).

## License

MIT — see [LICENSE](LICENSE).
