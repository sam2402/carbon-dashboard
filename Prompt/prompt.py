import json
import pandas as pd

default_kWperday = 500

# Default server hardware configuration list
server_configurations = {
    'Intel Xeon Platinum 8280': 450,
    'Intel Xeon Gold 6248': 300,
    'AMD EPYC 7601:': 250,
    'Intel Xeon Silver 4210': 200,
    'AMD EPYC 7302P': 150,
    'Intel Xeon E5-2697 v2':140,
    'AMD EPYC 7401P': 120,
    'Intel Xeon E5-2650 v4': 100,
    'AMD EPYC 7351P': 90,
    'Intel Xeon E5-2660 v4': 80
}

# Default energy types list
energy_types = {
    'Coal': 1000,
    'Petroleum': 800,
    'Natural Gas': 500,
    'Biomass Engergy': 200,
    'Battery': 50,
    'Solar PV': 50,
    'Subterranean heat': 45,
    'Water Power': 20,
    'Wind': 10,
    'Nuclear Energy': 10
}

# Default cooling types list
cooling_types = {
    'Traditional air conditioning system': 950,
    'Water-cooled chiller': 250,
    'Water-cooled heat exchanger': 150,
    'Direct air cooling system (dry cooling)': 100,
    'Indirect air cooling system (dry cooling)': 50,
    'Air-side economizer cooling system (dry cooling)': 30,
    'Heat recovery system (water-cooled or dry-cooled)': 20,
    'Direct evaporative cooling system (wet cooling)': 20,
    'Indirect evaporative cooling system (wet cooling)': 15,
    'Heat pipe cooling system (water-cooled or dry-cooled)': 10
}


def get_prompt(carbon_data):
    # Get the last day of carbon emissions data
    last_day_data = carbon_data[-1]
    carbon_emisson = last_day_data['value']
    carbon_kWh = carbon_emisson/default_kWperday

    #The initial data of this server
    server_location = last_day_data['location']
    server_energy_type = last_day_data['energy type']
    server_useage_rate = last_day_data['server usage']
    server_work_time = last_day_data['server work time']
    server_cooling_type = last_day_data['cooling type']
    server_configuration = last_day_data['server configuration']
        
    #predict of future cabon emisson with changes
    calculated_future_carbon = carbon_kWh

    #prompt format
    prompt = "Hi, we are running an project that help Volvo to reduce the carbon emisson of their sale software server. The current co2 emisson per day is " + str(carbon_emisson) + ". and The server is located in " + server_location + ". We want to reduce the carbon by these sections, can you help us getting more detail advice and explain it: "
        
    # Prioritise the use of energy that is clean 
    if calculated_future_carbon > 100:
        if server_energy_type in energy_types:
            current_energy_type = server_energy_type
            for energy_type, energy_type_carbon_value in energy_types.items():
                calculated_future_carbon = calculated_future_carbon - energy_types[current_energy_type] + energy_type_carbon_value
                if energy_type_carbon_value < energy_types[current_energy_type] and calculated_future_carbon < 100:
                    advice_energy_type = "Use of cleaner energy sources: " + energy_type + ". "
                    prompt = prompt + advice_energy_type
                    break
                elif energy_type == 'Nuclear Energy' and calculated_future_carbon > 100:
                    advice_energy_type = "Use of cleaner energy sources: Nuclear Energy. "
                    prompt = prompt + advice_energy_type
                    break
        else:
            advice_energy_type = "Use of cleaner energy sources: Nuclear Energy. "
            prompt = prompt + advice_energy_type
    else:
        prompt = "Hi, we are running an project that help Volvo to reduce the carbon emisson of their sale software server. The current co2 emisson per day is " + str(carbon_emisson) +". and The server is located in "+ server_location +". The current energy type of server use is: "+ server_energy_type + ". The current cooling type of server use is: "+ server_cooling_type + ". The current server usage rate is: " + str(server_useage_rate) + ". The current server work hours per day is : " + str(server_work_time) + ". The current cpu of server use is: "+ server_configuration + ". Can you help us getting more detail advice in reduce carbon emisson and explain it."
                        
    # Increase server usage
    if calculated_future_carbon > 100:
        if server_useage_rate < 80:
            current_server_usage = server_useage_rate
            changed_server_usage = current_server_usage + 10
            while changed_server_usage <= 80:
                changed_server_usage += 10
                calculated_future_carbon = calculated_future_carbon * 0.85
                if calculated_future_carbon < 100:
                    advice_server_usage = "Increase the server usage rate to: "+ changed_server_usage +"%. "
                    break
        advice_server_usage = "Increase the server usage rate to: 80%. "
        prompt = prompt + advice_server_usage
        if server_useage_rate >= 80:
            advice_server_usage = "The server usage rate is very high now we will reduce carbon in the other sections. "
            prompt = prompt + advice_server_usage

    else:
        advice_server_usage = None


    # Reduction of server working hours/day
    if calculated_future_carbon > 100:
        if server_work_time > 18:
            current_server_work_time = server_work_time
            changed_server_work_time = current_server_work_time - 1
            while changed_server_work_time > 18:
                changed_server_work_time -= 1
                calculated_future_carbon = calculated_future_carbon - 300
                if calculated_future_carbon < 100:
                    advice_server_work_time = "Reduce the server work time to: "+ changed_server_work_time +". "
                    prompt = prompt + advice_server_work_time
                    break
        advice_server_work_time = "Reduce the server work time to: 18h. "
        prompt = prompt + advice_server_work_time
        if server_work_time <= 18:
            advice_server_work_time = "The server work time is very low now we will reduce carbon in the other sections. "
            prompt = prompt + advice_server_work_time
    else:
        advice_server_work_time = None

    # Use Cleaner cooling types
    if calculated_future_carbon > 100:
        if server_cooling_type in cooling_types:
            current_cooling_type = server_cooling_type
            for cooling_type, cooling_type_carbon_value in cooling_types.items():
                calculated_future_carbon = calculated_future_carbon - cooling_types[current_cooling_type] + cooling_type_carbon_value
                if cooling_type_carbon_value < cooling_types[current_cooling_type] and calculated_future_carbon < 100:
                    advice_cooling_type = "Use of cleaner cooling type: " + cooling_type + ". "
                    prompt = prompt + advice_cooling_type
                    break
                elif cooling_type == 'Heat pipe cooling system (water-cooled or dry-cooled)' and calculated_future_carbon > 100:
                    advice_cooling_type = "Use of cleaner cooling type: Heat pipe cooling system (water-cooled or dry-cooled). "
                    prompt = prompt + advice_cooling_type
                    break
        else:
            advice_cooling_type = "Use of cleaner cooling type: Heat pipe cooling system (water-cooled or dry-cooled). "
            prompt = prompt + advice_cooling_type
    else:
        advice_cooling_type = None
        
    # Replace server hardware configurations that consume less energy
    if calculated_future_carbon > 100:
        if server_configuration in server_configurations:
            current_server_configuration = server_configuration
            for configuration, configuration_carbon_value in server_configurations.items():
                calculated_future_carbon = calculated_future_carbon - server_configurations[configuration] + configuration_carbon_value
                if configuration_carbon_value < server_configurations[configuration] and calculated_future_carbon < 100:
                    advice_server_configuration = "Change the CPU current using to: " + configuration + ". "
                    prompt = prompt + advice_server_configuration
                    break
                elif configuration == 'Intel Xeon E5-2660 v4' and calculated_future_carbon > 100:
                    advice_server_configuration = "Change the CPU current using to: Intel Xeon E5-2660 v4. "
                    prompt = prompt + advice_server_configuration
                    break
        else:
            advice_server_configuration = "Change the CPU current using to: Intel Xeon E5-2660 v4. "
            prompt = prompt + advice_server_configuration
    else:
        advice_server_configuration = None
            
    # if predict future carbon emisson still too high cosider about moving the server location
    if calculated_future_carbon > 100:
        advice_location = "Move the server to a higher Latitude/ higher altitude region would help reduce the carbon emisson if possilbe. "
        prompt = prompt + advice_location
    else:
        advice_location = None
        
    return prompt

# Read the data from list_dic.py
from list_dic import list
x_list = list

y = get_prompt(x_list)