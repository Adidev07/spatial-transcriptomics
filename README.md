# Spatial Gene Expression Interpolation

Estimate masked fictional gene profiles using a spatial kernel and explicitly separate interpolation from extrapolation.

**Category:** Biology / Spatial ML

**Execution:** Actual local algorithm or workflow; no external model service required.

## Run

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
python -m unittest discover -v
```

Open `results/report.html` after running. Python 3.10+ is required. Use `--help` for input and seed options.

## Architecture

```mermaid
flowchart LR
  A[CLI and input] --> B[Domain pipeline]
  B --> C[Validation or evaluation]
  C --> D[JSON and HTML report]
```

## Algorithm

Use Gaussian distance weights over observed spatial spots to interpolate multi-gene expression. Select length scale using a validation subset from one tissue, then evaluate a separate synthetic tissue with its own observed reference spots.

## Evaluation

Report RMSE for random masked spots and an edge-region holdout. Compare with the mean observed expression vector; fit length scale without reading final masked targets.

## Limitations

This is spatial interpolation on smooth synthetic fields, not a spatial foundation model. Tissue boundaries, cellular mixtures and discontinuities can violate smoothness.

## Documentation

- [PDF project guide](PROJECT_GUIDE.pdf)
- [Editable guide](GUIDE.md)
- [Model and system card](MODEL_CARD.md)
- [Measured results](results/metrics.json)
- [Test output](TEST_RESULTS.txt)

## Extend it

Add real spatial data, tissue-level train/test splits, graph-based models, boundary-aware kernels and uncertainty estimates.

AI-assisted educational project with synthetic data. Review, customize and explain your own contribution accurately. MIT license.

## Biology scope and current relevance

Default inputs are synthetic or project-authored. No clinical deployment or wet-lab validation is claimed. See [research context](RESEARCH_CONTEXT.md) and [data provenance](DATA_PROVENANCE.md).

- [Universal cell embedding provides a foundation model for cell biology](https://www.nature.com/articles/s41586-026-10689-z) (2026)
