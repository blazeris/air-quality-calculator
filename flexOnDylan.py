
# List of all breakpoints for respective levels of quality
quality_levels = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
pollutant_names = ['PM-2.5', 'PM-10', 'NO-2', 'SO-2', 'CO', 'O-3']
AQI_breakpoints = [50, 100, 150, 200, 300, 500]

PM25_breakpoints = [12, 35.4, 55.4, 150.4, 250.4, 500.4] # Truncate to 1 decimal place
PM10_breakpoints = [54, 154, 254, 354, 424, 604]
NO2_breakpoints = [53, 100, 360, 649, 1249, 2049]
SO2_breakpoints = [35, 75, 185, 304, 604, 1004]
CO_breakpoints = [4.4, 9.4, 12.4, 15.4, 30.4, 50.4] # Truncate to 1 decimal place
O3_breakpoints = [0, 0, 164, 204, 404, 604]

PM25, PM10, NO2, SO2, CO, O3, AQI, NAME = 0, 1, 2, 3, 4, 5, 6, 7

# Pollutant type will be integers that are equal to the indexes of this list
pollutant_breakpoints = [PM25_breakpoints, PM10_breakpoints, NO2_breakpoints, SO2_breakpoints, CO_breakpoints, O3_breakpoints, AQI_breakpoints]

# Desired decimal places for each pollutant
pollutant_decimal_places = [1, 0, 0, 0, 1, 0]

#List of lists containing data for each location in the following format
# [Location name, PM25, PM10, NO2, SO2, CO, O3, Highest AQI]
locations = []

# Truncates a given float to a given number of decimals
def truncate_decimals(float_number, num_of_decimals):
    e = 10 ** num_of_decimals
    number = float(int(float_number * e) / e)
    if num_of_decimals == 0:
        return int(number)
    return float(number)

# Prompts user to input all the data for every single location
def input_locations():
    global locations, AQI, NAME
    num_of_locations = None

    while num_of_locations is None or num_of_locations <= 0:
        num_of_locations = int(input('How many locations? '))

    for i in range(1, num_of_locations + 1):
        location_data = [None] * 8
        Ip_values = []

        location_data[NAME] = str(input('What is the name of location ' + str(i) + '? '))

        has_valid_value = False
        while(has_valid_value == False):
            for j in range(PM25, O3 + 1):
                pollutant_value = float(input(' -> Enter ' + pollutant_names[j] + ' concentration: '))

                if pollutant_value is not None and pollutant_value >= 0 and (j != O3 or pollutant_value > 125):
                    pollutant_value = truncate_decimals(pollutant_value, pollutant_decimal_places[j])
                    location_data[j] = pollutant_value

                    Ip = calculate_pollutant_index(pollutant_value, j)
                    Ip_values.append(Ip)
                    if pollutant_value is not None and pollutant_value >= 0:
                        has_valid_value = True
                        print('\t' + pollutant_names[j] + ' concentration of ' + str(pollutant_value) + ' is index level ' + str(Ip))
                else:
                    Ip_values.append(None)
                    location_data[j] = None

        location_data[AQI] = Ip_values[find_max(Ip_values)]
        locations.append(location_data)
        print('\nAQI for ' + str(location_data[NAME]) + ' is ' + str(location_data[AQI]))
        print('Air Quality: ' + quality_levels[find_quality_level(location_data[AQI], AQI)] + '\n')

# Finds the index with the highest value in a list
def find_max(values):
    if len(values) > 0:
        max = None
        for i in range(0, len(values)):
            if values[i] is not None:
                max = i
        if max is not None:
            for i in range(0, len(values)):
                if values[i] is not None and values[i] > values[max]:
                    max = i
        return max
    return -1

# Finds the quality level of a given value of a given type
# Quality level of 0 represents "Good" while 5 would represent "Hazardous"
def find_quality_level(value, type):
    global pollutant_breakpoints, O3
    quality_level = 0
    for i in range(0, len(pollutant_breakpoints[type]) - 1):
        # If it's higher than an upper breakpoint, the quality level will be higher
        if value is not None and value > pollutant_breakpoints[type][i] and (type != O3 or value >= 125):
            quality_level += 1
    return quality_level

# Finds the lower breakpoint of a given quality level and type
def find_lower_breakpoint(quality_level, type):
    global PM25, CO
    if quality_level == 0:
        return 0
    increment = 1
    if type == PM25 or type == CO:
        increment = 0.1
    return pollutant_breakpoints[type][quality_level - 1] + increment

# Calculates the AQI of a given pollutant value and given type
def calculate_pollutant_index(pollutant_value, type):
    quality_level = find_quality_level(pollutant_value, type)

    Chigh = pollutant_breakpoints[type][quality_level]
    Clow = find_lower_breakpoint(quality_level, type)

    Ihigh = pollutant_breakpoints[AQI][quality_level]
    Ilow = find_lower_breakpoint(quality_level, AQI)

    return round((Ihigh - Ilow) / (Chigh - Clow) * (pollutant_value - Clow) + Ilow)

# Finds the mean value of a list
def mean(values):
    sum = 0
    num_of_inputs = 0

    for value in values:
        if value is not None and value >= 0:
            sum += value
            num_of_inputs += 1
    if num_of_inputs == 0:
        return None
    return sum / num_of_inputs

# Prints out the AQI summary
def print_summary():
    global locations

    location_AQI_values = []
    for location in locations:
        location_AQI_values.append(location[AQI])
    max_AQI_index = find_max(location_AQI_values)
    print('Summary\n\tLocation with highest AQI is ' + locations[max_AQI_index][NAME] + ' (' + str(location_AQI_values[max_AQI_index]) + ')')
    PM25_values = []
    for location in locations:
        PM25_values.append(location[PM25])
    print('\tAverage PM-2.5 concentration : ' + str(mean(PM25_values)))

### MAIN ####
input_locations()
print_summary()