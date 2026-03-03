import streamlit

import streamlit_flow

if "state" not in streamlit.session_state:
    state = streamlit.session_state["state"] = streamlit_flow.State([], [])

    handle_1 = streamlit_flow.Handle("top", style={"backgroundColor": "red"})
    handle_2 = streamlit_flow.Handle("top", style={"backgroundColor": "green"})
    handle_3 = streamlit_flow.Handle("bottom")
    handle_4 = streamlit_flow.Handle("left")
    handle_1.add_valid_targets(handle_2)
    node_1 = streamlit_flow.MarkdownNode(0, 50, "Hello", handles=[handle_1, handle_2, handle_3, handle_4])
    state.nodes.append(node_1)
    node_2 = streamlit_flow.MarkdownNode(50, 0, "Pop", handles=[handle_1, handle_2, handle_3, handle_4])
    state.nodes.append(node_2)
    edge = streamlit_flow.Edge(node_1, handle_1, node_2, handle_4)
    state.edges.append(edge)

state = streamlit.session_state["state"] = streamlit_flow.render(
    "A",
    streamlit.session_state["state"],
    allow_new_edges=True,
    get_edge_on_click=True,
    get_node_on_click=True,
)

print(state.selected)
