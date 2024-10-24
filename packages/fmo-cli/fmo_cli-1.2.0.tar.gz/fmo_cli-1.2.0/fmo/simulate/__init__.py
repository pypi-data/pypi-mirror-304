import math
from typing import Tuple
import geojson
import random
from datetime import datetime, timedelta
    

def generate_spiral_path(lat: float, lng: float, n: int = 150, seed=None):
    #x = R1.cos (n1(θ+ψ1)) + R2.cos (n2(θ+ψ2))
    #y = R1.sin (n1(θ+ψ1)) + R2.sin (n2(θ+ψ2)) 
    
    #As 'θ' varies from 0 to 2π this will trace one lap around the circle ('R' is the
    #radius). This is our basic wheel. If we multiply θ by a positive integer this will be
    #equivalent to making the wheel rotate faster. A negative integer will make the wheel
    #rotate in the opposite direction. To create the spirograph patterns we combine two
    #wheels rotating at different speeds, say n1 and n2.
    
    #The Second wheel of radius R2 makes n2 full turns as it travels n1 times around the
    #inner wheel of radius R1.

    #The starting positions of the wheels can be changed by adding in a phase component: ψ

    #http://eddaardvark.co.uk/python_patterns/spirograph.html

    random.seed(seed)

    coords = []
    frame = FrameXY(lat, lng)
    
    step = 2*math.pi / n
    offset = random.random() * 2*math.pi
    r1 = 50.0
    r2 = -80.0
    speed1 = 1.9
    speed2 = 4.5
    speed3 = 0.1
    skew_x = 0.5 + random.random()
    skew_y = 0.5 + random.random()

    for i in range(n):
        t = (i*step) + offset
        r1x = r1
        r1y = r1
        x = (r1x*math.cos(speed1*t)) + (r2*math.cos(speed2*t))
        y = (r1y*math.sin(speed1*t)) + (r2*math.sin(speed2*t))

        x = x * skew_x
        y = y * skew_y

        # rotate the frame
        x = (x*math.cos(t*speed3)) - (y*math.sin(t*speed3))
        y = (y*math.cos(t*speed3)) + (x*math.sin(t*speed3))

        coords.append(frame.xy_to_latlng((x, y)))

    return coords

def coords_to_path_points(coords, t = None, delta = None):
    if t is None:
        t = datetime.now()
    if delta is None:
        delta = timedelta(seconds=15)
    
    features = []
    for i, coord in enumerate(coords):
        feature = geojson.Feature(
            geometry=geojson.Point((coord[1], coord[0])), 
            properties={"timestamp": (t + delta * i).isoformat()}
        )
        features.append(feature)
        
    feature_collection = geojson.FeatureCollection(features)
    return feature_collection

class FrameXY:
    def __init__(self, lat: float, lng: float):
        """Coordinate system in meters, centered at the given gps coord

        Args:
            lat (float): Latitude
            lng (float): Longitude
        """
        self.lat = lat
        self.lng = lng

    def xy_to_latlng(self, point: Tuple[float, float]) -> Tuple[float, float]:
        """Transform a XY coordinate in meters to a lat lng
        X axis moves east/west
        Y axis moves north/south

        Args:
            point (Tuple[float, float]): X and Y coordinates

        Returns:
            Tuple[float, float]: Lat and Lng coordinates
        """
        meters_north = point[1]
        meters_east = point[0]
        # Move north/south (latitude)
        delta_lat = meters_north / 111320
        # Move east/west (longitude), adjusting for latitude
        delta_lng = meters_east / (111320 * math.cos(math.radians(self.lat)))

        new_lat = self.lat + delta_lat
        new_lng = self.lng + delta_lng

        return (new_lat, new_lng)