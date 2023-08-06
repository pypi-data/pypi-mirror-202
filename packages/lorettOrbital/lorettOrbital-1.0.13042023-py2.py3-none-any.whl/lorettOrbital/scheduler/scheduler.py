##
# @file scheduler.py
#
# @brief A group of classes describing interaction with satellites. TLE, orbital position and schedule.
#
# @section schedulerDependencies Libraries/Modules
# - datetime standart library (https://docs.python.org/3/library/datetime.html)
#   - Access to datetime and timedelta classes.
#
# - math standart library (https://docs.python.org/3/library/math.html)
#   - Access to radians, tan, sin and cos functions.
#
# - pathlib standart library (https://docs.python.org/3/library/pathlib.html)
#   - Access to Path class.
#
# - typing standart library (https://docs.python.org/3/library/typing.html)
#   - Access to List, Tuple, Any and Callable class.
#
# - dataclasses standart library (https://docs.python.org/3/library/dataclasses.html)
#   - Access to dataclass decorator and field function.
#
# - pyorbital library (https://pypi.org/project/pyorbital/)
#   - Access to Orbital and tlefile classes.
#
# - prettytable library (https://pypi.org/project/prettytable/)
#   - Access to the PrettyTable class for beautiful schedule formatting.
#
# - verboselogs library (https://pypi.org/project/verboselogs/)
#   - Access to VerboseLogger class.
#
# - requests library (https://pypi.org/project/requests/)
#   - Access to get function and exceptions.
#
# - exceptions module (local)
#   - Access to lorettOrbital exceptions classes.
#
# @section todo TODO
# - Adaptation of pyephem to the pyorbital style.
#
# @section autor Author(s)
# - Created by MrFentazis on 23/03/2023.
#


# Impors
from pyorbital.orbital import Orbital, tlefile
from datetime import datetime, timedelta
from math import radians, tan, sin, cos
from prettytable import PrettyTable
from pathlib import Path
#!!!

from verboselogs import VerboseLogger
from lorettOrbital.exceptions import *

from requests import get, exceptions
from typing import List, Tuple, Any, Callable

from dataclasses import dataclass, field

# Global Constants
## Station types list; rotator - classic azimuth and elevation systems; legacy - minutes:seconds special type for V. Rosental lorett systems.
stationTypes = [
                "rotator",
                "legacy" # for Rosental systems
                ]

## Satellite TLE sources list.
sources = {
    "default": ["https://celestrak.com/NORAD/elements/active.txt"],
    "weather": ["https://celestrak.org/NORAD/elements/weather.txt"]
}

## List of active satellites by communication bands
satLists = {
    ### Actual X-band satellites list.
    "X": [
            "TERRA",
            "AQUA",
            "HAISI 1",
            "NOAA 20",
            "NOAA 21 (JPSS-2)",
            "SUOMI NPP",
            "FENGYUN 3E",
            "FENGYUN 3D",
            "2022-019J",
            #"EOS-6 (OCEANSAT-3)", # It has both a transmitter and equipment and the frequency is known, but it seems to transmit data only over certain territories.
            #"ARKTIKA-M 1", # No info
    ],
    
    ### Actual L-band HRPT satellites list.
    "L": [
            "NOAA 18",
            "NOAA 19",
            "METEOR-M 2",
            "METEOR-M2 2",
            "METOP-B",
            "METOP-C",
            #"ARKTIKA-M 1", # It has a transmitter and the necessary equipment, but it doesn't seem to be working at the moment
    ],
    
    ### Actual APT-band satellites list.
    "APT": [
           "NOAA 15",
            "NOAA 18",
            "NOAA 19",
            "METEOR-M 2" 
    ]
}

# Classes
@dataclass
class SchedulerConfig:
    """The class for contain data of station config
        dataclass that defines the settings of the Scheduler object
        
            @param stationName: str
            @param lat: float
            @param lon: float
            @param alt: float in kilometers
            @param satList: dict = satListLBand
            @param sampleRate: int = 6e6
            @param horizon: int = 10
            @param minApogee: int = 30
   
            @param path: str = '.'
            @param timeZone: int = 0
            
    """    
    stationName: str
    lat: float
    lon: float
    alt: float
    
    source: Any = field(default_factory= lambda: sources["default"]) # List or str
    satList: list = field(default_factory= lambda: satLists["L"])
    stationType: str = field(default_factory= lambda: stationTypes[0])
    horizon: int = 10
    minApogee: int = 30
    
    path: str = '.'
    timeZone: int = 0
    

@dataclass
class SatPass:
    """The class for contain data of sat pass
        dataclass describing a certain flight of the satellite over the observer.
            @param satName: str
            @param orb: Orbital
            @param culmination: float
            @param timeStart: datetime
            @param timeEnd: datetime
            @param timeCulmination: datetime
            @param status: str
    """
    satName: str
    orb: Orbital
    culmination: float
    timeStart: datetime
    timeEnd: datetime
    timeCulmination: datetime
    status: str = "wait"
    
    def __str__(self) -> str:
        return f"""SatPass(satName={self.satName}, culmination={round(self.culmination, 2)}, timeStart={self.timeStart.strftime("%d.%m.%Y")}, timeEnd={self.timeEnd.strftime("%d.%m.%Y")}, timeCulmination={self.timeCulmination.strftime("%d.%m.%Y")})"""


@dataclass
class TrackFile:
    """The class for contain data of trackFile
        dataclass describing the exported trajectory file
            @param satName: str
            @param timeStart: datetime
            @param trackPath: Path
    """
    satName: str
    timeStart: datetime
    trackPath: Path


@dataclass
class SphereCoordinates:
    """The class for contain pair sphere coordinates 
        dataclass describing a point in spherical coordinates.
            @param azimuth: float
            @param elevation: float
            @param time: datetime
    """
    azimuth: float
    elevation: float
    time: datetime
    
    
@dataclass
class SphereAltCoordinates:
    """The class for contain pair sphere alternative coordinates 
        dataclass describing a point in alternative spherical coordinates. Uses Degrees:Minutes as a string.
            @param azimuth: str
            @param elevation: str
            @param time: datetime
    """
    azimuth: str
    elevation: str
    time: datetime
    
    
@dataclass
class XYCoordinates:
    """The class for contain pair XY coordinates
        dataclass describing a point in XY coordinates. 
    
            @param x: float
            @param y: float
    """
    x: float
    y: float
    time: datetime
    


class Scheduler:
    '''
        The Scheduler class for working with the schedule and trajectories of satellites    
    '''

    def __init__(self, 
                 config: SchedulerConfig,
                 logger: VerboseLogger = None
                 ) -> None:
        
        """ The Scheduler class initilisazer
        
        @param config: StationConfig
        @param logger: VerboseLogger = None
        
        @return An instance of the Scheduler class initialized with the specified name.
        
        """

        self.logger: VerboseLogger = logger
        
        ## Check of sources
        ## TODO fix multisources mode
        if isinstance(config.source, str):
            
            ## if it is name of source from sources list
            if config.source in sources.keys():
                config.source = sources[config.source]
            
            else:
                if self.logger != None:
                    self.logger.warning(f'Unknown source "{config.source}", use default')
                    config.source = sources['default']
        
        self.config: SchedulerConfig = config

        self.satList: list = self.config.satList
        self.horizon: int = self.config.horizon
        self.minApogee: int = self.config.minApogee
        self.path = config.path
        
        ## Check station type
        if self.config.stationType not in stationTypes:
            if self.logger != None:
                self.logger.warning(f'Unexpected stationType "{self.config.stationType}", use default')
            
            self.config.stationType = stationTypes[0]
            
        self.stationType: str = self.config.stationType

        ## alt <= 9km - most higest earth place
        if not all([(abs(self.config.lon) <= 180, abs(self.config.lat) <= 90), self.config.alt <= 9]):
            raise InvalidCoordinates
        
        self.lon = round(self.config.lon, 5)
        self.lat = round(self.config.lat, 5)
        self.alt = round(self.config.alt, 5)

        self.timeZone = self.config.timeZone
        self.stationName = self.config.stationName

        if self.path == ".":
            self.path = Path.cwd()

        self.path = Path(self.path)

        self._createSubDirectories()
        
        self.update()

    
    def _createSubDirectories(self) -> None:
        """ The Service method for creating additional directories in path
        """

        self.tlePath = self.path / "tle" 
        
        if not self.tlePath.exists():
            if self.logger != None:
                self.logger.info("Create tle subdirectory")
            self.tlePath.mkdir(parents=True, exist_ok=True)

        
        self.tracksPath = self.path / "tracks" 
        
        if not self.tracksPath.exists():
            if self.logger != None:
                self.logger.info("Create tracks subdirectory")
            self.tracksPath.mkdir(parents=True, exist_ok=True)


        self.schedulePath = self.path / "schedule"
        
        if not self.schedulePath.exists():
            if self.logger != None:
                self.logger.info("Create schedule subdirectory")
            self.schedulePath.mkdir(parents=True, exist_ok=True)


    def sphericalToDecart(self, azimuth: float, elevation: float, time: datetime, convert: Callable[[float, float], list[float, float]]) -> XYCoordinates:
        """ The service method for converting from spherical coordinates to custom X Y coordinates using a custom function
            
        @param azimuth: float
        @param elevation: float
        
        @return coordinates: XYCoordinates
        """

        #if elevation == 90:
        #    return 0, 0

        azimuth = radians((azimuth + self.azimuthCorrection) % 360)
        elevation = radians(elevation)

        x, y = convert(azimuth, elevation)
        
        return XYCoordinates(x=x, y=y)
    
        #return XYCoordinates(y=-(self.config.focus / tan(elevation)) * cos(azimuth),
        #                     x=-(self.config.focus / tan(elevation)) * sin(azimuth), time=time)

    
    def degreesToDegreesAndMinutes(self, azimuth: float, elevation: float, time: datetime) -> SphereAltCoordinates:
        """ The method that translates angular coordinates to the form degrees:minutes (a, e) --> SphereAltCoordinates(a:m, e:m)

        @param azimuth: float (degree)
        @param elevation: float (degree)
        
        @return coordinates: SphereAltCoordinates
        
        """
        azimuthM = '000:00'
        elevationM = '000:00'
        
        if isinstance(azimuth, (float, int)):
            minutes = azimuth * 60
            degrees = minutes // 60
            minutes %= 60

            azimuthM = f"{int(degrees):03}:{int(minutes):02}"
            
        if isinstance(elevation, (float, int)):
            minutes = elevation * 60
            degrees = minutes // 60
            minutes %= 60

            elevationM = f"{int(degrees):03}:{int(minutes):02}"

        return SphereAltCoordinates(azimuth=azimuthM, elevation=elevationM, time=time)

    
    def update(self) -> bool:
        """ The method that updates TLE files
        
        @return status: bool
        """
        if self.logger != None:
            self.logger.info("Check update TLE")
            
        tleFile = self.tlePath / "tle.txt"
        now = datetime.utcnow()
        
        try:
            try:
                if tleFile.exists():
                    with open(tleFile, "r") as file:
                        lines = file.readlines()
                        dateTLE = datetime.strptime(lines[1].strip(), "# %Y%m%d %H%M%S")

                        ## Check old tles
                        oldSats = []
                        for i in range(2, len(lines), 3):
                            name = lines[i].strip()
                                
                            if len(lines) - i > 3:
                                try:
                                    line1 = lines[i+1].strip()
                                    line2 = lines[i+2].strip()
                                    tlefile.Tle(platform=name, line1=line1, line2=line2)
                                    oldSats.append(name)
                                        
                                except tlefile.ChecksumError:
                                    if self.logger != None:
                                        self.logger.info("Found bad TLE")
                                        self.logger.verbose(f"Found bad TLE name: {name}")
                                    continue
                            
                        ## If all satellites are found in the file and it is relevant
                        if all(i in oldSats for i in self.satList) and (now - dateTLE < timedelta(days=1)):
                            if self.logger != None:
                                self.logger.info("Use actual TLE")
                            return True
                            
                else:
                    oldSats = []
            
            except ValueError as e:
                self.logger.warning(f"Found bad tle data in {tleFile}")
                
            content = ""
            newSats = []
            for i in self.config.source:
                tle = get(i)

                if tle.status_code == 200:
                    lines = tle.text.split("\n")
                    for i in range(0, len(lines), 3):
                        name = lines[i].strip()
                            
                        if len(lines) - i > 3:
                            try:
                                line1 = lines[i+1].strip()
                                line2 = lines[i+2].strip()
                                tlefile.Tle(platform=name, line1=line1, line2=line2)
                                newSats.append(name)
                                content += f"{name}\n{line1}\n{line2}\n"
                                    
                            except (tlefile.ChecksumError, IndexError):
                                if self.logger != None:
                                    self.logger.info(f"Found bad TLE for {name}. skip")
                                continue
                    
                else:
                    if self.logger != None:
                        self.logger.warning(f"Connection failed code {tle.status_code}")
            
            ## if it was possible to get the tle of all the necessary satellites
            if all(i in newSats for i in self.satList):
                with open(tleFile, "w") as file:
                    ## dont remove this line, stupid pyorbital 
                    ## does not perceive comments in TLE and breaks down
                    file.write("# Autoupdated tle\n")
                    
                    file.write( now.strftime("# %Y%m%d %H%M%S\n"))
                    file.write(content)

                if self.logger != None:
                    self.logger.info("TLE updated")

                return True

            if content == "" and self.logger != None:
                self.logger.warning("Failed update TLE")

            ## the update failed, but the old file has all the satellites
            if content == "" and all(i in oldSats for i in self.config.satList) and self.logger != None:
                self.logger.warning(f"Use old TLE {dateTLE}")
                return False
                
            else:
                if self.logger != None:
                    self.logger.error(f"Failed to get TLE. exit")
                    

            return True
                    
        except Exception as e:
            if self.logger != None:
                self.logger.info(f"Exception in Scheduler.update {repr(e)}")
                self.logger.verbose(f"Exception message: {e}")

            return False
        

    @staticmethod
    def getCoordinatesByIp() -> Tuple[float, float, float]:
        """ The method that gets the station coordinates by his ip.

        Returned Altitude in kilometers.

        ATTENTION!

        THESE COORDINATES MAY BE VERY INACCURATE.

        USE IT ONLY FOR MAKING AN APPROXIMATE SCHEDULE.\n\n


        @return list[lon: float, lat: float, alt: float]


        If there is an error: lon = 0; lat = 0; alt = 0

        """

        try:
            query = get("http://ip-api.com/json").json()

            lon = query['lon']
            lat = query['lat']

            # temporary return only elevation by coordinates
            query = get(
                f'https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}').json()
            alt = query['results'][0]['elevation']

        except exceptions.ConnectionError:
            print('Error when get coordinates')
            print("No internet connection\n")

            return 0, 0, 0

        except Exception as e:
            print('Error when get coordinates')
            print(str(e))

            return 0, 0, 0

        alt /= 1000

        return lon, lat, alt


    def getSatellitePasses(self, start: datetime, length: int, satellite: str, tol: float = 0.001, updateTLE: bool = False) -> Tuple[Orbital, List[datetime]]:
        """ The method that calculates satellite passes by input parametres

        @param satellite: str
        @param start: datetime
        @param length: int
        @param tol: float
        @param updateTLE: bool

        @return passes: list[Orbital, list[datetime, datetime, datetime]]
        
        """

        if updateTLE:
            self.update()

        orb = Orbital(satellite, tle_file=str(self.tlePath / "tle.txt") )

        return orb, orb.get_next_passes(start, length, self.lon, self.lat, self.alt, tol, self.horizon)


    def getSchedule(self, timeStart: datetime, length: int, saveSchedule: bool=False, updateTLE: bool=False) -> List[SatPass]:
        """ The method that makes up the schedule, according to the parameters.
        
        It does not take into account time zone curves, since I am too lazy to saw the implementation for the sake of several points of the planet
        
        @param length: int
        @param saveSchedule: bool
        @param updateTLE: bool

        @return schedule: list[SatPass]

        """

        #self._checkCoordinates()

        if updateTLE:
            self.update()

        schedule = []
        
        for i in self.satList:
            orb, passes = self.getSatellitePasses(start=timeStart, length=length, satellite=i)
        
            for j in passes:
                culmination = orb.get_observer_look(j[2], lat = self.lat, lon = self.lon, alt = self.alt)[1]
                # if apogee > minApogee
                if culmination >= self.config.minApogee:
                    schedule.append(SatPass(satName = i, orb = orb, culmination=culmination, timeStart=j[0], timeEnd=j[1], timeCulmination=j[2]))
        
        ## Sort by time start 
        schedule = sorted(schedule, key=lambda p: p.timeStart)
        self.schedule = schedule

        timeCorrection = timedelta(hours=self.timeZone)
        
        ## Generate pretty string and file for schedule
        if saveSchedule:
            th = ["Satellite", "DateTime", "Azimuth", "Elevation"]
            td = []

            for satPass in schedule:
                start = satPass.timeStart
                stop = satPass.timeEnd
                apogee = satPass.timeCulmination

                td.append([satPass.satName,
                           (start + timeCorrection).strftime("%Y.%m.%d %H:%M:%S"),
                           *map(lambda x: round(x, 2), 
                           satPass.orb.get_observer_look(start, self.lon, self.lat, self.alt))])

                td.append([satPass.satName,
                           (apogee + timeCorrection).strftime("%Y.%m.%d %H:%M:%S"),
                           *map(lambda x: round(x, 2), 
                           satPass.orb.get_observer_look(apogee, self.lon, self.lat, self.alt))])

                td.append([satPass.satName,
                           (stop + timeCorrection).strftime("%Y.%m.%d %H:%M:%S"),
                           *map(lambda x: round(x, 2), 
                           satPass.orb.get_observer_look(stop, self.lon, self.lat, self.alt))])

                td.append([" ", " ", " ", " "])

                table = PrettyTable(th)

            ## Adding rows to tables
            for i in td:
                table.add_row(i)

            if self.logger != None:
                self.logger.info(f"Calculate schedule. {len(schedule)} passes found")
            
            ## Generate schedule string
            schedule = f"Satellits Schedule / LorettOrbital {__version__}\n"
            schedule += f"Coordinates of the position: {round(self.lon, 4)}° {round(self.lat, 4)}° {self.alt}km\n"
            schedule += f"Time zone: UTC {'+' if self.timeZone >= 0 else '-'}{abs(self.timeZone)}:00\n"
            schedule += f"Start: {(timeStart + timeCorrection).strftime('%Y.%m.%d %H:%M:%S')}\n"
            schedule += f"Stop:  {(start + timedelta(hours=length)).strftime('%Y.%m.%d %H:%M:%S')}\n"

            schedule += f"Minimum Elevation: {self.config.horizon}°\n"
            schedule += f"Minimum Apogee: {self.config.minApogee}°\n"

            schedule += f"Number of passes: {len(td)//4}\n\n"
            schedule += table.get_string()

            name = self.schedulePath / f'Schedule_{datetime.now().strftime("%Y-%m-%dT%H-%M")}.txt'

            with open(name, 'w') as file:
                file.write(schedule)

        return self.schedule


    def generateTrackFile(self, satPass: SatPass, timestep: int = 1) -> TrackFile:
        """
        The method for generating a track file for Rosental systems
        

        @param satPass: list[SatPass] 
        @param timestep: float

        @return TrackFile
        """
        
        ## timestep should only be an integer due to the format of the time record in the file: %H:%M:%S. The real part is simply lost.
        if timestep < 1:
            timestep = 1
            
        if isinstance(timestep, float):
            timestep = int(timestep)
        
        t = (satPass.timeEnd - satPass.timeStart)
        time = satPass.timeStart
        
        satTrack = []
        
        for i in range(0, int(t.total_seconds()/timestep)+1): 
            time += timedelta(seconds=timestep) 
            azimuth, elevation  = satPass.orb.get_observer_look(time, lat = self.lat, lon = self.lon, alt = self.alt)
            
            sphCoords = self.degreesToDegreesAndMinutes(azimuth, elevation, time)
            
            satTrack.append(sphCoords)

        
        trackPath = self.tracksPath / f"{satPass.satName.replace(' ', '-')}_{self.stationType}_{satPass.timeStart.strftime('%Y-%m-%dT%H-%M')}.txt"
        
        try:
            with open(trackPath, "w") as file:
                startTime = satPass.timeStart.strftime('%Y-%m-%d   %H:%M:%S') + " UTC"

                metaData = f"Satellite: {satPass.satName}\n" +                                        \
                            f"Start date & time: {startTime}\n" +                                      \
                            f"Orbit: {satPass.orb.get_orbit_number(satPass.timeStart)}\n\n"
                metaData += "Time (UTC)   Azimuth (deg:min)   Elevation (deg:min)\n\n"

                ## Write metadata
                file.write(metaData)

                for i in satTrack:
                    file.write(f"{i.time.strftime('%H:%M:%S')}   {i.azimuth}   {i.elevation}\n")
                    
        except:
            if self.logger != None:
                self.logger.error(f"Failed generate legacy track for {satPass.satName}")

        if self.logger != None:
            self.logger.info(f"Generate legacy track for {satPass.satName}")
        
        return TrackFile(satName=satPass.satName, timeStart=satPass.timeStart, trackPath=trackPath)
    
    
    def getSateliteTrack(self, satPass: SatPass, timestep: float = 0.5, save: bool = True) -> List[SphereCoordinates]:
        """ The method for getting satellite trajectory
        
        @param satPass: SatPass
        @param timestep: float
        @param save: bool
        
        @return satTrack: list[SphereCoordinates]
        
        """
        
        t = (satPass.timeEnd - satPass.timeStart)
        
        satTrack = []
        time = satPass.timeStart
        
        for i in range(0, int(t.total_seconds()/timestep)+1): 
            time += timedelta(seconds=timestep) 
            azimuth, elevation  = satPass.orb.get_observer_look(time, lat = self.lat, lon = self.lon, alt = self.alt)
            azimuth = round(azimuth, 2)
            elevation = round(elevation, 2)
            
            satTrack.append(SphereCoordinates(azimuth = round(azimuth, 2),
                                        elevation = round(elevation, 2),
                                        time=time))
        
        if self.logger != None:
            self.logger.info(f"Generate track for {satPass.satName}")
        
        ## Save track file if needed
        if save:
            trackPath = self.tracksPath / f"{satPass.satName.replace(' ', '-')}_{self.stationType}_{satPass.timeStart.strftime('%Y-%m-%dT%H-%M')}.txt"

            try:
                with open(trackPath, "w") as file:
                    startTime = satPass.timeStart.strftime('%Y-%m-%d   %H:%M:%S') + " UTC"

                    metaData = f"{self.stationType.upper()} track file / LorettOrbital {__version__}\n" + \
                            f"StationName: {self.stationName}\n" +                                     \
                            f"Station Position: {self.lon}° {self.lat}° {self.alt}km\n" +              \
                            f"Satellite: {satPass.satName}\n" +                                        \
                            f"Start date & time: {startTime}\n" +                                      \
                            f"Orbit: {satPass.orb.get_orbit_number(satPass.timeStart)}\n\n"

                    metaData += "Time (UTC)   Azimuth (deg)   Elevation (deg)\n\n"

                    ## Write metadata
                    file.write(metaData)

                    for i in satTrack:
                        file.write(f"{i.time}   {i.azimuth:.2f}   {i.elevation:.2f}\n")  
            except:
                if self.logger != None:
                    self.logger.error(f"Failed generate legacy track for {satPass.satName}") 
            
        return satTrack


    def setCoordinates(self, lat: float, lon: float, alt: float) -> bool:
        """ The method for setting the station location

        @param lat: float
        @param lon: float
        @param alt: float
            
        @return status: bool
        """
            
        if self._checkCoordinates(lat, lon, alt):
            self.lat = round(lat, 5)
            self.lon = round(lon, 5)
            self.alt = round(alt, 5)
            
            if self.logger != None:
                self.logger.info(f"Set coordinates {self.lat} {self.lon} {self.alt}")

            return True

        return False


    def setTimeZone(self, timeZone: int) -> bool:
        """ The Method for change timezone
            
            @param timeZone: int
            @return status: bool
        """
        if abs(timeZone) > 12:
            if self.logger != None:
                self.logger.warning(f"Fail set timezone UTC {self.timeZone:+}")
            
            return False

        self.timeZone = timeZone
        
        if self.logger != None:
            self.logger.info(f"Set timezone UTC {self.timeZone:+}")
        
        return True

    
    def getStation(self) -> dict:
        """ The Method returned station info
            
            @return info: dict
        """
        return {"stationName": self.stationName,

                "lon": self.lon,
                "lat": self.lat,
                "alt": self.alt,

                'satList': [i[0] for i in self.satList],
                'horizon': self.config.horizon,
                'minApogee': self.config.minApogee
                }


    def getCoordinates(self) -> dict:
        """ The method returned station coordinates
            
            @return coordinates: dict
        """
        return {"lon": self.lon,
                "lat": self.lat,
                "alt": self.alt}
        
    def getTLEPath(self) -> str:
        """The method returned TLE Path
        
            @return tlePath: Path
        """
        return self.tlePath / "tle.txt" 




