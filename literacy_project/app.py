import streamlit as st
import os
from PIL import Image
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


APP_PATH = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Education Dashboard", layout="wide")
st.write("App folder:", APP_PATH)
st.title("📚 Education Dashboard (SQL + EDA)")

# -------------------------------
# MySQL connection
# -------------------------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",             # MySQL username
            password="rohini",             # MySQL password
            database="Global_literacy", # Your DB name
            port=3306
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"❌ Database connection failed: {e}")
        st.stop()

# -------------------------------
# Sidebar for sections
# -------------------------------
tab1, tab2, tab3=st.tabs([
        "🧮 SQL Queries",
        "📊 EDA Visualizations",
        "🌍 Country Profile"
    ]
)

# ========================================
# Section 1: SQL Queries
# ========================================
with tab1: 
    st.header("🧮 Execute Predefined SQL Queries")

queries = {
    "1. Top 5 Adult Literacy Countries (2020)": """
        SELECT country,
       adult_literacy_rate__population_both_sexes AS adult_literacy
FROM literacy_rates
WHERE year = 2020
  AND adult_literacy_rate__population_both_sexes IS NOT NULL
ORDER BY adult_literacy DESC
LIMIT 5;
    """,
    
    "2. Countries where Female Youth Literacy < 80%": """
        SELECT
    country,
    year,
    youth_literacy_rate__population_15_24_years__female
FROM literacy_rates
WHERE youth_literacy_rate__population_15_24_years__female < 80
  AND youth_literacy_rate__population_15_24_years__female IS NOT NULL
ORDER BY youth_literacy_rate__population_15_24_years__female ASC;
    """,

    "3. Average Adult Literacy per Continent": """
        SELECT
    owid_region,
    ROUND(AVG(adult_literacy_rate__population_both_sexes),  2) AS avg_adult_literacy
FROM literacy_rates
WHERE adult_literacy_rate__population_both_sexes IS NOT NULL
  AND owid_region IS NOT NULL
GROUP BY owid_region
ORDER BY avg_adult_literacy DESC;
    """,

    "4. Countries with Illiteracy % > 20% (2000)": """
        SELECT 
    country,
    illiteracy_percent
FROM illiteracy_population
where year=2000
and illiteracy_percent >20
order by illiteracy_percent DESC;
    """,

    "5. Trend of Illiteracy % for India (2000-2020)": """
        SELECT 
year,
illiteracy_percent
FROM illiteracy_population 
WHERE country='India'
AND year BETWEEN 2000 AND 2020
ORDER by year;
    """,

    "6. Top 10 countries with largest Illiterate population (last year)": """
       SELECT country,
illiteracy_rate
FROM illiteracy_population
WHERE year = (SELECT MAX(year) FROM illiteracy_population)
ORDER BY illiteracy_rate DESC
LIMIT 10;
    """,

    "7. Countries with Avg Years Schooling > 7 & GDP < 5000": """
        select country,
avg_years_schooling,
gdp_per_capita
from gdp_schooling 
where avg_years_schooling >7
and gdp_per_capita <5000
order by avg_years_schooling DESC;
    """,

    "8. Rank countries by GDP per Schooling (2020)": """
        select country,
gdp_per_schooling_year
from gdp_schooling
where year=2020
and gdp_per_schooling_year is not null
order by gdp_per_schooling_year DESC;
    """,

    "9. Global Average Schooling Years per Year": """
        select year,
round(avg(avg_years_schooling), 2) as global_avg_schooling 
from gdp_schooling
where avg_years_schooling is not null
group by year
order by year;
    """,

    "10. list top 10 countries in 2020 with highest GDP per capita but lowest average":
 """
      SELECT
    country,
    gdp_per_capita,
    avg_years_schooling
FROM gdp_schooling
WHERE year = 2020
  AND avg_years_schooling < 6
  AND gdp_per_capita IS NOT NULL
ORDER BY gdp_per_capita DESC
LIMIT 10;
    """,

    "11. show countries where the illiterate population is high despite having more than 5 average year of schooling.": """
        SELECT
    i.country,
    i.year,
    i.illiteracy_rate,
    g.avg_years_schooling
FROM illiteracy_population i
JOIN gdp_schooling g
  ON i.country = g.country
 AND i.`year` = g.`year`
WHERE g.avg_years_schooling > 5
  AND i.illiteracy_rate >= 15
ORDER BY i.illiteracy_rate DESC
LIMIT 10;
    """,

    "12. Compare Literacy Rates & GDP Growth for Zambia (last 20 years)":
"""      
  SELECT
    l.`year`,
    l.adult_literacy_rate__population_both_sexes AS literacy_rate,
    g.gdp_per_capita
FROM literacy_rates l
JOIN gdp_schooling g
  ON l.country = g.country
 AND l.`year` = g.`year`
WHERE l.country = 'Zambia'
  AND l.`year` >= 2010
ORDER BY l.`year`;
    """,

    "13. Youth Literacy Male vs Female Gap (GDP > 30000, 2020)": """
        SELECT
    l.country,
    l.youth_literacy_rate__population_15_24_years__male AS male_literacy,
    l.youth_literacy_rate__population_15_24_years__female AS female_literacy,
    (l.youth_literacy_rate__population_15_24_years__male -
     l.youth_literacy_rate__population_15_24_years__female) AS gender_gap,
    g.gdp_per_capita
FROM literacy_rates l
JOIN gdp_schooling g
  ON l.country = g.country
 AND l.`year` = g.`year`
WHERE l.`year` = 2020
  AND g.gdp_per_capita > 30000
  AND l.youth_literacy_rate__population_15_24_years__male IS NOT NULL
  AND l.youth_literacy_rate__population_15_24_years__female IS NOT NULL
ORDER BY ABS(gender_gap) DESC;
    """
}

# -------------------------------
# Select query
# -------------------------------
query_selected = st.selectbox("Select a Query to Run:", list(queries.keys()))

# -------------------------------
# Run selected query
# -------------------------------
if st.button("▶ Run Query"):
    conn = get_connection()
    cursor = conn.cursor()

    sql_query = queries[query_selected]

    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

        if df.empty:
            st.warning("⚠️ No data found.")
        else:
            st.success(f"✅ Query executed successfully ({len(df)} rows)")
            st.dataframe(df, use_container_width=True)

    except mysql.connector.Error as e:
        st.error(f"❌ Error executing query:\n{e}")
    finally:
        cursor.close()
        conn.close()


# -------------------------------
# Section 2: EDA Visualizations
# -------------------------------
with tab2: 
    st.header("📊 EDA Visualizations (from Jupyter)")

import os
from PIL import Image
import streamlit as st

APP_PATH = os.path.dirname(os.path.abspath(__file__))

plots = [
    ("1️⃣ Literacy Growth Rate Distribution", "Literacy_Growth_Rate_Distribution.png"),
    ("2️⃣ Illiteracy Male vs Female", "Average_Youth_Illiteracy_Male_vs_Female.png"),
    ("3️⃣ Average Youth Literacy Rate by Gender", "Youth_Literacy_Rate.png"),
    ("4️⃣ Literacy Rate by Income Group", "literacy_by_income_group.png"),
    ("5️⃣ Literacy Distribution Across Selected Countries", "Literacy_Distribution_Across_Selected_Countries.png"),
    ("6️⃣ Youth Literacy avg vs Year top 8", "Top_8_Countries_by_Average_Youth_Literacy.png"),
    ("7️⃣ Bottom 5 Countries by Average Youth Literacy", "Bottom_5_Countries_by_Average_Youth_Literacy.png"),
    ("8️⃣ Top 7 Countries with Largest Youth Literacy Gender Gap", "Top_7_Countries_with_Largest_Youth_Literacy_Gender_Gap.png")
]

for title, filename in plots:
        st.subheader(title)
        img_path = os.path.join(APP_PATH, filename)

        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.error(f"❌ File not found: {filename}")



# ============================
# PAGE 3: COUNTRY PROFILE
# ============================

with tab3:
    st.header("🌍 Country Profile")
    st.write("Select a country to view indicators over time")

    conn = get_connection()

    countries = pd.read_sql(
        "SELECT DISTINCT country FROM literacy_rates ORDER BY country",
        conn
    )

    selected_country = st.selectbox(
        "Select Country",
        countries["country"]
    )

    df = pd.read_sql(
        f"""
        SELECT year,
               adult_literacy_rate__population_both_sexes
        FROM literacy_rates
        WHERE country = '{selected_country}'
        ORDER BY year
        """,
        conn
    )

    if df.empty:
        st.warning("No data available.")
    else:
        st.line_chart(df.set_index("year"))

    conn.close()