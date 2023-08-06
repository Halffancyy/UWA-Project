# Name: Shijun Shao; Student ID: 23926903
def main(csvfile):

    try:
        # Open the CSV file and read its contents.
        with open(csvfile, 'r') as file:
            lines = file.readlines()
            
        # Create two dictionaries to store information.
        Task1_dict = {}
        Task2_dict = {}
        
        # Grab column names from the first row.
        first_row = lines[0].rstrip('\n').split(',')
        
        # Find the index of required columns.
        regions_index = first_row.index('Regions')
        country_index = first_row.index('Country')
        population_index = first_row.index('Population')
        land_area_index = first_row.index('Land Area')
        net_change_index = first_row.index('Net Change')
        
        # Iterate over the remaining rows.
        for line in lines[1:]:
            row = line.strip('\n').split(',')
        
            # Check the validity of the data.
            if (
                len(row) == len(first_row) and # If there is any invalid data then entire row(s) should be ignored.
                row[regions_index] and
                row[country_index] and
                row[population_index] and
                row[land_area_index] and
                row[net_change_index]
            ):
                regions_name = row[regions_index].lower() # Uniform region names in lowercase mode.
                country_name = row[country_index].lower()
                population = int(row[population_index])
                land_area = float(row[land_area_index])
                net_change = int(row[net_change_index])
            
            if(
                int(row[population_index]) != float(row[population_index]) or # Ensure that the number of people is integer.
                population < 0 or # Ensure that the number of people and land area are positive.
                land_area < 0
            ):
                continue
        
            # Add the relevant information to Task1_dict.
            if regions_name in Task1_dict:
                Task1_data = Task1_dict[regions_name]
                Task1_data['Population'].append(population)
                Task1_data['Countries'].append(country_name)
                Task1_data['Land area'].append(land_area)
            else:
                Task1_dict[regions_name] = {
                    'Population': [population],
                    'Countries': [country_name],
                    'Land area':[land_area]
                }
        
            # Add the relevant information to Task2_dict.
            if regions_name in Task2_dict:
                Task2_data = Task2_dict[regions_name]
            else:
                Task2_data = {}
        
            Task2_data[country_name] = [
                population,
                net_change,
                '',
                land_area, 
                country_name
            ]
        
            Task2_dict[regions_name] = Task2_data
        
        # Store the statistical information into Task1_dict.
        for region, data in Task1_dict.items():
            population = data['Population']
            land_area = data['Land area']
            standard_error = std_error(population)
            cosine_similarity = similarity(population,land_area)
        
            Task1_dict[region] = [standard_error, cosine_similarity]
            
        # Store the statistical information into Task2_dict.
        for region, data in Task2_dict.items():

            population_data = [[country_data[0], round(country_data[0]/country_data[3], 4), country_data[4]] for country_data in data.values() if country_data[3] != 0]
            region_population = sum(country_data[0] for country_data in population_data)
        
            for country, country_data in data.items():
                population = country_data[0]
                net_change = country_data[1]
                land_area = country_data[3]
                country_name = country_data[4]
                percentage_population = percentage(population, region_population)
                density_population = density(population, land_area)
                
                info = [population,density_population,country_name]
                rank_population = rank(population_data,info)
        
                country_data[2] = percentage_population
                country_data[3] = density_population
                country_data[4] = rank_population
        
        return Task1_dict, Task2_dict
    
    except:
        return "Error: This file does not exist.", "Error: This file does not exist."
        
# Task 1) a: Calculate standard error of population for each region.
def std_error(population):
    mean_population = sum(population) / len(population)
    std_deviation = ((sum((x - mean_population) ** 2 for x in population) / (len(population) - 1))) ** 0.5
    std_error = std_deviation / len(population) ** 0.5
    return round(std_error, 4)

# Task 1) b: Calculate the cosine similarity between population and land area for each region.
def similarity(population, land_area):
    molecular = sum(x * y for x,y in zip(population, land_area))
    abs_population = (sum(x ** 2 for x in population)) ** 0.5
    abs_land_area = (sum(y ** 2 for y in land_area)) ** 0.5
    denominator = abs_population * abs_land_area
    similarity = molecular / denominator
    return round(similarity, 4)

# Task 2) a: Calculate the percentage of population with respect to a region.
def percentage(population, region_population):
    if region_population == 0:
        return 0
    else:
        percentage = (population * 100) / region_population
        return round(percentage, 4)
    
# Task 2) b: Calculate the density of population.
def density(population, land_area):
    if land_area == 0:
        return 0
    else:
        density =  population / land_area
        return round(density, 4)

# Task 2) c: Calculate the rank.
def rank(population_data,info):
    sorted_data = sorted(population_data, key=lambda x: (-x[0], -x[1], x[2]))
    rank = sorted_data.index(info) + 1
    return rank


   

