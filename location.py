import streamlit as st
import folium
import pandas as pd
from geopy.distance import geodesic
from sklearn.preprocessing import MinMaxScaler
from streamlit_folium import st_folium

def show():
    # CSS code for styling
    css_code = """
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .stButton > button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        .stNumberInput, .stButton {
            margin-bottom: 15px;
        }
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

    # Load data
    data = pd.read_csv('res maiti.csv', encoding='ISO-8859-1')

    # Data preprocessing
    data = data.dropna(subset=['Latitude', 'Longitude', 'Total_score', 'Reviewscount'])
    scaler = MinMaxScaler()
    data[['Normalized_Score', 'Normalized_Reviews']] = scaler.fit_transform(
        data[['Total_score', 'Reviewscount']].fillna(0)
    )

    # Functions for distance calculation and place recommendation
    def calculate_distance(user_location, place_location):
        return geodesic(user_location, place_location).kilometers

    def recommend_places(user_lat, user_lon, max_distance_km=5, top_n=10, min_reviews=10, category=None):
        data['Distance'] = data.apply(
            lambda row: calculate_distance((user_lat, user_lon), (row['Latitude'], row['Longitude'])), axis=1)
        filtered_data = data[(data['Distance'] <= max_distance_km) & (data['Reviewscount'] >= min_reviews)]
        
        # Filter by category if a category is selected
        if category:
            filtered_data = filtered_data[filtered_data['Category'] == category]

        if filtered_data.empty:
            return "No places found matching the criteria."
        
        # Sort and select the top N places
        top_places = filtered_data.sort_values(by=['Normalized_Score', 'Normalized_Reviews'], ascending=[False, False]).head(top_n)
        
        return {"Recommended Places": top_places[['Place_name', 'Address1', 'Reviewscount', 'Total_score', 'Distance', 'Category']]}

    st.title("Place Recommendation System")

    # Initial coordinates for the map
    initial_location = [27.6885, 85.29988]

    # Create Folium map
    osm_map = folium.Map(location=initial_location, zoom_start=13)
    osm_map.add_child(folium.LatLngPopup())

    # Display the map
    st_data = st_folium(osm_map, width=700, height=500)

    # Initialize session state for storing coordinates
    if 'lat' not in st.session_state:
        st.session_state.lat = initial_location[0]
    if 'lon' not in st.session_state:
        st.session_state.lon = initial_location[1]

    # Update coordinates if a click is detected
    if st_data['last_clicked']:
        st.session_state.lat = st_data['last_clicked']['lat']
        st.session_state.lon = st_data['last_clicked']['lng']

    # Display current coordinates
    st.write(f"Current coordinates: Latitude {st.session_state.lat:.6f}, Longitude {st.session_state.lon:.6f}")

    # User input for additional filtering criteria
    max_distance_km = st.number_input("Enter the maximum distance (in kilometers) to search for places:", min_value=0.0, step=0.1, format="%.1f")
    top_n = st.number_input("Enter the number of top places to recommend:", min_value=1, step=1)
    min_reviews = st.number_input("Enter the minimum number of reviews for a place to be considered popular:", min_value=0, step=1)

    # Dropdown for selecting category filter
    category_options = data['Category'].unique()
    category = st.selectbox("Select a category to filter places:", options=["All"] + list(category_options))

    if st.button("Get Recommendations"):
        if max_distance_km <= 0 or top_n <= 0 or min_reviews < 0:
            st.error("Distance, number of places, and minimum reviews must be positive values.")
        else:
            # Use selected category for filtering
            selected_category = category if category != "All" else None
            results = recommend_places(st.session_state.lat, st.session_state.lon, max_distance_km, top_n, min_reviews, selected_category)

            if isinstance(results, dict):
                for section, df in results.items():
                    st.subheader(section)
                    st.dataframe(df)
            else:
                st.error(results)

if __name__ == "__main__":
    show()
