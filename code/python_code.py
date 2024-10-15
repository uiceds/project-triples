import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

# Load the dataset
file_path = 'path_to_your_flight_dataset.csv'  
df = pd.read_csv('/Users/sofiafrenkknaul/Documents/GitHub/project-triples/data/modified_flight_dataset_with_CO2_emission.csv')# Replace with the correct path to the dataset Sofia

# Quick overview of the dataset
print(df.head())

# Summary statistics for the numerical columns
print(df.describe())

# Renaming the 'Date' column to 'Day' if necessary (depending on your dataset)
df.rename(columns={'Date': 'Day'}, inplace=True)

# Combine 'Day', 'Month', and 'Year' into a single 'Adjusted_Date' column
df['Adjusted_Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

# Calculate total flight duration (hours + minutes)
df['Total_Duration'] = df['Duration_hours'] + df['Duration_min'] / 60  # Convert to total hours

# Basic EDA: Distribution of Flight Prices
plt.figure(figsize=(10, 6))
plt.hist(df['Price'], bins=50, color='skyblue', edgecolor='black')
plt.title('Distribution of Flight Prices', fontsize=16)
plt.xlabel('Price (INR)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True)
plt.show()

# Distribution of Flight Durations (in hours)
plt.figure(figsize=(10, 6))
plt.hist(df['Total_Duration'], bins=50, color='lightgreen', edgecolor='black')
plt.title('Distribution of Flight Durations (Hours)', fontsize=16)
plt.xlabel('Duration (Hours)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True)
plt.show()

# Relationship between Total Stops and Price
plt.figure(figsize=(10, 6))
df.groupby('Total_Stops')['Price'].mean().plot(kind='bar', color='salmon', edgecolor='black')
plt.title('Average Flight Price by Number of Stops', fontsize=16)
plt.xlabel('Total Stops', fontsize=12)
plt.ylabel('Average Price (INR)', fontsize=12)
plt.grid(True)
plt.show()

# Plot average flight price over time (using Adjusted Date)
plt.figure(figsize=(10, 6))
df.groupby('Adjusted_Date')['Price'].mean().plot(kind='line', marker='o', color='orange')
plt.title('Average Flight Price Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Average Price (INR)', fontsize=12)
plt.grid(True)
plt.show()

# Analyze the most frequent Origin-Destination (O/D) pairs
od_pairs = df.groupby(['Source', 'Destination']).size().reset_index(name='Count').sort_values(by='Count', ascending=False)
print(od_pairs.head())

# Analyze the most attractive destinations (highest count of flights arriving at each destination)
top_destinations = df['Destination'].value_counts().reset_index(name='Count').rename(columns={'index': 'Destination'}).sort_values(by='Count', ascending=False)
print(top_destinations.head())

# Mean price by airline
mean_price_by_airline = df.groupby('Airline')['Price'].mean().reset_index().sort_values(by='Price', ascending=False)
print(mean_price_by_airline)

# Airlines with the most number of flights
flights_by_airline = df['Airline'].value_counts().reset_index(name='Count').rename(columns={'index': 'Airline'}).sort_values(by='Count', ascending=False)
print(flights_by_airline)

# Identify airlines frequently used in long-haul flights (flights with duration > 10 hours)
long_haul_flights = df[df['Total_Duration'] > 10]
long_haul_by_airline = long_haul_flights['Airline'].value_counts().reset_index(name='Long_Haul_Count').rename(columns={'index': 'Airline'}).sort_values(by='Long_Haul_Count', ascending=False)
print(long_haul_by_airline)

#SVD and PCA analysis of data to extract patterns

#1. handling categorical variables with one-hot encoding
#using DataFrames, CategoricalArrays, MLJ
#df[:Airline] = categorical(df[:Airline])
#X_encoded = MLJ.OneHotEncoder() |> fit_transform(df)

print("PROCESSED CATEGORICAL DATA:")
df = pd.get_dummies(df, columns=['Airline', 'Fleet', 'Source', 'Destination'], drop_first=True)
print(df[['Airline_Air India',
       'Airline_GoAir', 'Airline_IndiGo', 'Airline_Jet Airways',
       'Airline_Jet Airways Business', 'Airline_Multiple carriers',
       'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
       'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
       'Fleet_Airbus A320', 'Fleet_Boeing 737s', 'Source_Chennai',
       'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai', 'Destination_Cochin',
       'Destination_Delhi', 'Destination_Hyderabad', 'Destination_Kolkata',
       'Destination_New Delhi']].head())

#2. normalizing numerical values
#X_encoded[:, :Fuel_Consumption_Rate] = (X_encoded[:, :Fuel_Consumption_Rate (liters/hr)] .- mean(X_encoded[:, :Fuel_Consumption_Rate (liters/hr)]))
#X_encoded[:, :CO2_Emitted] = (X_encoded[:, :CO2_Emitted (US Ton)] .- mean(X_encoded[:, :CO2_Emitted (US Ton)]))

df['Fuel_Consumption_normalized'] = df['Fuel_Consumption_Rate (liters/hr)'] - df['Fuel_Consumption_Rate (liters/hr)'].mean()
df['CO2_Emitted_normalized'] = df['CO2_Emitted (US Ton)'] - df['CO2_Emitted (US Ton)'].mean()

print("PROCESSED NUMERICAL DATA:")
normalized_data_df = df[['Fuel_Consumption_normalized', 'CO2_Emitted_normalized']]
print(normalized_data_df.head())

ax = normalized_data_df.hist(bins=20, figsize=(10, 6))
ax[0, 0].set_title('Fuel Consumption Normalized')
ax[0, 1].set_title('CO2 Emitted Normalized')
plt.suptitle('Normalized Numerical Data', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

#3. SVD of normalized numerical data
#using LinearAlgebra
#F=svd(normalized_data_df)
numpy_numerical_data = normalized_data_df.to_numpy()
U, Sigma, Vt = np.linalg.svd(numpy_numerical_data)


#singular_values_plot = plot(F.S, yaxis=log, xlabel = "singular value number", ylabel = "square root of variance")
singular_values_plot = plt.plot(Sigma, marker = 'o')
plt.yscale('log')
plt.xlabel('Singular Value Number')
plt.ylabel('Square Root of Variance')
plt.title('Singular Values Plot')

plt.show()

#4. examination of variance of first few singular values to see if the data is compressible
#ie, to see if we can reduce the number of variables/dimensions and only focus on those
fraction_of_variance = np.sum(Sigma[:2] ** 2)/np.sum(Sigma ** 2)
print(f"Fraction of variance captured by the first 3 singular values: {fraction_of_variance:.4f}")
print("The output of this fraction is 1.000, indicating that the number of variables in our dataset is sufficiently small.")

#5. PCA analysis
pca = PCA(n_components=2)
data_pca = pca.fit_transform(numpy_numerical_data)

#extract the principal component loadings
print("Table of principal components")
loadings = pca.components_
variables = ['Fuel_Consumption_normalized', 'CO2_Emitted_normalized']
loadings_df = pd.DataFrame(loadings, columns=variables)
print(loadings_df.head())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data_pca[:, 0], data_pca[:, 1], alpha=0.6)
ax.set_xlabel('First Principal Component')
ax.set_ylabel('Second Principal Component')
plt.title('PCA: First, Second, and Third Principal Components')
plt.show()
explained_variance = pca.explained_variance_ratio_
print(f"Explained variance by component: {explained_variance}")
#We only have 2 numerical variables, so it makes sense that most of the data points are concentrated around the second and third principal components, because they correspond to the two numerical variables.
#If we use PCA, we might lose valuable information from other features like Fuel Consumption and CO2 Emissions