# Data Visualization Final Project

## Project Title
Data Visualization Final Project: Social Network Analysis and Live Crypto Monitoring Dashboard

## Group Members
- OSAMA MUSTAFA ELTAYEB - 220208982
- KHALED BA GERI - 220208883
- WALEED AHMED AWADH AL-FAREH - 230208818
- ALI AHMED AWADH AL-FAREH - 230208822



## Project Overview
This project contains two required data visualization tracks:

1. **Track A: Social Network Visualization & Community Discovery**
2. **Track B: Real-Time Data Visualization Dashboard**

The goal of the project is to design clear, interactive, and meaningful visualizations that help users understand network structures and real-time temporal changes.

---

# Track A: Social Network Visualization & Community Discovery

## Description
Track A analyzes a Game of Thrones character network. Each node represents a character, and each edge represents a relationship between two characters.

The dashboard visualizes:
- Character relationships
- Community groups
- Key actors based on degree centrality
- Relationship strength using edge thickness

## Dataset
The network data is stored in:

```text
track_a_social_network/data/edges.csv
track_a_social_network/data/nodes.csv


###### How to Run Track A
**From the project root folder, run:
py -m streamlit run .\track_a_social_network\social_network_analysis.py

For macOS or Linux:
python -m streamlit run track_a_social_network/social_network_analysis.py


###### Track B: Real-Time Data Visualization Dashboard
**Description

Track B is a live crypto monitoring dashboard built with Streamlit. It monitors cryptocurrency price movement and displays recent changes using a sliding-window line chart.


###### Live App Link

Replace the placeholder below with the deployed Streamlit app link:
[https://data-visualization-final-project-ihooixvaftnea5yhhxyz9f.streamlit.app]
(https://data-visualization-final-project-ihooixvaftnea5yhhxyz9f.streamlit.app)

###### How to Run Track B Locally

From the project root folder, run:

py -m streamlit run .\track_b_realtime_dashboard\crypto_dashboard.py

For macOS or Linux:

python -m streamlit run track_b_realtime_dashboard/crypto_dashboard.py

If another Streamlit app is already running, use a different port:

py -m streamlit run .\track_b_realtime_dashboard\crypto_dashboard.py --server.port 8502

**Installation**

Install all required libraries using:

py -m pip install -r requirements.txt

For macOS or Linux:

python -m pip install -r requirements.txt

###### Required Libraries

The project uses the following Python libraries:

streamlit
pandas
plotly
requests
networkx
pyvis
matplotlib
python-louvain
streamlit-autorefresh

###### Project Structure
Data_Visualisation_Final_Project/
│
├── README.md
├── requirements.txt
│
├── track_a_social_network/
│   ├── social_network_analysis.py
│   ├── data/
│   │   ├── edges.csv
│   │   └── nodes.csv
│   └── output/
│
└── track_b_realtime_dashboard/
    └── crypto_dashboard.py
