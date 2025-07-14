# 🤖 Diffbot Conversational Analytics Dashboard

Transform your data analysis workflow with AI that executes real code and provides transparent calculations. This Streamlit application demonstrates how to build conversational analytics using [Diffbot LLM](https://diffy.chat/) for A/B testing, market research, and custom data analysis.

## ✨ Features

### 📈 A/B Test Analyzer
- Input control and treatment group data
- Get comprehensive statistical analysis with p-values, confidence intervals
- View interactive visualizations of conversion rates
- Export results with transparent JavaScript calculations

### 🔍 Real-time Market Research  
- Research any topic with current data and proper citations
- Quick access to common benchmarks (mobile app, e-commerce, SaaS)
- Get industry statistics with source attribution
- Export research findings

### 📊 Custom Data Analysis
- Upload CSV files for conversational analysis
- Built-in sample datasets for immediate testing
- Request specific analyses (trends, correlations, predictions)
- Executable code provided for all calculations

### 📋 Session Management
- Track analysis history across your session
- Export all results to CSV format
- API usage monitoring
- Clear, intuitive interface

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Diffbot API token ([Get free token](https://app.diffbot.com/get-started))

### Installation

1. **Install uv (if not already installed)**
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or with pip
   pip install uv
   ```

2. **Clone or download this repository**
   ```bash
   git clone https://github.com/yourusername/diffbot-analytics.git
   cd diffbot-analytics
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your DIFFBOT_API_TOKEN
   ```

5. **Run the application**
   ```bash
   uv run streamlit run analytics_dashboard.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended)
**Free hosting with zero configuration**

1. Fork this repository to your GitHub account
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository and `analytics_dashboard.py`
5. Add `DIFFBOT_API_TOKEN` to Streamlit Cloud secrets
6. Deploy with one click!

Your app will be available at: `https://your-username-diffbot-analytics-main.streamlit.app`

### Option 2: Docker Deployment
**For self-hosting or production environments**

1. **Build the Docker image**
   ```bash
   docker build -t diffbot-analytics .
   ```

2. **Run with environment variables**
   ```bash
   docker run -p 8501:8501 -e DIFFBOT_API_TOKEN=your_token diffbot-analytics
   ```

3. **Or use Docker Compose**
   ```bash
   docker-compose up
   ```

### Option 3: Local Development
**For testing and development**

```bash
# Install dependencies
uv sync

# Set environment variable
export DIFFBOT_API_TOKEN=your_token_here

# Run locally
uv run streamlit run analytics_dashboard.py
```

## 📊 Usage Examples

### A/B Test Analysis
1. Navigate to the "A/B Test Analyzer" tab
2. Enter your control group data (users and conversions)
3. Enter your treatment group data
4. Click "Analyze A/B Test"
5. Get statistical significance, p-values, and confidence intervals
6. Download results as CSV

### Market Research
1. Go to "Market Research" tab
2. Enter your research topic (e.g., "mobile app retention rates 2024")
3. Or use quick research buttons
4. Get current industry data with citations
5. Export findings

### Custom Data Analysis
1. Switch to "Custom Analysis" tab
2. Upload your CSV file or use sample data
3. Describe your analysis needs
4. Get insights with executable code
5. Export comprehensive results

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```env
DIFFBOT_API_TOKEN=your_diffbot_api_token_here
```

### Streamlit Configuration
The app includes custom styling in `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## 📁 Project Structure

```
diffbot-analytics/
├── analytics_dashboard.py      # Main Streamlit application
├── pyproject.toml             # Python project configuration and dependencies
├── uv.lock                   # Dependency lock file (auto-generated)
├── .env.example              # Environment variable template
├── .gitignore               # Git ignore rules
├── Dockerfile               # Docker container setup
├── docker-compose.yml       # Docker Compose configuration
├── README.md               # This documentation
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
├── sample_data/
│   ├── ab_test_sample.csv  # Sample A/B test data
│   └── sales_data_sample.csv # Sample sales data
└── deploy/
    ├── streamlit_cloud.md  # Streamlit Cloud deployment guide
    └── docker_deploy.md    # Docker deployment guide
```

## 🔒 Security Best Practices

- **Never commit API keys** to version control
- **Use environment variables** for sensitive configuration
- **Enable rate limiting** in production environments
- **Implement user authentication** for production deployments
- **Monitor API usage** to prevent quota exhaustion

## 🚨 Troubleshooting

### Common Issues

**"Diffbot API token not found" error**
- Ensure your `.env` file contains `DIFFBOT_API_TOKEN=your_token`
- Check that the token is valid at [app.diffbot.com](https://app.diffbot.com)

**"ModuleNotFoundError" when running**
- Install dependencies: `uv sync`
- Ensure you're running with: `uv run streamlit run analytics_dashboard.py`

**Slow API responses**
- Try the `diffbot-small-xl` model for faster responses
- Check your internet connection
- Verify API quota remaining

**CSV upload issues**
- Ensure file is valid CSV format
- Check file size (max 200MB)
- Verify column headers don't contain special characters

## 📈 Performance Tips

1. **Use caching** - The app caches the Diffbot client for better performance
2. **Choose appropriate models** - Use `diffbot-small-xl` for speed, `diffbot-large` for complex analysis
3. **Limit data size** - Large datasets may hit API limits; consider sampling
4. **Monitor usage** - Track API calls in the sidebar

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to your branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🔗 Related Resources

- [Diffbot LLM Documentation](https://docs.diffbot.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Original Article: Transparent Calculations and Real-Time Research](https://codecut.ai/conversational-ai-code-execution-data-analysis/)
- [CodeCut AI Blog](https://codecut.ai/) - More data science tutorials

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/diffbot-analytics/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/diffbot-analytics/discussions)
- **Email**: your-email@example.com

---

Built with ❤️ using [Streamlit](https://streamlit.io/) and [Diffbot LLM](https://diffy.chat/)