## Relationship between price and meter square - Scatter plot###

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

# Read the Excel file
file_path = 'Home Sale Data.xls'
df = pd.read_excel(file_path, header=[1])

# Extract relevant columns
price = df['Price(TL)']
meter_square = df['m² (Net)']

# Create scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(meter_square, price, color='blue', alpha=0.5)

# Format y-axis ticks to display six decimal places
def format_price_ticks(x, pos):
    return f'{x} TL'

plt.gca().yaxis.set_major_formatter(FuncFormatter(format_price_ticks))

plt.title('Price vs. Meter Square')
plt.xlabel('Meter Square')
plt.ylabel('Price')
plt.grid(True)
plt.show()


##Transportation network for five different disctricts in one chart - Pie chart###

# Select the variables you are interested in
selected_variables = [ 'Airport', 'Marmaray', 'Metro', 'Metrobus', 'Minibus', 'Bus stop']

# Replace 1 with 'Yes' and 0 with 'No' for selected variables
df[selected_variables] = df[selected_variables].replace({1: 'Yes', 0: 'No'})

# Select the districts you are interested in
selected_districts = ['Bagcilar', 'Esenyurt', 'Kucukcekmece', 'Pendik', 'Umraniye']

# Create a single figure for all pie charts
fig, axes = plt.subplots(nrows=1, ncols=len(selected_districts), figsize=(15, 5))

# Create pie charts for each selected district with counts of 'Yes' variables
for i, district in enumerate(selected_districts):
    district_data = df[df['District'] == district]
    yes_counts = district_data[selected_variables].eq('Yes').sum()

    axes[i].pie(yes_counts, labels=yes_counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    axes[i].set_title(f'Percentage of Transportation Networks\nin {district}', fontsize=10)

    # Set smaller font size for labels
    axes[i].tick_params(axis='both', labelsize=6)

# Adjust the layout for better visibility
plt.tight_layout()
plt.show()


## m² (Net) Histogram with Msquare for each Districts ###

filtered_df = df[df['District'].isin(selected_districts)]

# Plot histogram for each district
plt.figure(figsize=(15, 5))

for i, district in enumerate(selected_districts, start=1):
    plt.subplot(1, len(selected_districts), i)
    district_data = filtered_df[filtered_df['District'] == district]
    sns.histplot(district_data['m² (Net)'], bins=10, kde=True, color='skyblue')
    
    plt.xlabel('m² (Net)')
    plt.ylabel('Frequency')
    plt.title(f'{district}')

plt.tight_layout()
plt.show()



##Number of rooms and price relationship between selected districts - Bar chart ###

# Filter data for the specified districts and room configurations
selected_rooms = ['1+1', '2+1', '3+1']

filtered_df = df[(df['District'].isin(selected_districts)) & (df['Number of rooms'].isin(selected_rooms))]

# Group by district and room configuration, and calculate the average price for each group
grouped_data = filtered_df.groupby(['District', 'Number of rooms'])['Price(TL)'].mean().reset_index()

# Pivot the data for plotting
pivot_data = grouped_data.pivot(index='District', columns='Number of rooms', values='Price(TL)')

# Plotting the grouped bar chart
ax = pivot_data.plot(kind='bar', color=['skyblue', 'lightgreen', 'lightcoral'])
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')
plt.xlabel('District')
plt.ylabel('Average Price')
plt.title('Average Price for Different Number of Rooms in Selected Districts')
plt.legend(title='Number of Rooms')
plt.show()


## Distrcis and Health and Wellness Facilities relationships - Bar ###

# Replace 1 with 'Yes' and 0 with 'No' for selected variables
selected_variables = ['Gym', 'Pharmacy', 'Hospital', 'The health clinic']
df[selected_variables] = df[selected_variables].replace({1: 'Yes', 0: 'No'})

# Select the districts you are interested in
filtered_df = df[df['District'].isin(selected_districts)]

# Plot stacked histograms for each selected variable
plt.figure(figsize=(20, 5))

for i, variable in enumerate(selected_variables, start=1):
    plt.subplot(1, 4, i)
    stacked_data = pd.crosstab(filtered_df['District'], filtered_df[variable], normalize='index')
    stacked_data.plot(kind='bar', stacked=True, color=['lightcoral', 'skyblue'], ax=plt.gca())

    plt.xlabel('District')
    plt.ylabel('Proportion')
    plt.title(f'Is the house close to the {variable}?')
    plt.legend(title='Value')

plt.tight_layout()
plt.show()

## Isolation comparison of 5 district - Bar ###

# Extract relevant columns
# Replace 1 with 'Yes' and 0 with 'No'
df['SoundInsulation'] = df['Sound insulation'].replace({1: 'Yes', 0: 'No'})
df['ThermalInsulation'] = df['Thermal Insulation'].replace({1: 'Yes', 0: 'No'})

# Plotting histograms
fig, axs = plt.subplots(1, 2, figsize=(15, 5))

# Sound Insulation
sound_insulation_counts = df.groupby(['District', 'SoundInsulation']).size().unstack().fillna(0)
axs[0].bar(sound_insulation_counts.index, sound_insulation_counts['Yes'], color='skyblue', label='Yes')
axs[0].bar(sound_insulation_counts.index, sound_insulation_counts['No'], color='lightcoral', label='No', bottom=sound_insulation_counts['Yes'])
axs[0].set_title('Sound Insulation')
axs[0].set_ylabel('Count')
axs[0].legend()
axs[0].tick_params(axis='x', labelsize=8)  # Adjust x-label font size

# Thermal Insulation
thermal_insulation_counts = df.groupby(['District', 'ThermalInsulation']).size().unstack().fillna(0)
axs[1].bar(thermal_insulation_counts.index, thermal_insulation_counts['Yes'], color='skyblue', label='Yes')
axs[1].bar(thermal_insulation_counts.index, thermal_insulation_counts['No'], color='lightcoral', label='No', bottom=thermal_insulation_counts['Yes'])
axs[1].set_title('Thermal Insulation')
axs[1].set_ylabel('Count')
axs[1].legend()
axs[1].tick_params(axis='x', labelsize=8)  # Adjust x-label font size


plt.show()

## Average Price of Houses by District - Line Chart ###

# Select relevant columns
selected_columns = ['District', 'Price(TL)']

# Group by district and calculate the average price
average_price_by_district = df[selected_columns].groupby('District').mean()

# Reset the index to make 'District' a regular column
average_price_by_district.reset_index(inplace=True)

# Create a line chart
plt.figure(figsize=(12, 6))
plt.plot(range(1, len(average_price_by_district) + 1), average_price_by_district['Price(TL)'], marker='o', linestyle='-', color='b')

# Set labels and title
plt.xlabel('Districts')
plt.xticks(range(1, len(average_price_by_district) + 1), average_price_by_district['District'], rotation=45, ha='right')
plt.ylabel('Average Price')
plt.title('Average Price of Houses by District')

# Show the plot
plt.tight_layout()
plt.show()

## Price of Houses for Top Districts - Line Chart ###

# Group by district and calculate the average price
average_price_by_district = df[selected_columns].groupby('District').mean()

# Reset the index to make 'District' a regular column
average_price_by_district.reset_index(inplace=True)

# Sort districts by average price
top_districts = average_price_by_district.nlargest(5, 'Price(TL)')

# Create a line chart for each top district
plt.figure(figsize=(12, 6))

for i, (_, district_row) in enumerate(top_districts.iterrows()):
    district_data = df[df['District'] == district_row['District']]
    plt.plot(range(1, len(district_data) + 1), district_data['Price(TL)'], marker='o', linestyle='-', label=district_row['District'])

# Set labels and title
plt.xlabel('Districts Total House Sale Numbers')
plt.ylabel('Price (TL)')
plt.title('Price of Houses for Top Districts')

# Show the legend
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()


