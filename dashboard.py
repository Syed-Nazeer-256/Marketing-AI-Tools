import streamlit as st
import pandas as pd
import datetime
import time
import os
import plotly.express as px
import plotly.graph_objects as go # Not explicitly used, but good to have if making complex plots
# from plotly.subplots import make_subplots # Not used in this version
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Tools Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    body, .main {
        font-family: 'Poppins', sans-serif;
        background-color: #f0f2f5; /* Light background for the whole page */
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2.5rem 1.5rem; /* Adjusted padding */
        border-radius: 15px; /* Slightly less rounded */
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.25);
        animation: slideInDown 1s ease-out;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.05"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.2;
    }
    .hero-title { font-size: 3rem; font-weight: 700; margin-bottom: 0.8rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.2); position: relative; z-index: 1; }
    .hero-subtitle { font-size: 1.2rem; font-weight: 300; opacity: 0.9; position: relative; z-index: 1; }
    
    /* Animations */
    @keyframes slideInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes slideInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.03); } 100% { transform: scale(1); } }
    
    /* Metric Cards */
    .metric-card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
    .metric-card {
        background: #ffffff; /* White background for cards */
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        text-align: center;
        animation: slideInUp 0.8s ease-out;
        border-top: 4px solid #667eea; /* Accent border */
        transition: all 0.3s ease;
    }
    .metric-card:hover { transform: translateY(-7px); box-shadow: 0 12px 30px rgba(0,0,0,0.12); }
    .metric-number { font-size: 2.5rem; font-weight: 700; color: #667eea; margin-bottom: 0.3rem; }
    .metric-label { font-size: 1rem; color: #555; font-weight: 500; }
    
    /* Chart & Form containers */
    .content-container { /* Generic container for charts, forms, tables */
        background: white;
        padding: 1.5rem; /* Adjusted padding */
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        animation: slideInUp 1s ease-out;
    }
    
    /* Table styling */
    .dataframe { animation: slideInUp 1s ease-out; border-radius: 10px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.07); }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
        border-radius: 25px; padding: 0.7rem 1.8rem; font-weight: 600; font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease; box-shadow: 0 5px 15px rgba(102, 126, 234, 0.25);
        text-transform: uppercase; letter-spacing: 0.5px;
    }
    .stButton > button:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(102, 126, 234, 0.35); animation: pulse 0.6s ease-in-out; }
    
    /* Navbar styling */
    .navbar-outer-container { display: flex; justify-content: center; width: 100%; margin-bottom: 2rem; margin-top: 1rem; animation: slideInDown 0.8s ease-out; }
    .navbar-container { background: white; padding: 0.5rem 0.7rem; border-radius: 50px; box-shadow: 0 6px 20px rgba(0,0,0,0.1); display: inline-block; }
    div[data-testid="stRadio"] > div { gap: 0.3rem; } /* Space between radio buttons */
    div[data-testid="stRadio"] label > div:first-child { /* Radio button pill */
        padding: 0.5rem 1.1rem; border-radius: 30px; background-color: #f8f9fa;
        color: #495057; font-weight: 500; transition: all 0.2s ease-in-out; border: 1px solid transparent; 
    }
    div[data-testid="stRadio"] label > div:first-child:hover { background-color: #e9ecef; color: #343a40; }
    
    /* Lottie container */
    .lottie-container { display: flex; justify-content: center; align-items: center; padding: 1rem; animation: fadeIn 1.5s ease-in; }
    
    /* Quick Stats on Dashboard */
    .quick-stats-container { padding: 1rem 0; margin-bottom:1.5rem; border-bottom: 1px solid #e0e0e0;}

    /* Footer */
    .footer { text-align: center; color: #777; padding: 1.5rem; background: #ffffff; border-radius: 12px; margin-top: 2rem; font-size:0.9rem;}
    .footer h4 {color: #667eea; margin-bottom: 0.5rem;}

    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.2rem; }
        .hero-subtitle { font-size: 1rem; }
        .metric-card-grid { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; }
        .metric-card { padding: 1rem; }
        .metric-number { font-size: 2rem; }
        .metric-label { font-size: 0.9rem; }
        .content-container { padding: 1rem; } 
        div[data-testid="stRadio"] label > div:first-child { padding: 0.4rem 0.8rem; font-size: 0.85rem; }
        .navbar-outer-container { margin-bottom: 1.5rem; margin-top: 0.5rem;}
        .stButton > button { padding: 0.6rem 1.5rem; font-size:0.9rem; }
        .quick-stats-container .stMetric {padding: 0.5rem;} 
        .quick-stats-container .stDownloadButton button { font-size: 0.85rem; padding: 0.5rem 1rem;}
        .footer {padding: 1rem; font-size:0.8rem;}
        .chart-cols-container { flex-direction: column; } /* Stack charts on mobile */
    }
    @media (max-width: 480px) { /* Even smaller screens */
        .hero-title { font-size: 1.8rem; }
        .hero-subtitle { font-size: 0.9rem; }
        .metric-card-grid { grid-template-columns: 1fr 1fr; } /* Force two columns */
         div[data-testid="stRadio"] > div { flex-wrap: wrap; justify-content: center; } 
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'data_updated' not in st.session_state:
    st.session_state.data_updated = False
if 'current_page_navbar' not in st.session_state:
    st.session_state.current_page_navbar = "🏠 Dashboard"

# --- Global Variables & Constants ---
CSV_FILE = "ai_tools_database.csv"
CSV_COLUMNS = ['Serial_Number', 'Name', 'Tool_Link', 'Category', 'Uploaded_By', 'Date_Time', 'Purpose']
UPLOADER_NAMES = ["Select your name", "Vamsi Krishna Yevvari", "Rayna", "Vijayashree", "Saakshi", "Sneha", "Sachin", "Manjunath", "Shamanth", "Swaroop", "Shahid", "Other"]
TOOL_CATEGORIES = ["Select Category", "Content Creation", "Image Generation", "Data Analysis", 
                   "Social Media Management", "Email Marketing", "SEO Tools", "Video Editing", 
                   "Voice/Audio", "Translation", "Chatbots", "Design Tools", "Analytics", 
                   "Productivity", "Research", "Code Generation", "Developer Tools", "Other"]


# --- Data Handling Functions ---
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        pd.DataFrame(columns=CSV_COLUMNS).to_csv(CSV_FILE, index=False)
    else: 
        try:
            df_existing = pd.read_csv(CSV_FILE)
            # Check and add 'Tool_Link' if missing (for backward compatibility)
            if 'Tool_Link' not in df_existing.columns and 'Name' in df_existing.columns:
                name_idx = df_existing.columns.get_loc('Name')
                df_existing.insert(name_idx + 1, 'Tool_Link', pd.NA)
                df_existing.to_csv(CSV_FILE, index=False)
        except pd.errors.EmptyDataError: 
            pd.DataFrame(columns=CSV_COLUMNS).to_csv(CSV_FILE, index=False)
        except Exception: pass 

@st.cache_data # Caching the data loading significantly improves performance
def load_data():
    initialize_csv()
    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty: return pd.DataFrame(columns=CSV_COLUMNS)
        
        # Ensure all defined columns exist, fill with NA if not
        for col in CSV_COLUMNS:
            if col not in df.columns:
                df[col] = pd.NA
        
        df['Date_Time'] = pd.to_datetime(df['Date_Time'], errors='coerce')
        df['Tool_Link'] = df['Tool_Link'].fillna('') # Ensure Tool_Link is never NaN for display
        
        # Return DataFrame with columns in the defined order
        return df[CSV_COLUMNS].sort_values('Date_Time', ascending=False)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(columns=CSV_COLUMNS)

def save_data(df):
    try:
        # Ensure DataFrame columns are in the correct order before saving
        df[CSV_COLUMNS].to_csv(CSV_FILE, index=False)
        st.session_state.data_updated = True
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False

def validate_inputs(name, tool_link, category, uploaded_by, purpose):
    errors = []
    if not name or len(name.strip()) < 2: errors.append("Tool name: min 2 characters.")
    if tool_link and not (tool_link.strip().startswith("http://") or tool_link.strip().startswith("https://")):
        errors.append("Tool link: must be a valid URL (http:// or https://).")
    if not category or category == "Select Category": errors.append("Category: please select one.")
    if not uploaded_by or uploaded_by == "Select your name": errors.append("Your Name: please select from dropdown.")
    if not purpose or len(purpose.strip()) < 5: errors.append("Purpose: min 5 characters.")
    return errors

def add_entry(name, tool_link, category, uploaded_by, purpose):
    df = load_data()
    serial_num = 1
    if not df.empty and pd.notna(df['Serial_Number'].max()): # Check if max is not NaN
        serial_num = int(df['Serial_Number'].max() + 1)
    
    new_entry_data = {
        'Serial_Number': serial_num,
        'Name': name.strip(),
        'Tool_Link': tool_link.strip() if tool_link else '',
        'Category': category,
        'Uploaded_By': uploaded_by.strip(), # .strip() in case "Other " was selected with space
        'Date_Time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Purpose': purpose.strip()
    }
    new_df_row = pd.DataFrame([new_entry_data])
    # Concatenate and ensure columns are in the correct order
    updated_df = pd.concat([new_df_row, df], ignore_index=True)[CSV_COLUMNS]
    
    if save_data(updated_df):
        st.cache_data.clear() # Crucial to clear cache after data modification
        return True
    return False

# --- UI Helper Functions ---
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=10) # Added timeout
        return r.json() if r.status_code == 200 else None
    except requests.exceptions.RequestException: # Catch specific request errors
        return None

def display_lottie(lottie_json, height=200, key_suffix=""):
    if lottie_json:
        animation_id = f"lottie-animation-{key_suffix}-{int(time.time() * 1000)}"
        st.markdown(f"""
        <div class="lottie-container">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.9.6/lottie.min.js"></script>
            <div id="{animation_id}" style="width: 100%; max-width: {height}px; height: auto;"></div>
            <script>
                var container = document.getElementById('{animation_id}');
                if (container && !container.classList.contains('lottie-rendered')) {{ // Check if already rendered
                    lottie.loadAnimation({{ 
                        container: container, 
                        renderer: 'svg', 
                        loop: true, 
                        autoplay: true, 
                        animationData: {json.dumps(lottie_json)} 
                    }});
                    container.classList.add('lottie-rendered'); // Mark as rendered
                }}
            </script>
        </div>""", unsafe_allow_html=True)

def display_navbar():
    st.markdown('<div class="navbar-outer-container"><div class="navbar-container">', unsafe_allow_html=True)
    page_options = ["🏠 Dashboard", "➕ Add Tools"]
    if st.session_state.current_page_navbar not in page_options: 
        st.session_state.current_page_navbar = page_options[0]
    
    selected_page = st.radio(
        "main_nav", 
        options=page_options,
        index=page_options.index(st.session_state.current_page_navbar),
        horizontal=True, 
        label_visibility="collapsed", 
        key="navbar_radio_selection" # Unique key for the radio widget itself
    )
    
    st.markdown('</div></div>', unsafe_allow_html=True) # Closes navbar-container and navbar-outer-container
    
    if selected_page != st.session_state.current_page_navbar:
        st.session_state.current_page_navbar = selected_page
        st.rerun() # Rerun the script to reflect page change
    return st.session_state.current_page_navbar

# --- Main Application Flow ---
page = display_navbar()

if page == "🏠 Dashboard":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    df_dashboard_data = load_data() # Load data once for this page
    
    # Quick Stats & Download Section
    st.markdown('<div class="quick-stats-container">', unsafe_allow_html=True)
    if not df_dashboard_data.empty:
        stat_cols = st.columns([2,2,3]) # Adjust column ratios as needed
        stat_cols[0].metric("Total Tools", len(df_dashboard_data))
        stat_cols[1].metric("Categories", df_dashboard_data['Category'].nunique())
        with stat_cols[2]:
            st.download_button(
                label="📥 Download Dataset", 
                data=df_dashboard_data.to_csv(index=False),
                file_name=f"ai_tools_dataset_{datetime.date.today().strftime('%Y%m%d')}.csv", 
                mime="text/csv",
                help="Download the complete dataset as CSV file.", 
                use_container_width=True
            )
    else:
        st.info("📊 No data yet. Add tools to see stats here!")
    st.markdown('</div>', unsafe_allow_html=True)

    # Hero Section
    st.markdown("""<div class="hero-container">
                    <div class="hero-title">AI Tools Dashboard</div>
                    <div class="hero-subtitle">Empowering Marketing Excellence Through AI Innovation</div>
                 </div>""", unsafe_allow_html=True)

    if df_dashboard_data.empty:
        col_center, _ = st.columns([3,1]) 
        with col_center:
             lottie_empty = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_VgJfK5.json")
             if lottie_empty: display_lottie(lottie_empty, height=300, key_suffix="empty_dashboard_lottie")
             st.markdown("<div style='text-align:center; margin-top:1rem;'><h3>No Tools Found</h3><p>Get started by adding tools using the '➕ Add Tools' page!</p></div>", unsafe_allow_html=True)
    else:
        # Metric Cards Grid
        st.markdown('<div class="metric-card-grid">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><div class="metric-number">{len(df_dashboard_data)}</div><div class="metric-label">Total AI Tools</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><div class="metric-number">{df_dashboard_data["Category"].nunique()}</div><div class="metric-label">Unique Categories</div></div>', unsafe_allow_html=True)
        recent_uploads = len(df_dashboard_data[df_dashboard_data['Date_Time'] >= (datetime.datetime.now() - datetime.timedelta(days=7))])
        st.markdown(f'<div class="metric-card"><div class="metric-number">{recent_uploads}</div><div class="metric-label">Added This Week</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><div class="metric-number">{df_dashboard_data["Uploaded_By"].nunique()}</div><div class="metric-label">Contributors</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Charts Section
        st.markdown('<div class="chart-cols-container">', unsafe_allow_html=True) # Wrapper for chart columns
        chart_cols = st.columns(2)
        with chart_cols[0]:
            st.markdown('<div class="content-container">', unsafe_allow_html=True)
            st.subheader("📊 Tools by Category")
            category_counts = df_dashboard_data['Category'].value_counts()
            fig_pie = px.pie(values=category_counts.values, names=category_counts.index, hole=0.4, 
                             color_discrete_sequence=px.colors.qualitative.Pastel) # Example color sequence
            fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=1)))
            fig_pie.update_layout(showlegend=True, height=350, font=dict(family="Poppins", size=11), 
                                  paper_bgcolor='rgba(0,0,0,0)', 
                                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with chart_cols[1]:
            st.markdown('<div class="content-container">', unsafe_allow_html=True)
            st.subheader("📈 Tools Added Over Time")
            df_time = df_dashboard_data.copy()
            df_time['Date'] = pd.to_datetime(df_time['Date_Time']).dt.date
            daily_counts = df_time.groupby('Date').size().reset_index(name='Count')
            daily_counts['Cumulative'] = daily_counts['Count'].cumsum()
            fig_line = px.line(daily_counts, x='Date', y='Cumulative', markers=True, color_discrete_sequence=['#764ba2']) # Using a partner color
            fig_line.update_traces(line=dict(width=2.5), marker=dict(size=6))
            fig_line.update_layout(height=350, font=dict(family="Poppins", size=11), 
                                   paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                   xaxis=dict(gridcolor='rgba(0,0,0,0.05)'), yaxis=dict(gridcolor='rgba(0,0,0,0.05)'))
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # Closes chart-cols-container

        # Recent Activity Table
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.subheader("🕒 Recent Activity (Top 10)")
        recent_df = df_dashboard_data.head(10).copy() # .copy() is good practice
        recent_df['Date_Time'] = pd.to_datetime(recent_df['Date_Time']).dt.strftime('%b %d, %Y %H:%M')
        display_df = recent_df.rename(columns={
            'Serial_Number': 'S.No', 'Name': 'Tool Name', 'Tool_Link': 'Link', 
            'Uploaded_By': 'Added By', 'Date_Time': 'Timestamp', 'Purpose': 'Purpose/Usage'
        })
        # Ensure only existing columns are selected for display
        cols_to_display = ['S.No', 'Tool Name', 'Link', 'Category', 'Added By', 'Timestamp', 'Purpose/Usage']
        existing_cols_for_display = [col for col in cols_to_display if col in display_df.columns]

        st.dataframe(
            display_df[existing_cols_for_display], 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "S.No": st.column_config.NumberColumn(width="small", format="%d"), 
                "Tool Name": st.column_config.TextColumn(width="medium"),
                "Link": st.column_config.LinkColumn(display_text="Visit 🔗", width="small", help="Link to tool"),
                "Category": st.column_config.TextColumn(width="small"), 
                "Added By": st.column_config.TextColumn(width="small"),
                "Timestamp": st.column_config.TextColumn(width="medium"), 
                "Purpose/Usage": st.column_config.TextColumn(width="large"),
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Closes page-container for Dashboard


elif page == "➕ Add Tools":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    
    header_cols = st.columns([3,1]) # Column for header text and Lottie
    with header_cols[0]:
        st.markdown("""<div class="hero-container" style="text-align: left; padding: 1.5rem 1.2rem; margin-bottom:1.5rem;">
                        <h1 style="font-size:2rem; margin-bottom:0.3rem;">Add New AI Tool</h1>
                        <p style="font-size:1rem; opacity:0.85;">Expand our AI toolkit for the marketing team.</p>
                     </div>""", unsafe_allow_html=True)
    with header_cols[1]:
        lottie_add = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_DMgKk1.json")
        if lottie_add: display_lottie(lottie_add, height=150, key_suffix="add_tool_page_icon")

    form_cols = st.columns([2,1]) # Columns for form and tips/recent
    with form_cols[0]:
        st.markdown('<div class="content-container">', unsafe_allow_html=True) 
        with st.form("add_tool_form", clear_on_submit=True):
            st.markdown("<h5>🛠️ Tool Information</h5>", unsafe_allow_html=True)
            
            name = st.text_input("Tool Name 🏷️", placeholder="e.g., ChatGPT, Midjourney", key="tool_name_input", help="Name of the AI tool")
            tool_link = st.text_input("Tool Link (Optional) 🔗", placeholder="e.g., https://www.example.com", key="tool_link_input", help="Direct link (optional)")
            category = st.selectbox("Category 📂", TOOL_CATEGORIES, key="tool_category_input", help="Primary function category")
            uploaded_by = st.selectbox("Your Name 👤", UPLOADER_NAMES, key="tool_uploader_input", help="Select your name")
            purpose = st.text_area("Purpose & Usage 📝", placeholder="Describe how this tool helps with marketing, its key features, and specific use cases...", key="tool_purpose_input", height=100, help="Detailed description")
            
            st.markdown("<br>", unsafe_allow_html=True) # Visual spacer
            submitted = st.form_submit_button("🚀 Add Tool to Database", use_container_width=True)
            
            if submitted:
                errors = validate_inputs(name, tool_link, category, uploaded_by, purpose)
                if errors:
                    for error in errors: st.error(f"⚠️ {error}")
                else:
                    with st.spinner("Adding tool to database..."):
                        time.sleep(0.5) 
                        if add_entry(name, tool_link, category, uploaded_by, purpose):
                            st.success("🎉 Tool added successfully!")
                            st.balloons()
                            time.sleep(1.5) 
                            st.rerun() # Rerun to clear form and update any views
                        else: 
                            st.error("❌ Failed to add tool. Please check logs or try again.")
        st.markdown('</div>', unsafe_allow_html=True) # Closes content-container for form
    
    with form_cols[1]:
        # Tips Section
        st.markdown("""
        <div class="content-container" style="background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%); color: #333;">
            <h5 style="color:#444; margin-bottom:0.5rem;">💡 Quick Tips</h5>
            <ul style="list-style-type: '✨ '; padding-left: 1.2rem; font-size:0.9rem; margin-bottom:0;">
                <li>Be specific with the tool name.</li>
                <li>Add a direct link if available.</li>
                <li>Select the most relevant category.</li>
                <li>Ensure your name is selected.</li>
                <li>Provide a clear, concise purpose.</li>
            </ul>
        </div>""", unsafe_allow_html=True)
        
        # Recent Additions Preview
        df_add_page_recent = load_data()
        if not df_add_page_recent.empty:
            st.markdown('<div class="content-container" style="margin-top:1.5rem;">', unsafe_allow_html=True)
            st.markdown("<h5 style='margin-bottom:0.7rem;'>📋 Recently Added (Top 3)</h5>", unsafe_allow_html=True)
            recent_display_cols = ['Name', 'Category', 'Uploaded_By']
            recent_display = df_add_page_recent.head(3)[recent_display_cols].rename(
                columns={'Name':'Tool', 'Category':'Type', 'Uploaded_By':'By'}
            )
            st.dataframe(recent_display, use_container_width=True, hide_index=True, height=130) 
            st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True) # Closes page-container for Add Tools

# --- Footer ---
st.markdown("<hr style='margin: 2rem 0; border-color: rgba(0,0,0,0.1);'>", unsafe_allow_html=True) # A bit more styled hr
st.markdown("""
<div class="footer">
    <h4>🤖 AI Tools Dashboard</h4>
    <p>Empowering Marketing Teams with AI Innovation</p>
    <p style="opacity: 0.7;">Streamlit App | Enhanced Version</p>
</div>""", unsafe_allow_html=True)
