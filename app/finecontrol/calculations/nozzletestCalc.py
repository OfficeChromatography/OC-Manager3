from finecontrol.calculations.sampleAppCalc import *

def calculate2(data):
    #data = SimpleNamespace(**data)

    if data["pressure_axis"] ==  "x":
        xlist = np.arange(data["pressure_start"], data["pressure_end"]+data["pressure_steps"]/2, data["pressure_steps"])
        xlabel = "pressure"
    elif data["pressure_axis"] ==  "y": 
        ylist = np.arange(data["pressure_start"], data["pressure_end"]+data["pressure_steps"]/2, data["pressure_steps"])
        ylabel = "pressure"
    else:
        data["pressure"] = data["pressure_start"]

    if data["frequency_axis"] ==  "x":
        xlist = np.arange(data["frequency_start"], data["frequency_end"]+data["frequency_steps"]/2, data["frequency_steps"])
        xlabel = "frequency"
    elif data["frequency_axis"] ==  "y": 
        ylist = np.arange(data["frequency_start"], data["frequency_end"]+data["frequency_steps"]/2, data["frequency_steps"])
        ylabel = "frequency"
    else:
        data["frequency"] = data["frequency_start"]

    if data["deltax_axis"] ==  "x":
        xlist = np.arange(data["deltax_start"], data["deltax_end"]+data["deltax_steps"]/2, data["deltax_steps"])
        xlabel = "delta_x"
    elif data["deltax_axis"] ==  "y": 
        ylist = np.arange(data["deltax_start"], data["deltax_end"]+data["deltax_steps"]/2, data["deltax_steps"])
        ylabel = "delta_x"
    else:
        data["delta_x"] = data["deltax_start"]

    data["main_property"] = 1
    data["value"] = 1
    data["height"] = 0
    data["gap"] = 4
    data["delta_y"] = 1.5
    
    data["size_x"]=float(data["size_x"])
    data["size_y"]=float(data["size_y"])
    data["offset_left"]=float(data["offset_left"])
    data["offset_right"]=float(data["offset_right"])
    data["offset_bottom"]=float(data["offset_bottom"])
    data["offset_top"]=float(data["offset_top"])

    listgcode = []
    offset_left = data["offset_left"]
    offset_right = data["offset_right"]
    offset_bottom = data["offset_bottom"]
    offset_top = data["offset_top"]
    working_area = [data["size_x"]-data["offset_right"]-data["offset_left"],
                    data["size_y"]-data["offset_bottom"]-data["offset_top"]]
    
    for idx,x in enumerate(xlist):
        data["offset_left"] = offset_left + idx*working_area[0]/len(xlist) # 2.5 34.16 65,83

        if len(xlist)<=1:
            data["offset_right"] = offset_right + (len(xlist)-idx)*(working_area[0]) - working_area[0]
        else:
            data["offset_right"] = offset_right + (len(xlist)-idx)*(working_area[0])/len(xlist) - (working_area[0])/len(xlist)
        
        data[xlabel] = x
        
        
        for idx2,y in enumerate(ylist):
            if len(ylist)<=1:
                data["offset_bottom"] = offset_bottom + idx2*(working_area[1])
            else:
                data["offset_bottom"] = offset_bottom + idx2*(working_area[1])/(len(ylist)-1)
            data[ylabel] = y
            
            gcode = calculateNozzleTest(data)
            
            print(data["offset_left"],data["offset_right"],data["offset_bottom"])

            listgcode.extend(gcode)
    
    #print(listgcode)
    return listgcode

        
    
def calculateNozzleTest(data):
    data = SimpleNamespace(**data)

    working_area = calculate_working_area(data)

    if int(data.main_property) == 1:
        n_bands, length = precalculations_when_nbands_option_selected(data, working_area[0])
    else:
        n_bands, length = precalculations_when_length_option_selected(data, working_area[0])

    band_application_times = [1]

    list_of_bands = []

    delta_x = float(data.delta_x)
    delta_y = float(data.delta_y)

    j = 0
    while sum(band_application_times) != 0:
        for i in range(0, n_bands):
            if band_application_times[i] == 0: continue
            bandlist = []
            zeros = (i * (length + data.gap)) + data.offset_left
            if j % 2:
                current_height = delta_y / 2
                while current_height <= data.height:
                    applicationline = []
                    current_length = delta_x / 2
                    while current_length <= length:
                        applicationline.append(
                            [current_length + float(zeros), float(data.offset_bottom) + current_height])
                        current_length += delta_x
                    bandlist.append(applicationline)
                    current_height += delta_y
            else:
                current_height = 0.
                while current_height <= data.height:
                    applicationline = []
                    current_length = 0.
                    while current_length <= length:
                        applicationline.append(
                            [current_length + float(zeros), float(data.offset_bottom) + current_height])
                        current_length += delta_x
                    bandlist.append(applicationline)
                    current_height += delta_y
            list_of_bands.append(bandlist)
        j += 1
        band_application_times = list(map(minusOneUntilZero, band_application_times))

    print_process = PrintingProcess(list_of_bands,
                                    data.motor_speed,
                                    data.frequency,
                                    data.temperature,
                                    data.pressure,
                                    [data.zero_x, data.zero_y],
                                    0)

    # Creates the Gcode for the application and return it
    return print_process.printing_process()
