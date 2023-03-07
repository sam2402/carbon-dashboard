import json

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

# Reading data from a JSON fileReading data from a JSON file
with open('carbon_data.json', 'r') as f:
    carbon_data = json.load(f)

# Get the last day of carbon emissions data
last_day_data = carbon_data[-1]

carbon_kWh = last_day_data['value']/default_kWperday
    
#predict of future cabon emisson with changes
calculated_future_carbon = carbon_kWh
# number of secetion changes
    
# Prioritise the use of energy that is clean
if calculated_future_carbon > 100:
    if last_day_data['energy type'] in energy_types:
        current_energy_type = last_day_data['energy type']
        for energy_type, energy_type_carbon_value in energy_types.items():
            calculated_future_carbon = calculated_future_carbon - energy_types[current_energy_type] + energy_type_carbon_value
            if energy_type_carbon_value < energy_types[current_energy_type] and calculated_future_carbon < 100:
                advice_energy_type = "Use of cleaner energy sources: " + energy_type + ". "
                break
            elif energy_type == 'Nuclear Energy' and calculated_future_carbon > 100:
                advice_energy_type = "Use of cleaner energy sources: Nuclear Energy. "
                break
    else:
        advice_energy_type = "Use of cleaner energy sources: Nuclear Energy. "
        n = 1
else:
    advice_energy_type ="The carbon emission is low enough, keep what you are doing. Donot need to make changes on energy type. "
                    
# Increase server usage
if calculated_future_carbon > 100:
    if last_day_data['server usage'] < 80:
        current_server_usage = last_day_data["server usage"]
        changed_server_usage = current_server_usage + 10
        while changed_server_usage <= 80:
            changed_server_usage += 10
            calculated_future_carbon = calculated_future_carbon * 0.85
            if calculated_future_carbon < 100:
                advice_server_usage = "Increase the server usage rate to: "+ changed_server_usage +"%. "
                break
    advice_server_usage = "Increase the server usage rate to: 80%. "
    if last_day_data['server usage'] >= 80:
        advice_server_usage = "The server usage rate is very high now we will reduce carbon in the other sections. "
else:
    advice_server_usage = "The carbon emission is low enough, keep what you are doing. Donot need to make changes on server usage rate. "
            
# Reduction of server working hours/day
if calculated_future_carbon > 100:
    if last_day_data['server work time'] > 18:
        current_server_work_time = last_day_data["server work time"]
        changed_server_work_time = current_server_work_time - 1
        while changed_server_work_time > 18:
            changed_server_work_time -= 1
            calculated_future_carbon = calculated_future_carbon - 300
            if calculated_future_carbon < 100:
                advice_server_work_time = "Reduce the server work time to: "+ changed_server_work_time +". "
    advice_server_work_time = "Reduce the server work time to: 18h. "
    if last_day_data['server work time'] <= 18:
        advice_server_work_time = "The server work time is very low now we will reduce carbon in the other sections. "
else:
    advice_server_work_time = "The carbon emission is low enough, keep what you are doing. Donot need to make changes on server work time. "
        
# Use Cleaner cooling types
if calculated_future_carbon > 100:
    if last_day_data['cooling type'] in cooling_types:
        current_cooling_type = last_day_data['cooling type']
        for cooling_type, cooling_type_carbon_value in cooling_types.items():
            calculated_future_carbon = calculated_future_carbon - cooling_types[current_cooling_type] + cooling_type_carbon_value
            if cooling_type_carbon_value < cooling_types[current_cooling_type] and calculated_future_carbon < 100:
                advice_cooling_type = "Use of cleaner cooling type: " + cooling_type + ". "
                break
            elif cooling_type == 'Heat pipe cooling system (water-cooled or dry-cooled)' and calculated_future_carbon > 100:
                advice_cooling_type = "Use of cleaner cooling type: Heat pipe cooling system (water-cooled or dry-cooled). "
                break
    else:
        advice_cooling_type = "Use of cleaner cooling type: Heat pipe cooling system (water-cooled or dry-cooled). "
else:
    advice_cooling_type = "The carbon emission is low enough, keep what you are doing. Donot need to make changes on cooling types. "
    
# Replace server hardware configurations that consume less energy
if calculated_future_carbon > 100:
    if last_day_data['server configuration'] in server_configurations:
        current_server_configuration = last_day_data['server configuration']
        for server_configuration, server_configuration_carbon_value in server_configurations.items():
            calculated_future_carbon = calculated_future_carbon - server_configurations[server_configuration] + server_configuration_carbon_value
            if server_configuration_carbon_value < server_configurations[server_configuration] and calculated_future_carbon < 100:
                advice_server_configuration = "Change the CPU current using to: " + server_configuration + ". "
                break
            elif server_configuration == 'Intel Xeon E5-2660 v4' and calculated_future_carbon > 100:
                advice_server_configuration = "Change the CPU current using to: Intel Xeon E5-2660 v4. "
                break
    else:
        advice_server_configuration = "Change the CPU current using to: Intel Xeon E5-2660 v4. "
else:
    advice_server_configuration = "The carbon emission is low enough, keep what you are doing. Donot need to make changes on server configuration. "
        
# if predict future carbon emisson still too high cosider about moving the server location
if calculated_future_carbon > 100:
    advice_location = "Move the server to a higher Latitude/ higher altitude region would help reduce the carbon emisson if possilbe. "
else:
    advice_location = "The carbon emission is low enough, keep what you are doing. Donot need to make changes on server location. "
    

# Create a dictionary to store variables
advice = {
    "advice_energy_type": advice_energy_type,
    "advice_server_usage": advice_server_usage,
    "advice_server_work_time": advice_server_work_time,
    "advice_cooling_type": advice_cooling_type,
    "advice_server_configuration": advice_server_configuration,
    "advice_location": advice_location
}

# Writing a dictionary to a JSON file
with open("advice.json", "w") as f:
    json.dump(advice, f)