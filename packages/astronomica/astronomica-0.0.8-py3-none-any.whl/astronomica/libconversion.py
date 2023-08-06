from astropy.time import Time
from skyfield.api import Angle, Distance

def fahrenheit_to_celsius(f):
    c = (f - 32) * 5/9
    return c

def celsius_to_fahrenheit(c):
    f = c * 9/5 + 32
    return f

def miles_to_kilometers(m):
    km = m * 1.60934
    return km

def kilometers_to_miles(km):
    m = km / 1.60934
    return m

def pounds_to_kilograms(lb):
    kg = lb * 0.453592
    return kg

def kilograms_to_pounds(kg):
    lb = kg / 0.453592
    return lb

def inches_to_centimeters(inch):
    cm = inch * 2.54
    return cm

def centimeters_to_inches(cm):
    inch = cm / 2.54
    return inch

def au_to_km(au):
    km = au * 149597870.7
    return km

def km_to_au(km):
    au = km / 149597870.7
    return au

def light_years_to_km(ly):
    km = ly * 9.461e+12
    return km

def km_to_light_years(km):
    ly = km / 9.461e+12
    return ly

def parsecs_to_light_years(pc):
    ly = pc * 3.26156
    return ly

def light_years_to_parsecs(ly):
    pc = ly / 3.26156
    return pc


def astropy_length_to_skyfield_length(length):
    skyfield_length = Distance(Angle(length.value), length.unit.name)
    return skyfield_length

def astropy_time_to_skyfield_time(time):
    skyfield_time = Time(time.jd, format='jd', scale='utc')
    return skyfield_time

def skyfield_time_to_astropy_time(time):
    astropy_time = Time(time.utc_datetime())
    return astropy_time
