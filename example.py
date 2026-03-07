import streamlit

import streamlit_flow


def add_node():
    new_node = streamlit_flow.MarkdownNode(
        0,
        50,
        "New",
        handle_ids={handle.id for handle in streamlit.session_state["handles"]},
    )

    streamlit.session_state["state"].nodes.append(new_node)


if "state" not in streamlit.session_state:
    state = streamlit.session_state["state"] = streamlit_flow.Diagram([], [], [], [])

    handle_1 = streamlit_flow.Handle("top", style={"backgroundColor": "red"})
    state.handles.append(handle_1)
    handle_2 = streamlit_flow.Handle("top", style={"backgroundColor": "green"})
    state.handles.append(handle_2)
    handle_3 = streamlit_flow.Handle("bottom")
    state.handles.append(handle_3)
    handle_4 = streamlit_flow.Handle("left")
    state.handles.append(handle_4)

    handle_1.add_valid_targets(handle_2.id)

    handles = streamlit.session_state["handles"] = [handle_1, handle_2, handle_3, handle_4]

    node_1 = streamlit_flow.MarkdownNode(0, 50, "Hello", handle_ids={handle.id for handle in handles})
    state.nodes.append(node_1)
    node_2 = streamlit_flow.MarkdownNode(50, 0, "Pop", handle_ids={handle.id for handle in handles})
    state.nodes.append(node_2)

streamlit.button("Add", on_click=add_node)

state = streamlit.session_state["state"] = streamlit_flow.render(
    "A",
    streamlit.session_state["state"],
    allow_new_edges=True,
    get_edge_on_click=True,
    get_node_on_click=True,
)

print(state.selected_id)
