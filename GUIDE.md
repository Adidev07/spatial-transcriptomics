# Spatial Gene Expression Interpolation

## Purpose and intended demonstration

Estimate masked fictional gene profiles using a spatial kernel and explicitly separate interpolation from extrapolation. This is a computational biology learning project with synthetic or fictional inputs, not a clinical or experimentally validated system.

## How the implementation works

Use Gaussian distance weights over observed spatial spots to interpolate multi-gene expression. Select length scale using a validation subset from one tissue, then evaluate a separate synthetic tissue with its own observed reference spots.

## Evaluation and evidence

Report RMSE for random masked spots and an edge-region holdout. Compare with the mean observed expression vector; fit length scale without reading final masked targets.

## Setup and commands

Requires Python 3.10 or newer and NumPy. Create a virtual environment: python -m venv .venv. On Windows use .venv\Scripts\python.exe if activation is unavailable. Install with python -m pip install -r requirements.txt. Run python app.py, then open results/report.html in your browser. Run python -m unittest discover -v to execute tests. The default seed is 42; change it with --seed. Replace sample_input.json using --input path-to-file.json, preserving its schema. Algorithm-only projects generate synthetic arrays from the seed rather than consuming external files.

## Architecture and file responsibilities

CLI arguments -> JSON input or seeded generator -> domain pipeline -> validation or evaluation -> JSON and HTML artifacts. Imported functions can be used in a notebook or a separate application. Model checkpoints preserve learned arrays where applicable; see app.py for parameter order. This package does not include a production web service. Each project is independent and includes its own helper code so the ZIP can be extracted and run alone. app.py holds the experiment and domain functions: tissue, interpolate, run. kit.py contains reporting, input loading and only the retrieval or generation helpers needed by this project. sample_input.json contains editable inputs. test_app.py checks domain behaviors; test_reporting.py checks metrics and HTML output boundaries. results/metrics.json records outputs and results/report.html provides a browser-readable report. Numeric projects also save arrays or learned parameters to results/artifacts.npz; inspect its keys with numpy.load. MODEL_CARD.md explains intended use and limits. .github/workflows/tests.yml runs tests and the fixture experiment. No API key is needed.

## Limitations and next improvements

This is spatial interpolation on smooth synthetic fields, not a spatial foundation model. Tissue boundaries, cellular mixtures and discontinuities can violate smoothness. Add real spatial data, tissue-level train/test splits, graph-based models, boundary-aware kernels and uncertainty estimates.

## Interview walkthrough

Present the problem and demonstrate one normal example, then one failure or boundary case. Explain the baseline or fixture mode, the split or validation design, and one limitation before discussing an extension. Be ready to trace data through the functions listed above. Explain why the chosen metric matches the task and why the available results cannot establish production performance. Add your own documented experiment and be precise about what you implemented or changed. These are AI-assisted educational projects; filenames and synthetic scores are not evidence of client work.

## Research context and reading

These topics were selected from research directions reviewed on 22 October 2026. Recent activity suggests useful skills to develop; it is not a forecast of hiring, commercial success or scientific validity. The implementation is a small educational baseline and does not reproduce or claim the performance of any cited foundation model. Reading: Universal cell embedding provides a foundation model for cell biology (2026): https://www.nature.com/articles/s41586-026-10689-z.