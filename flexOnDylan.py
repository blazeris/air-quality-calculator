
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

# Pollutant type will be integers that are equal to the indexes of this list
pollutant_breakpoints = [AQI_breakpoints, PM25_breakpoints, PM10_breakpoints, NO2_breakpoints, SO2_breakpoints, CO_breakpoints, O3_breakpoints]

# Desired decimal places for each pollutant
pollutant_decimal_places = [1, 0, 0, 0, 1, 0]

#List of lists containing data for each location in the following format
# [Location name, PM25, PM10, NO2, SO2, CO, O3, Highest AQI]
locations = []

# Truncates a given float to a given number of decimals
def truncate_decimals(float_number, num_of_decimals):
    e = 10 ** num_of_decimals
    sig_figs = int((float_number * e) // 1)
    return float(sig_figs / e)

# Prompts user to input all the data for every single location
def input_locations():
    global locations
    location_data = []
    AQI_values = []
    num_of_locations = None
    while num_of_locations is None or num_of_locations <= 0:
        num_of_locations = int(input('How many locations? '))
    for i in range(1, num_of_locations + 1):
        location_data.append(str(input('What is the name of location ' + str(i) + '? ')))

        for i in range(0, len(pollutant_names)):
            pollutant_value = float(input(' -> Enter ' + pollutant_names[i] + ' concentration: '))
            pollutant_value = truncate_decimals(pollutant_value, pollutant_decimal_places[i])
            location_data.append(pollutant_value)

            AQI = calculate_pollutant_index(pollutant_value, i + 1)
            AQI_values.append(AQI)
            if(pollutant_value >= 0):
                print('\t' + pollutant_names[i] + ' concentration of ' + str(pollutant_value) + ' is index level ' + str(AQI))

        location_data.append(find_max(AQI_values))
        locations.append(location_data)
        print('\nAQI for ' + location_data[0] + ' is ' + str(location_data[6]))
        print('Air Quality: ' + quality_levels[find_quality_level(location_data[5], 0)])

# Finds the highest value in a list
def find_max(values):
    if len(values) > 0:
        max = 0
        for i in range(0,len(values)):
            if values[i] > max:
                max = i
        return max
    return -1
# Finds the quality level of a given value of a given type
# Quality level of 0 represents "Good" while 5 would represent "Hazardous"
def find_quality_level(value, type):
    global pollutant_breakpoints
    quality_level = 0
    for i in range(0, len(pollutant_breakpoints[type])):
        # If it's higher than an upper breakpoint, the quality level will be higher
        if value > pollutant_breakpoints[type][i] and (type != 5 or value >= 125):
            quality_level += 1
    return quality_level

def find_lower_breakpoint(quality_level, type):
    if quality_level == 0:
        return 0
    increment = 1
    if type == 1 or type == 5:
        increment = 0.1
    return pollutant_breakpoints[type][quality_level - 1] + increment

# Calculates the AQI of a given pollutant value and given type
def calculate_pollutant_index(pollutant_value, type):
    quality_level = find_quality_level(pollutant_value, type)

    Chigh = pollutant_breakpoints[type][quality_level]
    Clow = find_lower_breakpoint(quality_level, type)

    Ihigh = pollutant_breakpoints[0][quality_level]
    Ilow = find_lower_breakpoint(quality_level, 0)

    return round((Ihigh - Ilow) / (Chigh - Clow) * (pollutant_value - Clow) + Ilow)

# Finds the mean value of a list
def mean(values):
    sum = 0
    for value in values:
        sum += value
    return sum / len(values)

def print_summary():
    global locations

    location_AQI_values = []
    for location in locations:
        location_AQI_values.append(location[6])
    max_AQI_index = find_max(location_AQI_values)

    print('\nSummary:\n\tLocation with highest AQI is ' + locations[max_AQI_index][0] + ' (' + str(
        location_AQI_values[max_AQI_index]) + ')')
    PM25_values = []
    for location in locations:
        PM25_values.append(location[1])
    print('\tAverage PM-2.5 concentration : ' + str(mean(PM25_values)))

### MAIN ####
input_locations()
print_summary()
