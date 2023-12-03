"""
Dash App for Genomic Data Visualization

This module sets up a Dash application to visualize genomic variant data using the Integrative Genomics Viewer (IGV).
It serves variant call format (VCF) files and their index files (TBI) from a specified directory within the package.
"""

import importlib.resources
from pathlib import Path

import dash
import dash_bio
from dash import html
from flask import Flask, send_from_directory
from flask_cors import CORS

# Access the data directory within the 'tests.data' package.
DATA_DIR = importlib.resources.files("tests.data")
assert isinstance(DATA_DIR, Path) and DATA_DIR.is_dir()

# Constants for sample name and file names.
SAMPLE_NAME = "SRR2980466"
SAMPLE_VCF = "SRR2980466_output_TD.vcf.gz"
SAMPLE_VCF_INDEX = "SRR2980466_output_TD.vcf.gz.tbi"

# Ensure the VCF and its index file exist in the data directory.
assert DATA_DIR.joinpath(SAMPLE_VCF).is_file()
assert DATA_DIR.joinpath(SAMPLE_VCF_INDEX).is_file()

# Constants for genomic data.
GENOME = "hg38"
REGION = "chr13:28,046,009-28,050,715"
ROUTE_ROOT = "data"

# Initialize Dash app and Flask server.
APP = dash.Dash(__name__)
server = APP.server
assert isinstance(server, Flask)


@server.route(f"/{ROUTE_ROOT}/<path:path>")
def send_data(path):
    """
    Serve a file from the data directory.

    :param path: Path to the file within the data directory.
    :return: Flask response object to send the file.
    """
    APP.logger.info(f"Serving file: {path}")
    try:
        response = send_from_directory(str(DATA_DIR), path, as_attachment=True)
        response.headers["Content-Type"] = "application/octet-stream"
        response.headers["Content-Disposition"] = f"attachment; filename={path}"
        return response
    except Exception as e:
        APP.logger.error(f"Error serving file: {e}")
        raise e


# Enable CORS for all routes using the specified root.
CORS(server, resources={rf"/{ROUTE_ROOT}/*": {"origins": "*"}})


def make_igv():
    """
    Create the IGV component for the Dash app.

    :return: IGV component configured with genomic data tracks.
    """
    track_data = [
        {
            "type": "variant",
            "format": "vcf",
            "url": f"{ROUTE_ROOT}/{SAMPLE_VCF}",
            "indexURL": f"{ROUTE_ROOT}/{SAMPLE_VCF_INDEX}",
            "name": f"{SAMPLE_NAME} FLT3-ITD variants",
            "squishedCallHeight": 1,
            "expandedCallHeight": 4,
            "displayMode": "EXPANDED",
            "minHeight": 50,
            "maxHeight": 500,
            "autoHeight": True,
        },
    ]

    return dash_bio.Igv(
        id="FLT3-ITD",
        genome=GENOME,
        locus=REGION,
        tracks=track_data,
    )


# Define the layout of the Dash app to include the IGV component.
APP.layout = html.Div([make_igv()])

if __name__ == "__main__":
    # Run the Dash app server on port 18050 in debug mode.
    APP.run_server(debug=True, port=18050)
