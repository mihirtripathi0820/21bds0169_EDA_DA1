# -*- coding: utf-8 -*-
"""21BDS0169_EDA_THEORY_DA1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NxVS0jwZCAu_9mnSSSGfJ8gvtOBwI5CK

# BCSE331L Exploratory Data Analysis - Digital Assessment I
# Name: Mihir Tripathi
# Reg. No.: 21BDS0169
"""

#21bds0169
#Mihir Tripathi

"""# Importing necessary libraries"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""# Load the dataset"""

url = "https://raw.githubusercontent.com/salemprakash/EDA/main/Data/PhDPublications.csv"
df = pd.read_csv(url)
df.head()

"""# 1. Data Dimension and Summary"""

print("Shape of the dataset:", df.shape)
print("\nData Types:\n", df.dtypes)
print("\nFirst 5 Rows:\n", df.head())
print("\nSummary Statistics:\n", df.describe())

"""# 2. Data Handling and Cleaning"""

print("\nMissing Values:\n", df.isnull().sum())
df.drop_duplicates(inplace=True)

"""# Handling missing values (if any)"""

df.fillna(df.mean(numeric_only=True), inplace=True)

"""# Reshaping the dataset using Hierarchical Indexing"""

df.set_index(['gender', 'married'], inplace=True)

print("\nDataset with Hierarchical Indexing:")
print(df.head())

grouped = df.groupby(level=[0, 1]).agg({'articles': ['mean', 'sum', 'count']})
print("\nGrouped Statistics (Articles) by Gender and Marital Status:")
print(grouped)

unstacked = grouped.unstack(level=0)
print("\nUnstacked Grouped Data:")
print(unstacked)

plt.figure(figsize=(6,4))
sns.heatmap(unstacked['articles']['mean'], annot=True, cmap='viridis')
plt.title('Average Articles by Gender and Marital Status-21bds0169')
plt.show()

df.reset_index(inplace=True)

"""#Discretization and binning

# 1. Discretization of 'articles' using Equal-Width Binning
"""

df['articles_bins_width'] = pd.cut(df['articles'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
print("\nEqual-Width Binning of 'articles':")
print(df['articles_bins_width'].value_counts())

"""# 2. Discretization of 'mentor' using Equal-Frequency Binning"""

df['mentor_bins_freq'] = pd.qcut(df['mentor'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
print("\nEqual-Frequency Binning of 'mentor':")
print(df['mentor_bins_freq'].value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x='mentor_bins_freq', data=df, palette='viridis')
plt.title('Equal-Frequency Binning of Mentor Score-21bds0169')
plt.show()

"""# 3. Custom Binning for 'prestige'"""

bins = [0, 1.5, 2.5, 3.5, 5]
labels = ['Low', 'Average', 'Good', 'Excellent']
df['prestige_category'] = pd.cut(df['prestige'], bins=bins, labels=labels)

print("\nCustom Binning for 'prestige':")
print(df['prestige_category'].value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x='prestige_category', data=df, palette='cividis')
plt.title('Custom Binning for Prestige Score-21bds0169')
plt.show()

"""# 4. Display Modified Dataset with Bins"""

print("\nDataset with Discretization Columns:")
print(df[['articles', 'articles_bins_width', 'mentor', 'mentor_bins_freq', 'prestige', 'prestige_category']].head())

"""# Outlier detection and filtering

# 1. Outlier Detection using IQR Method
"""

def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers

articles_outliers = detect_outliers_iqr(df, 'articles')
mentor_outliers = detect_outliers_iqr(df, 'mentor')

print(f"\nOutliers in 'articles' column:\n{articles_outliers}")
print(f"\nOutliers in 'mentor' column:\n{mentor_outliers}")

"""# Visualize Outliers using Boxplots"""

plt.figure(figsize=(6,4))
sns.boxplot(x=df['articles'], color='orange')
plt.title('Boxplot of Articles (with Outliers)-21bds0169')
plt.show()

plt.figure(figsize=(6,4))
sns.boxplot(x=df['mentor'], color='green')
plt.title('Boxplot of Mentor Score (with Outliers)-21bds0169')
plt.show()

"""# 2. Filtering Out Outliers"""

def remove_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    return filtered_data

df_clean = remove_outliers_iqr(df, 'articles')
df_clean = remove_outliers_iqr(df_clean, 'mentor')

print("\nShape of Dataset Before Removing Outliers:", df.shape)
print("Shape of Dataset After Removing Outliers:", df_clean.shape)

"""# 3. Visualize After Outlier Removal"""

plt.figure(figsize=(6,4))
sns.boxplot(x=df_clean['articles'], color='cyan')
plt.title('Boxplot of Articles (After Outlier Removal)-21bds0169')
plt.show()

plt.figure(figsize=(6,4))
sns.boxplot(x=df_clean['mentor'], color='purple')
plt.title('Boxplot of Mentor Score (After Outlier Removal)-21bds0169')
plt.show()

"""# 4. Display Cleaned Dataset"""

print("\nCleaned Dataset (Outliers Removed):")
print(df_clean.head())

df_clean.to_csv('PhDPublications_Cleaned.csv', index=False)

"""# 3. Univariate Analysis"""

df.rename(columns={"prestige": "price"}, inplace=True)
roll_number = "21BDS00169"

"""# 1. Distribution Plot - Histogram

# Histogram for Height
"""

plt.figure(figsize=(8,6))
plt.hist(df["mentor"], bins=10, color='blue', edgecolor='black', alpha=0.7)
plt.xlabel("Mentor")
plt.ylabel("Frequency")
plt.title(f"{roll_number} - Height Distribution Histogram")
plt.show()

"""# Histogram for Price"""

plt.figure(figsize=(8,6))
plt.hist(df["price"], bins=10, color='green', edgecolor='black', alpha=0.7)
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.title(f"{roll_number} - Price Distribution Histogram")
plt.show()

"""# 2. Distribution Plot - Density"""

plt.figure(figsize=(8,6))
sns.kdeplot(df["price"], fill=True, color="red")
plt.xlabel("Price")
plt.ylabel("Density")
plt.title(f"{roll_number} - Price Density Plot")
plt.show()

"""# 3. Histogram and Density Combined"""

plt.figure(figsize=(8,6))
sns.histplot(df["price"], bins=10, kde=True, color="purple", edgecolor="black", alpha=0.6)
plt.xlabel("Price")
plt.ylabel("Density")
plt.title(f"{roll_number} - Price Histogram with Density Overlay")
plt.show()

"""# 3. Histogram and Density Combined"""

plt.figure(figsize=(8,6))
sns.histplot(df["price"], bins=10, kde=True, color="purple", edgecolor="black", alpha=0.6)
plt.xlabel("Price")
plt.ylabel("Density")
plt.title(f"{roll_number} - Price Histogram with Density Overlay")
plt.show()

"""# 4. Box Plot"""

plt.figure(figsize=(8,6))
sns.boxplot(y=df["price"], color="orange")
plt.title(f"{roll_number} - Boxplot of Price")
plt.ylabel("Price")
plt.show()

"""# 5. Barplot

# Vertical Bar Plot
"""

plt.figure(figsize=(8,6))
sns.countplot(data=df, x="articles", color="teal")
plt.xlabel("No of Cylinders")
plt.ylabel("Count")
plt.title(f"{roll_number} - Barplot for No. of Cylinders (Vertical)")
plt.show()

"""# Horizontal Bar Plot"""

plt.figure(figsize=(8,6))
sns.countplot(data=df, y="articles", color="teal")
plt.xlabel("Count")
plt.ylabel("No of Cylinders")
plt.title(f"{roll_number} - Barplot for No. of Cylinders (Horizontal)")
plt.show()

"""# 6. Pie Plot"""

df["gender"].value_counts().plot.pie(autopct='%1.1f%%', colors=["blue", "red"], figsize=(8,6))
plt.title(f"{roll_number} - Pie Chart for Drive Wheel")
plt.ylabel("")  # Hide Y label
plt.show()

"""# 7. Dot Plot"""

plt.figure(figsize=(8,6))
sns.stripplot(x=df["price"], jitter=True, color="brown", alpha=0.6)
plt.title(f"{roll_number} - Dot Plot for Price")
plt.xlabel("Price")
plt.show()

"""# 4. Bivariate Analysis

# 1. Categorical vs. Categorical

# Contingency Table
"""

contingency_table = pd.crosstab(df['gender'], df['married'])
print(contingency_table)

"""# 1.1 Stacked Bar Chart"""

contingency_table.plot(kind="bar", stacked=True, figsize=(8,6))
plt.xlabel("Gender")
plt.ylabel("Count")
plt.title("Stacked Bar Chart: Gender vs Married-21BDS0169")
plt.legend(title="Married")
plt.show()

"""# 1.2 Grouped Bar Plot"""

plt.figure(figsize=(8,6))
sns.countplot(data=df, x="gender", hue="married", dodge=True)
plt.title("Grouped Bar Plot: Gender vs Married-21BDS0169")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.show()

"""# 2. Quantitative vs. Quantitative

# 2.1 Scatter Plot
"""

plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x="prestige", y="mentor")
plt.title("Scatter Plot: Prestige vs Mentor-21BDS0169")
plt.xlabel("Prestige")
plt.ylabel("Mentor")
plt.show()

"""# 2.2 Line Plot"""

plt.figure(figsize=(8,6))
sns.lineplot(data=df, x="prestige", y="mentor")
plt.title("Line Plot: Prestige vs Mentor-21BDS0169")
plt.xlabel("Prestige")
plt.ylabel("Mentor")
plt.show()

"""# 3. Categorical vs. Quantitative

# 3.1 Bar Chart
"""

plt.figure(figsize=(8,6))
sns.barplot(data=df, x="gender", y="prestige")
plt.title("Bar Chart: Gender vs Prestige-21BDS0169")
plt.xlabel("Gender")
plt.ylabel("Prestige")
plt.show()

"""# 3.2 Density Plot"""

plt.figure(figsize=(8,6))
sns.kdeplot(data=df, x="prestige", hue="gender", fill=True)
plt.title("Density Plot: Gender vs Prestige-21BDS0169")
plt.xlabel("Prestige")
plt.show()

"""# 3.3 Box Plot"""

plt.figure(figsize=(8,6))
sns.boxplot(data=df, x="gender", y="prestige")
plt.title("Box Plot: Gender vs Prestige-21BDS0169")
plt.xlabel("Gender")
plt.ylabel("Prestige")
plt.show()

"""# 3.4 Violin Plot"""

plt.figure(figsize=(8,6))
sns.violinplot(data=df, x="gender", y="prestige")
plt.title("Violin Plot: Gender vs Prestige-21BDS0169")
plt.xlabel("Gender")
plt.ylabel("Prestige")
plt.show()

"""# 3.5 Combined Violin and Boxplot"""

plt.figure(figsize=(8,6))
sns.violinplot(data=df, x="gender", y="prestige", inner=None, alpha=0.7)
sns.boxplot(data=df, x="gender", y="prestige", width=0.2, boxprops={'zorder': 2})
plt.title("Combined Violin and Box Plot-21BDS0169")
plt.xlabel("Gender")
plt.ylabel("Prestige")
plt.show()

"""# 4. Multivariate Analysis

# 4.1 Scatter Plot (Color as 3rd Variable)
"""

plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x="prestige", y="mentor", hue="gender")
plt.title("Scatter Plot with Gender as Color-21BDS0169")
plt.xlabel("Prestige")
plt.ylabel("Mentor")
plt.show()

"""# 4.2 Scatter Plot (Color as 3rd, Shape as 4th Variable)"""

plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x="prestige", y="mentor", hue="gender", style="married")
plt.title("Scatter Plot with Gender (Color) and Married (Shape)-21BDS0169")
plt.xlabel("Prestige")
plt.ylabel("Mentor")
plt.show()

"""# 4.3 Scatter Plot (Color as 3rd, Size as 4th Variable)"""

plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x="prestige", y="mentor", hue="gender", size="articles")
plt.title("Scatter Plot with Gender (Color) and Articles (Size)-21BDS0169")
plt.xlabel("Prestige")
plt.ylabel("Mentor")
plt.show()

"""# 4.4 Bubble Plot"""

plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x="prestige", y="mentor", hue="gender", size="articles", alpha=0.6)
plt.title("Bubble Plot: Prestige vs Mentor with Gender and Articles-21BDS0169")
plt.xlabel("Prestige")
plt.ylabel("Mentor")
plt.show()

"""# 4.5 Facet Grid (Histogram)"""

g = sns.FacetGrid(df, col="gender")
g.map(plt.hist, "prestige-21BDS0169", bins=10, color="blue")
plt.show()

"""# 4.6 Facet Grid (Grid)"""

g = sns.FacetGrid(df, row="gender", col="married")
g.map(plt.hist, "prestige-21BDS0169", bins=10, color="green")
plt.show()

plt.figure(figsize=(8,6))
sns.pairplot(df, hue='gender', diag_kind='kde', palette='husl')
plt.suptitle('Pairplot of Dataset Attributes', y=1.02)
plt.show()

from sklearn.preprocessing import LabelEncoder
label_enc = LabelEncoder()
for column in ['gender', 'married']:
    df[column] = label_enc.fit_transform(df[column])
numeric_df = df.select_dtypes(include=[np.number])
plt.figure(figsize=(7,5))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()

"""# FUNDAMENTALS OF TIME SERIES ANALYSIS (TSA)

# Importing necessary libraries
"""

import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller

"""# Time-Based Indexing"""

df['rownames'] = pd.to_datetime(df['rownames'], format='%Y', errors='coerce')
df.set_index('rownames', inplace=True)
print("\nFirst 5 Rows of Time Series Data:")
print(df.head())

"""# 4. Checking Stationarity (ADF Test)"""

def adf_test(series):
    result = adfuller(series.dropna())
    labels = ['ADF Statistic', 'p-value', '#Lags Used', 'Number of Observations Used']
    for value, label in zip(result, labels):
        print(f"{label}: {value}")
    if result[1] <= 0.05:
        print("\nThe series is stationary.")
    else:
        print("\nThe series is not stationary. Differencing may be required.")

print("\nADF Test for 'articles':")
adf_test(df['articles'])

"""# 5. TSA with Open Power System Data (Example)

# Load Open Power System Data (for comparison and practice)
"""

opsd_url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
opsd = pd.read_csv(opsd_url, parse_dates=['Date'], index_col='Date')

"""# Quick plot of power system data"""

plt.figure(figsize=(8,4))
plt.plot(opsd['Consumption'], label='Power Consumption', color='purple')
plt.title('Daily Power Consumption in Germany')
plt.xlabel('Date')
plt.ylabel('Consumption (GWh)')
plt.grid(True)
plt.legend()
plt.show()

"""# 5. Optional: Reset Index if Needed"""

df_reset = df.reset_index()
print("\nDataFrame with 'rownames' Restored as Column:")
print(df_reset.head())

"""# 8. Autocorrelation and Partial Autocorrelation"""

plt.figure(figsize=(12,5))
plt.subplot(121)
plot_acf(df['articles'].dropna(), lags=20, ax=plt.gca(), title='Autocorrelation')
plt.subplot(122)
plot_pacf(df['articles'].dropna(), lags=20, ax=plt.gca(), title='Partial Autocorrelation')
plt.show()

"""#1D Statistical Data analysis

# Import necessary libraries
"""

from scipy.stats import skew, kurtosis

"""# 1. Measures of Central Tendency

# Mean Variations
"""

mean_arithmetic = df["price"].mean()
mean_weighted = np.average(df["price"], weights=df["articles"])  # Weighted Mean
mean_trimmed = df["price"].sort_values().iloc[int(0.05*len(df)): int(0.95*len(df))].mean()  # Trimmed Mean

print(f"Arithmetic Mean: {mean_arithmetic}")
print(f"Weighted Mean: {mean_weighted}")
print(f"Trimmed Mean (5% trim): {mean_trimmed}")

"""# Median Variations"""

median = df["price"].median()
quantiles = df["price"].quantile([0.25, 0.5, 0.75])  # Quartiles
deciles = df["price"].quantile([i/10 for i in range(1, 10)])  # Deciles
percentiles = df["price"].quantile([i/100 for i in range(1, 100)])  # Percentiles

print(f"Median: {median}")
print(f"Quantiles:\n{quantiles}")
print(f"Deciles:\n{deciles}")
print(f"Percentiles (First 10 shown):\n{percentiles.head(10)}")

"""# 2. Measures of Dispersion"""

range_value = df["price"].max() - df["price"].min()
iqr = df["price"].quantile(0.75) - df["price"].quantile(0.25)  # Interquartile Range
interdecile_range = df["price"].quantile(0.9) - df["price"].quantile(0.1)  # Interdecile Range
std_dev = df["price"].std()
variance = df["price"].var()
skewness = skew(df["price"])
kurt = kurtosis(df["price"])

print(f"Range: {range_value}")
print(f"IQR: {iqr}")
print(f"Interdecile Range: {interdecile_range}")
print(f"Standard Deviation: {std_dev}")
print(f"Variance: {variance}")
print(f"Skewness: {skewness}")
print(f"Kurtosis: {kurt}")

"""# 3. Frequency Distribution & Plots

# Frequency Distribution
"""

freq_dist = pd.cut(df["price"], bins=10).value_counts()
print("Frequency Distribution:\n", freq_dist)

"""# Histogram"""

plt.figure(figsize=(8,5))
sns.histplot(df["price"], bins=10, kde=True, color="blue", edgecolor="black")
plt.title("Histogram of Price-21bds0169")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()

"""# Relative Frequency Distribution"""

rel_freq = freq_dist / freq_dist.sum()
print("Relative Frequency Distribution:\n", rel_freq)

"""# Cumulative Frequency Distribution"""

cum_freq = freq_dist.cumsum()
print("Cumulative Frequency Distribution:\n", cum_freq)

"""# 4. Categorical Variable Analysis

# Pie Chart for Gender
"""

df["gender"].value_counts().plot.pie(autopct='%1.1f%%', colors=["blue", "red"], figsize=(7,7))
plt.title("Pie Chart for Gender")
plt.ylabel("")
plt.show()

"""# Stacked Bar Plot for Gender and Married Status"""

df_ct = pd.crosstab(df["gender"], df["married"])
df_ct.plot(kind="bar", stacked=True, colormap="coolwarm", figsize=(8,5))
plt.title("Stacked Bar Chart: Gender vs Married")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.legend(title="Married")
plt.show()

"""#2D Analysis"""

import plotly.express as px
import statsmodels.api as sm
from scipy.stats import chi2_contingency
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

"""# 1. Create a 2-Way Contingency Table (Categorical vs Categorical)"""

cat_cat_table = pd.crosstab(df["gender"], df["married"])
print("Categorical-Categorical Contingency Table:\n", cat_cat_table)

"""
# 2. Create a 2-Way Contingency Table (Categorical vs Numerical)"""

cat_num_table = df.groupby("gender")["articles"].mean()
print("\nCategorical-Numerical Contingency Table:\n", cat_num_table)

"""# 3. Create a 3-Way Contingency Table"""

three_way_table = pd.crosstab(index=df["gender"], columns=[df["married"], df["kids"]])
print("\n3-Way Contingency Table:\n", three_way_table)

"""# 4. Apply Row Profile, Column Profile, Relative Frequency, Chi-Square Test

# Row Profile (Normalize by Row)
"""

row_profile = cat_cat_table.div(cat_cat_table.sum(axis=1), axis=0)
print("\nRow Profile Dataset:\n", row_profile)

"""# Column Profile (Normalize by Column)"""

col_profile = cat_cat_table.div(cat_cat_table.sum(axis=0), axis=1)
print("\nColumn Profile Dataset:\n", col_profile)

"""# Relative Frequency Dataset"""

relative_freq = cat_cat_table / cat_cat_table.sum().sum()
print("\nRelative Frequency Dataset:\n", relative_freq)

"""# Chi-Square Test"""

chi2_stat, p_val, dof, expected = chi2_contingency(cat_cat_table)
print("\nChi-Square Test Results:\n", f"Chi2 Stat: {chi2_stat}, p-value: {p_val}")

"""# 2D Box Plot (Categorical vs Numerical)"""

plt.figure(figsize=(8,5))
sns.boxplot(data=df, x="gender", y="articles", palette="coolwarm")
plt.title("Box Plot: Gender vs Articles")
plt.show()

"""#Hierachical Clustering"""

from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram

"""# Selecting numerical features for clustering"""

df_numeric = df.select_dtypes(include=[np.number])

"""# Function to compute distance matrix and display dendrogram"""

def hierarchical_clustering(distance_metric, method='ward'):
    print(f"\nComputing {distance_metric} Distance Matrix...\n")

    # Compute Distance Matrix
    distance_matrix = pdist(df_numeric, metric=distance_metric)
    distance_df = pd.DataFrame(squareform(distance_matrix),
                               index=df_numeric.index,
                               columns=df_numeric.index)

    print("Distance Matrix:")
    print(distance_df)

    # Compute Hierarchical Clustering
    linkage_matrix = linkage(distance_matrix, method=method)

    # Plot Dendrogram
    plt.figure(figsize=(10, 5))
    dendrogram(linkage_matrix, labels=df_numeric.index, leaf_rotation=90)
    plt.title(f"Dendrogram using {distance_metric} distance & {method} method-21bds0169")
    plt.xlabel("Data Points")
    plt.ylabel("Distance")
    plt.show()

"""# 1. Euclidean Distance"""

hierarchical_clustering('euclidean')

"""# 2. Manhattan Distance"""

hierarchical_clustering('cityblock')

"""# 3. Maximum Distance (Chebyshev)"""

hierarchical_clustering('chebyshev')

"""# 4. Canberra Distance"""

hierarchical_clustering('canberra')

"""# 5. Binary Distance"""

hierarchical_clustering('hamming')

"""# 6. Minkowski Distance (p=3)"""

hierarchical_clustering('minkowski')

"""#K-mean and dbscan clustering"""

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
import plotly.express as px

df_numeric = df.select_dtypes(include=[np.number])

"""# 1. Scale the Numerical Columns"""

scaler = StandardScaler()
data_scaled = scaler.fit_transform(df_numeric)
print("\nScaled Data:\n", pd.DataFrame(data_scaled, columns=df_numeric.columns).head())

"""# 2. Using the Elbow Method to find Optimal Clusters"""

wcss = []  # Within Cluster Sum of Squares
K = range(1, 11)  # Checking 1 to 10 clusters

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=123, n_init=10)
    kmeans.fit(data_scaled)
    wcss.append(kmeans.inertia_)

"""# Plot the Elbow Curve"""

plt.figure(figsize=(8, 5))
plt.plot(K, wcss, marker='o', linestyle='-', color='b')
plt.title("Elbow Method for Optimal Clusters-21bds0169")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS (Within-Cluster Sum of Squares)")
plt.show()

"""# 3. Applying K-Means Clustering with k=5"""

kmeans_result = KMeans(n_clusters=5, random_state=123, n_init=10)
df["KMeans_Cluster"] = kmeans_result.fit_predict(data_scaled)

"""# Plot K-Means Clusters"""

plt.figure(figsize=(8, 5))
sns.scatterplot(x=df_numeric.iloc[:, 0], y=df_numeric.iloc[:, 1], hue=df["KMeans_Cluster"], palette="viridis")
plt.title("K-Means Clustering-21bds0169")
plt.xlabel(df_numeric.columns[0])
plt.ylabel(df_numeric.columns[1])
plt.legend(title="Cluster")
plt.show()

"""# 4. Apply DBSCAN Clustering (epsilon=0.5, min_samples=5)"""

dbscan = DBSCAN(eps=0.5, min_samples=5)
df["DBSCAN_Cluster"] = dbscan.fit_predict(data_scaled)

"""
# Visualizing DBSCAN Results"""

plt.figure(figsize=(8, 5))
sns.scatterplot(x=df_numeric.iloc[:, 0], y=df_numeric.iloc[:, 1], hue=df["DBSCAN_Cluster"], palette="coolwarm")
plt.title("DBSCAN Clustering")
plt.xlabel(df_numeric.columns[0])
plt.ylabel(df_numeric.columns[1])
plt.legend(title="Cluster")
plt.show()

"""#Principal Component Analysis"""

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

"""# Selecting only numerical columns for PCA"""

df_numeric = df.select_dtypes(include=[np.number])

"""# 1. Standardizing the Data"""

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_numeric)

"""# 2. Performing PCA"""

pca = PCA()
pca_result = pca.fit(df_scaled)

"""# 3. Print PCA Results (Eigenvalues and Component Loadings)"""

print("\nExplained Variance (Eigenvalues):")
print(pca.explained_variance_ratio_)
print("\nPrincipal Component Loadings:")
loadings = pd.DataFrame(pca.components_, columns=df_numeric.columns)
print(loadings)

"""# 4. Scree Plot (Determine Optimal Components)"""

plt.figure(figsize=(8, 5))
plt.plot(range(1, len(pca.explained_variance_ratio_) + 1),
         np.cumsum(pca.explained_variance_ratio_), marker='o', linestyle='-', color='b')
plt.title("Scree Plot (Cumulative Variance Explained)-21bds0169")
plt.xlabel("Number of Principal Components")
plt.ylabel("Cumulative Explained Variance")
plt.grid(True)
plt.show()

"""# 5. Selecting Optimal Number of Components (n_comp)"""

n_comp = 2  # Select based on scree plot

pca_optimal = PCA(n_components=n_comp)
df_pca = pca_optimal.fit_transform(df_scaled)

"""# 6. Visualizing PCA Components (Biplot)"""

plt.figure(figsize=(8, 5))
plt.scatter(df_pca[:, 0], df_pca[:, 1], alpha=0.7, edgecolors='k', cmap='viridis')
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA Biplot-21bds0169")
plt.grid(True)
plt.show()

"""# 7. Interpreting Results"""

print("\nSummary of PCA:")
print(pd.DataFrame({
    "Component": range(1, n_comp + 1),
    "Explained Variance": pca_optimal.explained_variance_ratio_,
    "Cumulative Variance": np.cumsum(pca_optimal.explained_variance_ratio_)
}))

"""#simple linear regression"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

"""# 1. Identify Feature Relationships using Pairplot"""

df = pd.read_csv(url)
sns.pairplot(df)
plt.show()

"""# 2. Assign Independent (X) & Dependent (Y) Variable"""

X = df[['prestige']]  # Independent Feature
Y = df['articles']     # Dependent Feature

"""# 3. Splitting Dataset (Training: 2/3, Test: 1/3)"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=1/3, random_state=123)

"""# 4. Fitting Simple Linear Regression Model"""

reg1 = LinearRegression()
reg1.fit(X_train, Y_train)

"""# 5. Checking Residual Errors (Model Summary)"""

X_train_sm = sm.add_constant(X_train)  # Add intercept for statsmodels
reg1_sm = sm.OLS(Y_train, X_train_sm).fit()
print("\nSimple Linear Regression Summary:\n", reg1_sm.summary())

"""# 6. Predicting Test Set Results"""

y_pred = reg1.predict(X_test)

"""# 7. Visualizing Test Set Results"""

plt.scatter(X_test, Y_test, color='blue', label="Actual Data")
plt.plot(X_test, y_pred, color='red', linewidth=2, label="Regression Line")
plt.xlabel("Prestige")
plt.ylabel("Articles Published")
plt.title("Simple Linear Regression-21bds0169")
plt.legend()
plt.show()