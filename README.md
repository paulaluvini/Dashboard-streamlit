# Streamlit Email Classification Dashboard

## Overview
This repository contains the source code for a **Streamlit dashboard** that visualizes email classification results. The dashboard connects to an API, retrieves email data, and provides insights into spam detection through various visualizations. As such, it was part of an assingment I completed for my MSc. Data Science from Universidad de San Andrés.

## Features
- Authentication via API token
- Visualization of email lengths
- Word cloud of most common terms
- Most frequent words analysis
- API usage metrics

## Repository Structure
```
├── .ebextensions/          # Configuration files for deployment
├── Dashboard_streamlit.py  # Main Streamlit dashboard script
├── Dockerfile              # Docker configuration for containerized deployment
├── app.py                  # Flask API (if applicable)
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Setup & Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run Dashboard_streamlit.py
   ```

## API Authentication
The script retrieves classified email data via an API. Ensure you replace credentials with your own in the script:
```python
URL_LOGIN = 'http://your-api-url.com/api-token-auth/'
data = {'username':'your_username','password':'your_password'}
```

## Deployment
To deploy using **Elastic Beanstalk**, ensure AWS CLI and EB CLI are installed:
```bash
eb init
eb create your-environment-name
```
For **Docker deployment**, build and run the container:
```bash
docker build -t streamlit-dashboard .
docker run -p 8501:8501 streamlit-dashboard
```
