# Goal: Parse Digitizer voltage readings into an accessible object

import math

class DigitizerData():
    """ A class used to store data in a simple accessible object from a digitizer fetch response
 
    Generally, this class will be used within an array of DigitizerData objects.

    Attributes
    ----------
    sample_number : int
        Sample number of the voltage reading
    voltage_reading : float
        Digitizer voltage reading
    time_since_start_seconds : float
        Time since the start of the sampling in seconds

    """

    sample_number = 0
    
    voltage_reading = math.nan

    time_since_start_seconds = 0

    def __init__(self):
        pass