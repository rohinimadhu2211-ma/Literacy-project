📚 Global Literacy & Socio-Economic Analysis Project
📌 Project Overview
This project analyzes global literacy trends and their relationship with economic and education indicators such as GDP per capita and average years of schooling.
Using real-world datasets from Our World in Data (OWID), the project applies data cleaning, feature engineering, exploratory data analysis (EDA), SQL analysis, and visualization to uncover meaningful insights.
The project is designed as an end-to-end data analytics solution, suitable for policy analysis, academic research, and business intelligence applications.
🎯 Objectives
Analyze adult and youth literacy trends over time
Study gender gaps in literacy
Understand the relationship between literacy, GDP, and education
Identify regional and country-level disparities
Build interactive dashboards and applications for insights delivery
🧰 Tools & Technologies Used
🐍 Python Ecosystem
Python 3.x
Pandas
NumPy
Matplotlib
Seaborn
📓 Jupyter Notebook
Used for:
Data loading
Data cleaning
Feature engineering
Exploratory Data Analysis (EDA)
Visualization
All analysis and charts were first developed and tested in Jupyter Notebook.
🗄️ SQL (Database)
SQL used to store cleaned data and run analytical queries
Tables created:
literacy_rates
illiteracy_population
gdp_schooling
Used for:
Aggregations
Filtering by year/country
Joining literacy, GDP, and schooling data
🌐 Streamlit (Web App)
Built a multi-page interactive dashboard
Pages include:
SQL Query Executor
EDA Visualizations
Country Profile Page
🔄 Project Workflow
1️⃣ Data Collection 📥
Datasets downloaded from Our World in Data
Data collection performed in Google Colab
CSV files imported into Jupyter Notebook for processing
2️⃣ Data Analysis in Jupyter Notebook 📓
Loaded datasets using Pandas
Cleaned missing and inconsistent values
Created derived features
Performed EDA using charts and plots
Generated insights and saved visual outputs
3️⃣ Data Storage Using SQL 🗄️
Cleaned datasets inserted into SQL tables
Composite key used: (country, year)
SQL queries used for:
Ranking countries
Identifying literacy gaps
Trend analysis
4️⃣ Visualization & App Development 🌐
Streamlit used to build an interactive web app
Data visualizations reused from analysis
Users can:
Select countries
View trends over time
Run SQL-based insights dynamically
📊 Key Insights Generated
Literacy rates generally improve with higher schooling years
Gender literacy gap is narrowing in many regions
Some countries show high literacy despite low GDP
Economic growth alone does not guarantee literacy improvement
🚀 Learning Outcomes
Hands-on experience with real-world datasets
Practical SQL analytics on socio-economic data
Dashboard development using Streamlit
End-to-end data analytics project workflow
🏷️ Technical Tags
Python, Jupyter Notebook, SQL, Streamlit, Pandas, NumPy, Matplotlib, Seaborn, Data Cleaning, EDA, Data Visualization, Education Analytics, Socio-Economic Analysis
