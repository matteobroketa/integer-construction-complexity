# Unit-Cost Binary–Ternary Construction

This repository contains the manuscript, verification code, and reproducibility materials for:

**Unit-Cost Binary–Ternary Construction**
Matteo Broketa

The project studies the minimum number of unit-cost operations needed to construct an integer from 1 using:

[
x\mapsto x+1,\qquad x\mapsto 2x,\qquad x\mapsto 3x.
]

The paper develops exact structural recurrences, mixed-radix formulations, general multiplier-set results, and a computer-assisted analysis of powers of two. In particular, it verifies that repeated doubling remains optimal through (2^{53}), while

[
C(2^{54})=53,
]

with optimal operation-count signature:

* 8 doublings
* 29 triplings
* 16 increments

## Repository contents

* `manuscript.pdf`
* `manuscript.tex` — LaTeX source
* `verify.py` — exact verification code
* `verification-output.txt` — recorded verification results

## Reproducibility

Run:

```bash
python verify.py
```

The verification uses exact integer arithmetic and includes independent cross-checks of the main recurrence on a large finite range.

## Status

This is an independent research preprint and has not been peer reviewed. This work was discovered and drafted with substantial assistance from large language models. All theorems have been verified by independent Python implementations using exact integer arithmetic (see verify.py).