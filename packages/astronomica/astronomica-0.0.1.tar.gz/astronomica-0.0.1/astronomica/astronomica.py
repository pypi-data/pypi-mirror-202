# import required libraries (math and datetime are always required, because of their uses)
import math
import datetime

class LST:
    def __init__(self, data):
        self.__dict__ = data

def local_julian_date(date=datetime.datetime.now()):
    time = date.timestamp() * 1000  # Convert to milliseconds
    tzoffset = date.utcoffset().total_seconds() // 60 if date.utcoffset() is not None else 0  # Convert to minutes
    return (time / 86400000) - (tzoffset / 1440) + 2440587.5  # return the Julian Date


J1970 = 2440588
dayMs = 24 * 60 * 60 * 1000

def fromJulian(j):
    return datetime.datetime.fromtimestamp((j + 0.5 - J1970) * dayMs / 1000)

LUNAR_MONTH = 29.530588853

def get_lunar_age():
    percent = get_lunar_age_percent()
    age = percent * LUNAR_MONTH
    return age


def get_lunar_age_percent():
    julian_date = local_julian_date()
    return normalize((julian_date - 2451550.1) / LUNAR_MONTH)


def normalize(value):
    value = value - int(value)
    if value < 0:
        value = value + 1
    return value


def getLunarPhase(date=datetime.datetime.now()):
    age = get_lunar_age()
    if age < 1.84566:
        return "New"
    elif age < 5.53699:
        return "Waxing Crescent"
    elif age < 9.22831:
        return "First Quarter"
    elif age < 12.91963:
        return "Waxing Gibbous"
    elif age < 16.61096:
        return "Full"
    elif age < 20.30228:
        return "Waning Gibbous"
    elif age < 23.99361:
        return "Last Quarter"
    elif age < 27.68493:
        return "Waning Crescent"
    return "New"

def solarMeanAnomaly(d):
    rad = math.pi / 180.0
    return rad * (357.5291 + 0.98560028 * d)


def daysSinceJ2000():
    # get current date and time in UTC
    now = datetime.datetime.utcnow()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    # calculate Julian Date
    a = math.floor((14 - month) / 12)
    Y = year + 4800 - a
    M = month + 12 * a - 3
    D = day
    UT = hour + minute / 60 + second / 3600
    JD = 367 * Y - math.floor(7 * (Y + math.floor((M + 9) / 12)) / 4) + math.floor(
        275 * M / 9) + D + 1721013.5 + UT / 24

    # calculate number of days since J2000.0
    days = (JD - 2451545.0) + (UT - 12) / 24
    return days

def declination(l, b):
    e = math.radians(23.4397)  # obliquity of the ecliptic in degrees
    return math.asin(
        math.sin(math.radians(b)) * math.cos(e) + math.cos(math.radians(b)) * math.sin(e) * math.sin(math.radians(l)))


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def decimalhours(now):
    return (((now.second / 60) + now.minute) / 60) + now.hour


def gst(jd, dechours):
    S = jd - 2451545
    T = S / 36525
    T0 = 6.697374558 + (2400.051336 * T) + (0.000025862 * T ** 2)
    if T0 < 0:
        T0 = (T0 + abs(T0) // 24 * 24) % 24
    else:
        T0 = T0 % 24
    T0 = T0 + (dechours * 1.002737909)
    if T0 < 0:
        T0 = T0 + 24
    if T0 > 24:
        T0 = T0 - 24
    return T0


def localSiderealTime(long):
    now = datetime.datetime.utcnow()
    jd = local_julian_date()
    dechours = decimalhours(now)
    gstime = gst(jd, dechours)
    LONGITUDE = long
    utcdiff = math.fabs(LONGITUDE) / 15
    if sign(LONGITUDE) == -1:
        lstime = gstime - utcdiff
    else:
        lstime = gstime + utcdiff
    if lstime > 24:
        lstime = lstime - 24
    if lstime < 0:
        lstime = lstime + 24

    raw = lstime
    h = math.floor(lstime)
    m = math.floor((lstime - h) * 60)
    s = math.floor((((lstime - h) * 60) - m) * 60)

    times = {
        "raw": raw,
        "hour": h,
        "minute": m,
        "second": s
    }
    return LST(times)


def eclipticLongitude(M):
    rad = math.pi / 180.0
    PI = math.pi

    C = rad * (1.9148 * math.sin(M) + 0.02 * math.sin(2 * M) + 0.0003 * math.sin(3 * M))  # equation of center
    P = rad * 102.9372  # perihelion of the Earth

    return M + C + P + PI

def solarHourAngle(longitude, lst):
    """Calculate the solar hour angle for a given longitude and local sidereal time."""
    # Convert longitude and LST to radians
    longitude = math.radians(longitude)
    lst = math.radians(lst)
    # Calculate the solar noon for the given longitude
    solarNoon = longitude + (12 - 12 * 4.0 / 1440) * math.radians(360) / 24
    # Calculate the solar hour angle
    hourAngle = lst - solarNoon
    return hourAngle


def altitude(lat, long):
    long = -long
    d = daysSinceJ2000()
    M = solarMeanAnomaly(d)
    L = eclipticLongitude(M)
    dec = declination(L, 0)
    H = solarHourAngle(long, localSiderealTime(long).raw)
    a = math.asin(math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(H))
    return math.degrees(a)


def azimuth(lat, long):
    long = -long
    d = daysSinceJ2000()
    M = solarMeanAnomaly(d)
    L = eclipticLongitude(M)
    H = solarHourAngle(long, localSiderealTime(long).raw)
    dec = declination(L, 0)
    return math.degrees(math.atan2(math.sin(H), math.cos(H) * math.sin(lat) - math.tan(dec) * math.cos(lat)))


class Observer:
    def __init__(self, latitude, longitude, planet, date=datetime.datetime.now()):
        self.lat = latitude
        self.long = -longitude  # convert to longitude west from just longitude
        self.dateToCalculate = date
        self.planet = planet
        self.meanA = None
        self.ceq = None
        self.v = None
        self.perihelion = None
        self.obliquity = None
        self.dist = None
        self.eclipticlong = None

    def julian_date(self):
        JD = local_julian_date(self.dateToCalculate)
        return JD

    def mean_anomaly(self):
        # formula from https://www.aa.quae.nl/en/reken/zonpositie.html
        # formula is M = (M0 + M1 * (J - J2000)) mod 360˚
        J2000 = 2451545
        m_list = [
            (174.7948, 4.09233445),
            (50.4161, 1.60213034),
            (357.5291, 0.98560028),
            (19.3730, 0.52402068),
            (20.0202, 0.08308529),
            (317.0207, 0.03344414),
            (141.0498, 0.01172834),
            (256.2250, 0.00598103),
            (14.882, 0.00396),
        ]
        planetMap = {
            'mercury': 0,
            'venus': 1,
            'earth': 2,
            'mars': 3,
            'jupiter': 4,
            'saturn': 5,
            'uranus': 6,
            'neptune': 7,
            'pluto': 8,
        }
        plan_number = planetMap.get(self.planet, 2) # if the planet is not found, calculate for earth
        m_row = m_list[plan_number]
        M = (m_row[0] + m_row[1] * (local_julian_date() - J2000)) % 360
        self.meanA = M
        return M

    def equation_of_center(self):
        planet = self.planet
        c_dict = {
            "mercury": [23.4400, 2.9818, 0.5255, 0.1058, 0.0241, 0.0055],  # 0.0026 is the maximum error
            "venus": [0.7758, 0.0033, 0, 0, 0, 0],  # 0.0000 is the maximum error
            "earth": [1.9148, 0.0200, 0.0003, 0, 0, 0],  # 0.0000 is the maximum error
            "mars": [10.6912, 0.6228, 0.0503, 0.0046, 0.0005, 0],  # 0.0001 is the maximum error
            "jupiter": [5.5549, 0.1683, 0.0071, 0.0003, 0, 0],  # 0.0001 is the maximum error
            "saturn": [6.3585, 0.2204, 0.0106, 0.0006, 0, 0],  # 0.0001 is the maximum error
            "uranus": [5.3042, 0.1534, 0.0062, 0.0003, 0, 0],  # 0.0001 is the maximum error
            "neptune": [1.0302, 0.0058, 0, 0, 0, 0],  # 0.0001 is the maximum error
            "pluto": [28.3150, 4.3408, 0.9214, 0.2235, 0.0627, 0.0174]  # 0.0096 is the maximum error
        }
        # the formula used is from https://www.aa.quae.nl/en/reken/zonpositie.html#10
        # c = c1 * sin(m) + c2 * sin(2m) + c3 * sin(3m) + c4 * sin(4m) + c5 * sin(5m) + c6 * sin(6m)
        c = c_dict.get(planet, [1.9148, 0.0200, 0.0003, 0, 0, 0])
        m = self.mean_anomaly()
        center_eq = c[0] * math.sin(m) + c[1] * math.sin(2 * m) + c[2] * math.sin(3 * m) + c[3] * math.sin(4 * m) + \
                    c[4] * math.sin(5 * m) + c[5] * math.sin(6 * m)
        self.ceq = center_eq
        return center_eq

    def true_anomaly(self):
        c = self.equation_of_center()
        m = self.mean_anomaly()
        self.v = c + m
        return m + c

    def set_perihelion_and_obliquity(self):
        perihelion_longitude_and_obliquity= [
            (230.3265,0.0351),
             (73.7576,2.6376),
              (102.9373,23.4393),
               (71.0041,25.1918),
                (237.1015,3.1189),
                 (99.4587,26.7285),
                  (5.4634,82.2298),
                   (182.2100,27.8477),
                    (184.5484,119.6075),
        ]
        planetMap = {
            'mercury': 0,
            'venus': 1,
            'earth': 2,
            'mars': 3,
            'jupiter': 4,
            'saturn': 5,
            'uranus': 6,
            'neptune': 7,
            'pluto': 8,
        }
        key = planetMap.get(self.planet, 2)
        datatuple = perihelion_longitude_and_obliquity[key]
        self.perihelion = datatuple[0]
        self.obliquity = math.radians(datatuple[1])

    def ecliptical_longitude(self):
        self.set_perihelion_and_obliquity() # setup information
        peri = self.perihelion
        L = self.mean_anomaly() + peri
        Lsun = L + 180
        long = (Lsun + self.equation_of_center()) % 360
        self.eclipticlong = math.radians(long)
        return math.radians(long)

    def equatorial_coordinates(self):
        long = self.ecliptical_longitude()
        asun = math.atan2(math.sin(long) * math.cos(self.obliquity), math.cos(long))
        decsun = math.asin(math.sin(long) * math.sin(self.obliquity))
        return {
            'ra': math.degrees(asun),
            'dec': math.degrees(decsun)
        }

    def local_solar_transit(self):
        Jtable = [
            [45.3497, 11.4556, 0,175.9386],
            [52.1268, -0.2516, 0.0099, -116.7505],
            [0.0009, 0.0053, -0.0068, 1.0000000],
            [0.9047, 0.0305, -0.0082, 1.027491],
            [0.3345, 0.0064, 0,0.4135778],
            [0.0766, 0.0078, -0.0040, 0.4440276],
            [0.1260, -0.0106, 0.0850, -0.7183165],
            [0.3841, 0.0019, -0.0066, 0.6712575],
            [4.5635,-0.5024, 0.3429, 6.387672]
        ]
        planetMap = {
            'mercury': 0,
            'venus': 1,
            'earth': 2,
            'mars': 3,
            'jupiter': 4,
            'saturn': 5,
            'uranus': 6,
            'neptune': 7,
            'pluto': 8,
        }
        plannumber = planetMap.get(self.planet, 2)
        Jrow = Jtable[plannumber]
        j0 = Jrow[0]
        j1 = Jrow[1]
        j2 = Jrow[2]
        j3 = Jrow[3]
        nx = (local_julian_date() - 2451545 -j0)/j3 - self.long /360
        n = math.floor(nx)
        jx = local_julian_date() + j3 * (n-nx)
        self.set_perihelion_and_obliquity()  # setup information
        peri = self.perihelion
        L = self.mean_anomaly() + peri
        lsun = L + 180
        jtransit = jx + j1 * math.sin(math.radians(self.mean_anomaly())) + j2 * math.sin(2 * math.radians(lsun))
        return jtransit + 1

    def distance_to_sun(self):
        square_table = [
            0.37073,
            0.72330,
            0.99972,
            1.51039,
            5.19037,
            9.52547,
            19.17725,
            30.10796,
            37.09129
        ]
        e_table = [
            0.20563,
            0.00677,
            0.01671,
            0.09340,
            0.04849,
            0.05551,
            0.04630,
            0.00899,
            0.2490,
        ]
        planetMap = {
            'mercury': 0,
            'venus': 1,
            'earth': 2,
            'mars': 3,
            'jupiter': 4,
            'saturn': 5,
            'uranus': 6,
            'neptune': 7,
            'pluto': 8,
        }
        key = planetMap.get(self.planet, 2)
        e = e_table[key]
        square = square_table[key]
        r = square/1 + e * math.cos(self.true_anomaly())
        self.dist = r
        return r

    def planet_heliocentric_coordinates(self):
        square_table = [
            0.37073,
            0.72330,
            0.99972,
            1.51039,
            5.19037,
            9.52547,
            19.17725,
            30.10796,
            37.09129
        ]
        e_table = [
            0.20563,
            0.00677,
            0.01671,
            0.09340,
            0.04849,
            0.05551,
            0.04630,
            0.00899,
            0.2490,
        ]
        planetMap = {
            'mercury': 0,
            'venus': 1,
            'earth': 2,
            'mars': 3,
            'jupiter': 4,
            'saturn': 5,
            'uranus': 6,
            'neptune': 7,
            'pluto': 8,
        }
        r = self.distance_to_sun()
        horse_table = [
            48.331,
            76.680,
            174.873,
            49.558,
            100.464,
            113.666,
            74.006,
            131.784,
            110.307
        ]
        i_table = [
            7.005,
            3.395,
            0.000,
            1.850,
            1.303,
            2.489,
            0.773,
            1.770,
            17.140,
        ]
        w_table = [
            29.125,
            54.884,
            288.064,
            286.502,
            273.867,
            339.391,
            98.999,
            276.340,
            113.768
        ]
        key = planetMap.get(self.planet, 2)
        i = i_table[key]
        horse = horse_table[key]
        w = w_table[key]
        v = self.true_anomaly()
        r = self.distance_to_sun()
        xplanet = r * (math.cos(horse) * math.cos(w + v) - math.sin(horse) * math.cos(i) * math.sin(w + v))
        yplanet = r * (math.sin(horse)*math.cos(w + v) + math.cos(horse ) *math.cos(i) * math.sin(w + v))
        zplanet = r * math.sin(i) * math.sin(w + v)
        return xplanet, yplanet, zplanet



star_catalog = {
    'Sun': 'G2V',
    'Sirius': 'A1V',
    'Betelgeuse': 'M2Iab',
    'Rigel': 'B8Ia',
    'Vega': 'A0Va',
    'Alpha Centauri A': 'G2V',
    'Alpha Centauri B': 'K1V',
    'Proxima Centauri': 'M5Ve',
    'Polaris': 'F7Ib',
    'Capella': 'G5III',
    'Arcturus': 'K1.5III',
    'Aldebaran': 'K5III',
    'Deneb': 'A2Ia',
    'Antares': 'M1.5Iab-IbB',
    'Altair': 'A7V',
    'Fomalhaut': 'A3V',
    'Spica': 'B1III-IV',
    'Bellatrix': 'B2III',
    'Regulus': 'B7V',
    'Mizar': 'A2V',
    'Castor': 'A1V',
    'Pollux': 'K0III',
    'Achernar': 'B3Vp',
    'Acrux': 'B0.5IV',
    'Alnair': 'B7IV-V',
    'Atria': 'K2Ib-IIa',
    'Canopus': 'F0Ib',
    'Gamma Velorum': 'WC8+O9I',
    'Hadar': 'B1IV',
    'Miaplacidus': 'A0III',
    'Naos': 'O5If',
    'Rigil Kentaurus': 'G2V+K1V',
    'Sadr': 'F8Ib',
    'Shaula': 'B0.5IV-V',
    'Suhail': 'K4Ib-II',
    'Vega': 'A0Va',
    'Achernar': 'B3Vpe',
    'Adhara': 'B2II',
    'Albireo A': 'K3II-III',
    'Albireo B': 'B8V',
    'Alcor': 'A5V',
    'Alioth': 'A0p',
    'Alkaid': 'B3V',
    'Alnath': 'B7III',
    'Alnilam': 'B0Ia',
    'Alnitak': 'O9.5Ib',
    'Alpha Aurigae': 'A7IV',
    'Alpha Boötis': 'K2III',
    'Alpha Camelopardalis': 'A3V',
    'Alpha Carinae': 'F0Ia',
    'Alpha Cephei': 'A7IV',
    'Alpha Columbae': 'B5III',
    'Alpha Crucis': 'B0.5IV',
    'Alpha Eridani': 'K0III',
    'Alpha Geminorum': 'A1V',
    'Alpha Herculis': 'K3II',
    'Alpha Leporis': 'B5V',
    'Alpha Lupi': 'B1.5III',
    'Alpha Ophiuchi': 'A5III',
    'Alpha Pavonis': 'B2IV',
    'Alpha Pegasi': 'B9III',
    'Alpha Persei': 'F5Ib',
}
def map_star(star):
    type = star_catalog.get(star, "Star not currently supported")
    return type

    
