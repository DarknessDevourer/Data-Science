🌾 Time Series Visualization Dashboard
This project is an interactive Streamlit application for visualizing agricultural indices (VCI, TCI, VHI) by region, week, and year. The dashboard allows you to explore trends over time, filter specific time ranges, and compare different regions.

🛠 Features
📊 Select index: VCI, TCI, or VHI

🌍 Choose region

📅 Filter by week and year

↕️ Sort index values (ascending or descending)

🔄 Reset all filters with one click

🧾 View data in table format

📈 Time series chart for selected region

📉 Comparison chart across all regions

📦 Dependencies
Streamlit

Pandas

Seaborn

Matplotlib

Install them with:

bash
Copy
Edit
pip install streamlit pandas seaborn matplotlib
🚀 How to Run
Make sure you have a df.csv file with the necessary columns: Area, Week, Year, VCI, TCI, VHI.

Update the file path in the load_data() function if needed:

python
Copy
Edit
df = pd.read_csv("path_to_your_csv/df.csv")
Run the app:

bash
Copy
Edit
streamlit run app.py
🧪 Expected CSV Format
Your df.csv file should include the following columns:

Area — name of the region

Year — year

Week — week number

VCI, TCI, VHI — numeric index values

Example:

Area	Year	Week	VCI	TCI	VHI
Region A	2022	12	34.5	45.2	39.1
Region B	2022	12	48.9	41.0	45.0
📌 Notes
The app uses st.session_state to preserve selected filters across interactions.

Data is cached using @st.cache_data for performance optimization.

Charts are generated with Seaborn and Matplotlib.

The layout is responsive and divided into a filter panel and a main output panel with tabs.
