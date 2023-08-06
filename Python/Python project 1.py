# Name: Shijun Shao, Student ID: 23926903
def main(csvfile, region):
    
    try:
        # Open the CSV file and read its contents
        with open(csvfile, 'r') as file:
            lines = file.readlines()
        
        # Store data from the CSV file into a list
        data=[]
        for line in lines:
            lst = line.rstrip('\n').split(',')
            data.append(lst)
        
        # Remove the column name from the first row
        New_lst = data.pop(0)

        # Task 1: Find the country name which has minimum and maximum population in a specific region which has positive net change in population.
        task1_specific_regions = [ line for line in data if int(line[3]) > 0 and line[5] == region ]
        maximum_population_country = max(task1_specific_regions,key=lambda x:int(x[1]))
        minmum_population_country = min(task1_specific_regions,key=lambda x:int(x[1]))
        
        # Task 2: Calculate the average and standard deviation of population for a specific region.
        specific_region = [ line for line in data if line[5] == region ]
        population_specific_region = [ int(line[1]) for line in specific_region ]
        if len(population_specific_region) != 0:
            avg_population = sum(population_specific_region) / len(population_specific_region)
            round_avg_population = round(avg_population,4)
        else:
            round_avg_population = 0
        if len(population_specific_region) > 1:
            stdv_population = round((sum((x - avg_population)**2 for x in population_specific_region) / (len(population_specific_region) - 1))**0.5,4)
        else:
            stdv_population = 0

        # Task 3: Calculate the density of population for each country in a specific region.
        country_density=[]
        for line in specific_region:
            population = int(line[1])
            land_area = int(line[4])
            density = round(population / land_area,4)
            country_density.append([line[0],density])
            country_density = sorted(country_density,key=lambda x:x[1],reverse=True)
            
        # Task 4: Calculate the correlation between population and land area for all the countries in a specific region.
        land_area_specific_region = [ int(line[4]) for line in specific_region ]
        if len(land_area_specific_region) != 0:
            avg_area = sum(land_area_specific_region) / len(land_area_specific_region)
            numerator = sum([(int(line[1]) - avg_population) * (int(line[4]) - avg_area) for line in specific_region])
            denominator = (sum([(int(line[1]) - avg_population) ** 2 for line in specific_region]) * sum([(int(line[4]) - avg_area) ** 2 for line in specific_region])) ** 0.5
        else:
            corr = 0        
        if denominator == 0:
            corr = 0
        else:
            corr = round(numerator / denominator,4)

        return [maximum_population_country[0],minmum_population_country[0]],[round_avg_population,stdv_population],country_density,corr

    # If the input region is not the region in the file, 0 will be output
    except:
        return "This file or region does not exist", "This file or region does not exist", "This file or region does not exist", "This file or region does not exist"