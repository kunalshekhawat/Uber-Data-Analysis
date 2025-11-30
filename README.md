Uber Data Analysis 🚕
A web application built with Streamlit showing Exploratory Data Analysis (EDA) on a Uber rides dataset for the National Capital Region (NCR). This dashboard provides insights into booking patterns, revenue, vehicle performance, and customer behavior.

📊 Dashboard Preview
![Untitled video - Made with Clipchamp](https://github.com/user-attachments/assets/d556e7b4-ec7d-43a9-b021-da96f94766ea)


✨ Key Features
This dashboard visualizes various aspects of the rides data, including:

Overall Business KPIs: A high-level summary of total bookings, successful trips, cancellations, and the overall cancellation rate.

Monthly Ride Volume: A time-series line graph with a gradient fill showing the trend of ride volume over the year.

Vehicle Popularity: A bar chart comparing the total number of bookings for each vehicle type (e.g., Auto, Go Mini, eBike).

Booking Status Breakdown: A pie chart illustrating the proportion of completed, cancelled, and incomplete rides.

Revenue Analysis: A vertical bar chart displaying the total revenue generated from different payment methods like UPI, Cash, and Debit Card.

Cancellation Patterns: Two separate pie charts detailing the most common reasons for cancellations by both customers and drivers.

Styled Summary Tables: Professional, report-ready tables for:

Average Customer and Driver Ratings by Vehicle Type.

Booking Funnel (Total, Success, Cancelled) by Vehicle Type.

Detailed Financial and Distance Performance by Vehicle Type.

🛠️ Technologies Used
Python: Core programming language.

Streamlit: For building the interactive web application.

Pandas: For data manipulation, cleaning, and aggregation.

Matplotlib & Seaborn: For creating the data visualizations.

⚙️ Setup and Local Installation
To run this project on your local machine, follow these steps:

1. Clone the repository:

git clone [https://github.com/kunalshekhawat/Uber-Data-Analysis.git]
cd Uber-Data-Analysis


2. Create and activate a virtual environment (recommended):

Windows:

python -m venv venv
.\venv\Scripts\activate

macOS / Linux:

python3 -m venv venv
source venv/bin/activate

3. Install the required dependencies:

pip install -r requirements.txt

4. Run the Streamlit app:

streamlit run dashboard.py

The application should now be running in your web browser!

📁 Project Structure
.
├── dashboard.py            # The main Streamlit application script
├── ncr_ride_bookings.csv     # The dataset used for the analysis
├── requirements.txt        # Python dependencies for the project
└── README.md               # You are here!
