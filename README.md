# Data Visualisation Final Project

Student: Abdulrahman Shaalan  
Student No: 210201916

## Project Overview

This project contains two compulsory parts:

1. **Track A - Social Network Visualization & Community Discovery**
   - Builds a character interaction network.
   - Uses weighted edges to represent relationship strength.
   - Applies Louvain community detection.
   - Scales node size using degree centrality.
   - Exports an interactive HTML network visualization.

2. **Track B - Real-Time Data Visualization**
   - Builds a live Bitcoin monitoring dashboard.
   - Uses CoinGecko API through REST polling.
   - Displays current price, 24h change, sliding-window price movement, connection status, and alerts.
   - Uses conditional formatting when the selected threshold is exceeded.

## Folder Structure

```text
Data_Visualisation_Final_Project/
│
├── track_a_social_network/
│   ├── data/
│   │   ├── edges.csv
│   │   └── nodes.csv
│   ├── social_network_analysis.py
│   └── output/
│
├── track_b_realtime_dashboard/
│   └── crypto_dashboard.py
│
├── report/
│   ├── technical_report.pdf
│   └── technical_report_draft.md
│
├── README.md
└── requirements.txt
```

## Installation

Open a terminal in the main project folder and run:

```bash
pip install -r requirements.txt
```

## Run Track A

```bash
python track_a_social_network/social_network_analysis.py
```

Output files:

```text
track_a_social_network/output/social_network.html
track_a_social_network/output/node_metrics_summary.csv
```

Open `social_network.html` in a browser to view the interactive network.

## Run Track B

```bash
streamlit run track_b_realtime_dashboard/crypto_dashboard.py
```

The Streamlit app will open in the browser. It updates automatically based on the selected refresh interval.

## Data Sources and Tools

- Track A uses a small prepared character interaction dataset stored in `edges.csv` and `nodes.csv`.
- Track B uses the CoinGecko Simple Price API.
- Network analysis is implemented with NetworkX.
- The interactive network is exported with PyVis.
- The real-time dashboard is implemented with Streamlit.

## Submission Notes

Upload this full folder to Google Drive, OneDrive, or Dropbox. Make sure the sharing setting is:

```text
Anyone with the link can view
```
