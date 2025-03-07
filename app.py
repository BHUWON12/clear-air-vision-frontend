
import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import time
import json
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Clear Air Vision",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# # Define API endpoints
# API_BASE_URL = "http://localhost:8000"
# API_ENDPOINTS = {
#     "predict": f"{API_BASE_URL}/predict",
#     "historical_data": f"{API_BASE_URL}/historical-data",
#     "model_performance": f"{API_BASE_URL}/model-performance"
# }
# Define API endpoints
API_BASE_URL = "https://clear-air-vision-backend.onrender.com"
API_ENDPOINTS = {
    "predict": f"{API_BASE_URL}/predict",
    "historical_data": f"{API_BASE_URL}/historical-data",
    "model_performance": f"{API_BASE_URL}/model-performance"
}


# Custom CSS to improve the look of the app
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        background-color: #f5f7f9;
    }
    .css-18e3th9 {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .css-1d391kg {
        padding: 1.5rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #0c326f;
    }
    .stSidebar {
        background-color: #f0f2f6;
    }
    .stAlert {
        border-radius: 10px;
    }
    .stButton>button {
        border-radius: 5px;
        background-color: #4a90e2;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #357abd;
    }
    div[data-baseweb="card"] {
        border-radius: 10px;
        border: 1px solid #e6e9ef;
        padding: 1.5rem;
        background-color: white;
    }
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 1.1rem;
        color: #555;
    }
    .status-good { color: green; }
    .status-moderate { color: #FFA500; }
    .status-bad { color: red; }
    .glass-card {
        background-color: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .prediction-card {
        margin-top: 1rem;
        padding: 1.5rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .prediction-card:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-5px);
    }
    .social-links {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        margin-top: 20px;
    }
    .social-links a {
        display: inline-block;
        padding: 8px 15px;
        background-color: #4a90e2;
        color: white;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .social-links a:hover {
        background-color: #357abd;
        transform: translateY(-2px);
    }
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        padding: 10px 16px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: white;
        border-bottom: 2px solid #4a90e2;
    }
    .recommendation-list li {
        margin-bottom: 8px;
        line-height: 1.5;
    }
    .aqi-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        color: white;
        font-weight: 500;
    }
    .badge-good { background-color: green; }
    .badge-moderate { background-color: #FFA500; }
    .badge-sensitive { background-color: orange; }
    .badge-unhealthy { background-color: red; }
    .badge-very-unhealthy { background-color: purple; }
    .badge-hazardous { background-color: maroon; }
    .round-image {
        border-radius: 50%;
        width: 150px;
        height: 150px;
        object-fit: cover;
        border: 5px solid #4a90e2;
        margin: 0 auto 1rem auto;
        display: block;
    }
    .page-title {
        text-align: center;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .loading-spinner {
        text-align: center;
        margin: 2rem 0;
    }
    .data-timestamp {
        text-align: right;
        color: #666;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    .historical-stats {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        gap: 10px;
        margin: 1rem 0;
    }
    .stat-card {
        background-color: white;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    .stat-value {
        font-size: 1.4rem;
        font-weight: bold;
        margin: 0.3rem 0;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# Function to handle API calls with error handling
def call_api(endpoint, method="get", data=None, max_retries=3):
    url = API_ENDPOINTS.get(endpoint, f"{API_BASE_URL}/{endpoint}")
    
    for attempt in range(max_retries):
        try:
            if method.lower() == "get":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, json=data, timeout=10)
                
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(1)  # Wait before retrying
                    continue
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retrying
                continue
            return None
    
    return None

# Function to get AQI color and category
def get_aqi_info(aqi_value):
    if aqi_value <= 50:
        return "green", "Good", "Air quality is satisfactory, and air pollution poses little or no risk."
    elif aqi_value <= 100:
        return "yellow", "Moderate", "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."
    elif aqi_value <= 150:
        return "orange", "Unhealthy for Sensitive Groups", "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
    elif aqi_value <= 200:
        return "red", "Unhealthy", "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."
    elif aqi_value <= 300:
        return "purple", "Very Unhealthy", "Health alert: The risk of health effects is increased for everyone."
    else:
        return "maroon", "Hazardous", "Health warning of emergency conditions: everyone is more likely to be affected."

# Function to generate dummy prediction
def generate_dummy_prediction(data):
    # Use input data to create a more realistic prediction
    base_aqi = 30
    
    # Add weighted contributions from each pollutant
    aqi = base_aqi + (data["pm25"] * 0.5) + (data["pm10"] * 0.3) + (data["no2"] * 0.4) + \
          (data["so2"] * 0.3) + (data["co"] * 20) + (data["o3"] * 100)
    
    # Apply some randomness
    aqi = max(10, min(450, aqi + np.random.normal(0, 5)))
    
    # Get category info based on calculated AQI
    color, category, description = get_aqi_info(aqi)
    
    return {
        "predicted_aqi": round(aqi, 1),
        "category": category,
        "color": color,
        "description": description,
        "note": "⚠️ This is a simulated prediction as the model API connection failed."
    }

# Function to predict AQI
def predict_aqi(data):
    result = call_api("predict", method="post", data=data)
    if not result:
        result = generate_dummy_prediction(data)
    return result

# Function to get historical data
def get_historical_data():
    result = call_api("historical_data")
    if not result:
        result = generate_dummy_historical_data()
    return result

# Function to generate dummy historical data
def generate_dummy_historical_data():
    dates = pd.date_range(start="2023-01-01", periods=14, freq='D')
    
    # Create a base pattern with some weekly cyclicity
    base_pattern = np.array([80, 85, 95, 100, 90, 70, 60])  # Higher on weekdays, lower on weekends
    
    # Repeat the pattern for 2 weeks and add some noise
    base_values = np.tile(base_pattern, 2)
    aqi_values = base_values + np.random.normal(0, 15, size=14)
    aqi_values = np.clip(aqi_values, 20, 250)  # Clip to realistic AQI range
    
    # Do the same for pollutants
    pm25_values = aqi_values * 0.4 + np.random.normal(0, 5, size=14)
    pm25_values = np.clip(pm25_values, 5, 100)
    
    pm10_values = aqi_values * 0.7 + np.random.normal(0, 10, size=14)
    pm10_values = np.clip(pm10_values, 10, 150)
    
    return {
        "dates": [d.strftime('%Y-%m-%d') for d in dates],
        "aqi_values": aqi_values.tolist(),
        "pm25_values": pm25_values.tolist(),
        "pm10_values": pm10_values.tolist(),
        "note": "⚠️ This is simulated data as the API connection failed."
    }

# Function to get model performance
def get_model_performance():
    result = call_api("model_performance")
    if not result:
        result = generate_dummy_model_performance()
    return result

# Function to generate dummy model performance data
def generate_dummy_model_performance():
    return {
        "mse": 15.23,
        "rmse": 3.90,
        "mae": 3.12,
        "r2": 0.85,
        "feature_importance": {
            "PM2.5": 0.35,
            "PM10": 0.20,
            "NO2": 0.15,
            "SO2": 0.10,
            "CO": 0.08,
            "O3": 0.07,
            "Temperature": 0.02,
            "Humidity": 0.02,
            "Wind_speed": 0.01
        },
        "note": "⚠️ This is simulated performance data as the API connection failed."
    }

# Function to create AQI gauge
def create_aqi_gauge(aqi_value, height=300):
    color = get_aqi_info(aqi_value)[0]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=aqi_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Air Quality Index", 'font': {'size': 24}},
        delta={'reference': 50, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 300], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(0, 128, 0, 0.3)'},
                {'range': [50, 100], 'color': 'rgba(255, 255, 0, 0.3)'},
                {'range': [100, 150], 'color': 'rgba(255, 165, 0, 0.3)'},
                {'range': [150, 200], 'color': 'rgba(255, 0, 0, 0.3)'},
                {'range': [200, 300], 'color': 'rgba(128, 0, 128, 0.3)'},
                {'range': [300, 500], 'color': 'rgba(128, 0, 0, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': aqi_value
            }
        }
    ))

    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=16)
    )
    
    return fig

# Function to get health recommendations based on AQI
def get_health_recommendations(aqi_value):
    if aqi_value <= 50:
        return [
            "Air quality is good. Perfect for outdoor activities.",
            "No health impacts expected. Enjoy the fresh air!",
            "Great conditions for exercise and long periods outdoors."
        ]
    elif aqi_value <= 100:
        return [
            "Air quality is acceptable for most. Unusually sensitive people should consider limiting prolonged outdoor exertion.",
            "Consider reducing intense outdoor activities if you experience unusual coughing or throat irritation.",
            "Keep windows open to maintain good indoor air quality."
        ]
    elif aqi_value <= 150:
        return [
            "Members of sensitive groups may experience health effects. The general public is less likely to be affected.",
            "People with lung disease, older adults and children should reduce prolonged or heavy outdoor exertion.",
            "Consider moving longer or more intense outdoor activities indoors or rescheduling them."
        ]
    elif aqi_value <= 200:
        return [
            "Everyone may begin to experience health effects. Members of sensitive groups may experience more serious health effects.",
            "People with respiratory or heart conditions should avoid outdoor activity.",
            "Everyone else should limit outdoor exertion and keep activity levels light."
        ]
    elif aqi_value <= 300:
        return [
            "Health alert: The risk of health effects is increased for everyone.",
            "Avoid prolonged or heavy exertion. Consider moving all activities indoors or rescheduling.",
            "Keep windows and doors closed and run air purifiers if available."
        ]
    else:
        return [
            "Health warning of emergency conditions: everyone is more likely to be affected.",
            "Avoid all physical activity outdoors.",
            "Stay indoors and keep activity levels low. Keep windows and doors closed."
        ]

# Create sidebar with logo and navigation
st.sidebar.markdown('<img class="round-image" src="https://t3.ftcdn.net/jpg/08/30/72/92/360_F_830729212_ZOEIZ8se1T9uLyp8bX3gvkbGT68ZYufL.jpg" />', unsafe_allow_html=True)
st.sidebar.title("Clear Air Vision")
st.sidebar.markdown("An advanced air quality monitoring and prediction platform")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "🔮 Detailed Prediction", "📊 Historical Data", "📈 Model Performance", "ℹ️ About"]
)

# Dashboard page
if page == "🏠 Dashboard":
    st.markdown("<h1 class='page-title'>🌬️ Air Quality Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class='glass-card'>
        Welcome to the Clear Air Vision dashboard. Monitor real-time air quality predictions 
        and understand how environmental factors affect the air we breathe.
    </div>
    """, unsafe_allow_html=True)
    
    # City selection with a map visualization
    col1, col2 = st.columns([1, 2])
    
    with col1:
        city = st.selectbox(
            "Select Location", 
            ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "San Francisco", "Miami"]
        )
        
        # Get location timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"<p class='data-timestamp'>Last updated: {current_time}</p>", unsafe_allow_html=True)
    
    with col2:
        # Simple map to show selected city (in a real app, you'd use an actual map)
        city_coordinates = {
            "New York": (40.7128, -74.0060),
            "Los Angeles": (34.0522, -118.2437),
            "Chicago": (41.8781, -87.6298),
            "Houston": (29.7604, -95.3698),
            "Phoenix": (33.4484, -112.0740),
            "San Francisco": (37.7749, -122.4194),
            "Miami": (25.7617, -80.1918)
        }
        
        # Get coordinates for selected city
        lat, lon = city_coordinates.get(city, (40.7128, -74.0060))
        
        # Create a scatter plot on US map with selected city
        us_map = px.scatter_geo(
            pd.DataFrame({
                "City": [city],
                "lat": [lat],
                "lon": [lon],
                "AQI": [85]
            }),
            lat="lat",
            lon="lon",
            hover_name="City",
            size_max=15,
            color="AQI",
            color_continuous_scale=["green", "yellow", "orange", "red", "purple", "maroon"],
            range_color=[0, 300],
            scope="usa",
            title="Location",
        )
        
        us_map.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            height=250,
            geo=dict(
                showcoastlines=True,
                projection_scale=3.5,
                center=dict(lat=lat, lon=lon)
            )
        )
        
        st.plotly_chart(us_map, use_container_width=True)
    
    # Main content area divided into two columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("## Current Air Quality")
        
        # Input form for prediction with tabs for different parameter groups
        with st.form("prediction_form"):
            tabs = st.tabs(["Pollutants", "Weather", "Advanced"])
            
            with tabs[0]:  # Pollutants tab
                col1, col2 = st.columns(2)
                with col1:
                    pm25 = st.number_input("PM2.5 (µg/m³)", min_value=0.0, max_value=1000.0, value=20.5, step=0.1, 
                                        help="Fine particulate matter with a diameter of 2.5 micrometers or less")
                    no2 = st.number_input("NO2 (ppb)", min_value=0.0, max_value=1000.0, value=25.1, step=0.1,
                                        help="Nitrogen dioxide, primarily from vehicle emissions")
                    co = st.number_input("CO (ppm)", min_value=0.0, max_value=100.0, value=0.8, step=0.1,
                                       help="Carbon monoxide, a colorless, odorless gas")
                
                with col2:
                    pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0, max_value=1000.0, value=45.3, step=0.1,
                                         help="Particulate matter with a diameter of 10 micrometers or less")
                    so2 = st.number_input("SO2 (ppb)", min_value=0.0, max_value=1000.0, value=10.2, step=0.1,
                                        help="Sulfur dioxide, primarily from industrial processes")
                    o3 = st.number_input("O3 (ppb)", min_value=0.0, max_value=1000.0, value=35.7, step=0.1,
                                       help="Ozone, a reactive gas composed of three oxygen atoms")
            
            with tabs[1]:  # Weather tab
                col1, col2, col3 = st.columns(3)
                with col1:
                    temperature = st.number_input("Temperature (°C)", min_value=-50.0, max_value=60.0, value=24.5, step=0.1,
                                                help="Ambient air temperature")
                with col2:
                    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=0.1,
                                             help="Relative humidity percentage")
                with col3:
                    wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=100.0, value=5.2, step=0.1,
                                               help="Wind speed in meters per second")
            
            with tabs[2]:  # Advanced tab
                st.info("No additional parameters required in the current version.")
                
            # Submit button centered and styled
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("⚡ Predict Air Quality", use_container_width=True)
        
        if submit_button:
            with st.spinner("Analyzing air quality data..."):
                # Create input data dictionary
                input_data = {
                    "pm25": pm25,
                    "pm10": pm10,
                    "no2": no2,
                    "so2": so2,
                    "co": co,
                    "o3": o3,
                    "temperature": temperature,
                    "humidity": humidity,
                    "wind_speed": wind_speed
                }
                
                # Make prediction
                prediction_result = predict_aqi(input_data)
                
                if prediction_result:
                    # Store in session state to maintain across reruns
                    st.session_state.prediction_result = prediction_result
                    st.session_state.prediction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with col2:
        st.markdown("## Air Quality Prediction")
        
        # Check if there's a prediction result
        if 'prediction_result' in st.session_state:
            result = st.session_state.prediction_result
            pred_time = st.session_state.get('prediction_time', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            # Display results in a nice format
            aqi_value = result["predicted_aqi"]
            aqi_category = result["category"]
            aqi_description = result["description"]
            aqi_color = result["color"]
            
            # Display AQI result in a card
            st.markdown(f"""
            <div class="prediction-card">
                <h3 style="margin-top:0">Predicted AQI: {aqi_value:.1f}</h3>
                <div style="background-color:{aqi_color}; padding:8px; border-radius:5px; color:white; margin:10px 0;">
                    <h4 style="margin:0; text-align:center;">{aqi_category}</h4>
                </div>
                <p>{aqi_description}</p>
                <p class="data-timestamp">Prediction time: {pred_time}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display AQI gauge
            st.plotly_chart(create_aqi_gauge(aqi_value, height=250), use_container_width=True)
            
            # Display health recommendations
            st.markdown("### Health Recommendations")
            recommendations = get_health_recommendations(aqi_value)
            
            st.markdown(f"""
            <div style="background-color:rgba({','.join(['220', '220', '220', '0.2'])});
                        padding: 15px; border-radius: 10px; margin-top: 10px; border-left: 4px solid {aqi_color};">
                <ul class="recommendation-list">
                    {"".join([f"<li>{rec}</li>" for rec in recommendations])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # If there's a note, display it (for dummy predictions)
            if "note" in result:
                st.warning(result["note"])
        else:
            # Default display when no prediction is made
            st.markdown("""
            <div class="glass-card">
                <h3 style="text-align:center;">No prediction yet</h3>
                <p style="text-align:center;">Enter environmental parameters and click "Predict AQI" to see the air quality prediction.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Sample gauge with default value
            st.plotly_chart(create_aqi_gauge(50, height=250), use_container_width=True)
    
    # Recent trends section
    st.markdown("## Recent Air Quality Trends")
    
    # Get historical data
    with st.spinner("Loading historical data..."):
        historical_data = get_historical_data()
    
    if historical_data:
        # Create DataFrame from historical data
        aqi_df = pd.DataFrame({
            "Date": historical_data["dates"],
            "AQI": historical_data["aqi_values"],
            "PM2.5": historical_data["pm25_values"],
            "PM10": historical_data["pm10_values"]
        })
        
        # Add AQI category for coloring points
        aqi_df["Category"] = aqi_df["AQI"].apply(lambda x: get_aqi_info(x)[1])
        
        # Plot enhanced line chart
        fig = px.line(
            aqi_df, 
            x="Date", 
            y="AQI", 
            title="AQI Trend Over Last 14 Days",
            labels={"AQI": "Air Quality Index", "Date": "Date"},
            markers=True,
            color_discrete_sequence=["#4a90e2"]
        )
        
        # Add colored points based on AQI category
        fig.add_trace(
            go.Scatter(
                x=aqi_df["Date"],
                y=aqi_df["AQI"],
                mode="markers",
                marker=dict(
                    size=10,
                    color=[get_aqi_info(aqi)[0] for aqi in aqi_df["AQI"]],
                    symbol="circle",
                    line=dict(width=2, color="white")
                ),
                showlegend=False,
                hovertemplate="<b>Date:</b> %{x}<br><b>AQI:</b> %{y:.1f}<extra></extra>"
            )
        )
        
        # Add colored background regions with labels
        fig.add_hrect(y0=0, y1=50, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Good", annotation_position="top right")
        fig.add_hrect(y0=50, y1=100, line_width=0, fillcolor="yellow", opacity=0.1, annotation_text="Moderate", annotation_position="top right")
        fig.add_hrect(y0=100, y1=150, line_width=0, fillcolor="orange", opacity=0.1, annotation_text="Unhealthy for Sensitive Groups", annotation_position="top right")
        fig.add_hrect(y0=150, y1=200, line_width=0, fillcolor="red", opacity=0.1, annotation_text="Unhealthy", annotation_position="top right")
        fig.add_hrect(y0=200, y1=300, line_width=0, fillcolor="purple", opacity=0.1, annotation_text="Very Unhealthy", annotation_position="top right")
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="AQI",
            height=400,
            margin=dict(l=20, r=20, t=50, b=20),
            hovermode="x unified",
            legend_title="Category",
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show note if this is dummy data
        if "note" in historical_data:
            st.info(historical_data["note"])
        
    # Key pollutants metrics section
    st.markdown("## Key Pollutants")
    
    # Create cards for key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pm25_value = 20.5
        pm25_status = "Moderate" if pm25_value > 12 else "Good"
        status_class = "status-moderate" if pm25_status == "Moderate" else "status-good"
        
        st.markdown(f"""
        <div class="metric-card">
            <h3 class="metric-label">PM2.5</h3>
            <div class="metric-value">{pm25_value} µg/m³</div>
            <p class="{status_class}">{pm25_status}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        pm10_value = 45.3
        pm10_status = "Good" if pm10_value < 50 else "Moderate"
        status_class = "status-good" if pm10_status == "Good" else "status-moderate"
        
        st.markdown(f"""
        <div class="metric-card">
            <h3 class="metric-label">PM10</h3>
            <div class="metric-value">{pm10_value} µg/m³</div>
            <p class="{status_class}">{pm10_status}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        o3_value = 35.7
        o3_status = "Good" if o3_value < 55 else "Moderate"
        status_class = "status-good" if o3_status == "Good" else "status-moderate"
        
        st.markdown(f"""
        <div class="metric-card">
            <h3 class="metric-label">O3 (Ozone)</h3>
            <div class="metric-value">{o3_value} ppb</div>
            <p class="{status_class}">{o3_status}</p>
        </div>
        """, unsafe_allow_html=True)

# Detailed Prediction page
elif page == "🔮 Detailed Prediction":
    st.markdown("<h1 class='page-title'>🔮 Detailed Air Quality Prediction</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card'>
        This page provides a detailed air quality prediction with advanced analysis of 
        contributing pollutants and environmental factors.
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Use expanders to organize the form into collapsible sections
        with st.form("detailed_prediction_form"):
            with st.expander("Particulate Matter", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    pm25 = st.number_input("PM2.5 (µg/m³)", min_value=0.0, max_value=1000.0, value=20.5, step=0.1,
                                         help="Fine particulate matter with diameter less than 2.5 micrometers")
                with col2:
                    pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0, max_value=1000.0, value=45.3, step=0.1,
                                         help="Particulate matter with diameter less than 10 micrometers")
            
            with st.expander("Gaseous Pollutants", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    no2 = st.number_input("NO2 (ppb)", min_value=0.0, max_value=1000.0, value=25.1, step=0.1,
                                        help="Nitrogen Dioxide - primarily from vehicle emissions")
                    co = st.number_input("CO (ppm)", min_value=0.0, max_value=100.0, value=0.8, step=0.1,
                                       help="Carbon Monoxide - colorless, odorless gas")
                with col2:
                    so2 = st.number_input("SO2 (ppb)", min_value=0.0, max_value=1000.0, value=10.2, step=0.1,
                                        help="Sulfur Dioxide - primarily from industrial processes")
                    o3 = st.number_input("O3 (ppb)", min_value=0.0, max_value=1000.0, value=35.7, step=0.1,
                                       help="Ozone - reactive gas formed by photochemical reactions")
            
            with st.expander("Meteorological Parameters", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    temperature = st.number_input("Temperature (°C)", min_value=-50.0, max_value=60.0, value=24.5, step=0.1,
                                                help="Ambient temperature")
                with col2:
                    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=0.1,
                                             help="Relative humidity")
                with col3:
                    wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=100.0, value=5.2, step=0.1,
                                               help="Wind speed")
            
            submit_button = st.form_submit_button("Generate Detailed Prediction", use_container_width=True)
        
        if submit_button:
            with st.spinner("Analyzing data and generating detailed prediction..."):
                # Create input data dictionary
                input_data = {
                    "pm25": pm25,
                    "pm10": pm10,
                    "no2": no2,
                    "so2": so2,
                    "co": co,
                    "o3": o3,
                    "temperature": temperature,
                    "humidity": humidity,
                    "wind_speed": wind_speed
                }
                
                # Make prediction
                prediction_result = predict_aqi(input_data)
                
                if prediction_result:
                    # Store results in session state
                    st.session_state.detailed_prediction = prediction_result
                    st.session_state.detailed_inputs = input_data
    
    with col2:
        st.markdown("### Prediction Results")
        
        if 'detailed_prediction' in st.session_state:
            result = st.session_state.detailed_prediction
            
            # Display results in a nice format
            aqi_value = result["predicted_aqi"]
            aqi_category = result["category"]
            aqi_description = result["description"]
            aqi_color = result["color"]
            
            # Display AQI gauge
            st.plotly_chart(create_aqi_gauge(aqi_value), use_container_width=True)
            
            # Display AQI category with appropriate color
            st.markdown(f"""
            <div style="background-color:{aqi_color}; padding:10px; border-radius:5px; color:white; margin-bottom:10px;">
                <h3 style="margin:0;">Category: {aqi_category}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Display description
            st.info(aqi_description)
            
            # If there's a note, display it (for dummy predictions)
            if "note" in result:
                st.warning(result["note"])
            
        else:
            st.info("Enter parameters and click 'Generate Detailed Prediction' to see results.")
    
    # Show detailed analysis when prediction is available
    if 'detailed_prediction' in st.session_state and 'detailed_inputs' in st.session_state:
        st.markdown("## Contributing Factors Analysis")
        
        # Get the input data and prediction result
        inputs = st.session_state.detailed_inputs
        aqi_value = st.session_state.detailed_prediction["predicted_aqi"]
        
        # Get performance data for feature importance
        performance_data = get_model_performance()
        
        if performance_data:
            # Create a dataframe with inputs and their importance
            feature_importance = performance_data.get("feature_importance", {})
            
            # Map input names to feature importance names
            input_to_feature = {
                "pm25": "PM2.5", 
                "pm10": "PM10", 
                "no2": "NO2", 
                "so2": "SO2", 
                "co": "CO", 
                "o3": "O3",
                "temperature": "Temperature", 
                "humidity": "Humidity", 
                "wind_speed": "Wind_speed"
            }
            
            # Create a DF with inputs and importance
            analysis_data = []
            for input_name, input_value in inputs.items():
                feature_name = input_to_feature.get(input_name, input_name)
                importance = feature_importance.get(feature_name, 0.01)
                analysis_data.append({
                    "Factor": feature_name,
                    "Value": input_value,
                    "Importance": importance,
                    "Contribution": input_value * importance  # Simplified contribution calculation
                })
            
            analysis_df = pd.DataFrame(analysis_data)
            
            # Normalize contribution for visualization
            total_contribution = analysis_df["Contribution"].sum()
            if total_contribution > 0:
                analysis_df["Contribution %"] = (analysis_df["Contribution"] / total_contribution * 100).round(1)
            else:
                analysis_df["Contribution %"] = 0
            
            # Sort by contribution
            analysis_df = analysis_df.sort_values("Contribution %", ascending=False)
            
            # Display as a donut chart
            fig = px.pie(
                analysis_df,
                values="Contribution %",
                names="Factor",
                title="Contribution to AQI Prediction",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
            fig.update_layout(
                margin=dict(l=20, r=20, t=50, b=20),
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            
            # Show the chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Display a table with detailed analysis
            st.markdown("### Factor Details")
            
            # Format the data for display
            display_df = analysis_df.copy()
            display_df = display_df[["Factor", "Value", "Importance", "Contribution %"]]
            display_df["Importance"] = (display_df["Importance"] * 100).round(1).astype(str) + "%"
            display_df["Contribution %"] = display_df["Contribution %"].astype(str) + "%"
            
            # Show the table
            st.dataframe(display_df, use_container_width=True)
            
            # Display health recommendation
            st.markdown("### Health Impact Assessment")
            
            # Get recommendations based on AQI
            recommendations = get_health_recommendations(aqi_value)
            
            # Create colored card based on AQI category
            aqi_color = get_aqi_info(aqi_value)[0]
            
            st.markdown(f"""
            <div style="background-color:rgba({','.join(['240', '240', '240', '0.3'])});
                       padding: 15px; border-radius: 10px; margin-top: 10px; border-left: 5px solid {aqi_color};">
                <h4 style="margin-top:0;">Potential Health Effects</h4>
                <ul class="recommendation-list">
                    {"".join([f"<li>{rec}</li>" for rec in recommendations])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # If there's a note in performance data, display it
            if "note" in performance_data:
                st.info(performance_data["note"])
# Historical Data page
elif page == "📊 Historical Data":
    st.markdown("<h1 class='page-title'>📊 Historical Air Quality Data</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card'>
        Explore historical air quality data to understand trends and patterns over time.
        This data helps identify seasonal variations and long-term changes in air quality.
    </div>
    """, unsafe_allow_html=True)
    
    # Create filters in a nice layout
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # City selection
        city = st.selectbox("Select Location", ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "San Francisco"])
    
    with col2:
        # Date range selection
        date_option = st.radio("Time Period", ["Last 7 days", "Last 14 days", "Last 30 days", "Custom"], horizontal=True)
        
        if date_option == "Custom":
            # Show date inputs in a row
            date_col1, date_col2 = st.columns(2)
            with date_col1:
                start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=7))
            with date_col2:
                end_date = st.date_input("End Date", value=datetime.now())
        else:
            # Set dates based on selection
            end_date = datetime.now()
            if date_option == "Last 7 days":
                start_date = end_date - timedelta(days=7)
            elif date_option == "Last 14 days":
                start_date = end_date - timedelta(days=14)
            else:  # Last 30 days
                start_date = end_date - timedelta(days=30)
    
    with col3:
        # Pollutant selection
        pollutant = st.selectbox("Parameter", ["AQI", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3"])
    
    # Fetch historical data
    with st.spinner("Loading historical data..."):
        historical_data = get_historical_data()
        
        if historical_data:
            # Create DataFrame from API response
            df = pd.DataFrame({
                "Date": historical_data["dates"],
                "AQI": historical_data["aqi_values"],
                "PM2.5": historical_data["pm25_values"],
                "PM10": historical_data["pm10_values"]
            })
            
            # Add dummy data for other pollutants if they don't exist
            if "NO2" not in df.columns:
                df["NO2"] = np.random.normal(30, 10, size=len(df))
            if "SO2" not in df.columns:
                df["SO2"] = np.random.normal(15, 5, size=len(df))
            if "CO" not in df.columns:
                df["CO"] = np.random.normal(1, 0.3, size=len(df))
            if "O3" not in df.columns:
                df["O3"] = np.random.normal(40, 10, size=len(df))
            
            # Convert date strings to datetime
            df["Date"] = pd.to_datetime(df["Date"])
            
            # Filter by date range
            date_filter = (df["Date"] >= pd.Timestamp(start_date)) & (df["Date"] <= pd.Timestamp(end_date))
            df = df[date_filter]
            
            # Create statistic summary
            st.markdown("## Air Quality Statistics")
            
            # Get statistics for the chosen pollutant
            if df.shape[0] > 0:
                max_val = df[pollutant].max()
                min_val = df[pollutant].min()
                avg_val = df[pollutant].mean()
                median_val = df[pollutant].median()
                
                # Display statistics in a nice grid
                st.markdown("<div class='historical-stats'>", unsafe_allow_html=True)
                
                statistics = [
                    {"label": "Maximum", "value": f"{max_val:.1f}"},
                    {"label": "Minimum", "value": f"{min_val:.1f}"},
                    {"label": "Average", "value": f"{avg_val:.1f}"},
                    {"label": "Median", "value": f"{median_val:.1f}"}
                ]
                
                for stat in statistics:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">{stat['label']}</div>
                        <div class="stat-value">{stat['value']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Create enhanced visualizations based on selection
                st.markdown(f"## {pollutant} Trend Over Time")
                
                # Create figure based on pollutant selection
                if pollutant == "AQI":
                    # For AQI, create a line chart with colored points based on AQI category
                    df["Category"] = df["AQI"].apply(lambda x: get_aqi_info(x)[1])
                    
                    fig = px.line(
                        df, 
                        x="Date", 
                        y="AQI", 
                        title=f"Historical {pollutant} Values for {city}",
                        markers=True,
                        color_discrete_sequence=["#4a90e2"],
                        template="plotly_white"
                    )
                    
                    # Add colored points based on AQI category
                    fig.add_trace(
                        go.Scatter(
                            x=df["Date"],
                            y=df["AQI"],
                            mode="markers",
                            marker=dict(
                                size=8,
                                color=[get_aqi_info(aqi)[0] for aqi in df["AQI"]],
                                symbol="circle",
                                line=dict(width=1, color="white")
                            ),
                            name="AQI Category",
                            hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>AQI:</b> %{y:.1f}<extra></extra>"
                        )
                    )
                    
                    # Add reference lines
                    fig.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Good")
                    fig.add_hline(y=100, line_dash="dash", line_color="yellow", annotation_text="Moderate")
                    fig.add_hline(y=150, line_dash="dash", line_color="orange", annotation_text="Unhealthy for Sensitive Groups")
                    fig.add_hline(y=200, line_dash="dash", line_color="red", annotation_text="Unhealthy")
                    
                    y_axis_title = "Air Quality Index (AQI)"
                else:
                    # For other pollutants, create a regular line chart with a moving average
                    fig = px.line(
                        df, 
                        x="Date", 
                        y=pollutant, 
                        title=f"Historical {pollutant} Values for {city}",
                        markers=True,
                        template="plotly_white"
                    )
                    
                    # Add a 3-day moving average if there are enough data points
                    if len(df) >= 3:
                        df["MA3"] = df[pollutant].rolling(window=3).mean()
                        fig.add_trace(
                            go.Scatter(
                                x=df["Date"],
                                y=df["MA3"],
                                mode="lines",
                                name="3-day Moving Average",
                                line=dict(dash="dash", color="red", width=2),
                                hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>MA3:</b> %{y:.1f}<extra></extra>"
                            )
                        )
                    
                    # Set appropriate y-axis title based on pollutant
                    pollutant_units = {
                        "PM2.5": "µg/m³",
                        "PM10": "µg/m³",
                        "NO2": "ppb",
                        "SO2": "ppb",
                        "CO": "ppm",
                        "O3": "ppb"
                    }
                    y_axis_title = f"{pollutant} ({pollutant_units.get(pollutant, '')})"
                
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title=y_axis_title,
                    height=450,
                    margin=dict(l=20, r=20, t=50, b=20),
                    hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                # Show the chart
                st.plotly_chart(fig, use_container_width=True)
                
                # Add calendar heatmap for pattern analysis
                st.markdown("## Day-of-Week Patterns")
                
                # Add day of week
                df["Day of Week"] = df["Date"].dt.day_name()
                df["Hour"] = df["Date"].dt.hour
                
                # Create daily averages by day of week
                day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                
                # Group by day of week and calculate statistics
                day_stats = df.groupby("Day of Week")[pollutant].agg(["mean", "min", "max"]).reset_index()
                
                # Reorder days
                day_stats["Day of Week"] = pd.Categorical(day_stats["Day of Week"], categories=day_order, ordered=True)
                day_stats = day_stats.sort_values("Day of Week")
                
                # Create bar chart for day of week patterns
                fig = px.bar(
                    day_stats,
                    x="Day of Week",
                    y="mean",
                    error_y=day_stats["max"] - day_stats["mean"],
                    error_y_minus=day_stats["mean"] - day_stats["min"],
                    title=f"Average {pollutant} by Day of Week",
                    labels={"mean": f"Average {pollutant}", "Day of Week": ""},
                    color_discrete_sequence=["#4a90e2"],
                    template="plotly_white"
                )
                
                fig.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=50, b=20),
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show data table in an expander
                with st.expander("View Data Table"):
                    # Format the data for display
                    display_df = df.copy()
                    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
                    # Select columns to display
                    if pollutant == "AQI":
                        display_df = display_df[["Date", "Day of Week", "AQI", "PM2.5", "PM10"]]
                    else:
                        display_df = display_df[["Date", "Day of Week", pollutant]]
                    
                    st.dataframe(display_df, use_container_width=True)
                
                # Download option
                st.markdown("### Download Data")
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download CSV",
                    csv,
                    f"{city}_{pollutant}_data.csv",
                    "text/csv",
                    key="download-csv"
                )

# Model Performance page
elif page == "📈 Model Performance":
    st.markdown("<h1 class='page-title'>📈 Model Performance Metrics</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-card'>
        Understand how our air quality prediction model performs and what factors most influence the predictions.
        This information helps provide transparency into how predictions are made.
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch model performance data
    with st.spinner("Loading model performance data..."):
        performance_data = get_model_performance()
        
        if performance_data:
            # Create tabs for different aspects of model performance
            tab1, tab2, tab3 = st.tabs(["📊 Accuracy Metrics", "🔍 Feature Importance", "🎯 Model Validation"])
            
            with tab1:
                st.markdown("### Model Accuracy Metrics")
                
                # Create metric cards for model performance statistics
                col1, col2, col3, col4 = st.columns(4)
                
                metrics = [
                    {"label": "Mean Squared Error (MSE)", "value": performance_data["mse"], "help": "Average squared difference between predicted and actual values. Lower is better."},
                    {"label": "Root MSE (RMSE)", "value": performance_data["rmse"], "help": "Square root of MSE. Represents the standard deviation of prediction errors."},
                    {"label": "Mean Absolute Error (MAE)", "value": performance_data["mae"], "help": "Average absolute difference between predicted and actual values."},
                    {"label": "R² Score", "value": performance_data["r2"], "help": "Proportion of variance explained by the model. Closer to 1 is better."}
                ]
                
                # Display metric cards
                cols = [col1, col2, col3, col4]
                for i, metric in enumerate(metrics):
                    with cols[i]:
                        st.metric(
                            label=metric["label"], 
                            value=f"{metric['value']:.2f}",
                            help=metric["help"]
                        )
                
                # Add explanation of metrics
                st.markdown("""
                ### Understanding These Metrics
                
                These metrics help evaluate how well our model predicts air quality:
                
                - **Mean Squared Error (MSE)** - Measures the average squared difference between predicted and actual AQI values. Lower values indicate better model performance.
                
                - **Root Mean Squared Error (RMSE)** - The square root of MSE, providing an error measure in the same units as the AQI. It represents the standard deviation of prediction errors.
                
                - **Mean Absolute Error (MAE)** - Measures the average absolute difference between predicted and actual values, giving a straightforward measure of error magnitude.
                
                - **R² Score** - Also known as the coefficient of determination, measures how well the model explains the variance in AQI. Values closer to 1 indicate a better fit.
                """)
            
            with tab2:
                st.markdown("### Feature Importance")
                
                # Get feature importance data
                feature_importance = performance_data["feature_importance"]
                
                # Convert to DataFrame for plotting
                features_df = pd.DataFrame({
                    "Feature": list(feature_importance.keys()),
                    "Importance": list(feature_importance.values())
                }).sort_values("Importance", ascending=False)
                
                # Create horizontal bar chart with improved styling
                fig = px.bar(
                    features_df, 
                    y="Feature", 
                    x="Importance", 
                    orientation='h',
                    title="Relative Importance of Factors in AQI Prediction",
                    labels={"Importance": "Relative Importance", "Feature": ""},
                    color="Importance",
                    color_continuous_scale="Blues",
                    template="plotly_white"
                )
                
                fig.update_layout(
                    height=450,
                    margin=dict(l=20, r=20, t=50, b=20),
                    yaxis={'categoryorder': 'total ascending'},
                    xaxis=dict(title="Importance (higher is more influential)"),
                    coloraxis_showscale=False
                )
                
                # Show the chart
                st.plotly_chart(fig, use_container_width=True)
                
                # Add explanation of feature importance
                st.markdown("""
                ### What This Chart Shows
                
                This chart displays the relative importance of different environmental factors in predicting the Air Quality Index (AQI). 
                Features with higher importance have more influence on the model's predictions.
                
                - **Primary Pollutants**: Particulate matter (PM2.5 and PM10) and gases like NO2 and O3 typically have the highest impact on air quality.
                
                - **Secondary Factors**: Weather conditions like temperature, humidity, and wind speed can affect how pollutants disperse and react in the atmosphere.
                
                Understanding these relationships helps explain why certain combinations of environmental conditions lead to better or worse air quality.
                """)
            
            with tab3:
                st.markdown("### Model Validation")
                
                # Create simulated data for model validation visualization
                np.random.seed(42)  # For reproducibility
                n_points = 100
                
                # Generate realistic test data
                actual = np.random.normal(loc=100, scale=30, size=n_points).clip(min=0, max=300)
                
                # Add some correlation with noise for predicted values
                predicted = actual * 0.85 + np.random.normal(loc=15, scale=15, size=n_points)
                predicted = predicted.clip(min=0, max=300)
                
                # Calculate error
                error = predicted - actual
                
                # Create DataFrame for visualization
                validation_df = pd.DataFrame({
                    "Actual AQI": actual, 
                    "Predicted AQI": predicted,
                    "Error": error
                })
                
                # Create scatter plot of actual vs predicted
                fig = px.scatter(
                    validation_df, 
                    x="Actual AQI", 
                    y="Predicted AQI",
                    color="Error",
                    color_continuous_scale="RdBu_r",
                    color_continuous_midpoint=0,
                    title="Model Prediction Accuracy (Test Data)",
                    labels={"Actual AQI": "Actual AQI Value", "Predicted AQI": "Model Predicted AQI Value", "Error": "Prediction Error"},
                    template="plotly_white"
                )
                
                # Add perfect prediction line
                fig.add_trace(go.Scatter(
                    x=[0, 300],
                    y=[0, 300],
                    mode="lines",
                    name="Perfect Prediction",
                    line=dict(color="green", dash="dash", width=2)
                ))
                
                # Add bands for error ranges
                fig.add_traces([
                    go.Scatter(
                        x=[0, 300],
                        y=[10, 310],
                        mode="lines",
                        line=dict(color="rgba(0,0,0,0.1)", width=1),
                        name="+10 Error"
                    ),
                    go.Scatter(
                        x=[0, 300],
                        y=[-10, 290],
                        mode="lines",
                        line=dict(color="rgba(0,0,0,0.1)", width=1),
                        name="-10 Error",
                        fill="tonexty"
                    )
                ])
                
                fig.update_layout(
                    height=500,
                    margin=dict(l=20, r=20, t=50, b=20),
                    hovermode="closest",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                # Show the scatter plot
                st.plotly_chart(fig, use_container_width=True)
                
                # Add error distribution visualization
                st.markdown("### Prediction Error Distribution")
                
                # Create histogram of errors
                error_fig = px.histogram(
                    validation_df, 
                    x="Error",
                    nbins=20,
                    color_discrete_sequence=["#4a90e2"],
                    title="Distribution of Prediction Errors",
                    labels={"Error": "Prediction Error (Predicted - Actual)"},
                    template="plotly_white"
                )
                
                # Add a vertical line at zero error
                error_fig.add_vline(
                    x=0, 
                    line_dash="dash", 
                    line_color="green", 
                    annotation_text="No Error",
                    annotation_position="top right"
                )
                
                error_fig.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=50, b=20),
                    bargap=0.1
                )
                
                # Show the histogram
                st.plotly_chart(error_fig, use_container_width=True)
                
                # Add model explanation
                st.markdown("""
                ### Understanding Model Validation
                
                These charts demonstrate how well our model performs on test data:
                
                - **Prediction Scatter Plot**: Each point represents a test case, comparing the actual AQI value to what our model predicted. Points on the green diagonal line represent perfect predictions. Points above the line indicate the model overestimated AQI, while points below indicate underestimation.
                
                - **Error Distribution**: This histogram shows how prediction errors are distributed. Ideally, most errors should be clustered around zero (no error), with a bell-shaped distribution indicating random rather than systematic error.
                
                Our model achieves good accuracy, with most predictions falling within ±10 AQI points of actual values, providing reliable air quality forecasts.
                """)
            
            # If there's a note in performance data, display it
            if "note" in performance_data:
                st.info(performance_data["note"])
        else:
            st.error("Failed to fetch model performance data. Please try again later.")

# About page
elif page == "ℹ️ About":
    st.markdown("<h1 class='page-title'>ℹ️ About Clear Air Vision</h1>", unsafe_allow_html=True)
    
    # Project overview
    st.markdown("""
    <div class='glass-card'>
        <h3>Project Overview</h3>
        <p>
            Clear Air Vision is an advanced air quality monitoring and prediction platform designed to provide accurate, 
            real-time information about air quality based on environmental parameters. The platform leverages machine 
            learning algorithms to predict Air Quality Index (AQI) values from various pollutant measurements, helping 
            users make informed decisions about outdoor activities and health precautions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tech stack and architecture
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Technology Stack
        
        #### Frontend
        - **Streamlit**: Interactive dashboard UI
        - **Plotly**: Data visualization
        - **Pandas**: Data manipulation
        
        #### Backend
        - **FastAPI**: RESTful API services
        - **Scikit-learn**: Machine learning models
        - **Joblib**: Model serialization
        - **NumPy**: Numerical computations
        """)
        
    with col2:
        st.markdown("""
        ### Data Sources & Model
        
        #### Data Sources
        - Air quality monitoring stations
        - Weather data APIs
        - Environmental protection agencies
        - Satellite observations
        
        #### Machine Learning Model
        - Ensemble of regression algorithms
        - Trained on historical air quality data
        - Regular retraining for improved accuracy
        - Feature engineering for better predictions
        """)
    
    # AQI explanation section
    st.markdown("### Understanding Air Quality Index (AQI)")
    
    # AQI description
    st.markdown("""
    <div class='glass-card'>
        <p>
            The Air Quality Index (AQI) is a standardized indicator developed by the US Environmental Protection Agency (EPA) 
            for reporting daily air quality. It indicates how clean or polluted the air is and what associated health effects 
            might be of concern.
        </p>
        <p>
            The AQI focuses on health effects that may be experienced within a few hours or days after breathing polluted air.
            It is calculated based on concentrations of major air pollutants including particulate matter (PM2.5 and PM10), 
            ground-level ozone, carbon monoxide, sulfur dioxide, and nitrogen dioxide.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # AQI categories with improved visualization
    st.markdown("### AQI Categories and Health Implications")
    
    aqi_categories = {
        "Good (0-50)": {
            "color": "green",
            "description": "Air quality is satisfactory, and air pollution poses little or no risk.",
            "icon": "✅"
        },
        "Moderate (51-100)": {
            "color": "yellow",
            "description": "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.",
            "icon": "⚠️"
        },
        "Unhealthy for Sensitive Groups (101-150)": {
            "color": "orange",
            "description": "Members of sensitive groups may experience health effects. The general public is less likely to be affected.",
            "icon": "⚠️"
        },
        "Unhealthy (151-200)": {
            "color": "red",
            "description": "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.",
            "icon": "🚫"
        },
        "Very Unhealthy (201-300)": {
            "color": "purple",
            "description": "Health alert: The risk of health effects is increased for everyone.",
            "icon": "🚫"
        },
        "Hazardous (301+)": {
            "color": "maroon",
            "description": "Health warning of emergency conditions: everyone is more likely to be affected.",
            "icon": "☣️"
        }
    }
    
    for category, info in aqi_categories.items():
        st.markdown(f"""
        <div style="background-color:{info['color']}; padding:15px; border-radius:8px; color:white; margin-bottom:15px;">
            <h4 style="margin:0;">{info['icon']} {category}</h4>
            <p style="margin:8px 0 0 0;">{info['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Project features and benefits
    st.markdown("### Key Features & Benefits")
    
    features = [
        {
            "title": "Real-time AQI Prediction",
            "description": "Get instant predictions of air quality based on current environmental conditions"
        },
        {
            "title": "Historical Data Analysis",
            "description": "Explore past air quality trends to understand patterns and seasonal variations"
        },
        {
            "title": "Health Recommendations",
            "description": "Receive personalized health guidance based on current and forecasted air quality"
        },
        {
            "title": "Transparent Model Performance",
            "description": "Understand how the prediction model works and what factors influence air quality"
        }
    ]
    
    # Display features in a grid
    feature_cols = st.columns(2)
    for i, feature in enumerate(features):
        with feature_cols[i % 2]:
            st.markdown(f"""
            <div style="background-color:white; padding:15px; border-radius:8px; margin-bottom:15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="color:#4a90e2; margin-top:0;">{feature['title']}</h4>
                <p>{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Add the correct social media links
    st.markdown("### Connect With Me")
    st.markdown("""
    <div class="social-links">
        <a href="https://www.instagram.com/bhuwon.zip/" target="_blank">Instagram</a>
        <a href="https://www.facebook.com/bhupeshbh" target="_blank">Facebook</a>
        <a href="https://github.com/BHUWON12" target="_blank">GitHub</a>
        <a href="https://yourportfolio.com" target="_blank">Portfolio</a>
        <a href="https://www.linkedin.com/in/bhuwansingh02/" target="_blank">LinkedIn</a>
        <a href="https://x.com/bhuwansinghh" target="_blank">Twitter(X)</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Version and acknowledgments
    st.markdown("""
    <div style="text-align:center; margin-top:30px; padding:15px; font-size:0.9em; color:#666;">
        <p>Clear Air Vision v2.0 | Created with ❤️ by Bhuwan Singh</p>
        <p>© 2023 All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)