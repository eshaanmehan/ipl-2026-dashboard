import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the professional page layout
st.set_page_config(page_title="IPL 2026 Indian Stars", page_icon="🏏", layout="wide")

# Custom CSS for a clean, modern UI
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    h1 {color: #1e3d59;}
    .stDataFrame {border-radius: 8px; overflow: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🏏 IPL 2026: Indian National Team Auction Tracker")
st.markdown("A premium dashboard analyzing the squad placements and auction values of India's core international players.")

# Realistic 2026 IPL Data (Prices in Crores)
data = {
    "Player": ["Virat Kohli", "Rohit Sharma", "Jasprit Bumrah", "Hardik Pandya", "Suryakumar Yadav", 
               "Rishabh Pant", "Shreyas Iyer", "Shubman Gill", "Ruturaj Gaikwad", "Ravindra Jadeja", 
               "KL Rahul", "Mohammed Shami", "Yashasvi Jaiswal", "Axar Patel", "Kuldeep Yadav", "Mohammed Siraj"],
    "Role": ["Batter", "Batter", "Bowler", "All-Rounder", "Batter", 
             "WK-Batter", "Batter", "Batter", "Batter", "All-Rounder", 
             "WK-Batter", "Bowler", "Batter", "All-Rounder", "Bowler", "Bowler"],
    "Franchise (2026)": ["RCB", "MI", "MI", "MI", "MI", 
                         "LSG", "PBKS", "GT", "CSK", "CSK", 
                         "LSG", "GT", "RR", "DC", "DC", "RCB"],
    "Status": ["Retained", "Retained", "Retained", "Retained", "Retained",
               "Auction", "Auction", "Retained", "Retained", "Retained",
               "Retained", "Auction", "Retained", "Retained", "Retained", "Retained"],
    "Price (Cr)": [21.0, 16.0, 18.0, 15.0, 15.0, 
                   27.0, 12.5, 16.5, 16.0, 16.0, 
                   17.0, 10.0, 14.0, 16.5, 12.0, 12.0]
}

df = pd.DataFrame(data)

# --- KEY METRICS ---
total_value = df["Price (Cr)"].sum()
max_price = df["Price (Cr)"].max()
top_player = df[df["Price (Cr)"] == max_price]["Player"].values[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Core Value", f"₹ {total_value} Cr")
col2.metric("Most Expensive (2026)", f"{top_player}", f"₹ {max_price} Cr")
col3.metric("Highest Representation", df["Franchise (2026)"].mode()[0])

st.divider()

# --- INTERACTIVE LAYOUT ---
left_col, right_col = st.columns([1.5, 1])

with left_col:
    st.subheader("Player Directory")
    
    # Filters
    f_col1, f_col2 = st.columns(2)
    selected_roles = f_col1.multiselect("Filter by Role", df["Role"].unique(), default=df["Role"].unique())
    selected_teams = f_col2.multiselect("Filter by Team", df["Franchise (2026)"].unique(), default=df["Franchise (2026)"].unique())
    
    filtered_df = df[(df["Role"].isin(selected_roles)) & (df["Franchise (2026)"].isin(selected_teams))]
    
    # Styled Dataframe
    st.dataframe(
        filtered_df.style.format({"Price (Cr)": "₹ {:.2f}"}), 
        use_container_width=True, 
        hide_index=True
    )

with right_col:
    st.subheader("Auction Value Breakdown")
    if not filtered_df.empty:
        # Plotly Bar Chart
        fig = px.bar(
            filtered_df.sort_values("Price (Cr)", ascending=True), 
            x="Price (Cr)", 
            y="Player", 
            color="Franchise (2026)",
            orientation='h', 
            text_auto='.2s',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")
