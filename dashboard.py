import streamlit as st
import pandas as pd
import datetime
import time
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json

# Configure page
st.set_page_config(
    page_title="AI Tools Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .main {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        animation: slideInDown 1s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.1;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* Animations */
    @keyframes slideInDown {
        from { opacity: 0; transform: translateY(-50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes bounce {
        0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }
        40%, 43% { transform: translate3d(0,-30px,0); }
        70% { transform: translate3d(0,-15px,0); }
        90% { transform: translate3d(0,-4px,0); }
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        animation: slideInUp 0.8s ease-out;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .metric-number {
        font-size: 3rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
        animation: bounce 2s infinite;
    }
    
    .metric-label {
        font-size: 1.1rem;
        color: #666;
        font-weight: 500;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        animation: slideInUp 1s ease-out;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Form styling */
    .form-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        animation: slideInUp 0.8s ease-out;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Table styling */
    .dataframe {
        animation: slideInUp 1s ease-out;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        animation: pulse 0.6s ease-in-out;
    }
    
    /* Navigation styling */
    .nav-container {
        background: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        animation: slideInDown 0.8s ease-out;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success/Error messages */
    .success-message {
        animation: fadeIn 0.5s ease-in;
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.3);
    }
    
    /* Lottie container */
    .lottie-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        animation: fadeIn 1.5s ease-in;
    }
    
    /* Stats grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.1rem;
        }
        .form-container {
            padding: 2rem;
        }
        .metric-card {
            padding: 1.5rem;
        }
    }
    
    /* Page transition */
    .page-container {
        animation: fadeIn 0.5s ease-in;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_updated' not in st.session_state:
    st.session_state.data_updated = False

# File path for CSV database
CSV_FILE = "ai_tools_database.csv"

# Define CSV columns
CSV_COLUMNS = [
    'Serial_Number', 'Name', 'Tool_Link', 'Category', 'Uploaded_By', 
    'Date_Time', 'Purpose'
]

# Initialize CSV file if it doesn't exist
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=CSV_COLUMNS)
        df.to_csv(CSV_FILE, index=False)
    else:
        # Ensure existing CSV has the Tool_Link column
        try:
            df_existing = pd.read_csv(CSV_FILE)
            if 'Tool_Link' not in df_existing.columns:
                # Find index of 'Name' column
                if 'Name' in df_existing.columns:
                    name_idx = df_existing.columns.get_loc('Name')
                    df_existing.insert(name_idx + 1, 'Tool_Link', pd.NA) # Or use '' for empty string
                    df_existing.to_csv(CSV_FILE, index=False)
                else: # If 'Name' isn't there, just append, though this is less ideal
                    df_existing['Tool_Link'] = pd.NA
                    df_existing.to_csv(CSV_FILE, index=False)


        except pd.errors.EmptyDataError:
            # If file is empty, re-initialize with correct columns
            df = pd.DataFrame(columns=CSV_COLUMNS)
            df.to_csv(CSV_FILE, index=False)
        except Exception as e:
            st.warning(f"Could not update existing CSV with Tool_Link column: {e}")


# Load data from CSV
@st.cache_data
def load_data():
    initialize_csv()
    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            return pd.DataFrame(columns=CSV_COLUMNS) # Ensure empty df has all columns
        # Ensure proper data types
        df['Date_Time'] = pd.to_datetime(df['Date_Time'], errors='coerce')
        # Fill NaN in Tool_Link with empty strings if you prefer for display
        if 'Tool_Link' in df.columns:
            df['Tool_Link'] = df['Tool_Link'].fillna('')
        else: # If somehow Tool_Link is still missing after init
            df['Tool_Link'] = ''
        return df.sort_values('Date_Time', ascending=False)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(columns=CSV_COLUMNS)

# Save data to CSV
def save_data(df):
    try:
        # Ensure all columns are present before saving, matching CSV_COLUMNS order
        df_to_save = pd.DataFrame(columns=CSV_COLUMNS)
        for col in CSV_COLUMNS:
            if col in df.columns:
                df_to_save[col] = df[col]
            else:
                df_to_save[col] = pd.NA # Or appropriate default
        
        df_to_save.to_csv(CSV_FILE, index=False)
        st.session_state.data_updated = True
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False

# Validate form inputs
def validate_inputs(name, tool_link, category, uploaded_by, purpose):
    errors = []
    
    if not name or len(name.strip()) < 2:
        errors.append("Tool name must be at least 2 characters long")
    
    # Tool link is optional, but if provided, check basic format
    if tool_link and not (tool_link.strip().startswith("http://") or tool_link.strip().startswith("https://")):
        errors.append("Tool link, if provided, must be a valid URL (e.g., http://example.com)")
        
    if not category or category == "Select Category":
        errors.append("Please select a valid category")
    
    if not uploaded_by or len(uploaded_by.strip()) < 2:
        errors.append("Uploader name must be at least 2 characters long")
    
    if not purpose or len(purpose.strip()) < 5:
        errors.append("Purpose must be at least 5 characters long")
    
    return errors

# Add new entry
def add_entry(name, tool_link, category, uploaded_by, purpose):
    df = load_data()
    
    # Generate new serial number
    if df.empty or df['Serial_Number'].isna().all(): # Check if 'Serial_Number' column is all NaN
        serial_num = 1
    else:
        serial_num = df['Serial_Number'].max() + 1
    
    # Create new entry
    new_entry = {
        'Serial_Number': serial_num,
        'Name': name.strip(),
        'Tool_Link': tool_link.strip() if tool_link else '', # Add tool link
        'Category': category,
        'Uploaded_By': uploaded_by.strip(),
        'Date_Time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Purpose': purpose.strip()
    }
    
    # Add to dataframe
    new_df_row = pd.DataFrame([new_entry])
    # Ensure columns match, especially if df was empty and didn't have all columns from CSV_COLUMNS
    new_df = pd.concat([new_df_row, df], ignore_index=True).reindex(columns=CSV_COLUMNS)

    if save_data(new_df):
        st.cache_data.clear()  # Clear cache to refresh data
        return True
    return False

# Load Lottie animation
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Display Lottie animation
def display_lottie(lottie_json, height=300):
    if lottie_json:
        st.markdown(f"""
        <div class="lottie-container">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.9.6/lottie.min.js"></script>
            <div id="lottie-animation" style="width: {height}px; height: {height}px;"></div>
            <script>
                var animation = lottie.loadAnimation({{
                    container: document.getElementById('lottie-animation'),
                    renderer: 'svg',
                    loop: true,
                    autoplay: true,
                    animationData: {json.dumps(lottie_json)}
                }});
            </script>
        </div>
        """, unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h2 style="color: white; margin-bottom: 2rem;">🤖 Navigation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "",
        ["🏠 Dashboard", "➕ Add Tools"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Load current data for sidebar stats
    df_sidebar = load_data() # Use a different variable name to avoid conflict if needed
    
    if not df_sidebar.empty:
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Tools", len(df_sidebar))
        with col2:
            st.metric("Categories", df_sidebar['Category'].nunique() if 'Category' in df_sidebar.columns else 0)
        
        # Download button
        csv_data = df_sidebar.to_csv(index=False)
        st.download_button(
            label="📥 Download Dataset",
            data=csv_data,
            file_name=f"ai_tools_dataset_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download the complete dataset as CSV file",
            use_container_width=True
        )

# Main content based on selected page
if page == "🏠 Dashboard":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">AI Tools Dashboard</div>
        <div class="hero-subtitle">Empowering Marketing Excellence Through AI Innovation</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df_dashboard = load_data()
    
    if df_dashboard.empty:
        # Empty state with Lottie animation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            lottie_empty = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_VgJfK5.json")
            if lottie_empty:
                display_lottie(lottie_empty, 400)
            
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <h3>No Data Available Yet</h3>
                <p style="color: #666; font-size: 1.1rem;">Start by adding your first AI tool to see beautiful analytics!</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{len(df_dashboard)}</div>
                <div class="metric-label">Total AI Tools</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            categories_count = df_dashboard['Category'].nunique() if 'Category' in df_dashboard.columns else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{categories_count}</div>
                <div class="metric-label">Categories</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            recent_uploads = len(df_dashboard[df_dashboard['Date_Time'] >= (datetime.datetime.now() - datetime.timedelta(days=7))]) if 'Date_Time' in df_dashboard.columns else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{recent_uploads}</div>
                <div class="metric-label">This Week</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            contributors = df_dashboard['Uploaded_By'].nunique() if 'Uploaded_By' in df_dashboard.columns else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{contributors}</div>
                <div class="metric-label">Contributors</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Row
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📊 Tools by Category")
            
            if 'Category' in df_dashboard.columns:
                category_counts = df_dashboard['Category'].value_counts()
                fig_pie = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    color_discrete_sequence=px.colors.sequential.Plasma,
                    hole=0.4
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                fig_pie.update_layout(
                    showlegend=True,
                    height=400,
                    font=dict(family="Poppins, sans-serif", size=12),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📈 Tools Added Over Time")
            
            if 'Date_Time' in df_dashboard.columns:
                df_time = df_dashboard.copy()
                df_time['Date'] = pd.to_datetime(df_time['Date_Time']).dt.date
                daily_counts = df_time.groupby('Date').size().reset_index(name='Count')
                daily_counts['Cumulative'] = daily_counts['Count'].cumsum()
                
                fig_line = px.line(
                    daily_counts,
                    x='Date',
                    y='Cumulative',
                    markers=True,
                    color_discrete_sequence=['#667eea']
                )
                fig_line.update_traces(line=dict(width=3), marker=dict(size=8))
                fig_line.update_layout(
                    height=400,
                    font=dict(family="Poppins, sans-serif", size=12),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
                )
                st.plotly_chart(fig_line, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent Activity
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🕒 Recent Activity")
        
        recent_df = df_dashboard.head(10).copy()
        if not recent_df.empty:
            if 'Date_Time' in recent_df.columns:
                recent_df['Date_Time'] = pd.to_datetime(recent_df['Date_Time']).dt.strftime('%Y-%m-%d %H:%M')
            
            # Rename columns for display
            display_df = recent_df.rename(columns={
                'Serial_Number': 'S.No.',
                'Name': 'Tool Name',
                'Tool_Link': 'Link', # Renaming for display
                'Category': 'Category',
                'Uploaded_By': 'Added By',
                'Date_Time': 'Date & Time',
                'Purpose': 'Purpose/Usage'
            })
            
            # Select and order columns for display
            display_cols = ['S.No.', 'Tool Name', 'Link', 'Category', 'Added By', 'Date & Time', 'Purpose/Usage']
            # Filter out any columns that might not exist if df was malformed (defensive)
            display_cols_present = [col for col in display_cols if col in display_df.columns]

            st.dataframe(
                display_df[display_cols_present],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "S.No.": st.column_config.NumberColumn("S.No.", width="small"),
                    "Tool Name": st.column_config.TextColumn("Tool Name", width="medium"),
                    "Link": st.column_config.LinkColumn( # Make the link clickable
                        "Link", 
                        help="Direct link to the tool",
                        display_text="Visit Tool 🔗",
                        width="medium"
                    ),
                    "Category": st.column_config.TextColumn("Category", width="medium"),
                    "Added By": st.column_config.TextColumn("Added By", width="medium"),
                    "Date & Time": st.column_config.TextColumn("Date & Time", width="medium"),
                    "Purpose/Usage": st.column_config.TextColumn("Purpose/Usage", width="large"),
                }
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "➕ Add Tools":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="hero-container" style="text-align: left; padding: 2rem;">
            <h1 style="margin-bottom: 0.5rem;">Add New AI Tool</h1>
            <p style="opacity: 0.9; font-size: 1.1rem;">Expand our AI toolkit by adding new tools for the marketing team</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        lottie_add = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_DMgKk1.json")
        if lottie_add:
            display_lottie(lottie_add, 200)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("add_tool_form", clear_on_submit=True):
            st.markdown("### 🛠️ Tool Information")
            
            st.markdown("**Tool Name** 🏷️")
            name = st.text_input(
                "tool_name_label", # Unique key for label
                placeholder="e.g., ChatGPT, Claude, Midjourney",
                key="tool_name_input", # Unique key for input widget
                label_visibility="collapsed",
                help="Enter the name of the AI tool"
            )
            
            st.markdown("**Tool Link (Optional)** 🔗") # New Field Label
            tool_link = st.text_input(
                "tool_link_label", # Unique key for label
                placeholder="e.g., https://chat.openai.com",
                key="tool_link_input", # Unique key for input widget
                label_visibility="collapsed",
                help="Enter the direct link to the AI tool's website (optional)"
            )
            
            st.markdown("**Category** 📂")
            category = st.selectbox(
                "category_label", # Unique key for label
                ["Select Category", "Content Creation", "Image Generation", "Data Analysis", 
                 "Social Media Management", "Email Marketing", "SEO Tools", "Video Editing", 
                 "Voice/Audio", "Translation", "Chatbots", "Design Tools", "Analytics", "PPT Creation","Others"],
                key="category_input", # Unique key for input widget
                label_visibility="collapsed",
                help="Select the primary function category of this AI tool"
            )
            
            st.markdown("**Your Name** 👤")
            uploaded_by = st.text_input(
                "uploader_label", # Unique key for label
                placeholder="Enter your name",
                key="uploader_input", # Unique key for input widget
                label_visibility="collapsed",
                help="Enter the name of the team member adding this tool"
            )
            
            st.markdown("**Purpose & Usage** 📝")
            purpose = st.text_area(
                "purpose_label", # Unique key for label
                placeholder="Describe how this tool helps with marketing tasks, its key features, and specific use cases...",
                key="purpose_input", # Unique key for input widget
                height=120,
                label_visibility="collapsed",
                help="Provide a detailed description of how this tool is used in marketing activities"
            )
            
            col1_btn, col2_btn, col3_btn = st.columns([1, 2, 1])
            with col2_btn:
                submitted = st.form_submit_button("🚀 Add Tool to Database", use_container_width=True)
            
            if submitted:
                errors = validate_inputs(name, tool_link, category, uploaded_by, purpose) # Pass tool_link
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    with st.spinner("Adding new tool to database..."):
                        time.sleep(1)
                        if add_entry(name, tool_link, category, uploaded_by, purpose): # Pass tool_link
                            st.success("🎉 Tool added successfully!")
                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Failed to add tool. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="form-container" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
            <h3>💡 Tips for Adding Tools</h3>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 1rem;">🎯 <strong>Be Specific:</strong> Include the exact tool name</li>
                <li style="margin-bottom: 1rem;">🔗 <strong>Add Link:</strong> Provide a direct URL to the tool if available</li>
                <li style="margin-bottom: 1rem;">📂 <strong>Choose Category:</strong> Select the most relevant category</li>
                <li style="margin-bottom: 1rem;">📝 <strong>Detailed Purpose:</strong> Explain how it helps marketing</li>
                <li style="margin-bottom: 1rem;">✨ <strong>Use Cases:</strong> Include specific examples</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        df_add_tools_page = load_data() # Use a different variable name
        if not df_add_tools_page.empty:
            st.markdown("""
            <div class="form-container">
                <h3>📋 Recent Additions</h3>
            </div>
            """, unsafe_allow_html=True)
            
            recent_tools = df_add_tools_page.head(3)[['Name', 'Tool_Link', 'Category']].rename(columns={
                'Name': 'Tool',
                'Tool_Link': 'Link',
                'Category': 'Type'
            })
            
            st.dataframe(recent_tools, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem; background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%); border-radius: 15px; margin-top: 2rem;">
    <h4 style="color: #667eea; margin-bottom: 1rem;">🤖 AI Tools Dashboard</h4>
    <p style="margin-bottom: 0.5rem;">Empowering Marketing Teams with AI Innovation</p>
    <p style="font-size: 0.9rem; opacity: 0.7;">Made with ❤️ using Streamlit | Version 2.1 (with Tool Links)</p>
</div>
""", unsafe_allow_html=True)
