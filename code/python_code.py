import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


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

#1. normalizing numerical values
#X_encoded[:, :Fuel_Consumption_Rate] = (X_encoded[:, :Fuel_Consumption_Rate (liters/hr)] .- mean(X_encoded[:, :Fuel_Consumption_Rate (liters/hr)]))
#X_encoded[:, :CO2_Emitted] = (X_encoded[:, :CO2_Emitted (US Ton)] .- mean(X_encoded[:, :CO2_Emitted (US Ton)]))

df['Fuel_Consumption_normalized'] = df['Fuel_Consumption_Rate (liters/hr)'] - df['Fuel_Consumption_Rate (liters/hr)'].mean()
df['Total_Duration'] = df['Duration_hours'] + df['Duration_min'] / 60 
df['Total_Duration_normalized'] = df['Total_Duration'] - df['Total_Duration'].mean()


print("PROCESSED NUMERICAL DATA:")
normalized_data_df = df[['Fuel_Consumption_normalized', 'Total_Duration_normalized']]
print(normalized_data_df.head())

ax = normalized_data_df.hist(bins=20, figsize=(10, 6))
ax[0, 0].set_title('Fuel Consumption Normalized')
ax[0, 1].set_title('Total Duration Normalized')
plt.suptitle('Normalized Numerical Data', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

#2. SVD of normalized numerical data
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

#3. examination of variance of first few singular values to see if the data is compressible
#ie, to see if we can reduce the number of variables/dimensions and only focus on those
fraction_of_variance = np.sum(Sigma[:2] ** 2)/np.sum(Sigma ** 2)
print(f"Fraction of variance captured by the first 2 singular values: {fraction_of_variance:.4f}")
print("The output of this fraction is 1.000, indicating that the number of variables in our dataset is sufficiently small.")

#4. PCA analysis
pca = PCA(n_components=2)
data_pca = pca.fit_transform(numpy_numerical_data)

#extract the principal component loadings
print("Table of principal components")
loadings = pca.components_
variables = ['Fuel_Consumption_normalized', 'Total_Duration_normalized']
loadings_df = pd.DataFrame(loadings, columns=variables)
print(loadings_df.head())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data_pca[:, 0], data_pca[:, 1], alpha=0.6)
ax.set_xlabel('First Principal Component')
ax.set_ylabel('Second Principal Component')
plt.title('PCA: First and Second Principal Components')
plt.show()
explained_variance = pca.explained_variance_ratio_
print(f"Explained variance by component: {explained_variance}")
#We only have 2 numerical variables, so it makes sense that most of the data points are concentrated around the second and third principal components, because they correspond to the two numerical variables.
#If we use PCA, we might lose valuable information from other features like Fuel Consumption and CO2 Emissions
<<<<<<< Updated upstream


#handling categorical variables with one-hot encoding
#using DataFrames, CategoricalArrays, MLJ
#df[:Airline] = categorical(df[:Airline])
#X_encoded = MLJ.OneHotEncoder() |> fit_transform(df)

print("PROCESSED CATEGORICAL DATA IN df_modified:")

#copy df into df_modified:
df_modified = df.copy()
df_modified.drop(columns=['Fuel_Consumption_normalized', 'Total_Duration_normalized'], inplace=True)

#replace duriation in hours and minutes to total duration in hours
df_modified['Total_Duration'] = df_modified['Duration_hours'] + df_modified['Duration_min'] / 60
df_modified.drop(columns=['Duration_hours', 'Duration_min'], inplace=True)

#create binary variable - 1 for cities if they appear in Table 2, 0 if they dont
frequent_routes = set((row['Source'], row['Destination']) for _, row in od_pairs.iterrows())
df_modified['Frequent_Route'] = df_modified.apply(lambda row: 1 if (row['Source'], row['Destination']) in frequent_routes else 0, axis=1)
df_modified.drop(columns=['Source', 'Destination', 'Adjusted_Date'], inplace=True)

#one-hot encoding of 'Airline'
df_modified = pd.get_dummies(df_modified, columns=['Airline', 'Fleet'], drop_first=True)
airline_columns = [value for value in df_modified.columns if 'Airline_' in value]
fleet_columns = [value for value in df_modified.columns if 'Fleet_' in value]

print("Airline columns after one-hot encoding:", airline_columns)
print("Fleet columns after one-hot encoding:", fleet_columns)

print("df_modified:")
print(df_modified.head())


#drop the CO2_Emitted (US Ton) column so it can be used as the independent variable
X = df_modified.drop(columns=['CO2_Emitted (US Ton)'])
y = df_modified['CO2_Emitted (US Ton)']

print("Verify data types in X:")
print(X.dtypes)


#split the data into training and testing
X_train, X_test, y_train, y_test =  train_test_split(X, y, test_size=0.2, random_state=42)

#initialize decision tree regressor
tree_model = DecisionTreeRegressor(criterion="squared_error", random_state=42)

#train the model
tree_model.fit(X_train, y_train)

#generate predictions
y_pred = tree_model.predict(X_test)

#evaluate the model
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)  
r2 = r2_score(y_test, y_pred)

print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R^2 Score: {r2}")


=======
print(df['Airlines'].unique())
>>>>>>> Stashed changes
