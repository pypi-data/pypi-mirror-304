import click
import geojson

from fmo.bed import BedRepository
from fmo.lease import LeaseRepository
from fmo.simulate import coords_to_path_points, generate_spiral_path
from fmo.draw import preview_geojson
from fmo.utils import geojson_center

@click.group()
def simulator():
    pass

@simulator.command()
@click.option("--output", "-o")
@click.option("--lat", default=None, type=float)
@click.option("--lng", default=None, type=float)
@click.option("--lease", default=None, type=str)
@click.option("--bed", default=None, type=str)
@click.option("-n", default=200, type=int)
@click.option("--seed", default=None, type=int)
@click.option("--preview", default=False, is_flag=True, help="Show the path on a map")
def spiral_path(output: str, lat, lng, lease, bed, n, seed, preview):
    if lease is not None:
        lease_repo = LeaseRepository()
        lease = lease_repo.get_lease_by_id(lease)
        if lease is None:
            click.echo("Lease not found")
            return
        
        lat, lng = lease.center()
    elif bed is not None:
        bed_repo = BedRepository()
        bed = bed_repo.get_bed_by_id(bed)
        if bed is None:
            click.echo("Bed not found")
            return
        
        lng, lat = geojson_center(bed["geometry"])
    elif lat is None or lng is None:
        click.echo("Must provide either lease or lat and lng")

    coords = generate_spiral_path(lat, lng, n=n, seed=seed)
    geo = coords_to_path_points(coords)

    if output is not None:
        try:
            with open(output, mode="w") as fp:
                geojson.dump(geo, fp)
        except IOError as err:
            click.echo(f"Failed to write to output file: {err.strerror}")

    if preview:
        preview_geojson(output, (lat, lng))

def register_commands(cli):
    cli.add_command(simulator)
