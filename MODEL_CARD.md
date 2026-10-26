# Model / system card

## Intended use

Estimate masked fictional gene profiles using a spatial kernel and explicitly separate interpolation from extrapolation. Educational local experiment; no production deployment is implied.

## Data

Synthetic arrays, manually written documents or replayed JSON. No real user records. Seeds and sample inputs are recorded in app.py and sample_input.json.

## Method

Use Gaussian distance weights over observed spatial spots to interpolate multi-gene expression. Select length scale using a validation subset from one tissue, then evaluate a separate synthetic tissue with its own observed reference spots.

## Evaluation protocol

Report RMSE for random masked spots and an edge-region holdout. Compare with the mean observed expression vector; fit length scale without reading final masked targets.

## Known limits

This is spatial interpolation on smooth synthetic fields, not a spatial foundation model. Tissue boundaries, cellular mixtures and discontinuities can violate smoothness.

## Verification status

Local tests and default experiment are executed during packaging. Live model generation is not exercised in the build. A successful validation result is limited to the checks implemented in code.

## Further work

Add real spatial data, tissue-level train/test splits, graph-based models, boundary-aware kernels and uncertainty estimates.
