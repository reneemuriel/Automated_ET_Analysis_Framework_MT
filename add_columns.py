"""add column fixation_object and column fixation_time """

# only 1 OOI per fixation possible -> choose closer one


# if last column is action
def add_fixation_object_action(data, pixel_distance):
    fixation_object = []
    for row in range(0,len(data)):
        hits_per_col_values = []
        hits_per_col_ooi = []
        for col in range (2,len(data.columns)-1):                     # from column 2 until column n-1 (beacuse last col = Action)
            if data.iloc[row][col] <= pixel_distance:   
                hits_per_col_values.append(data.iloc[row][col])
                hits_per_col_ooi.append(data.columns[col])
        if len(hits_per_col_values)>0:
            index_min = hits_per_col_values.index(min(hits_per_col_values))
            fixation_object.append(hits_per_col_ooi[index_min])
        else:
            fixation_object.append('BG')
    data['fixation_object'] = fixation_object


# if last column is not action
def add_fixation_object(data, pixel_distance):
    fixation_object = []
    for row in range(0,len(data)):
        hits_per_col_values = []
        hits_per_col_ooi = []
        for col in range (2,len(data.columns)):                     
            if data.iloc[row][col] <= pixel_distance:   
                hits_per_col_values.append(data.iloc[row][col])
                hits_per_col_ooi.append(data.columns[col])
        if len(hits_per_col_values)>0:
            index_min = hits_per_col_values.index(min(hits_per_col_values))
            fixation_object.append(hits_per_col_ooi[index_min])
        else:
            fixation_object.append('BG')
    data['fixation_object'] = fixation_object




# def add_fixation_time
def add_fixation_time(data):
    fixation_time = []
    for row in range (0,len(data)):
        fixation_time.append(data['end_time'][row]-data['start_time'][row])
    data['fixation_time'] = fixation_time
