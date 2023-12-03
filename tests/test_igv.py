import importlib.resources
from pathlib import Path

import dash
import dash_bio
from dash import html
from flask import Flask, send_from_directory
from flask_cors import CORS

DATA_DIR = importlib.resources.files("tests.data")
assert isinstance(DATA_DIR, Path) and DATA_DIR.is_dir()

SAMPLE_NAME = "SRR2980466"

SAMPLE_VCF = "SRR2980466_output_TD.vcf.gz"
assert DATA_DIR.joinpath(SAMPLE_VCF).is_file()

SAMPLE_VCF_INDEX = "SRR2980466_output_TD.vcf.gz.tbi"
assert DATA_DIR.joinpath(SAMPLE_VCF_INDEX).is_file()

GENOME = "hg38"
REGION = "chr13:28,046,009-28,050,715"

ROUTE_ROOT = "data"


APP = dash.Dash(__name__)
server = APP.server

assert isinstance(server, Flask)


@server.route(f"/{ROUTE_ROOT}/<path:path>")
def send_data(path):
    APP.logger.info(f"Serving file: {path}")
    try:
        response = send_from_directory(str(DATA_DIR), path, as_attachment=True)
        response.headers["Content-Type"] = "application/octet-stream"
        response.headers["Content-Disposition"] = f"attachment; filename={path}"
        return response
    except Exception as e:
        APP.logger.error(f"Error serving file: {e}")
        raise e


@server.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response


# Enable CORS for all routes
CORS(server, resources={r"/track_data/*": {"origins": "*"}})


def make_igv():
    genome = GENOME
    region = REGION
    vcf = f"{ROUTE_ROOT}/{SAMPLE_VCF}"
    vcf_index = f"{ROUTE_ROOT}/{SAMPLE_VCF_INDEX}"
    track_data = [
        {
            "type": "variant",
            "format": "vcf",
            "url": vcf,
            "indexURL": vcf_index,
            "name": f"{SAMPLE_NAME} FLT3-ITD",
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
        genome=genome,
        locus=region,
        tracks=track_data,
    )


APP.layout = html.Div([make_igv()])

if __name__ == "__main__":
    APP.run_server(debug=True, port=18050)
