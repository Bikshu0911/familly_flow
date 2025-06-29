import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout

st.set_page_config(
    page_title="Raju's Family Tree",
    page_icon="👪",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Family tree data as a dictionary, now with local image paths (place images in ./)
family_tree = {
    "name": "Raju & Heroji",
    "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/raju.JPG",
    "children": [
        {
            "name": "Vasantha & Kishan",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/vasantha.JPG",
            "children": [
                {"name": "Laasya Sree", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/laasya.JPG"},
                {"name": "Jeevana", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/jeevana.JPG"},
                {"name": "Harsith", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/harsith.JPG"}
            ]
        },
        {
            "name": "Lalitha & Nandulal",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/lalli.JPG",
            "children": [
                {"name": "Goutham Deekshith", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/goutham.JPG"},
                {"name": "Yashaswi", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/lucky.JPG"}
            ]
        },
        {
            "name": "Anitha & Madhu",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/anu.JPG",
            "children": [
                {"name": "Praneeth Ram Chandru", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/praneeth.JPG"},
                {"name": "Liya Sri Varshini", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/liya.JPG"}
            ]
        },
        {
            "name": "Sunitha & Suresh",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/sunitha.JPG",
        },
        {
            "name": "Sabitha & Jagan",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/sabitha.JPG",
            "children": [
                {"name": "Jaishnavi", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/jaishnavi.JPG"}
            ]
        },
        {
            "name": "Nagamani",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/nagamani.JPG"
        },
        {
            "name": "Bikshapathi",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/bikshu.JPG"
        }
    ]
}

nodes = []
edges = []

def build_flow(tree, parent_id=None, level=1, idx=0, y_offset=0):
    node_id = f"{tree['name'].replace(' ', '_').lower()}"
    # Positioning: x by level, y by idx/y_offset
    pos = (100 * level, 100 + idx * 80 + y_offset)
    node_type = 'input' if level == 1 else ('default' if level == 2 else 'output')
    image_url = tree.get("image", "")
    if image_url:
        # Use Streamlit's static file serving for local images
        content = f"""<div style="text-align:center;">
<img src="{image_url}" alt="{tree['name']}" width="80"><br>
<b>{tree['name']}</b>
</div>"""
    else:
        content = f"<b>{tree['name']}</b>"
    node_kwargs = {
        "id": node_id,
        "pos": pos,
        "data": {"content": content},
        "node_type": node_type,
        "draggable": False
    }
    if level == 1:
        node_kwargs["source_position"] = "bottom"
    elif level == 2:
        node_kwargs["source_position"] = "bottom"
        node_kwargs["target_position"] = "top"
    else:
        node_kwargs["target_position"] = "top"
    nodes.append(StreamlitFlowNode(**node_kwargs))
    if parent_id:
        edges.append(StreamlitFlowEdge(
            f"{parent_id}-{node_id}", parent_id, node_id,
            animated=True, marker_end={'type': 'arrow'}
        ))
    # Recursively add children
    children = tree.get("children", [])
    for c_idx, child in enumerate(children):
        build_flow(child, node_id, level+1, c_idx, y_offset + idx * 80)

# Build nodes and edges from the dictionary
build_flow(family_tree)

if 'static_flow_state' not in st.session_state:
    st.session_state.static_flow_state = StreamlitFlowState(nodes, edges)


streamlit_flow(
    'static_flow',
    st.session_state.static_flow_state,
    fit_view=True,
    show_minimap=False,
    show_controls=True,
    pan_on_drag=True,
    allow_zoom=True,
    layout=TreeLayout(direction='down'),
    get_node_on_click=True,
    get_edge_on_click=True,
    enable_pane_menu=True,
    enable_node_menu=True,
    enable_edge_menu=True,
)
