# Unit-Cost Binary–Ternary Construction

This repository contains the manuscript, verification code, and reproducibility materials for:

**Unit-Cost Binary–Ternary Construction**  
**Matteo Broketa**

This project studies the minimum number of unit-cost operations needed to construct an integer from `1` using:

- `x → x + 1`
- `x → 2x`
- `x → 3x`


The underlying step-count sequence is closely related to **OEIS A056796**.

This project instead defines `C(n)` starting from `1`.

Therefore, for `n ≥ 1`:

**A056796(n) = C(n) + 1**

OEIS: https://oeis.org/A056796

## Main results

The paper develops:

- an exact residue-normalization recurrence;
- a lossless mixed-radix formulation of the shortest-construction problem;
- results for general finite multiplier sets;
- a boundary-exhaustion theorem for smooth-minus-one inputs;
- a multiplicative-rank analysis of the exact state space;
- an exact defect identity for powers of two;
- a reduction connecting power-of-two shortcuts with the complexity of Mersenne numbers `2^k - 1`;
- fixed-tripling stabilization and finite stopping results;
- a local binary/ternary swap law and quotient-lattice formulation.

A central computer-assisted result is that repeated doubling is optimal through `2^53`, while:

**C(2^54) = 53**

Every optimal 53-step construction of `2^54` has the operation-count signature:

- 8 doublings
- 29 triplings
- 16 increments

The first observed record defects for powers of two occur at exponents:

`54, 126, 1008, 1028`

with record defects:

`1, 2, 3, 4`

## Repository contents

- `manuscript.pdf` — research preprint
- `manuscript.tex` — LaTeX source
- `verify.py` — exact verification code
- `verification-output.txt` — recorded verification results
- supporting certificates, tables, and computational data

## Reproducibility

Run:

python verify.py

## Status

This is an independent research preprint and has not been peer reviewed. This work was discovered and drafted with substantial assistance from large language models. All theorems have been verified by independent Python implementations using exact integer arithmetic (see verify.py).
