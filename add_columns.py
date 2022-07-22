# add column fixation_object
def add_fixation_object(data, pixel_distance, ):
    fixation_object = [] 
    for row in range(0,len(data)):
        fixation_object.append([])                                  # make sublist for every row so that multiple OOI can be added
        for col in range (2,len(data.columns)):
            if data.iloc[row][col] <= pixel_distance:               # if the given distance is smaller than or equal to the pre-defined pixel distance
                fixation_object[row].append(data.columns[col])      # fill the respective column name into the list
        if fixation_object[row] == []:                              # if there is no fixation on an OOI,'Non-OOI' is filled into the list
            fixation_object[row] = ['Non-IOO']
    data['fixation_object'] = fixation_object

# def add_fixation_time
def calculate_fixation_time(data):
    fixation_time = [0]*len(data)
    for row in range (0,len(data)):
        fixation_time[row] = data['end_time'][row]-data['start_time'][row]
    data['fixation_time'] = fixation_time


# calculate average fixation time per OOI of entire trial


# calculate average fixation time per OOI per step


# count duration per step (or maybe from other file?)
