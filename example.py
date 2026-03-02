import streamlit

import streamlit_flow

if "state" not in streamlit.session_state:
    state = streamlit.session_state["state"] = streamlit_flow.StreamlitFlowState([], [])

    handle_1 = streamlit_flow.StreamlitFlowHandle("top", style={"backgroundColor": "red"})
    handle_2 = streamlit_flow.StreamlitFlowHandle("top", style={"backgroundColor": "green"})
    handle_3 = streamlit_flow.StreamlitFlowHandle("bottom")
    handle_4 = streamlit_flow.StreamlitFlowHandle("left")
    node_1 = streamlit_flow.StreamlitFlowMarkdownNode(0, 50, "Hello", handles=[handle_1, handle_2, handle_3, handle_4])
    state.nodes.append(node_1)
    node_2 = streamlit_flow.StreamlitFlowMarkdownNode(50, 0, "Pop", handles=[handle_1, handle_2, handle_3, handle_4])
    state.nodes.append(node_2)
    edge = streamlit_flow.StreamlitFlowEdge(node_1, handle_1, node_2, handle_4)
    state.edges.append(edge)

state = streamlit.session_state["state"] = streamlit_flow.streamlit_flow(
    "A",
    streamlit.session_state["state"],
    allow_new_edges=True,
    get_edge_on_click=True,
    get_node_on_click=True,
)

print(state.selected)
