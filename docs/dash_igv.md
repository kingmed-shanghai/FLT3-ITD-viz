# Dash IGV Visualization App Sample Usage

## Overview

The `test_igv.py` script in the `tests` directory demonstrates setting up a Dash application for visualizing genomic data with the Integrative Genomics Viewer (IGV). It employs a Flask server to serve genomic data files (VCF and TBI) and uses the Dash framework to embed the IGV component for interactive visualization.

## Features

- **Package-Based Data Serving**: Uses `importlib.resources` to serve VCF and TBI files from the `tests.data` directory in the package.
- **IGV Integration**: Embeds the IGV component in a Dash application for interactive genomic data visualization.
- **CORS Configuration**: Enables Cross-Origin Resource Sharing (CORS) to allow requests from any origin.

## Running the App

To run the app, navigate to the project root directory and execute the following command:

```bash
python -m tests.test_igv
```

This command starts the Dash server on `http://localhost:18050`.

## Visualization

Upon navigating to `http://localhost:18050` in a web browser, the IGV component will be displayed, pre-loaded with the specified VCF file, ready for interactive exploration.

## Key Components

- **Flask Route (`send_data`)**: Serves the VCF and TBI files from the package.
- **IGV Component Setup (`make_igv`)**: Configures the IGV component with predefined genomic data tracks.
- **Dash Layout**: Defines the layout of the Dash app to include the IGV component.
- **CORS Policy**: Allows access to data files from any origin.

