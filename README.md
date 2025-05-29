# AI Tool Dashboard

A Streamlit application for managing AI tools with filtering, updating, and download capabilities.

## Features

- **AI Tool List**: Display a list of AI tools with their website links and categories
- **Category Filtering**: Filter AI tools by multiple categories
- **Update Form**: Add new AI tools or update existing ones
- **Download Button**: Export the AI tool list as an Excel file
- **Lottie Animations**: Visual feedback for loading and success states
- **Responsive UI**: Clean and intuitive interface with hover effects

## Project Structure

```
ai_tool_dashboard/
├── app.py              # Main Streamlit application
├── data/
│   └── ai_tools.csv    # CSV file containing AI tool data
├── assets/
│   └── lottie/         # Lottie animation files
│       ├── loading.json
│       ├── success.json
│       └── robot.json
└── README.md           # Documentation
```

## Requirements

- Python 3.6+
- Streamlit
- Pandas
- Openpyxl
- Streamlit-Lottie
- Requests

## Installation

1. Clone the repository or download the files
2. Install the required packages:
   ```
   pip install streamlit pandas openpyxl streamlit-lottie requests
   ```

## Usage

1. Navigate to the project directory
2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
3. The app will open in your default web browser

## Features in Detail

### AI Tool List
- Tools are displayed in a responsive card layout
- Each card shows the tool name, website link, and categories
- Cards have hover effects for better user experience

### Category Filtering
- Select multiple categories from the dropdown
- The tool list updates dynamically based on selected filters
- All unique categories are extracted from the data

### Update Form
- Add new AI tools with name, website, and categories
- Update existing tools by entering the same name
- Select from existing categories or add new ones
- Visual feedback with loading and success animations

### Excel Download
- Download the complete AI tool list as an Excel file
- Clean formatting with proper column headers
- Animation indicates the download process

## Performance Optimization

- Data caching for faster loading times
- Efficient category extraction and filtering
- Responsive UI with smooth transitions
- Optimized animations that don't impact performance

## Customization

You can customize the app by:
- Modifying the CSS styles in the `main()` function
- Adding more Lottie animations for different states
- Extending the data structure with additional fields
- Changing the color scheme to match your branding
