import os
from typing import List
from fmo.api import FMO, FMO_API_URL

class BedRepository:
    def __init__(self):
        fmo_token = os.getenv("FMO_TOKEN")
        fmo_url = os.getenv("FMO_API_URL", FMO_API_URL)
        self.fmo = FMO(fmo_token, fmo_url)

    def get_bed_list(self) -> List:
        beds = self.fmo.list_beds()
        return beds

    def get_bed_by_id(self, bed_id) -> dict:
        beds = self.get_bed_list()
        beds = list(filter(lambda l: l['uid'] == bed_id, beds))
        if len(beds) == 0:
            return None
        
        return beds[0]