import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Uber Analysis Dashboard",
    page_icon="🚕",
    layout="wide"
)

# --- 2. DATA LOADING & CACHING ---
@st.cache_data
def load_data(file_path):
    """
    Loads data from a CSV and performs initial cleaning.
    Using st.cache_data ensures the data is loaded only once.
    """
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    # Clean up potential extra quotes from column names
    df.columns = df.columns.str.strip().str.replace('"', '')
    # Clean up data in object columns
    for col in df.select_dtypes(['object']).columns:
        df[col] = df[col].str.strip().str.replace('"', '')
    return df

df = load_data("ncr_ride_bookings.csv")

# --- 3. MAIN DASHBOARD ---
# st.title("Uber Data  Analytics")
st.markdown("<h1 style='text-align: center;'>Uber Data  Analysis</h1>", unsafe_allow_html=True)


# --- 4. TOP-LEVEL KPI METRICS & SUMMARY TABLE ---
st.header("Overall Business Summary")

# --- KPI Cards ---
total_bookings = len(df)
success_bookings = len(df[df['Booking Status'] == 'Completed'])
cancelled_bookings = len(df[(df['Cancelled Rides by Customer'] == 1) | (df['Cancelled Rides by Driver'] == 1)])
cancellation_rate = (cancelled_bookings / total_bookings) * 100 if total_bookings > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bookings", f"{total_bookings:,}")
col2.metric("Successful Bookings", f"{success_bookings:,}")
col3.metric("Cancelled Bookings", f"{cancelled_bookings:,}")
col4.metric("Cancellation Rate", f"{cancellation_rate:.1f}%")

st.markdown("---")

# --- 5. RIDE VOLUME AND POPULARITY ---
st.header("Ride Volume and Popularity of Vehicles")
col1, col2 = st.columns(2)

with col1:
    # --- Monthly Ride Volume Line Graph ---
    df['Month'] = df['Date'].dt.month_name()
    monthly_rides = df['Month'].value_counts()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    monthly_rides = monthly_rides.reindex(month_order).dropna()

    plt.style.use('default')
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=monthly_rides.index, y=monthly_rides.values, linestyle='-', linewidth=2.5, color='grey', ax=ax1)
    ax1.fill_between(monthly_rides.index, monthly_rides.values, 11000, color='grey', alpha=0.3)
    # ax1.set_title('Ride Volume Over Time', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Number of Rides')
    ax1.set_xlabel(None)
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_ylim(11800, 13000)
    sns.despine()
    st.pyplot(fig1)

with col2:
    # --- Vehicle Type Popularity Bar Chart ---
    vehicle_counts = df['Vehicle Type'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=vehicle_counts.index, y=vehicle_counts.values, palette='viridis', ax=ax2)
    # ax2.set_title('Popularity of Vehicle Types', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Vehicle Type')
    ax2.set_ylabel('Number of Bookings')
    for index, value in enumerate(vehicle_counts.values):
        ax2.text(index, value + 50, str(value), color='black', ha='center')
    sns.despine()
    st.pyplot(fig2)


st.markdown("---")

# --- 6. BOOKING STATUS & REVENUE ---
st.header("Booking Status & Revenue by method")
col1, col2 = st.columns(2)

with col1:
    # --- Booking Status Pie Chart ---
    booking_status_counts = df['Booking Status'].value_counts()
    fig3, ax3 = plt.subplots(figsize=(10, 7))
    wedges, _, _ = ax3.pie(booking_status_counts, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'), textprops=dict(color="w"))
    ax3.legend(wedges, booking_status_counts.index, title="Booking Status", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))
    # ax3.set_title('Booking Status Breakdown', fontsize=16, fontweight='bold')
    st.pyplot(fig3)

with col2:
    # --- Revenue by Payment Method Bar Chart ---
    revenue_df = df.dropna(subset=['Booking Value', 'Payment Method'])
    revenue_by_payment = revenue_df.groupby('Payment Method')['Booking Value'].sum().sort_values(ascending=False)
    fig4, ax4 = plt.subplots(figsize=(10, 7))
    revenue_by_payment.plot(kind='bar', color=sns.color_palette("viridis", len(revenue_by_payment)), width=0.8, ax=ax4)
    ax4.set_xlabel('Payment Method')
    ax4.set_ylabel('Total Revenue (in INR)')
    ax4.tick_params(axis='x', rotation=0)
    for i, value in enumerate(revenue_by_payment):
        ax4.text(i, value + 50000, f'₹{int(value):,}', ha='center')
    sns.despine()
    st.pyplot(fig4)


st.markdown("---")

# --- 7. CANCELLATION ANALYSIS ---
st.header("Cancellation Analysis")
col1, col2 = st.columns(2)

with col1:
    # --- Customer Cancellation Reasons Pie Chart ---
    customer_cancellations_df = df[df['Cancelled Rides by Customer'] == 1].dropna(subset=['Reason for cancelling by Customer'])
    customer_reason_counts = customer_cancellations_df['Reason for cancelling by Customer'].value_counts()
    if not customer_reason_counts.empty:
        fig5, ax5 = plt.subplots(figsize=(10, 7))
        wedges, _, _ = ax5.pie(customer_reason_counts, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'), pctdistance=0.8, wedgeprops={'linewidth': 0})
        ax5.legend(wedges, customer_reason_counts.index, title="Customer Reasons", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))
        ax5.set_title('Cancellation Reasons: By Customer', fontsize=16, fontweight='bold')
        st.pyplot(fig5)
    else:
        st.write("No customer cancellation data to display.")

with col2:
    # --- Driver Cancellation Reasons Pie Chart ---
    driver_cancellations_df = df[df['Cancelled Rides by Driver'] == 1].dropna(subset=['Driver Cancellation Reason'])
    driver_reason_counts = driver_cancellations_df['Driver Cancellation Reason'].value_counts()
    if not driver_reason_counts.empty:
        fig6, ax6 = plt.subplots(figsize=(10, 7))
        wedges, _, _ = ax6.pie(driver_reason_counts, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'), pctdistance=0.8, wedgeprops={'linewidth': 0})
        ax6.legend(wedges, driver_reason_counts.index, title="Driver Reasons", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))
        ax6.set_title('Cancellation Reasons: By Driver', fontsize=16, fontweight='bold')
        st.pyplot(fig6)
    else:
        st.write("No driver cancellation data to display.")


st.markdown("---")

# --- 8. RATINGS ANALYSIS ---
st.header("Ratings Analysis by Vehicle Type")
col1, col2 = st.columns(2)

with col1:
    # --- Average Customer Ratings Table ---
    ratings_df = df[df['Booking Status'] == 'Completed'].dropna(subset=['Customer Rating', 'Vehicle Type'])
    ratings_df['Customer Rating'] = pd.to_numeric(ratings_df['Customer Rating'], errors='coerce')
    ratings_df.dropna(subset=['Customer Rating'], inplace=True)
    average_ratings_table = ratings_df.groupby('Vehicle Type')['Customer Rating'].mean().reset_index()
    average_ratings_table.rename(columns={'Customer Rating': 'Average Rating (1-5)'}, inplace=True)
    average_ratings_table = average_ratings_table.sort_values(by='Average Rating (1-5)', ascending=False)
    average_ratings_table['Average Rating (1-5)'] = average_ratings_table['Average Rating (1-5)'].round(2)
    average_ratings_table.reset_index(drop=True, inplace=True)

    fig7, ax7 = plt.subplots(figsize=(6, 3))
    ax7.axis('tight'); ax7.axis('off')
    the_table = ax7.table(cellText=average_ratings_table.values, colLabels=average_ratings_table.columns, loc='center', cellLoc='center')
    the_table.set_fontsize(12); the_table.scale(1.2, 1.2)
    for (row, col), cell in the_table.get_celld().items():
        cell.set_edgecolor('grey')
        if row == 0:
            cell.set_text_props(weight='bold', color='white'); cell.set_facecolor('#40466e')
        else:
            cell.set_facecolor('#f2f2f2' if row % 2 == 0 else '#ffffff')
    ax7.set_title('Average Customer Ratings', fontsize=16, fontweight='bold', pad=20)
    st.pyplot(fig7)

with col2:
    # --- Average Driver Ratings Table ---
    driver_ratings_df = df[df['Booking Status'] == 'Completed'].dropna(subset=['Driver Ratings', 'Vehicle Type'])
    driver_ratings_df['Driver Ratings'] = pd.to_numeric(driver_ratings_df['Driver Ratings'], errors='coerce')
    driver_ratings_df.dropna(subset=['Driver Ratings'], inplace=True)
    average_driver_ratings_table = driver_ratings_df.groupby('Vehicle Type')['Driver Ratings'].mean().reset_index()
    average_driver_ratings_table.rename(columns={'Driver Ratings': 'Average Driver Rating (1-5)'}, inplace=True)
    average_driver_ratings_table = average_driver_ratings_table.sort_values(by='Average Driver Rating (1-5)', ascending=False)
    average_driver_ratings_table['Average Driver Rating (1-5)'] = average_driver_ratings_table['Average Driver Rating (1-5)'].round(2)
    average_driver_ratings_table.reset_index(drop=True, inplace=True)

    fig8, ax8 = plt.subplots(figsize=(6, 3))
    ax8.axis('tight'); ax8.axis('off')
    the_table2 = ax8.table(cellText=average_driver_ratings_table.values, colLabels=average_driver_ratings_table.columns, loc='center', cellLoc='center')
    the_table2.set_fontsize(12); the_table2.scale(1.2, 1.2)
    for (row, col), cell in the_table2.get_celld().items():
        cell.set_edgecolor('grey')
        if row == 0:
            cell.set_text_props(weight='bold', color='white'); cell.set_facecolor('#40466e')
        else:
            cell.set_facecolor('#f2f2f2' if row % 2 == 0 else '#ffffff')
    ax8.set_title('Average Driver Ratings', fontsize=16, fontweight='bold', pad=20)
    st.pyplot(fig8)

st.markdown("---")

# --- 9. DETAILED PERFORMANCE SUMMARY TABLES (BY VEHICLE) ---
st.header("Detailed Performance Summaries by Vehicle")

# --- Bookings Summary by Vehicle Type Table ---
st.subheader("Bookings Summary")
total_bookings_veh = df.groupby('Vehicle Type').size().reset_index(name='Total Bookings')
success_bookings_veh = df[df['Booking Status'] == 'Completed'].groupby('Vehicle Type').size().reset_index(name='Success Bookings')
cancelled_rides_df = df[(df['Cancelled Rides by Customer'] == 1) | (df['Cancelled Rides by Driver'] == 1)]
cancelled_bookings_veh = cancelled_rides_df.groupby('Vehicle Type').size().reset_index(name='Cancelled Bookings')
summary_table_veh = pd.merge(total_bookings_veh, success_bookings_veh, on='Vehicle Type', how='left')
summary_table_veh = pd.merge(summary_table_veh, cancelled_bookings_veh, on='Vehicle Type', how='left').fillna(0)
summary_table_veh['Cancellation Rate (%)'] = ((summary_table_veh['Cancelled Bookings'] / summary_table_veh['Total Bookings']) * 100).fillna(0)
summary_table_veh = summary_table_veh.sort_values(by='Total Bookings', ascending=False)
summary_table_veh['Total Bookings'] = summary_table_veh['Total Bookings'].map('{:,.0f}'.format)
summary_table_veh['Success Bookings'] = summary_table_veh['Success Bookings'].astype(int).map('{:,.0f}'.format)
summary_table_veh['Cancelled Bookings'] = summary_table_veh['Cancelled Bookings'].astype(int).map('{:,.0f}'.format)
summary_table_veh['Cancellation Rate (%)'] = summary_table_veh['Cancellation Rate (%)'].map('{:.1f}%'.format)
summary_table_veh.rename(columns={'Vehicle Type': 'Vehicle'}, inplace=True)

fig9, ax9 = plt.subplots(figsize=(10, 3))
ax9.axis('tight'); ax9.axis('off')
the_table3 = ax9.table(cellText=summary_table_veh.values, colLabels=summary_table_veh.columns, loc='center', cellLoc='center')
the_table3.set_fontsize(12); the_table3.scale(1.2, 1.4)
for (row, col), cell in the_table3.get_celld().items():
    cell.set_edgecolor('grey')
    if row == 0:
        cell.set_text_props(weight='bold', color='white'); cell.set_facecolor('#40466e')
    else:
        cell.set_facecolor('#f2f2f2' if row % 2 == 0 else '#ffffff')
st.pyplot(fig9)


# --- Vehicle Performance Summary Table (ADDED) ---
st.subheader("Financial & Distance Performance")
df['Booking Value'] = pd.to_numeric(df['Booking Value'], errors='coerce')
df['Ride Distance'] = pd.to_numeric(df['Ride Distance'], errors='coerce')
summary_table_perf = df.groupby('Vehicle Type').agg(
    Total_Booking_Value=('Booking Value', 'sum'),
    Total_Distance_Travelled=('Ride Distance', 'sum'),
    Avg_Distance_Travelled=('Ride Distance', 'mean')
).reset_index()
completed_rides_df = df[df['Booking Status'] == 'Completed']
success_value = completed_rides_df.groupby('Vehicle Type')['Booking Value'].sum().reset_index()
success_value.rename(columns={'Booking Value': 'Success_Booking_Value'}, inplace=True)
summary_table_perf = pd.merge(summary_table_perf, success_value, on='Vehicle Type', how='left')
summary_table_perf.rename(columns={'Vehicle Type': 'Vehicle', 'Total_Booking_Value': 'Total Booking Value (INR)', 'Success_Booking_Value': 'Success Booking Value (INR)', 'Avg_Distance_Travelled': 'Avg. Distance (km)', 'Total_Distance_Travelled': 'Total Distance (km)'}, inplace=True)
summary_table_perf = summary_table_perf.sort_values(by='Total Booking Value (INR)', ascending=False)
summary_table_perf['Total Booking Value (INR)'] = summary_table_perf['Total Booking Value (INR)'].map('{:,.0f}'.format)
summary_table_perf['Success Booking Value (INR)'] = summary_table_perf['Success Booking Value (INR)'].fillna(0).map('{:,.0f}'.format)
summary_table_perf['Total Distance (km)'] = summary_table_perf['Total Distance (km)'].map('{:,.1f}'.format)
summary_table_perf['Avg. Distance (km)'] = summary_table_perf['Avg. Distance (km)'].map('{:.1f}'.format)
summary_table_perf = summary_table_perf[['Vehicle', 'Total Booking Value (INR)', 'Success Booking Value (INR)', 'Avg. Distance (km)', 'Total Distance (km)']]

fig10, ax10 = plt.subplots(figsize=(12, 3))
ax10.axis('tight'); ax10.axis('off')
the_table4 = ax10.table(cellText=summary_table_perf.values, colLabels=summary_table_perf.columns, loc='center', cellLoc='center')
the_table4.set_fontsize(12); the_table4.scale(1.2, 1.4)
for (row, col), cell in the_table4.get_celld().items():
    cell.set_edgecolor('grey')
    if row == 0:
        cell.set_text_props(weight='bold', color='white'); cell.set_facecolor('#40466e')
    else:
        cell.set_facecolor('#f2f2f2' if row % 2 == 0 else '#ffffff')
st.pyplot(fig10)

