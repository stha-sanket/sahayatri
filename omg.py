import streamlit as st
import base64
import requests

# Define the min and max costs for each category
# Chitwan
chitwan_activities = {
    "Jungle Safari 100-200": (100, 200),
    "Elephant Ride 30-150": (30, 150),
    "Canoeing 30-50": (30, 50),
    "Fishing 10-50": (10, 50),
    "Tharu Museum 5-10": (5, 10)
}

chitwan_guides = {
    "Full-time Guide 400-600": (400, 600),
    "Cultural Guide 200-300": (250, 300),
    "Trekking Guide 300-500": (350, 500)
}

chitwan_accommodations = {
    "Homestay 10-50": (10, 50),
    "Basic Lodge 15-50": (15, 50),
    "Luxury Lodge 100-300": (100, 300),
    "Basic Hotel 15-30": (15, 30),
    "Luxury Hotel 100-400": (100, 400)
}

# Everest
everest_activities = {
    "Sherpa Village Tour 100-200": (100, 150),
    "Everest Summit Path 150-200": (150, 200),
    "Helicopter Tour 1000-1200": (1000, 1200),
    "Camping in Base Camp 400-500": (400, 500),
    "Mountain Flight 250-300": (250, 300)
}

everest_guides = {
    "Full-time Guide 450-600": (450, 500),
    "Cultural Guide 250-300": (250, 300),
    "Trekking Guide 350-400": (350, 400)
}

everest_porters = {
    "Full-time Porter 180-200": (180, 200),
    "Halfway Porter 90-100": (90, 100),
    "Multiple Porters 300-350": (300, 350)
}

everest_accommodations = {
    "Homestay 15-20": (15, 20),
    "Basic Lodge 40-50": (40, 50),
    "Luxury Lodge 130-150": (130, 150),
    "Basic Hotel 70-80": (70, 80),
    "Luxury Hotel 180-200": (180, 200)
}

# Lumbini
lumbini_activities = {
    "Lumbini Museum 10-20": (10, 20),
    "Ashok Pillar 5-10": (5, 10),
    "Cycling 2-5": (2, 5),
    "Meditation 5-15": (5, 15)
}

lumbini_guides = {
    "Full-time Guide 300-450": (300, 450),
    "Cultural Guide 150-300": (150, 300),
}

lumbini_accommodations = {
    "Homestay 5-50": (5, 50),
    "Basic Lodge 8 - 20": (8, 20),
    "Luxury Lodge 60-140": (60, 140),
    "Basic Hotel 8 - 30": (8, 30),
    "Luxury Hotel 75-200": (75, 200)
}

# Pokhara
pokhara_activities = {
    "Boating 5-30": (5, 30),
    "Paragliding 70-150": (70, 150),
    "Rafting 20-100": (20, 100),
    "Zip Lining 50-120": (50, 120),
    "Hot Air Balloon 90-200": (90, 200),
    "Bungee Jumping 70-120": (70, 120)
}

pokhara_guides = {
    "Full-time Guide 450-500": (450, 500),
    "Cultural Guide 250-300": (250, 300),
    "Trekking Guide 350-400": (350, 400)
}

pokhara_accommodations = {
    "Homestay 10-60": (10, 60),
    "Basic Lodge 8 - 20": (8, 20),
    "Luxury Lodge 100-300": (100, 300),
    "Basic Hotel 10 - 40": (10, 40),
    "Luxury Hotel 100-400": (100, 400)
}

# Function to calculate the total cost
def calculate_total(selected_options):
    return sum(selected_options.values())

# Function to encode images to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# CSS code
css_code = """
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
        color: #333;
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
    .stCheckbox {
        margin-bottom: 15px;
    }
    .stSelectbox {
        margin-bottom: 15px;
    }
    .stNumberInput {
        margin-bottom: 20px;
    }
    .stWarning {
        color: #dc3545;
    }
    .stSuccess {
        color: #28a745;
    }
    .stInfo {
        color: #17a2b8;
    }
    .stSubheader {
        font-size: 24px;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .stWrite {
        font-size: 18px;
        margin-bottom: 10px;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    .activity-container h2 {
        font-size: 22px;
        margin-bottom: 15px;
    }
    .activity-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .doctor-card {
        width: 300px;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        background-color: #fff;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 250px;
    }
    .doctor-image {
        border-radius: 10%;
        width: 350px;
        height: 150px;
        object-fit: cover;
        margin: 0 auto 15px;
    }
    .doctor-info {
        font-size: 14px;
        color: #333;
        font-family: 'Arial', sans-serif;
    }
    .doctor-name {
        font-weight: bold;
        font-size: 18px;
        margin-top: 10px;
        color: #ff0000;
    }
    .doctor-position {
        color: #555;
        margin-top: 5px;
        font-size: 13px;
    }
    .doctor-nmc {
        color: #888;
        margin-top: 5px;
        font-size: 12px;
    }
    @media (max-width: 600px) {
        .reason {
            flex: 1 1 100%;
        }
    }
</style>
"""

# Main function for Streamlit
def show():
    st.markdown(css_code, unsafe_allow_html=True)  # Embed CSS
    st.image('wow.jpg')
    st.title("Nepal Trip Budget Calculator")

    doctors = [
        {"name": "Pokhare", "image": "pokhara.jpg"},
        {"name": "Everest", "image": "everest.png"},
        {"name": "Chitwan", "image": "chit.png"},
        {"name": "Lumbini", "image": "lumbini.jpg"}
    ]

    # Displaying doctors in a grid layout with two columns
    for i in range(0, len(doctors), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(doctors):
                doctor = doctors[i + j]
                with cols[j]:
                    image_base64 = get_image_base64(doctor['image'])
                    st.markdown(f"""
                        <div class="doctor-card">
                            <div>
                                <img src="data:image/jpeg;base64,{image_base64}" class="doctor-image" alt="{doctor['name']}">
                                <div class="doctor-info">
                                    <div class="doctor-name">{doctor['name']}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    st.write("\n")
    st.write("\n")

    # Select Destination
    destination = st.selectbox("Choose your destination:", ["Chitwan", "Everest", "Lumbini", "Pokhara"])

    # Get the user's budget
    budget = st.number_input("Enter your budget:", min_value=0, step=10, value=1000)

    selected_options = {}

    # Define the data based on the selected destination
    if destination == "Chitwan":
        activities = chitwan_activities
        guides = chitwan_guides
        accommodations = chitwan_accommodations
    elif destination == "Everest":
        activities = everest_activities
        guides = everest_guides
        accommodations = everest_accommodations
    elif destination == "Lumbini":
        activities = lumbini_activities
        guides = lumbini_guides
        accommodations = lumbini_accommodations
    else:
        activities = pokhara_activities
        guides = pokhara_guides
        accommodations = pokhara_accommodations

    st.subheader("Activities")
    for activity, (min_cost, max_cost) in activities.items():
        selected = st.checkbox(activity, key=f"activity_{activity}")
        if selected:
            selected_options[activity] = (min_cost + max_cost) / 2  # Use average cost

    st.subheader("Guides")
    for guide, (min_cost, max_cost) in guides.items():
        selected = st.checkbox(guide, key=f"guide_{guide}")
        if selected:
            selected_options[guide] = (min_cost + max_cost) / 2  # Use average cost

    st.subheader("Accommodations")
    for accommodation, (min_cost, max_cost) in accommodations.items():
        selected = st.checkbox(accommodation, key=f"accommodation_{accommodation}")
        if selected:
            selected_options[accommodation] = (min_cost + max_cost) / 2  # Use average cost

    # Calculate and display the total cost
    total_cost = calculate_total(selected_options)

    # Display the selected options and their costs
    st.write("## Selected Options and Costs")
    for option, cost in selected_options.items():
        st.write(f"{option}: ${cost:.2f}")

    # Display the total cost and compare it with the user's budget
    st.write(f"**Total Cost:** ${total_cost:.2f}")
    if total_cost > budget:
        st.write("**Warning:** Your selected options exceed your budget!")
    else:
        st.write("**Success:** Your selected options are within your budget!")

    # Email input
    email = st.text_input("Enter your email address:")

    # Book Now button
    if st.button("Book Now"):
        if email:
            form_data = {
                "destination": destination,
                "selected_options": selected_options,
                "total_cost": total_cost,
                "budget": budget,
                "email": email
            }
            response = requests.post("https://formspree.io/f/xjkbzlgg", json=form_data)

            if response.status_code == 200:
                st.success("Your booking request has been sent successfully! Please wait for a follow up email within 2 business days")
            else:
                st.error("There was an error sending your booking request.")
        else:
            st.warning("Please enter your email address before booking.")

if __name__ == "__main__":
    show()
