# ------------------------------------------------------------
# Track A - Social Network Visualization & Community Discovery
# Project: Game of Thrones Social Network Analysis
# ------------------------------------------------------------

import os
import csv
import tempfile

import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
from networkx.algorithms.community import greedy_modularity_communities


# ------------------------------------------------------------
# Streamlit Page Setup
# ------------------------------------------------------------

st.set_page_config(
    page_title="Social Network Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
        .main-title {
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 18px;
            color: #ffffff;
        }

        .section-title {
            font-size: 20px;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 12px;
            color: #ffffff;
        }

        div[data-testid="stMetric"] {
            background-color: #111827;
            padding: 14px;
            border-radius: 14px;
            border: 1px solid #2d3748;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 14px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 24px;
            font-weight: 800;
        }

        section[data-testid="stSidebar"] {
            background-color: #1f2430;
        }

        .network-wrapper {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #d9d9d9;
            background-color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# File Paths
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EDGES_FILE = os.path.join(DATA_DIR, "edges.csv")


# ------------------------------------------------------------
# Sample Data Creation
# ------------------------------------------------------------

def create_sample_edges_file():
    """
    Create a sample Game of Thrones relationships CSV file
    if the file does not already exist.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(EDGES_FILE):
        return

    sample_edges = [
        ["source", "target", "relationship", "weight"],

        ["Jon Snow", "Arya Stark", "Sibling", 5],
        ["Jon Snow", "Sansa Stark", "Sibling", 5],
        ["Jon Snow", "Bran Stark", "Sibling", 4],
        ["Arya Stark", "Sansa Stark", "Sibling", 4],
        ["Bran Stark", "Sansa Stark", "Sibling", 4],

        ["Ned Stark", "Jon Snow", "Father Figure", 5],
        ["Ned Stark", "Arya Stark", "Father", 5],
        ["Ned Stark", "Sansa Stark", "Father", 5],
        ["Ned Stark", "Bran Stark", "Father", 5],
        ["Catelyn Stark", "Sansa Stark", "Mother", 5],
        ["Catelyn Stark", "Arya Stark", "Mother", 5],
        ["Catelyn Stark", "Bran Stark", "Mother", 5],

        ["Daenerys Targaryen", "Jon Snow", "Alliance", 4],
        ["Daenerys Targaryen", "Tyrion Lannister", "Advisor", 5],
        ["Daenerys Targaryen", "Jorah Mormont", "Loyal Supporter", 5],
        ["Daenerys Targaryen", "Missandei", "Friend", 5],
        ["Daenerys Targaryen", "Grey Worm", "Commander", 4],

        ["Tyrion Lannister", "Jaime Lannister", "Sibling", 5],
        ["Tyrion Lannister", "Cersei Lannister", "Sibling Conflict", 4],
        ["Jaime Lannister", "Cersei Lannister", "Sibling", 5],
        ["Tywin Lannister", "Tyrion Lannister", "Father", 4],
        ["Tywin Lannister", "Jaime Lannister", "Father", 4],
        ["Tywin Lannister", "Cersei Lannister", "Father", 4],

        ["Cersei Lannister", "Sansa Stark", "Political Conflict", 3],
        ["Cersei Lannister", "Daenerys Targaryen", "Enemy", 5],
        ["Cersei Lannister", "Jon Snow", "Enemy", 4],

        ["Tyrion Lannister", "Jon Snow", "Friendship", 4],
        ["Tyrion Lannister", "Sansa Stark", "Marriage / Political Link", 3],
        ["Jaime Lannister", "Brienne of Tarth", "Respect", 4],
        ["Arya Stark", "The Hound", "Companion", 4],
        ["Bran Stark", "Samwell Tarly", "Knowledge Link", 3],
        ["Jon Snow", "Samwell Tarly", "Friendship", 5],
        ["Jon Snow", "Tormund Giantsbane", "Alliance", 4],
        ["Sansa Stark", "Littlefinger", "Political Manipulation", 3],
        ["Ned Stark", "Robert Baratheon", "Friendship", 5],
        ["Robert Baratheon", "Cersei Lannister", "Marriage", 4],
    ]

    with open(EDGES_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(sample_edges)


# ------------------------------------------------------------
# Load Data
# ------------------------------------------------------------

def load_edges():
    """
    Load edges from CSV file.
    Expected columns:
    source, target, relationship, weight
    """
    create_sample_edges_file()

    edges = []

    with open(EDGES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            source = row.get("source", "").strip()
            target = row.get("target", "").strip()
            relationship = (
    row.get("relationship")
    or row.get("relation")
    or "Relationship"
).strip()

            try:
                weight = int(row.get("weight", 1))
            except ValueError:
                weight = 1

            if source and target:
                edges.append({
                    "source": source,
                    "target": target,
                    "relationship": relationship,
                    "weight": weight
                })

    return edges


# ------------------------------------------------------------
# Build NetworkX Graph
# ------------------------------------------------------------

def build_graph(edges):
    """
    Build NetworkX graph from edge list.
    """
    graph = nx.Graph()

    for edge in edges:
        graph.add_edge(
            edge["source"],
            edge["target"],
            relationship=edge["relationship"],
            weight=edge["weight"]
        )

    return graph


# ------------------------------------------------------------
# Community Detection
# ------------------------------------------------------------

def detect_communities(graph):
    """
    Detect communities using greedy modularity.
    """
    if graph.number_of_nodes() == 0:
        return {}, []

    communities = list(greedy_modularity_communities(graph))

    community_map = {}
    for index, community in enumerate(communities):
        for node in community:
            community_map[node] = index

    return community_map, communities


# ------------------------------------------------------------
# Basic Network Statistics
# ------------------------------------------------------------

def get_top_actors(graph, limit=5):
    """
    Return top nodes based on degree centrality.
    """
    if graph.number_of_nodes() == 0:
        return []

    centrality = nx.degree_centrality(graph)
    sorted_actors = sorted(
        centrality.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_actors[:limit]


def get_graph_summary(graph, communities):
    """
    Return summary statistics.
    """
    if graph.number_of_nodes() == 0:
        density = 0
    else:
        density = nx.density(graph)

    return {
        "characters": graph.number_of_nodes(),
        "relationships": graph.number_of_edges(),
        "communities": len(communities),
        "density": round(density, 3)
    }


# ------------------------------------------------------------
# PyVis Network Creation
# ------------------------------------------------------------

def create_pyvis_network(graph, community_map, show_edge_labels=False, enable_physics=False):
    """
    Create interactive PyVis network.
    """
    net = Network(
        height="760px",
        width="100%",
        bgcolor="#ffffff",
        notebook=False,
        cdn_resources="in_line"
    )

    # Good layout spacing without manually forcing x/y positions
    net.barnes_hut(
        gravity=-12000,
        central_gravity=0.25,
        spring_length=220,
        spring_strength=0.03,
        damping=0.85,
        overlap=1
    )

    community_colors = [
        "#4C78A8",
        "#F58518",
        "#54A24B",
        "#E45756",
        "#72B7B2",
        "#B279A2",
        "#FF9DA6",
        "#9D755D",
        "#BAB0AC",
    ]

    degree_dict = dict(graph.degree())

    # Add all nodes first
    for node in graph.nodes():
        degree = degree_dict.get(node, 1)
        community_id = community_map.get(node, 0)
        color = community_colors[community_id % len(community_colors)]

        node_size = 18 + (degree * 3)

        net.add_node(
            node,
            label=node,
            title=f"""
            <b>{node}</b><br>
            Connections: {degree}<br>
            Community: {community_id + 1}
            """,
            color=color,
            size=node_size
        )

    # Add all edges after nodes
    for source, target, data in graph.edges(data=True):
        relationship = data.get("relationship", "Relationship")
        weight = data.get("weight", 1)

        edge_label = ""

        net.add_edge(
    source,
    target,
    label=edge_label,
    title=f"{source} → {target}<br>Relationship: {relationship}",
    value=weight,
    width=2,
    font={
        "size": 6,
        "align": "middle"
    }
)

    # Keep physics controllable from sidebar
    net.toggle_physics(enable_physics)

    return net


# ------------------------------------------------------------
# Add Custom HTML Style
# ------------------------------------------------------------

def add_custom_html_style(html_content, summary, top_actors):
    """
    Add small fixed information panel inside the HTML network.
    This panel is small and does not cover the main network.
    """
    top_actor_items = ""

    for actor, score in top_actors:
        top_actor_items += f"<li>{actor}: {score:.2f}</li>"

    custom_style = f"""
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }}

        #mynetwork {{
            width: 100% !important;
            height: 760px !important;
            border: 1px solid #ddd;
            border-radius: 12px;
        }}

        .small-info-box {{
            position: absolute;
            top: 12px;
            left: 12px;
            z-index: 999;
            background: rgba(255, 255, 255, 0.92);
            padding: 10px 12px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.12);
            font-size: 12px;
            max-width: 260px;
            line-height: 1.35;
        }}

        .small-info-box h3 {{
            margin: 0 0 6px 0;
            font-size: 14px;
        }}

        .small-info-box p {{
            margin: 3px 0;
        }}

        .small-info-box ul {{
            margin: 4px 0 0 18px;
            padding: 0;
        }}
    </style>

    <div class="small-info-box">
        <h3>Game of Thrones Network</h3>
        <p><b>Characters:</b> {summary["characters"]}</p>
        <p><b>Relationships:</b> {summary["relationships"]}</p>
        <p><b>Communities:</b> {summary["communities"]}</p>
        <p><b>Density:</b> {summary["density"]}</p>
        <p><b>Top actors:</b></p>
        <ul>
            {top_actor_items}
        </ul>
    </div>
    """

    html_content = html_content.replace("<body>", f"<body>{custom_style}")

    return html_content


# ------------------------------------------------------------
# Streamlit App
# ------------------------------------------------------------

def main():
    st.title("Game of Thrones Social Network Dashboard")

    st.caption(
        "Track A - Social Network Visualization & Community Discovery"
    )

    edges = load_edges()
    graph = build_graph(edges)
    community_map, communities = detect_communities(graph)
    summary = get_graph_summary(graph, communities)
    top_actors = get_top_actors(graph, limit=5)

    # ---------------- Sidebar Controls ----------------
    with st.sidebar:
        st.header("Dashboard Controls")

        show_edge_labels = st.checkbox(
            "Show relationship labels",
            value=False
        )

        enable_physics = st.checkbox(
            "Enable network physics",
            value=False
        )

        show_data_table = st.checkbox(
            "Show data table",
            value=False
        )

        st.divider()

        st.subheader("Project Files")
        st.write("Edge list:")
        st.code(EDGES_FILE)

    # ---------------- Small Summary Cards ----------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Characters", summary["characters"])

    with col2:
        st.metric("Relationships", summary["relationships"])

    with col3:
        st.metric("Communities", summary["communities"])

    with col4:
        st.metric("Density", summary["density"])

    # ---------------- Main Network ----------------
    st.subheader("Interactive Social Network")

    net = create_pyvis_network(
        graph=graph,
        community_map=community_map,
        show_edge_labels=show_edge_labels,
        enable_physics=enable_physics
    )

    html_content = net.generate_html()
    html_content = add_custom_html_style(
        html_content=html_content,
        summary=summary,
        top_actors=top_actors
    )

    components.html(
        html_content,
        height=790,
        scrolling=False
    )

    # ---------------- Optional Data Table ----------------
    if show_data_table:
        st.subheader("Relationship Data")

        st.dataframe(
            edges,
            use_container_width=True
        )

    # ---------------- Explanation ----------------
    with st.expander("Project Explanation"):
        st.write(
            """
            This dashboard visualizes relationships between Game of Thrones characters.
            Each node represents a character, and each edge represents a relationship.
            The network also applies community detection to identify groups of closely
            connected characters.
            """
        )

        st.write(
            """
            Larger nodes indicate characters with more connections.
            Edge labels describe the type of relationship, such as sibling, alliance,
            friendship, enemy, or political conflict.
            """
        )


# ------------------------------------------------------------
# Run App
# ------------------------------------------------------------

if __name__ == "__main__":
    main()