import streamlit as st
import pandas as pd
import hashlib
import os
import re
import pickle as pk
import time
import random
import string

# Load model
model = pk.load(open('model.pkl','rb'))

# CSV Database
CSV_FILE = "users2.csv"
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Username", "Email", "Password"])
    df.to_csv(CSV_FILE, index=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_password(password):
    return len(password) > 8 and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

def register_user(username, email, password):
    df = pd.read_csv(CSV_FILE)
    if username in df["Username"].values:
        return False  # User already exists
    new_user = pd.DataFrame([[username, email, hash_password(password)]], columns=["Username", "Email", "Password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return True

def authenticate_user(username, password):
    df = pd.read_csv(CSV_FILE)
    hashed_password = hash_password(password)
    user = df[(df["Username"] == username) & (df["Password"] == hashed_password)]
    return not user.empty

def email_exists_in_database(email):
    """Check if the email exists in your user database."""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return email in df["Email"].values
    return False

def update_user_password(email, new_password):
    """Update the user's password in your database."""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        if email in df["Email"].values:
            hashed_password = hash_password(new_password)
            df.loc[df["Email"] == email, "Password"] = hashed_password
            df.to_csv(CSV_FILE, index=False)
            return True
    return False

def logout():
    st.session_state["authenticated"] = False
    st.session_state["page"] = "Login"
    st.rerun()
def show_loading():
    with st.spinner("🔮 Processing..."):
        time.sleep(2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def reset_password(email):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        if email in df["Email"].values:
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            hashed_new_password = hash_password(new_password)
            df.loc[df["Email"] == email, "Password"] = hashed_new_password
            df.to_csv(CSV_FILE, index=False)
            return new_password  # In a real app, send via email instead
        else:
            return None
    return None

st.session_state.setdefault("page", "Login")

# UI Styling with transparent buttons, neon effects, and nature-inspired animation
st.markdown("""
    <style>
        body {background-color: #0d0d0d; color: #fff;}
        .main {text-align: center;}
        .stButton>button {background-color: rgba(0, 0, 0, 0.2); color: white; border-radius: 10px; border: 2px solid #00ffff; transition: all 0.3s ease-in-out;}
        .stTextInput>div>div>input {background-color: #222; color: white; border: 1px solid #00ffff; padding: 8px; border-radius: 8px;}
        .stButton>button:hover {box-shadow: 0 0 20px #00ffff; transform: scale(1.05);}
        @keyframes neonGlow {
            0% {box-shadow: 0 0 5px #00ffff;}
            50% {box-shadow: 0 0 20px #00ffff;}
            100% {box-shadow: 0 0 5px #00ffff;}
        }
        .stTextInput>div>div>input:focus {animation: neonGlow 1.5s infinite alternate;}
        @keyframes futuristicGlow {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        body {background: linear-gradient(270deg, #0d0d0d, #002222, #003333, #005555); background-size: 400% 400%; animation: futuristicGlow 10s ease infinite;}
        
        /* Nature-Inspired Animation */
        @keyframes natureBackground {
            0% {background-image: url('https://source.unsplash.com/1600x900/?clouds');}
            50% {background-image: url('https://source.unsplash.com/1600x900/?forest');}
            100% {background-image: url('https://source.unsplash.com/1600x900/?water');}
        }
        .nature-bg {animation: natureBackground 15s infinite alternate ease-in-out;}
    </style>
""", unsafe_allow_html=True)

# 

# Navigation Logic
if st.session_state["page"] == "Sign Up":
    st.title("🌀 Create Identity")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        show_loading()
        if not is_valid_password(password):
            st.error("Password must be more than 8 characters and include a special character.")
        elif password == confirm_password:
            if register_user(username, email, password):
                st.success("Account created! Go to Login page.")
                st.session_state["page"] = "Login"
                st.rerun()
            else:
                st.error("Username already exists.")
        else:
            st.error("Passwords do not match.")
    if st.button("Go to Login"):
        st.session_state["page"] = "Login"
        st.rerun()

elif st.session_state["page"] == "Forgot Password":
    st.title("🔁🔑 Recover Password")
    email = st.text_input("Enter your registered email")
    
    # Only show password fields if email is entered
    if email:
        new_password = st.text_input("Enter new password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        
        if st.button("Set New Password"):
            # First verify email exists
            if email_exists_in_database(email):
                if new_password == confirm_password:
                    # Update password in database
                    success = update_user_password(email, new_password)
                    if success:
                        st.success("Password updated successfully!")
                        st.info("You can now login with your new password.")
                    else:
                        st.error("Failed to update password. Please try again.")
                else:
                    st.error("Passwords do not match. Please try again.")
            else:
                st.error("Email not found. Please check and try again.")
    
    if st.button("Back to Login"):
        st.session_state["page"] = "Login"
        st.rerun()

        

elif st.session_state["page"] == "Login":
    # Your login page code here
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
        margin-bottom: 30px;
        color: #1E88E5;
    }
    .login-container {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        max-width: 500px;
        margin: 0 auto;
    }
    .btn-custom {
        background-color: #1E88E5;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .divider {
        margin: 25px 0;
        text-align: center;
        position: relative;
    }
    .divider:before {
        content: "";
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background-color: #e0e0e0;
        z-index: 1;
    }
    .divider-text {
        background-color: #f8f9fa;
        display: inline-block;
        position: relative;
        z-index: 2;
        padding: 0 10px;
        color: #757575;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with animation
    st.markdown('<h1 class="main-header">🔑 Login Access</h1>', unsafe_allow_html=True)
    
    # Start login container
    st.markdown('<div class="login-contaier">', unsafe_allow_html=True)
    
    # Initialize the trigger in session state if not already present
    if "login_trigger" not in st.session_state:
        st.session_state["login_trigger"] = False
    
    # Function to handle login attempt
    def login_attempt():
        st.session_state["login_trigger"] = True
    
    # Function to check credentials and redirect
    def process_login():
        if authenticate_user(st.session_state.get("username", ""), 
                          st.session_state.get("password", "")):
            # Add a loading spinner for better user experience
            with st.spinner("Logging you in..."):
                time.sleep(0.8)  # Short delay for visual effect
            st.success("Access Granted! Welcome back.")
            st.session_state["page"] = "Upload"
            st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")
    
    # Username and password inputs with session state keys
    st.markdown("### 📲 Enter")
    username = st.text_input("Username", key="username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", key="password", placeholder="Enter your password", on_change=login_attempt)
    
    # Remember me checkbox
    remember_me = st.checkbox("Remember me", value=False)
    
    # Check if login was triggered by Enter key
    if st.session_state["login_trigger"]:
        process_login()
        st.session_state["login_trigger"] = False
    
    # Regular login button with full width and custom styling
    if st.button("Login", use_container_width=True, type="primary"):
        process_login()
    
    # Divider
    st.markdown('<div class="divider"><span class="divider-text">OR</span></div>', unsafe_allow_html=True)
    
    # Navigation buttons in columns
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Forgot Password?", use_container_width=True):
            st.session_state["page"] = "Forgot Password"
            st.rerun()
    with col2:
        if st.button("Sign Up", use_container_width=True):
            st.session_state["page"] = "Sign Up"
            st.rerun()
    
        # Footer
    st.markdown("""
    <style>
    @keyframes moveText {
        0% { transform: translateX(-100%); }
        50% { transform: translateX(10%); }
        100% { transform: translateX(0); }
    }
    
    .moving-text {
        text-align: center;
        margin-top: 30px;
        font-size: 12px;
        color: #757575;
        animation: moveText 3s ease-out forwards;
    }
    </style>
    
    <div class="moving-text">
        Welcome...! to Car Price Prediction
    </div>
    """, unsafe_allow_html=True)

    
elif st.session_state["page"] == "Upload":
    st.title("📂 Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        st.session_state["uploaded_data"] = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.session_state["page"] = "Preview"
        st.rerun()
        
if st.session_state["page"] == "Preview":
    st.title("🔍 Preview Dataset")
    if "uploaded_data" in st.session_state and st.session_state["uploaded_data"] is not None:
        df = st.session_state["uploaded_data"]
        st.dataframe(df, use_container_width=True, height=300)
        if st.button("TEST | TRAIN"):
            st.session_state["page"] = "Prediction"
            st.rerun()
        if st.button("Preview Dataset"):
            st.write(df.head())
    else:
        st.warning("No file uploaded. Go to the upload page.")
        if st.button("Back to Upload"):
            st.session_state["page"] = "Upload"
            st.rerun()


if st.session_state.get("page") == "Prediction":
    # This will only show when the page is set to "Prediction"
    st.markdown(
        """
        <marquee behavior="scroll" direction="left" scrollamount="10" style="font-size:40px; color:#00ffa3;">
          🏁 🏎️ Car Price Prediction ML Model 🏎️💨
        </marquee>
        """,
        unsafe_allow_html=True
    )

    st.title("Car Price Estimator")

    try:
        cars_data = pd.read_csv('Cardetails.csv')  # Ensure correct path
    except FileNotFoundError:
        st.error("Error: Cardetails.csv not found. Please check the file path.")
        st.stop()

    cars_data['name'] = cars_data['name'].apply(lambda x: x.split(' ')[0].strip())

    name = st.selectbox('Select Car Brand', cars_data['name'].unique())
    year = st.slider('Car Manufactured Year', 1994, 2024)
    km_driven = st.slider('No of kms Driven', 11, 200000)
    fuel = st.selectbox('Fuel type', cars_data['fuel'].unique())
    seller_type = st.selectbox('Seller type', cars_data['seller_type'].unique())
    transmission = st.selectbox('Transmission type', cars_data['transmission'].unique())
    owner = st.selectbox('Owner Type', cars_data['owner'].unique())
    mileage = st.slider('Car Mileage', 10, 40)
    engine = st.slider('Engine CC', 700, 5000)
    max_power = st.slider('Max Power', 0, 200)
    seats = st.slider('No of Seats', 5, 10)

    # Predict button will only appear on the "Prediction" page
    if st.button("🔮 Predict Price"):
        # Prepare input data for prediction
        input_data = pd.DataFrame(
            [[name, year, km_driven, fuel, seller_type, transmission, owner, mileage, engine, max_power, seats]],
            columns=['name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner',
                     'mileage', 'engine', 'max_power', 'seats']
        )

        # Encoding for categorical columns
        encoding = {
            'owner': {'First Owner': 1, 'Second Owner': 2, 'Third Owner': 3, 'Fourth & Above Owner': 4, 'Test Drive Car': 5},
            'fuel': {'Diesel': 1, 'Petrol': 2, 'LPG': 3, 'CNG': 4},
            'seller_type': {'Individual': 1, 'Dealer': 2, 'Trustmark Dealer': 3},
            'transmission': {'Manual': 1, 'Automatic': 2}
        }

        # Apply encoding
        for column, mapping in encoding.items():
            input_data[column] = input_data[column].map(mapping)

        # Convert 'name' column to category codes (encoded)
        input_data['name'] = input_data['name'].astype('category').cat.codes

        # Now use 'input_data' in the model prediction
        try:
            price = model.predict(input_data)[0]  # Change 'features' to 'input_data'
            st.success(f"💰 Estimated Price: ₹{price:,.2f}")
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
