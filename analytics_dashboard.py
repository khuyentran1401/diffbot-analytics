import streamlit as st
import pandas as pd
import os
import io
import base64
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Conversational Analytics Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Diffbot client
@st.cache_resource
def get_diffbot_client():
    """Initialize and cache the Diffbot client"""
    api_key = os.getenv("DIFFBOT_API_TOKEN")
    if not api_key:
        st.error("⚠️ Diffbot API token not found. Please add it in the sidebar.")
        return None
    
    return OpenAI(
        base_url="https://llm.diffbot.com/rag/v1",
        api_key=api_key
    )

def analyze_with_diffbot(query, model="diffbot-small-xl"):
    """Send query to Diffbot and return response"""
    client = get_diffbot_client()
    if not client:
        return "Please configure your Diffbot API token first."
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def create_ab_test_visualization(control_users, control_conversions, treatment_users, treatment_conversions):
    """Create visualization for A/B test results"""
    # Calculate rates
    control_rate = (control_conversions / control_users) * 100 if control_users > 0 else 0
    treatment_rate = (treatment_conversions / treatment_users) * 100 if treatment_users > 0 else 0
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(name='Control', x=['Conversion Rate (%)'], y=[control_rate], marker_color='lightblue'),
        go.Bar(name='Treatment', x=['Conversion Rate (%)'], y=[treatment_rate], marker_color='lightcoral')
    ])
    
    fig.update_layout(
        title='A/B Test Conversion Rates Comparison',
        yaxis_title='Conversion Rate (%)',
        barmode='group',
        showlegend=True
    )
    
    return fig

def export_results_to_csv(data, filename):
    """Export analysis results to CSV format"""
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📄 Download CSV Report</a>'
    return href

def main():
    # Header
    st.title("🤖 Conversational Analytics Dashboard")
    st.markdown("*Powered by Diffbot LLM - Get instant insights with transparent calculations*")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Diffbot API Token", 
            type="password", 
            value=os.getenv("DIFFBOT_API_TOKEN", ""),
            help="Get your free API token at app.diffbot.com/get-started"
        )
        
        if api_key:
            os.environ["DIFFBOT_API_TOKEN"] = api_key
            st.success("✅ API Token configured")
        else:
            st.warning("⚠️ Please enter your Diffbot API token")
        
        st.divider()
        
        # Model selection
        model_choice = st.selectbox(
            "Model Selection",
            ["diffbot-small-xl", "diffbot-large"],
            help="Small-XL is faster and cheaper, Large is more capable"
        )
        
        st.divider()
        
        # Usage statistics
        st.header("📊 Session Stats")
        if "query_count" not in st.session_state:
            st.session_state.query_count = 0
        st.metric("Queries Made", st.session_state.query_count)
    
    # Main interface tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 A/B Test Analyzer", 
        "🔍 Market Research", 
        "📊 Custom Analysis",
        "📋 Analysis History"
    ])
    
    # A/B Test Analysis Tab
    with tab1:
        st.header("📈 A/B Test Statistical Analysis")
        st.markdown("Compare two groups and get comprehensive statistical analysis with transparent calculations.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🅰️ Control Group")
            control_users = st.number_input("Number of Users", value=1000, min_value=1, key="control_users")
            control_conversions = st.number_input("Number of Conversions", value=50, min_value=0, key="control_conv")
            
            if control_users > 0:
                control_rate = (control_conversions / control_users) * 100
                st.metric("Conversion Rate", f"{control_rate:.2f}%")
        
        with col2:
            st.subheader("🅱️ Treatment Group")
            treatment_users = st.number_input("Number of Users", value=1000, min_value=1, key="treatment_users")
            treatment_conversions = st.number_input("Number of Conversions", value=65, min_value=0, key="treatment_conv")
            
            if treatment_users > 0:
                treatment_rate = (treatment_conversions / treatment_users) * 100
                st.metric("Conversion Rate", f"{treatment_rate:.2f}%")
                
                # Show improvement
                if control_users > 0:
                    improvement = treatment_rate - control_rate
                    st.metric("Improvement", f"{improvement:+.2f} pp", delta=f"{improvement:+.2f}")
        
        # Visualization
        if control_users > 0 and treatment_users > 0:
            fig = create_ab_test_visualization(control_users, control_conversions, treatment_users, treatment_conversions)
            st.plotly_chart(fig, use_container_width=True)
        
        if st.button("🔬 Analyze A/B Test", type="primary"):
            if not api_key:
                st.error("Please configure your Diffbot API token in the sidebar.")
                return
                
            query = f"""
            Analyze my A/B test results:
            - Control: {control_users} users with {control_conversions} conversions ({(control_conversions/control_users)*100:.2f}% conversion rate)
            - Treatment: {treatment_users} users with {treatment_conversions} conversions ({(treatment_conversions/treatment_users)*100:.2f}% conversion rate)
            
            Calculate statistical significance, p-value, confidence intervals, and interpret results.
            Provide the executable JavaScript code for calculations.
            """
            
            with st.spinner("🧮 Calculating statistical significance..."):
                result = analyze_with_diffbot(query, model_choice)
                st.session_state.query_count += 1
                
                # Store in history
                if "analysis_history" not in st.session_state:
                    st.session_state.analysis_history = []
                
                st.session_state.analysis_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "A/B Test",
                    "query": f"Control: {control_users}/{control_conversions}, Treatment: {treatment_users}/{treatment_conversions}",
                    "result": result
                })
                
                st.markdown("### 📊 Analysis Results")
                st.markdown(result)
                
                # Export option
                export_data = [{
                    "Type": "A/B Test Analysis",
                    "Control_Users": control_users,
                    "Control_Conversions": control_conversions,
                    "Treatment_Users": treatment_users,
                    "Treatment_Conversions": treatment_conversions,
                    "Analysis_Result": result.replace('\n', ' ')[:500] + "..."
                }]
                
                st.markdown(
                    export_results_to_csv(export_data, f"ab_test_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"),
                    unsafe_allow_html=True
                )
    
    # Market Research Tab
    with tab2:
        st.header("🔍 Real-time Market Research")
        st.markdown("Get current market data, trends, and benchmarks with proper source citations.")
        
        # Initialize session state for research topic
        if "research_topic" not in st.session_state:
            st.session_state.research_topic = ""
        
        research_topic = st.text_input(
            "🎯 What would you like to research?", 
            value=st.session_state.research_topic,
            placeholder="Click an example below or type your own research question...",
            help="Be specific for better results. Include year, industry, or metric type."
        )
        
        # Update session state when user types
        st.session_state.research_topic = research_topic
        
        # Example prompts for quick selection
        st.markdown("**Try these example research prompts:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📱 Mobile App Retention by Industry", use_container_width=True):
                st.session_state.research_topic = "What are mobile app retention rates by industry in 2024? Include fintech, gaming, and e-commerce benchmarks with day 1, day 7, and day 30 retention rates."
                st.rerun()
            
            if st.button("🛒 E-commerce Conversion Benchmarks", use_container_width=True):
                st.session_state.research_topic = "E-commerce conversion rate benchmarks by device type and industry for 2024. Include average order values and cart abandonment rates."
                st.rerun()
        
        with col2:
            if st.button("💰 SaaS Pricing & Conversion Trends", use_container_width=True):
                st.session_state.research_topic = "Current SaaS pricing trends for B2B software in 2024. Include average price per seat, conversion rates by company size, and freemium vs paid model performance."
                st.rerun()
                
            if st.button("📧 Email Marketing Benchmarks", use_container_width=True):
                st.session_state.research_topic = "Email marketing benchmarks 2024: open rates, click rates, and conversion rates by industry. Include data for B2B vs B2C and mobile vs desktop performance."
                st.rerun()
        
        if st.button("🔍 Research Topic", type="primary"):
            if not research_topic:
                st.warning("Please enter a research topic.")
                return
                
            if not api_key:
                st.error("Please configure your Diffbot API token in the sidebar.")
                return
            
            query = f"""
            Research current trends and data about: {research_topic}
            
            Provide:
            1. Specific statistics and metrics
            2. Recent industry data (prefer 2024 data)
            3. Cite recent, credible sources with URLs
            4. Compare different industries or segments if relevant
            5. Identify key trends and patterns
            """
            
            with st.spinner("🔍 Researching latest data..."):
                result = analyze_with_diffbot(query, model_choice)
                st.session_state.query_count += 1
                
                # Store in history
                if "analysis_history" not in st.session_state:
                    st.session_state.analysis_history = []
                
                st.session_state.analysis_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "Market Research",
                    "query": research_topic,
                    "result": result
                })
                
                st.markdown("### 📈 Research Results")
                st.markdown(result)
                
                # Export option
                export_data = [{
                    "Type": "Market Research",
                    "Topic": research_topic,
                    "Research_Result": result.replace('\n', ' ')[:1000] + "..."
                }]
                
                st.markdown(
                    export_results_to_csv(export_data, f"market_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"),
                    unsafe_allow_html=True
                )
    
    # Custom Analysis Tab
    with tab3:
        st.header("📊 Custom Data Analysis")
        st.markdown("Upload your data and get conversational analysis with executable code.")
        
        # File upload section
        uploaded_file = st.file_uploader(
            "📁 Upload CSV data", 
            type=['csv'],
            help="Upload a CSV file for analysis. Maximum file size: 200MB"
        )
        
        # Sample data option
        st.markdown("**Or try with sample data:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📈 Use Sample A/B Test Data"):
                # Create sample A/B test data
                sample_data = pd.DataFrame({
                    'user_id': range(1, 2001),
                    'group': ['control' if i < 1000 else 'treatment' for i in range(2000)],
                    'converted': [1 if (i < 1000 and i % 20 == 0) or (i >= 1000 and i % 15 == 0) else 0 for i in range(2000)]
                })
                st.session_state.sample_data = sample_data
                uploaded_file = "sample"
        
        with col2:
            if st.button("📊 Use Sample Sales Data"):
                # Create sample sales data
                dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
                sample_data = pd.DataFrame({
                    'date': dates,
                    'sales': [100 + (i % 30) * 10 + (i % 7) * 5 for i in range(len(dates))],
                    'visitors': [1000 + (i % 50) * 20 for i in range(len(dates))]
                })
                st.session_state.sample_data = sample_data
                uploaded_file = "sample"
        
        # Data analysis section
        if uploaded_file:
            if uploaded_file == "sample" and "sample_data" in st.session_state:
                df = st.session_state.sample_data
                st.success("✅ Sample data loaded!")
            else:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success("✅ File uploaded successfully!")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                    return
            
            # Data preview
            st.markdown("### 👀 Data Preview")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Rows", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            st.dataframe(df.head(10), use_container_width=True)
            
            # Data info
            with st.expander("📋 Data Information"):
                buffer = io.StringIO()
                df.info(buf=buffer)
                st.text(buffer.getvalue())
            
            # Analysis request
            analysis_request = st.text_area(
                "🎯 What analysis would you like?", 
                placeholder="e.g., Calculate seasonal trends, find correlations, predict next quarter, analyze conversion funnel",
                help="Be specific about what insights you want to discover from your data."
            )
            
            # Pre-built analysis options
            st.markdown("**Quick Analysis Options:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📈 Trend Analysis"):
                    analysis_request = "Analyze trends over time, identify seasonal patterns, and forecast future values"
            
            with col2:
                if st.button("🔗 Correlation Analysis"):
                    analysis_request = "Find correlations between variables and identify key relationships in the data"
            
            with col3:
                if st.button("📊 Summary Statistics"):
                    analysis_request = "Provide comprehensive summary statistics and identify outliers or anomalies"
            
            if st.button("🔍 Analyze Data", type="primary"):
                if not analysis_request:
                    st.warning("Please describe what analysis you'd like.")
                    return
                    
                if not api_key:
                    st.error("Please configure your Diffbot API token in the sidebar.")
                    return
                
                # Prepare data summary for analysis
                data_summary = f"""
                Dataset Overview:
                - Shape: {df.shape[0]} rows, {df.shape[1]} columns
                - Columns: {', '.join(df.columns.tolist())}
                - Data types: {df.dtypes.to_dict()}
                
                First 5 rows:
                {df.head().to_string()}
                
                Summary statistics:
                {df.describe().to_string()}
                """
                
                query = f"""
                Analyze this dataset and {analysis_request}
                
                {data_summary}
                
                Provide:
                1. Clear insights and findings
                2. Executable JavaScript or Python code for calculations
                3. Specific recommendations based on the data
                4. Any patterns or anomalies discovered
                """
                
                with st.spinner("🤖 Analyzing your data..."):
                    result = analyze_with_diffbot(query, model_choice)
                    st.session_state.query_count += 1
                    
                    # Store in history
                    if "analysis_history" not in st.session_state:
                        st.session_state.analysis_history = []
                    
                    st.session_state.analysis_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "type": "Custom Analysis",
                        "query": analysis_request,
                        "result": result
                    })
                    
                    st.markdown("### 🧠 Analysis Results")
                    st.markdown(result)
                    
                    # Export option
                    export_data = [{
                        "Type": "Custom Data Analysis",
                        "Dataset_Info": f"{df.shape[0]} rows, {df.shape[1]} columns",
                        "Analysis_Request": analysis_request,
                        "Analysis_Result": result.replace('\n', ' ')[:1000] + "..."
                    }]
                    
                    st.markdown(
                        export_results_to_csv(export_data, f"custom_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"),
                        unsafe_allow_html=True
                    )
    
    # Analysis History Tab
    with tab4:
        st.header("📋 Analysis History")
        st.markdown("Review your previous analyses and export results.")
        
        if "analysis_history" in st.session_state and st.session_state.analysis_history:
            # Display history
            for i, analysis in enumerate(reversed(st.session_state.analysis_history)):
                with st.expander(f"🕒 {analysis['timestamp']} - {analysis['type']}"):
                    st.markdown(f"**Query:** {analysis['query']}")
                    st.markdown("**Result:**")
                    st.markdown(analysis['result'][:500] + "..." if len(analysis['result']) > 500 else analysis['result'])
            
            # Export all history
            if st.button("📤 Export All History"):
                st.markdown(
                    export_results_to_csv(
                        st.session_state.analysis_history, 
                        f"analysis_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    ),
                    unsafe_allow_html=True
                )
            
            # Clear history option
            if st.button("🗑️ Clear History", type="secondary"):
                st.session_state.analysis_history = []
                st.session_state.query_count = 0
                st.success("History cleared!")
                st.rerun()
        else:
            st.info("No analysis history yet. Start by running an analysis in one of the other tabs!")
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        Built with ❤️ using Streamlit and Diffbot LLM | 
        <a href='https://github.com/yourusername/diffbot-analytics' target='_blank'>View Source</a> |
        <a href='https://app.diffbot.com/get-started' target='_blank'>Get Diffbot API Key</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()