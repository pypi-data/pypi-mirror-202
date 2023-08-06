import ephem
import numpy as np

from pyorbital.orbital import Orbital as OldOrbital
from datetime import datetime, timedelta
from typing import Tuple
from exceptions import ChecksumError

from math import pi, acos, cos, radians


TLE_URLS = ('http://www.celestrak.com/NORAD/elements/active.txt',
            'http://celestrak.com/NORAD/elements/weather.txt',
            'http://celestrak.com/NORAD/elements/resource.txt',
            'https://www.celestrak.com/NORAD/elements/cubesat.txt',
            'http://celestrak.com/NORAD/elements/stations.txt',
            'https://www.celestrak.com/NORAD/elements/sarsat.txt',
            'https://www.celestrak.com/NORAD/elements/noaa.txt',
            'https://www.celestrak.com/NORAD/elements/amateur.txt',
            'https://www.celestrak.com/NORAD/elements/engineering.txt')


infTime = ephem.Date(float("inf"))

class Orbital:
    """
        A class simulating an orbital one.orbital.Orbital, but based on Piefem. 
        Solves the problem of "Calculations in deep space are not supported" when
        calculating high orbits, such as the ARKTIKA M1

        The *satellite* parameter is the name of the satellite to work on and is
        used to retrieve the right TLE data for internet or from *tle_file* in case
        it is provided.
        
        In:
            satellite: str
            tle_file: str
            line1: str
            line2: str
    """
    
    def __init__(self, satellite: str, tle_file: str = None, line1: str = None, line2: str = None) -> None:
        self.satelliteName: str = satellite.upper()
        self._line1: str = None
        self._line2: str = None
        
        if line1 is not None and line2 is not None:
            self._line1 = line1.strip()
            self._line2 = line2.strip()
            self.tle =  ephem.readtle(self.satelliteName, self._line1, self._line2)
            
        else:
            if tle_file:
                with open(tle_file, 'r') as f:
                    lines = f.readlines()
                    for i in range(len(lines)):
                        # if Satellite founded in tle file and line1 and line2 exist
                        if self.satelliteName in lines[i] and (len(lines) - i >= 2):
                            self._line1 = lines[i+1].strip()
                            self._line2 = lines[i+2].strip()
                            
                            self.tle =  ephem.readtle(self.satelliteName, self._line1, self._line2)
                            
                            break
                        
            if not self.tle:
                raise KeyError(f"Found no TLE entry for {satellite}")
            
        self._checksum()
        
        
    def _checksum(self):
        """Calculate checksum for the current TLE."""
        for line in [self._line1, self._line2]:
            check = 0
            for char in line[:-1]:
                if char.isdigit():
                    check += int(char)
                if char == "-":
                    check += 1

            if (check % 10) != int(line[-1]):
                raise ChecksumError(self.satelliteName + " " + line)
    
    
    def get_observer_look(self, utc_time: datetime, lon: float, lat: float, alt: float) -> Tuple[float, float]:
        """
            Calculate observers look angle to a satellite.
            
            In:
                utc_time: datetime Observation time
                lon: float Longitude of observer position on ground in degrees east
                lat: float Latitude of observer position on ground in degrees north
                alt: float Altitude above sea-level (geoid) of observer position on ground in km
            Out:
                Azimuth: float
                Elevation: float
        """
        
        obs = ephem.Observer()
        obs.lat = str(lat)
        obs.lon = str(lon)
        obs.date = utc_time.strftime("%Y/%m/%d %H:%M:%S")
        
        self.tle.compute(obs)
        
        azimuth: float = self.tle.az
        elevation: float = self.tle.alt

        return azimuth / pi * 180.0 , elevation / pi * 180.0
        
    
    def get_next_passes(self, utc_time: datetime, length: int, lon: float, lat: float, alt: float, tol: float=0.1, horizon: int=0):
        """
            Calculate passes for the next hours for a given start time and a
            given observer.

            Original by Martin.
            In:
                utc_time: datetime Observation time
                length: int Number of hours to find passes
                lon: float Longitude of observer position on ground
                lat: float Latitude of observer position on ground
                alt: float Altitude above sea-level (geoid) of observer position on ground
                tol: float precision of the result in seconds
                horizon: int the elevation of horizon to compute risetime and falltime.

            Out:
                [(rise-time, fall-time, max-elevation-time), ...]
        """
        
        # FIX IT
        #if tol < 0.1: tol = 0.1
        obs = ephem.Observer()
        obs.lat = str(lat)
        obs.lon = str(lon)
        obs.date = utc_time.strftime("%Y/%m/%d %H:%M:%S")
        obs.pressure = 0
        obs.horizon = '20:0'
        obs.date = obs.next_pass(self.tle)[0]
        self.tle.compute(obs)
        el = self.tle.alt / 3.14159 * 180.0
        print(el)
        """
        obs = ephem.Observer()
        obs.lat = ephem.degrees(str(lat))
        obs.lon = ephem.degrees(str(lon))
        obs.elevation = 1000*alt
        obs.horizon = "30:00" #ephem.degrees(radians(horizon))
        obs.date = ephem.Date(utc_time.strftime("%Y/%m/%d %H:%M:%S"))
        
        pas = obs.next_pass(self.tle)
        start: datetime = utc_time
        end: datetime = utc_time + timedelta(hours=length)
        """
        """
        ris = obs.next_rising(self.tle, start=start)
        time = datetime.strptime(str(ephem.Date(ris)), "%Y/%m/%d %H:%M:%S")
        print(self.get_observer_look(time, lat=55.671226, lon=37.625304, alt=0.16))
        print()
        """
        """
        search: datetime = datetime.strptime(str(pas[0]), "%Y/%m/%d %H:%M:%S")
        final: datetime = datetime.strptime(str(pas[2]), "%Y/%m/%d %H:%M:%S")
        
        #while start < end:
        _, el = self.get_observer_look(search, lon, lat, alt)
        while abs(horizon - el) > 15:
            search += timedelta(minutes=1)
            _, el = self.get_observer_look(search, lon, lat, alt)
            
        while abs(horizon - el) > 3:
            search += timedelta(seconds=1)
            _, el = self.get_observer_look(search, lon, lat, alt)
            
        while abs(horizon - el) > tol:
            search += timedelta(microseconds=500)
            _, el = self.get_observer_look(search, lon, lat, alt)
            
            
        _, el = self.get_observer_look(final, lon, lat, alt)
        while abs(horizon - el) > 15:
            final -= timedelta(minutes=1)
            _, el = self.get_observer_look(final, lon, lat, alt)
            
        while abs(horizon - el) > 3:
            final -= timedelta(seconds=1)
            _, el = self.get_observer_look(final, lon, lat, alt)
            
        while abs(horizon - el) > tol:
            final -= timedelta(microseconds=500)
            _, el = self.get_observer_look(final, lon, lat, alt)
            #print(horizon - el)
        """            
        
        
        #pas[0] = ephem.Date(search.strftime("%Y/%m/%d %H:%M:%S"))
        #pas[2] = ephem.Date(final.strftime("%Y/%m/%d %H:%M:%S"))
        return pas #ephem.Date(search.strftime("%Y/%m/%d %H:%M:%S")), pas[1], ephem.Date(final.strftime("%Y/%m/%d %H:%M:%S"))
    

    def get_lonlatalt(self, utc_time: datetime) -> Tuple[float, float, float]:
        self.tle.compute(utc_time.strftime("%Y/%m/%d %H:%M:%S"))
        return self.tle.sublong / pi * 180.0, self.tle.sublat / pi * 180.0, self.tle.elevation
        
    def __str__(self) -> str:
        return self.satelliteName + " " + str(self.tle)
    
if __name__ == "__main__":
    orb = Orbital("NOAA 19", "./lorettOrbital/tle/tle.txt")
    #porb = OldOrbital("NOAA 19", "./lorettOrbital/tle/tle.txt")
    
    t = orb.get_next_passes(datetime.utcnow(), length=24, lat=55.671226, lon=37.625304, alt=0.16, horizon=55)[0::2]
    
    for i in t:
        print(ephem.Date(i), end=" ")
        
        time = datetime.strptime(str(ephem.Date(i)), "%Y/%m/%d %H:%M:%S")
        print(orb.get_observer_look(time, lat=55.671226, lon=37.625304, alt=0.16), end=" ")
        
        print()
        
    print(t)
    
    #print(orb.get_lonlatalt(utc_time=datetime.utcnow()))
    