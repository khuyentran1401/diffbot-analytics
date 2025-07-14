# 🌐 Deploying to Streamlit Cloud

Streamlit Cloud offers the easiest way to deploy your Diffbot Analytics Dashboard with zero configuration and free hosting.

## Prerequisites

- GitHub account
- Forked/copied version of this repository
- Diffbot API token

## Step-by-Step Deployment

### 1. Prepare Your Repository

1. **Fork this repository** or create your own copy on GitHub
2. **Ensure all files are committed** to your repository
3. **Verify your repository structure** matches:
   ```
   your-repo/
   ├── analytics_dashboard.py
   ├── pyproject.toml
   ├── .streamlit/config.toml
   └── README.md
   ```

### 2. Deploy to Streamlit Cloud

1. **Visit Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select your repository
   - Choose the main branch
   - Set main file path: `analytics_dashboard.py`

3. **Configure Secrets**
   - In the app settings, go to "Secrets"
   - Add your environment variables:
   ```toml
   DIFFBOT_API_TOKEN = "your_actual_diffbot_token_here"
   ```

4. **Deploy**
   - Click "Deploy!"
   - Wait for the build to complete (usually 2-3 minutes)

### 3. Access Your App

Your app will be available at:
```
https://your-username-repository-name-main-app-id.streamlit.app
```

## Configuration Options

### Custom Domain (Paid Plans)
For production deployments, consider upgrading to Streamlit Cloud's paid plans for:
- Custom domains
- Password protection
- Increased resource limits
- Priority support

### Environment Variables
Add these secrets in Streamlit Cloud settings:
```toml
# Required
DIFFBOT_API_TOKEN = "your_diffbot_token"

# Optional - for production
STREAMLIT_SHARING_MODE = "production"
```

## Monitoring and Maintenance

### App Logs
- Access logs from the Streamlit Cloud dashboard
- Monitor performance and errors
- Set up alerts for downtime

### Updates
- Push changes to your GitHub repository
- Streamlit Cloud automatically redeploys
- Check deployment status in the dashboard

### Resource Management
- Monitor app resource usage
- Optimize for Streamlit Cloud limits:
  - CPU: 1 vCPU
  - RAM: 800 MB
  - Storage: 1 GB

## Troubleshooting

### Common Issues

**Build Failed**
- Check `pyproject.toml` syntax
- Verify all dependencies are available
- Ensure Python version compatibility (3.11+)
- Note: Streamlit Cloud automatically detects and uses uv when `pyproject.toml` is present

**App Won't Start**
- Check for syntax errors in `analytics_dashboard.py`
- Verify import statements
- Review Streamlit Cloud logs

**Secrets Not Working**
- Ensure secrets are properly formatted in TOML
- Check for typos in variable names
- Restart the app after adding secrets

**API Errors**
- Verify Diffbot API token is valid
- Check API quota and limits
- Monitor API usage in Diffbot dashboard

### Performance Tips

1. **Optimize Data Processing**
   - Limit dataset sizes
   - Use caching (`@st.cache_data`)
   - Process data efficiently

2. **Reduce API Calls**
   - Cache API responses
   - Implement request throttling
   - Use session state appropriately

3. **UI Optimization**
   - Minimize complex visualizations
   - Use progressive loading
   - Optimize image sizes

## Security Best Practices

1. **API Key Management**
   - Never commit API keys to repository
   - Use Streamlit Cloud secrets
   - Rotate keys regularly

2. **Access Control**
   - Consider password protection for sensitive data
   - Monitor app usage
   - Implement rate limiting if needed

3. **Data Protection**
   - Don't store sensitive data in the app
   - Use HTTPS (automatically provided)
   - Validate user inputs

## Support

- **Streamlit Cloud Docs**: [docs.streamlit.io/streamlit-cloud](https://docs.streamlit.io/streamlit-cloud)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: [Report issues in this repository](https://github.com/yourusername/diffbot-analytics/issues)