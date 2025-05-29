import streamlit as st
import pandas as pd
import json
import requests
from streamlit_lottie import st_lottie
import os
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="AI Tool Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load Lottie animations
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def load_lottie_file(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading animation: {e}")
        return None

# Function to load data
@st.cache_data(ttl=5)  # Cache with 5 second time-to-live for auto refresh
def load_data():
    try:
        df = pd.read_csv("data/ai_tools.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=["name", "website", "categories"])

# Function to save data
def save_data(df):
    try:
        df.to_csv("data/ai_tools.csv", index=False)
        # Clear the cache to force a reload of the data
        load_data.clear()
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# Function to get all unique categories
@st.cache_data
def get_all_categories(df):
    all_categories = []
    for cats in df["categories"].dropna():
        categories = cats.split("|")
        all_categories.extend(categories)
    return sorted(list(set(all_categories)))

# Function to convert dataframe to Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='AI Tools')
    processed_data = output.getvalue()
    return processed_data

# Main app
def main():
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4527A0;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #5E35B1;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #6200EA;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #3700B3;
        box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.2);
    }
    .download-btn {
        text-align: center;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load Lottie animations
    lottie_robot = load_lottie_file('assets/lottie/robot.json')
    lottie_loading = load_lottie_file('assets/lottie/loading.json')
    lottie_success = load_lottie_file('assets/lottie/success.json')
    
    # Header with title and animation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if lottie_robot:
            st_lottie(lottie_robot, height=150, key="robot")
    with col2:
        st.markdown('<h1 class="main-header">AI Tool Dashboard</h1>', unsafe_allow_html=True)
    with col3:
        if lottie_robot:
            st_lottie(lottie_robot, height=150, key="robot2")
    
    # Load data
    df = load_data()
    
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["📋 AI Tools", "➕ Add/Update Tool"])
    
    with tab1:
        st.markdown('<h2 class="subheader">AI Tool Explorer</h2>', unsafe_allow_html=True)
        
        # Get all categories for filtering
        all_categories = get_all_categories(df)
        
        # Category filter
        st.markdown("### Filter by Categories")
        selected_categories = st.multiselect(
            "Select categories to filter:",
            options=all_categories,
            default=[]
        )
        
        # Filter data based on selected categories
        if selected_categories:
            filtered_df = df[df["categories"].apply(
                lambda x: any(cat in str(x).split("|") for cat in selected_categories)
            )]
        else:
            filtered_df = df
        
        # Display filtered tools
        st.markdown(f"### Showing {len(filtered_df)} AI Tools")
        
        # Create columns for better display
        cols = st.columns(3)
        
        # Display tools in cards
        for i, (_, row) in enumerate(filtered_df.iterrows()):
            col_idx = i % 3
            with cols[col_idx]:
                st.markdown(f"""
                <div class="card">
                    <h3>{row['name']}</h3>
                    <p><a href="{row['website']}" target="_blank">{row['website']}</a></p>
                    <p><strong>Categories:</strong> {row['categories'].replace('|', ', ')}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Download button with animation
        st.markdown("### Download AI Tool List")
        col1, col2 = st.columns([3, 1])
        with col1:
            excel_data = to_excel(df)
            st.download_button(
                label="📥 Download as Excel",
                data=excel_data,
                file_name="ai_tools.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_button"
            )
        with col2:
            if lottie_loading:
                st_lottie(lottie_loading, height=80, key="download_animation")
    
    with tab2:
        st.markdown('<h2 class="subheader">Add or Update AI Tool</h2>', unsafe_allow_html=True)
        
        # Form for adding/updating tools
        with st.form("tool_form"):
            tool_name = st.text_input("Tool Name")
            website = st.text_input("Website URL")
            
            # Category selection with option to add new
            existing_categories = get_all_categories(df)
            selected_cats = st.multiselect(
                "Select Categories",
                options=existing_categories,
                default=[]
            )
            
            # Option to add new category
            new_category = st.text_input("Add New Category (optional)")
            
            submitted = st.form_submit_button("Save Tool")
            
            if submitted:
                if not tool_name or not website:
                    st.error("Tool name and website are required!")
                else:
                    # Show loading animation
                    if lottie_loading:
                        loading_placeholder = st.empty()
                        with loading_placeholder:
                            st_lottie(lottie_loading, height=100, key="saving_animation")
                    
                    # Process categories
                    final_categories = selected_cats.copy()
                    if new_category:
                        final_categories.append(new_category)
                    
                    categories_str = "|".join(final_categories)
                    
                    # Check if tool already exists
                    existing_tool = df[df["name"] == tool_name]
                    
                    success = False
                    if len(existing_tool) > 0:
                        # Update existing tool
                        df.loc[df["name"] == tool_name, ["website", "categories"]] = [website, categories_str]
                        success = save_data(df)
                        if success:
                            # Replace loading with success animation
                            loading_placeholder.empty()
                            if lottie_success:
                                with st.container():
                                    st_lottie(lottie_success, height=100, key="success_animation")
                            st.success(f"Updated {tool_name} successfully!")
                    else:
                        # Add new tool
                        new_row = pd.DataFrame({
                            "name": [tool_name],
                            "website": [website],
                            "categories": [categories_str]
                        })
                        df = pd.concat([df, new_row], ignore_index=True)
                        success = save_data(df)
                        if success:
                            # Replace loading with success animation
                            loading_placeholder.empty()
                            if lottie_success:
                                with st.container():
                                    st_lottie(lottie_success, height=100, key="success_animation")
                            st.success(f"Added {tool_name} successfully!")
                    
                    # Rerun to refresh the data after a short delay
                    if success:
                        import time
                        time.sleep(1.5)  # Give time to see the success animation
                        st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    main()
