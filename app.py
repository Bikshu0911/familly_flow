import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout
from streamlit_js_eval import streamlit_js_eval

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

with open("main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get the viewport height from the browser
# page_width = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH',  want_output = True,)

# Family tree data as a dictionary, now with local image paths (place images in ./)
family_tree = {
    "name": "Raju & Heroji",
    "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/raju.JPG",
    "marries": 1,
    "children": [
        {
            "name": "Vasantha & Kishan",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/vasantha.JPG",
            "marries": 1,
            "children": [
                {"name": "Laasya Sree", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/laasya.JPG", "marries": 0},
                {"name": "Jeevana", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/jeevana.JPG", "marries": 0},
                {"name": "Harsith", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/harsith.JPG", "marries": 0}
            ]
        },
        {
            "name": "Lalitha & Nandulal",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/lalli.JPG",
            "marries": 1,
            "children": [
                {"name": "Goutham Deekshith", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/goutham.JPG", "marries": 0},
                {"name": "Yashaswi", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/lucky.JPG", "marries": 0}
            ]
        },
        {
            "name": "Anitha & Madhu",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/anu.JPG",
            "marries": 1,
            "children": [
                {"name": "Praneeth Ram Chandru", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/praneeth.JPG", "marries": 0},
                {"name": "Liya Sri Varshini", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/liya.JPG", "marries": 0}
            ]
        },
        {
            "name": "Sunitha & Suresh",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/sunitha.JPG",
            "marries": 1,
        },
        {
            "name": "Sabitha & Jagan",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/sabitha.JPG",
            "marries": 1,
            "children": [
                {"name": "Jaishnavi", "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/jaishnavi.JPG", "marries": 0}
            ]
        },
        {
            "name": "Nagamani",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/nagamani.JPG",
            "marries": 0
        },
        {
            "name": "Bikshapathi",
            "image": "https://raw.githubusercontent.com/Bikshu0911/familly_flow/main/photos/bikshu.JPG",
            "marries": 0
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
    marries = tree.get("marries", 0)
    # Set border color based on marries value
    border_color = "red" if marries == 1 else "green"
    style = {
        "border": f"3px solid {border_color}",
        "borderRadius": "10px",
        "background": "#fff"
    }
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
        "draggable": True,
        "style": style
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


# height=int(int(page_width) * (10 / 16)) - 50

streamlit_flow(
    'static_flow',
    st.session_state.static_flow_state,
    fit_view=True,
    show_minimap=False,
    show_controls=False,
    pan_on_drag=True,
    allow_zoom=True,
    layout=TreeLayout(direction='down'),
    get_node_on_click=True,
    get_edge_on_click=True,
    enable_pane_menu=True,
    enable_node_menu=True,
    enable_edge_menu=True,
    # height=height,
    hide_watermark=True
)
