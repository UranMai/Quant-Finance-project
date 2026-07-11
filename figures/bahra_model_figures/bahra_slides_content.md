# Bahra model — paste-ready content for "Modeling The Smile"

Numbers cover **both deck comparison days**: SPX **2023-12-29** (benchmark) and SPX **2023-03-10**
(SVB collapse), shared 80/20 split, full cleaned quote set. Pooled across 12 monthly refits the
hold-out IV RMSE is 0.0157. Plots live in `figures/bahra_model_figures/`.

---

## A. Main deck

### DONE — already in the deck (slides 3–5)
Model-description tagline; RMSE row **0.0130 / 0.0126**; arbitrage row **0 (by construction)** /
**9 → 0 (repaired)**.

### NEW — the SVB day (2023-03-10), the Methods slide's second comparison day
| Model | Train IV RMSE | Holdout IV RMSE | Butterfly | Calendar |
|---|---|---|---|---|
| **Bahra Mixing** | **0.0171** | **0.0171** | **0** (by constr.) | 3 → **0** (repaired) |

In-sample ≈ held-out **on the stress day** (0.01708 vs 0.01706) — the fit is not memorizing.
Arbitrage stayed structural under stress: min g(k) = +0.011 on every expiry; the 3 as-fit calendar
crossings repaired with max price displacement ≈ 2 SPX index points. (Reference: `svi.ipynb`'s own
3/10 IV-RMSE print is 0.0420.) The symmetry theorem bites hardest here: forcing unit means costs
9.3× in the fit objective (431 vs 114 bps in-sample IV) — stress is when skew matters most.

### Slide "Arbitrage Plots" — add our plot
Insert `bahra_butterfly_2023-12-29.png`, caption:
> Bahra: g(k) ≥ 0 on every expiry — 0 butterfly violations (the only model arbitrage-free by construction).

---

## B. Appendix — Bahra section (three slides, same format as Uran/Yvonne)

### Slide B1 — "Risk-Neutral Density Mixture (Bahra)" — Nico
- Instead of fitting the smile (SVI) or the dynamics (Heston), this fits the **risk-neutral probability
  density itself** — a 4-component **free-mean lognormal mixture**, one per expiry.
- **Breeden–Litzenberger:** the call price's second strike-derivative *is* the density, so
  "no negative probabilities" (butterfly) is just convexity. Starting from a genuine density,
  **no-butterfly-arbitrage and the forward (martingale) condition hold by construction**, not by penalty.
- Prices are **closed-form** (a π-weighted sum of Black–Scholes terms — no quadrature); the smile is
  recovered afterward by inverting Black–Scholes in total variance.
- A small **theorem**: any *unit-mean* mixture forces a symmetric smile (zero skew) for every M — so
  freeing the (mean-corrected) means is exactly what makes **equity skew** representable.

### Slide B2 — "Bahra: fit and the density" — Nico
Images: `bahra_smiles_2023-12-29.png` (left) · `bahra_density_2023-12-29.png` (right); alternative
lead image: `bahra_surface_2023-12-29.png` (all 42 smiles in 3-D with the held-out beads — the
whole-day analogue of Heston's smile surface, with no interpolation between expiries).
- Tracks **held-out** quotes across maturities — held-out IV RMSE **0.0126** (SPX 2023-12-29).
- The object we actually model is the **density**: a labeled sum of 4 lognormals, with skew and a
  sharp near-money "pin" of mass that a single lognormal cannot produce.

### Slide B3 — "Bahra: arbitrage-free by construction" — Nico
Images: `bahra_butterfly_2023-12-29.png` (+ optionally `bahra_calendar_repair_2023-12-29.png`)
- **Butterfly g(k) ≥ 0 on every expiry → 0 violations, by construction** (vs Heston 6, GP 25).
- **Calendar:** 9 as-fit crossings across expiries → **0 after a certified cummax repair**
  (the companion figure shows one crossing and its repair).
- The **only** model in the lineup that is static-arbitrage-free end to end — and the density's
  **moments** (VIX-like standard deviation, SKEW-like skewness) are directly interpretable.

### Slide B4 (optional) — "Bahra: stress test and robustness" — Nico
Images: `bahra_smiles_2023-03-10_SVB.png` (left) · `bahra_out_of_time_2023-01-04.png` (right top)
· `bahra_identifiability_2023-01-04.png` (right bottom)
- **SVB-collapse day:** held-out IV RMSE **0.0171 ≈ in-sample 0.0171** — no memorization under stress;
  arbitrage-free by construction on the day it matters.
- **Shelf life:** freeze a fit and price later days — 159 → 329 → 746 bps at +1/+5/+10 trading days;
  a calibration is good for about a day (matches the abstract's "stress test by starving of data").
- **What is stable:** refit 40× under bid–ask noise — parameters wander up to 72% (a mixture is
  non-identified) while the density's standard deviation moves **0.1%**: report moments, not parameters.

---

## C. Plot files (`figures/bahra_model_figures/`)
- `bahra_smiles_2023-12-29.png` — fitted smile vs held-out quotes, 4 maturities (benchmark day).
- `bahra_smiles_2023-03-10_SVB.png` — same layout on the SVB-collapse stress day.
- `bahra_surface_2023-12-29.png` — 3-D: all 42 fitted smiles + 1,317 held-out beads, no cross-expiry fill.
- `bahra_density_2023-12-29.png` — density as a labeled sum of 4 lognormals vs a single lognormal.
- `bahra_butterfly_2023-12-29.png` — exact g(k) ≥ 0 on every expiry (0 butterfly violations).
- `bahra_calendar_repair_2023-12-29.png` — one as-fit calendar crossing and its cummax repair.
- `bahra_out_of_time_2023-01-04.png` — frozen fit vs same-day refit at +1/+5/+10 trading days.
- `bahra_identifiability_2023-01-04.png` — parameters wander, moments pinned (40 refits under noise).

## D. Honest framing (for the talk track)
- On the full cleaned quote set (6,580 quotes incl. illiquid wings) our hold-out IV RMSE is **0.0126**.
  Like-for-like caution: on Heston's liquidity-filtered ~800-quote universe (mid>5, 30<dte<300, vol>10)
  Heston still fits tighter — 0.0126 vs our 0.0156 — its 5 parameters concentrate on the liquid core,
  while our density also carries the hard illiquid wings the filter removes. (GP's 0.0024 is
  near-interpolation on a ~8/92 split — a different task.) Our edge is being the **only end-to-end
  arbitrage-free** model **and** handing back an interpretable density.
- Heads-up for the team: the deck's **Heston** RMSE (0.0269 / 0.0258) differs from the current
  `Heston_model.ipynb` (~0.013) and from the README — worth reconciling with Uran so the cross-model
  numbers are on one footing before recording.
