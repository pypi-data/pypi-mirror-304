import os
from typing import List
from fmo.api import FMO, FMO_API_URL


class Lease:
    def __init__(self, lease_data):
        self._data = lease_data

    def center(self):
        coords = [(c['lat'], c['lng']) for c in self._data["coords"]]
        return coords[0]

    def geojson_data(self):
        coords = [(c['lng'], c['lat']) for c in self._data["coords"]]
        geojson_data = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [coords]
            }
        }

        return geojson_data
    
class LeaseRepository:
    def __init__(self):
        fmo_token = os.getenv("FMO_TOKEN")
        fmo_url = os.getenv("FMO_API_URL", FMO_API_URL)
        self.fmo = FMO(fmo_token, fmo_url)

    def get_lease_list(self) -> List[Lease]:
        leases = self.fmo.list_water_leases()
        return [Lease(l) for l in leases]

    def get_lease_by_id(self, lease_id) -> Lease:
        leases = self.fmo.list_water_leases()
        leases = list(filter(lambda l: l['leaseId'] == lease_id, leases))
        if len(leases) == 0:
            return None
        
        return Lease(leases[0])