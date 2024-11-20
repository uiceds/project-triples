import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV


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


#handling categorical variables with one-hot encoding
#using DataFrames, CategoricalArrays, MLJ
#df[:Airline] = categorical(df[:Airline])
#X_encoded = MLJ.OneHotEncoder() |> fit_transform(df)

print("PROCESSED CATEGORICAL DATA IN df_modified:")

#copy df into df_modified:
df_modified = df.copy()

print("df_modified:")
print(df_modified.head())

df_modified.drop(columns=['Fuel_Consumption_normalized', 'Total_Duration_normalized'], inplace=True)

#replace duriation in hours and minutes to total duration in hours
df_modified['Total_Duration'] = df_modified['Duration_hours'] + df_modified['Duration_min'] / 60
df_modified.drop(columns=['Duration_hours', 'Duration_min', 'Dep_hours', 'Dep_min', 'Arrival_hours', 'Arrival_min', 'Day', 'Month', 'Year'], inplace=True)

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

#FEATURE SELECTION FROM RANDOM FOREST
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFECV

df_analyse_features_1 = df_modified.copy()

X_analyse_features_1 = df_analyse_features_1.drop(columns=['CO2_Emitted (US Ton)'])
y_analyse_features_1 = df_analyse_features_1['CO2_Emitted (US Ton)'].values

features = X_analyse_features_1.columns

X_train_analyse_features, X_test_analyse_features, y_train_analyse_features, y_test_analyse_features = train_test_split(X_analyse_features_1, y_analyse_features_1, test_size=0.2, random_state=42)

rf = RandomForestRegressor(random_state=0)

rf.fit(X_analyse_features_1,y_analyse_features_1)

f_i = list(zip(features,rf.feature_importances_))
f_i.sort(key = lambda x : x[1])
plt.barh([x[0] for x in f_i],[x[1] for x in f_i])
plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Feature Importances from Random Forest for Original Dataset")

plt.show()

#remove data that is binary value 
X_for_corrplot = df_modified.drop(columns=['Fleet_Airbus A320', 'Fleet_Boeing 737s', 'Frequent_Route'])
#correlation matrix for variables to get a visual on correlation among variables before applying decision trees
corr_matrix = X_for_corrplot.corr()
# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix of Features for Original Data")
plt.show()

#drop CO2_Emitted (US Ton) column so it can be used as the independent variable
X_original = df_modified.drop(columns=['CO2_Emitted (US Ton)'])
y_original = df_modified['CO2_Emitted (US Ton)']

print("Verify data types in X_original:")
print(X_original.dtypes) ###


#split the data into training and testing
X_original_train, X_original_test, y_original_train, y_original_test =  train_test_split(X_original, y_original, test_size=0.2, random_state=42)

#initialize decision tree regressor
tree_model_original = DecisionTreeRegressor(criterion="squared_error", random_state=42)

#train the model
tree_model_original.fit(X_original_train, y_original_train)

#generate predictions
y_original_pred = tree_model_original.predict(X_original_test)

#evaluate the model
mse = mean_squared_error(y_original_test, y_original_pred)
rmse = np.sqrt(mse)  
r2 = r2_score(y_original_test, y_original_pred)

print(f"Original Root Mean Squared Error (RMSE) for Original Data: {rmse}")
print(f"Original R^2 Score for Original Data: {r2}") #The R^2 value is suspiciosly perfect, let's check if any variables are correlated


#first plots:
#scatter plot
plt.figure(figsize=(10,6))
plt.scatter(y_original_test, y_original_pred, alpha=0.6)
plt.plot([y_original_test.min(), y_original_test.max()], [y_original_test.min(), y_original_test.max()], 'r--')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values for Original Data')
plt.show()

#residuals plot
residuals = y_original_test - y_original_pred
plt.figure(figsize=(10, 6))
plt.scatter(y_original_pred, residuals, alpha=0.6)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot for Original Data')
plt.show()

#histogram
plt.figure(figsize=(10, 6))
plt.hist(residuals, bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Distribution of Residuals for Original Data')
plt.show()

#CO2 EMITTED / TOTAL DURATION -- BINOMIAL DISTRIBUTION
#there is a definite correlation between CO2 emitted and total duration of flight, which would be obvious because the longer the flight is, the more CO2 it will emit. 
#Hence, we will transform the dependent variable, CO2 Emmitted (US Ton) to CO2 Emitted/Hour by dividing CO2 Emmitted (US Ton) by Total Duration (hours)
#I will conduct PCA on all variables except the binary variable Frequent_Route

#TO DO:
#bring back 0/1 values and use random forest package (feature explanation -- which indep variable most useful for prediction)

df_modified2 = df_modified.copy()

df_modified2['CO2_Emitted/Hour'] = df_modified2['CO2_Emitted (US Ton)'] / df_modified2['Total_Duration']
df_modified2 = df_modified2.drop(columns=['CO2_Emitted (US Ton)', 'Total_Duration'])

plt.figure(figsize=(10, 5))
plt.hist(df_modified2['CO2_Emitted/Hour'], bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Transformed CO2_Emitted/Hour')
plt.ylabel('Frequency')
plt.title('Distribution of Transformed CO2_Emitted/Hour')
plt.show()

plt.figure(figsize=(10, 5))
plt.hist(df_modified2['Fuel_Consumption_Rate (liters/hr)'], bins=30, color='salmon', edgecolor='black')
plt.xlabel('Transformed Fuel Consumption Rate (liters/hr)')
plt.ylabel('Frequency')
plt.title('Distribution of Transformed Fuel Consumption Rate')
plt.show()

#feature selection
df_analyse_features_2 = df_modified2.copy()

X_analyse_features_2 = df_analyse_features_2.drop(columns=['CO2_Emitted/Hour'])
y_analyse_features_2 = df_analyse_features_2['CO2_Emitted/Hour'].values

features2 = X_analyse_features_2.columns

X_train_analyse_features2, X_test_analyse_features2, y_train_analyse_features2, y_test_analyse_features2 = train_test_split(X_analyse_features_2, y_analyse_features_2, test_size=0.2, random_state=42)

rf = RandomForestRegressor(random_state=0)

rf.fit(X_analyse_features_2,y_analyse_features_2)

f_i = list(zip(features2,rf.feature_importances_))
f_i.sort(key = lambda x : x[1])
plt.barh([x[0] for x in f_i],[x[1] for x in f_i])
plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Feature Importances from Random Forest for Dataset with CO2_Emitted/Hour")

plt.show()


#correlation matrix for variables to get a visual on correlation among variables before applying decision trees
#corr_matrix = X_for_corrplot2.corr()
corr_matrix2 = df_modified2.drop(columns=['Frequent_Route'])

corr_matrix2 = corr_matrix2.corr()

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix2, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix of Features for CO2_Emissions/Hour Data")
plt.show()

print("df_modified2 head:")
df_modified2.head()

print(df_modified2[['CO2_Emitted/Hour', 'Fuel_Consumption_Rate (liters/hr)']].head())

X_df2 = df_modified2.drop(columns=['CO2_Emitted/Hour'])
#X_df = X_df.astype(np.float64) #might need to get rid of

#X_df = X_df.fillna(X_df.mean())
print(X_df2.dtypes)
'''X = X_df.values
std_dev = X.std(axis=0)
zero_std_columns = (std_dev == 0)


print("Standard deviation of each column in X:", std_dev)
print("Columns with zero standard deviation:", zero_std_columns)

# Remove columns with zero standard deviation from X
X_reduced = X[:, ~zero_std_columns]'''

y2 = df_modified2['CO2_Emitted/Hour'].values

#split the data
X_train2, X_test2, y_train2, y_test2 = train_test_split(X_df2, y2, test_size=0.2, random_state=42)
#X_train = X_train.astype(np.float64)
print(X_train2.dtypes)

'''
#normalize data
X_train_norm = (X_train - X_train.mean(axis=0)) / X_train.std(axis=0)
X_test_norm = (X_test - X_train.mean(axis=0)) / X_train.std(axis=0)
y_norm = (y - y.mean()) / y.std()

#Perform SVD for PCA
U, Sigma, Vt = np.linalg.svd(X_train_norm, full_matrices=False)

#calculate the total variance explained by each component
explained_variance = np.square(Sigma) / np.sum(np.square(Sigma))

#calculate cumulative explained variance
cumulative_variance = np.cumsum(explained_variance)

#choose the minimum number of components that explain at least 90% variance
num_components = np.argmax(cumulative_variance >= 0.90) + 1  # +1 to account for zero-based indexing
print(f"Number of components explaining 90% variance: {num_components}")

#only use number of components equal to `num_components`
U_reduced = U[:, :num_components]
Sigma_reduced = np.diag(Sigma[:num_components])
Vt_reduced = Vt[:num_components, :]
X_train_pca = X_train_norm @ Vt_reduced.T
X_test_pca = X_test_norm @ Vt_reduced.T'''

#train the Decision Tree Regressor on the transformed training data
tree_model2 = DecisionTreeRegressor(criterion="squared_error", random_state=42)
'''param_grid = {
    'max_depth': [5, 10, 15, 20, 25, None],
    'min_samples_split': [2, 5, 10, 20]
}
grid_search = GridSearchCV(estimator=tree_model2, param_grid=param_grid, scoring='neg_mean_squared_error', cv=5, n_jobs=-1)

grid_search.fit(X_train, y_train)

# Get the best parameters and best score
best_params = grid_search.best_params_
best_score = np.sqrt(-grid_search.best_score_)

tree_model2 = DecisionTreeRegressor(**best_params, random_state=42)'''
tree_model2.fit(X_train2, y_train2)

# Generate predictions
y_pred2 = tree_model2.predict(X_test2)

# Calculate and print RMSE and R^2 Score on test data
rmse = np.sqrt(mean_squared_error(y_test2, y_pred2))
r2 = r2_score(y_test2, y_pred2)
print(f"Tuned RMSE on Test Set for CO2_Emissions/Hour Data: {rmse}")
print(f"Tuned R^2 Score on Test Set  for CO2_Emissions/Hour Data: {r2}")

#PLOTS TO VISUALIZE THE OUTCOME

#scatter plot
plt.figure(figsize=(10,6))
plt.scatter(y_test2, y_pred2, alpha=0.6)
plt.plot([y_test2.min(), y_test2.max()], [y_test2.min(), y_test2.max()], 'r--')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values for CO2_Emissions/Hour Data')
plt.show()

#residuals plot
residuals2 = y_test2 - y_pred2
plt.figure(figsize=(10, 6))
plt.scatter(y_pred2, residuals2, alpha=0.6)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot for CO2_Emissions/Hour Data')
plt.show()

#histogram
plt.figure(figsize=(10, 6))
plt.hist(residuals2, bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Distribution of Residuals for CO2_Emissions/Hour Data')
plt.show()

#EMISSIONS PER FUEL USAGE RATE -- NON BINOMIAL
df_modified3 = df_modified.copy()
df_modified3['CO2_Emitted/Fuel_Usage_Rate'] = df_modified3['CO2_Emitted (US Ton)'] / df_modified3['Fuel_Consumption_Rate (liters/hr)']
df_modified3 = df_modified3.drop(columns=['CO2_Emitted (US Ton)', 'Fuel_Consumption_Rate (liters/hr)']) #, 'Total_Duration'

plt.figure(figsize=(10, 5))
plt.hist(df_modified3['CO2_Emitted/Fuel_Usage_Rate'], bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Transformed CO2_Emitted/Fuel_Usage_Rate')
plt.ylabel('Frequency')
plt.title('Distribution of Transformed CO2_Emitted/Fuel_Usage_Rate')
plt.show()

plt.figure(figsize=(10, 5))
plt.hist(df_modified3['Total_Duration'], bins=30, color='salmon', edgecolor='black')
plt.xlabel('Transformed Total_Duration')
plt.ylabel('Frequency')
plt.title('Distribution of Total_Duration')
plt.show()


#feature selection
df_analyse_features_3 = df_modified3.copy()

X_analyse_features_3 = df_analyse_features_3.drop(columns=['CO2_Emitted/Fuel_Usage_Rate'])
y_analyse_features_3 = df_analyse_features_3['CO2_Emitted/Fuel_Usage_Rate'].values

features3 = X_analyse_features_3.columns

X_train_analyse_features3, X_test_analyse_features3, y_train_analyse_features3, y_test_analyse_features3 = train_test_split(X_analyse_features_3, y_analyse_features_3, test_size=0.2, random_state=42)

rf = RandomForestRegressor(random_state=0)

rf.fit(X_analyse_features_3,y_analyse_features_3)

f_i = list(zip(features3,rf.feature_importances_))
f_i.sort(key = lambda x : x[1])
plt.barh([x[0] for x in f_i],[x[1] for x in f_i])
plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Feature Importances from Random Forest for Dataset with CO2_Emitted/Fuel_Usage_Rate")

plt.show()

#correlation matrix
corr_matrix3 = df_modified3.drop(columns=['Frequent_Route'])
corr_matrix3 = corr_matrix3.corr()
# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix3, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix of Features for CO2_Emissions/Fuel_Usage_Rate Data")
plt.show()

X_df3 = df_modified3.drop(columns=['CO2_Emitted/Fuel_Usage_Rate'])
y3 = df_modified3['CO2_Emitted/Fuel_Usage_Rate'].values
X_train3, X_test3, y_train3, y_test3 = train_test_split(X_df3, y3, test_size=0.2, random_state=42)
tree_model3 = DecisionTreeRegressor(criterion="squared_error", random_state=42)
tree_model3.fit(X_train3, y_train3)

# Generate predictions
y_pred3 = tree_model3.predict(X_test3)

# Calculate and print RMSE and R^2 Score on test data
rmse = np.sqrt(mean_squared_error(y_test3, y_pred3))
r2 = r2_score(y_test3, y_pred3)
print(f"Tuned RMSE on Test Set for CO2_Emissions/Fuel_Usage_Rate Data: {rmse}")
print(f"Tuned R^2 Score on Test Set for CO2_Emissions/Fuel_Usage_Rate Data: {r2}")

#PLOTS TO VISUALIZE THE OUTCOME

#scatter plot
plt.figure(figsize=(10,6))
plt.scatter(y_test3, y_pred3, alpha=0.6)
plt.plot([y_test3.min(), y_test3.max()], [y_test3.min(), y_test3.max()], 'r--')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values for CO2_Emissions/Fuel_Usage_Rate Data')
plt.show()

#residuals plot
residuals3 = y_test3 - y_pred3
plt.figure(figsize=(10, 6))
plt.scatter(y_pred3, residuals3, alpha=0.6)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot for CO2_Emissions/Fuel_Usage_Rate Data')
plt.show()

#histogram
plt.figure(figsize=(10, 6))
plt.hist(residuals3, bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Distribution of Residuals for CO2_Emissions/Fuel_Usage_Rate Data')
plt.show()


#NEURAL NETWORK PORTION:

'''df_neural_network = df.copy()

df_neural_network['Total_Duration'] = df_neural_network['Duration_hours'] + df_neural_network['Duration_min'] / 60
df_neural_network.drop(columns=['Duration_hours', 'Duration_min', 'Dep_hours', 'Dep_min', 'Arrival_hours', 'Arrival_min', 'Day', 'Month', 'Year'], inplace=True)

frequent_routes = set((row['Source'], row['Destination']) for _, row in od_pairs.iterrows())
df_neural_network['Frequent_Route'] = df_neural_network.apply(lambda row: 1 if (row['Source'], row['Destination']) in frequent_routes else 0, axis=1)
df_neural_network.drop(columns=['Source', 'Destination', 'Adjusted_Date'], inplace=True)

df_neural_network = pd.get_dummies(df_neural_network, columns=['Airline', 'Fleet'], drop_first=True)
airline_columns_neural_network = [value for value in df_neural_network.columns if 'Airline_' in value]
fleet_columns_neural_network = [value for value in df_neural_network.columns if 'Fleet_' in value]

print("Airline columns after one-hot encoding:", airline_columns_neural_network)
print("Fleet columns after one-hot encoding:", fleet_columns_neural_network)

print("df_neural_network:")
print(df_neural_network.head()) 

X_neural_network = df_neural_network.drop(columns=['CO2_Emitted (US Ton)'])
y_neural_network = df_neural_network['CO2_Emitted (US Ton)'].values


X_train_neural_network, X_test_neural_network, y_train_neural_network, y_test_neural_network = train_test_split(X_neural_network.to_numpy(), y_neural_network, test_size=0.2, random_state=42)
print(X_neural_network.shape)
print(X_neural_network.columns)
X_train_neural_network = X_train_neural_network.astype(np.float64)

print(X_train_neural_network.dtype)
print(type(X_train_neural_network))
print(type(y_train_neural_network))
print(type(y_train_neural_network.dtype))

scaler_X = StandardScaler()
X_train_neural_network = scaler_X.fit_transform(X_train_neural_network)
X_test_neural_network = scaler_X.transform(X_test_neural_network)

scaler_y = StandardScaler()
y_train_neural_network = scaler_y.fit_transform(y_train_neural_network.reshape(-1, 1)).flatten()
y_test_neural_network = scaler_y.transform(y_test_neural_network.reshape(-1, 1)).flatten()

degree = min(3, X_train_neural_network.shape[1])
initial_beta = np.arange(degree, dtype=np.float64)
padded_beta = np.zeros(X_train_neural_network.shape[1], dtype=np.float64)

padded_beta[:degree] = initial_beta

print(padded_beta)
    
def polymodel(beta, x_values):
    powers = np.arange(len(beta)) 
    model_output = np.sum(beta * (x_values ** powers), axis = 1)
    return model_output


def gradient_of_error(residuals, x_values, beta, lambda_=0.01):
    regularization_term = lambda_ * beta
    gradient = (
        np.mean(residuals[:, None] * (x_values ** np.arange(len(beta))), axis=0)
        + regularization_term
    )
    return gradient

def minimize(model_f, beta_guess, x_values, y_values, niu, number_steps):
    beta = beta_guess
    for _ in range(number_steps):
        residuals = model_f(beta, x_values) - y_values
        gradient = gradient_of_error(residuals, x_values, beta)
        beta -= niu * gradient
    return beta 

def train(f_model, beta_guess, x_values, y_values, niu, number_steps):
    minimized_beta = minimize(f_model, beta_guess, x_values, y_values, niu, number_steps)
    return minimized_beta

#initial_beta = np.arange(X_train_neural_network.shape[1], dtype=np.float64)
learning_rate = 0.001
num_steps = 500

final_beta = train(polymodel, padded_beta, X_train_neural_network, y_train_neural_network, learning_rate, num_steps)



y_pred = polymodel(final_beta, X_test_neural_network)
mse = mean_squared_error(y_test_neural_network, y_pred)
print(f"Mean Squared Error on Test Set: {mse}")'''

#NEURAL NETWORKS WITH PACKAGES
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

df_neural_network = df.copy()

df_neural_network['Total_Duration'] = df_neural_network['Duration_hours'] + df_neural_network['Duration_min'] / 60
df_neural_network.drop(columns=['Duration_hours', 'Duration_min', 'Dep_hours', 'Dep_min', 'Arrival_hours', 'Arrival_min', 'Day', 'Month', 'Year'], inplace=True)

frequent_routes = set((row['Source'], row['Destination']) for _, row in od_pairs.iterrows())
df_neural_network['Frequent_Route'] = df_neural_network.apply(lambda row: 1 if (row['Source'], row['Destination']) in frequent_routes else 0, axis=1)
df_neural_network.drop(columns=['Source', 'Destination', 'Adjusted_Date'], inplace=True)

df_neural_network = pd.get_dummies(df_neural_network, columns=['Airline', 'Fleet'], drop_first=True)
airline_columns_neural_network = [value for value in df_neural_network.columns if 'Airline_' in value]
fleet_columns_neural_network = [value for value in df_neural_network.columns if 'Fleet_' in value]

print("Airline columns after one-hot encoding:", airline_columns_neural_network)
print("Fleet columns after one-hot encoding:", fleet_columns_neural_network)

print("df_neural_network:")
print(df_neural_network.head()) 

X_neural_network = df_neural_network.drop(columns=['CO2_Emitted (US Ton)']).values
y_neural_network = df_neural_network['CO2_Emitted (US Ton)'].values

#Split the data
X_train_neural_network, X_test_neural_network, y_train_neural_network, y_test_neural_network = train_test_split(X_neural_network, y_neural_network, test_size=0.2, random_state=42)

#Normalize the data
X_train_neural_norm = (X_train_neural_network - X_train_neural_network.mean(axis=0)) / X_train_neural_network.std(axis=0)
X_test_norm = (X_test_neural_network - X_train_neural_network.mean(axis=0)) / X_train_neural_network.std(axis=0)


#build layered model
model = Sequential()
model.add(Dense(64, input_dim=X_train_neural_network.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))

#Implement radient descent
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

#Train the model
model.fit(X_train_neural_network, y_train_neural_network, epochs=50, batch_size=32, validation_data=(X_test_neural_network, y_test_neural_network))

#Evaluate the model
loss = model.evaluate(X_test_neural_network, y_test_neural_network)
print(f"Test Loss (MSE): {loss}")