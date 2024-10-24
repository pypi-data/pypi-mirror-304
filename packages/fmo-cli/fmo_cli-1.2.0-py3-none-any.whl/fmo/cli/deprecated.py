import os
import click

from fmo.draw import preview_geojson
from fmo.nmea import parse_nmea_file
from fmo.api import FMO, FMO_API_URL
from fmo.simulate.path_gen import PathCreator

"""
Here is a collection of commands that are considered deprecated
They still work but will not be shown in the fmo help section
"""

@click.command(hidden=True)
@click.argument('file')
def nmea(file):
    click.echo(file)
    if not file.endswith(".csv"):
        click.echo("Expecting a CSV file")
        return

    df = parse_nmea_file(file)
    print(df)

@click.command(hidden=True)
@click.option('--format', default="CSV", help="What format is the file? NMEA, CSV, GEOJSON")
@click.argument('file')
def upload_path(file, format):

    fmo_token = os.getenv("FMO_TOKEN")
    fmo_url = os.getenv("FMO_API_URL", FMO_API_URL)

    fmo = FMO(fmo_token, fmo_url)

    if format.lower() == "nmea":
        path = parse_nmea_file(file)
        df = path.dataframe()
        print(df)
        fmo.upload_path(path)
        return

    click.echo(f"Unexpected format: {format}")

@click.command(hidden=True)
@click.option('--format', default="geojson", help="What format is the file? NMEA, CSV, GEOJSON")
@click.argument('file')
def preview_path(file, format):
    if format.lower() == "nmea":
        path = parse_nmea_file(file)
        preview_geojson(path.geojson())
        return
    
    if format.lower() == "geojson":
        preview_geojson(file)
        return

    click.echo(f"Unexpected format: {format}")
    
@click.command(hidden=True)
@click.option("--output", "-o", default="output.json", help="Where to save the geojson result")
def generate_harvest_path(output):
    pc = PathCreator()
    points = pc.create_path()
    geojson_str = pc.gps_to_geojson(points)
    with open(output,'w+') as output_file:
        output_file.write(geojson_str)

def register_commands(cli):
    cli.add_command(nmea)
    cli.add_command(upload_path)
    cli.add_command(preview_path)
    cli.add_command(generate_harvest_path)