import React, { useRef, useEffect, useState, useMemo } from "react"
import {
    Streamlit,
} from "streamlit-component-lib"
import { v4 as uuidv4 } from 'uuid';
import ReactFlow, {
    Controls,
    Background,
    MiniMap,
    useNodesState,
    useEdgesState,
    addEdge,
    ReactFlowProvider,
    useNodesInitialized,
    useReactFlow,
} from 'reactflow';

import 'reactflow/dist/style.css';
import 'bootstrap/dist/css/bootstrap.css';
import "bootstrap-icons/font/bootstrap-icons.css";

import './style.css';

import {StreamlitFlowMarkdownNode} from "./components/StreamlitFlowMarkdownNode";
import createElkGraphLayout from "./layouts/ElkLayout";

const StreamlitFlowComponent = (props) => {    
    const [viewFitAfterLayout, setViewFitAfterLayout] = useState(null);
    const [nodes, setNodes, onNodesChange] = useNodesState(props.args.nodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(props.args.edges);
    const [lastUpdateTimestamp, setLastUpdateTimestamp] = useState(props.args.timestamp);
    const [layoutNeedsUpdate, setLayoutNeedsUpdate] = useState(false);
    

    const [connectingNodeId, setConnectingNodeId] = useState(null)
    const [connectingHandleId, setConnectingHandleId] = useState(null)
    const [validTargetHandleIds, setValidTargetHandleIds] = useState(null);
    
    const [layoutCalculated, setLayoutCalculated] = useState(false);

    const nodesInitialized = useNodesInitialized({'includeHiddenNodes': false});


    const ref = useRef(null);
    const {fitView, getNodes, getEdges} = useReactFlow();

    const nodeTypes = useMemo(() => ({StreamlitFlowMarkdownNode: (props) => <StreamlitFlowMarkdownNode {...props} connectingNodeId={connectingNodeId} connectingHandleId={connectingHandleId} validTargetHandleIds={validTargetHandleIds}/>,}), [connectingNodeId,connectingHandleId,validTargetHandleIds]);

    // Helper Functions
    const handleLayout = () => {
        createElkGraphLayout(getNodes(), getEdges(), props.args.layoutOptions)
            .then(({nodes, edges}) => {
                setNodes(nodes);
                setEdges(edges);
                setViewFitAfterLayout(false);
                handleDataReturnToStreamlit(nodes, edges, null);
                setLayoutCalculated(true);
            })
            .catch(err => console.log(err));
    }

    const handleDataReturnToStreamlit = (_nodes, _edges, selectedId) => {

        const timestamp = (new Date()).getTime();
        setLastUpdateTimestamp(timestamp);
        Streamlit.setComponentValue({'nodes': _nodes, 'edges': _edges, 'selectedId': selectedId, 'timestamp': timestamp});
    }

    useEffect(() => Streamlit.setFrameHeight());

    // Layout calculation
    useEffect(() => {
        if(nodesInitialized && !layoutCalculated)
            handleLayout();
    }, [nodesInitialized, layoutCalculated]);

    // Update elements if streamlit sends new arguments - check by comparing timestamp recency
    useEffect(() => {
        if (lastUpdateTimestamp <= props.args.timestamp)
        {
            setLayoutNeedsUpdate(true);
            setNodes(props.args.nodes);
            setEdges(props.args.edges);
            setLastUpdateTimestamp((new Date()).getTime());
            handleDataReturnToStreamlit(props.args.nodes, props.args.edges, null);
        }

    }, [props.args.nodes, props.args.edges]);

    // Handle layout when streamlit sends new state
    useEffect(() => {
        if(layoutNeedsUpdate)
        {
            setLayoutNeedsUpdate(false);
            setLayoutCalculated(false);
        }
    }, [nodes, edges])

    // Auto zoom callback
    useEffect(() => {
        if(!viewFitAfterLayout && props.args.fitView)
        {
            fitView();
            setViewFitAfterLayout(true);
        }
    }, [viewFitAfterLayout, props.args.fitView]);

    // Theme callback
    useEffect(() => {
        setEdges(edges.map(edge => ({...edge, labelStyle:{'fill': props.theme.base === "dark" ? 'white' : 'black'}})))
    }, [props.theme.base])

    // Flow interaction callbacks

    const handlePaneClick = (event) => {
        handleDataReturnToStreamlit(nodes, edges, null);
    }

    const handleNodeClick = (event, node) => {
        if (props.args.getNodeOnClick)
            handleDataReturnToStreamlit(nodes, edges, node.id);
    }

    const handleEdgeClick = (event, edge) => {
        if (props.args.getEdgeOnClick)
            handleDataReturnToStreamlit(nodes, edges, edge.id);
    }

    const handleConnectStart = (_, {nodeId,handleId}) => {
        const node = nodes.find(node => node.id === nodeId);
        const handles = node.data.handles
        const handle = handles.find(handle => handle.id === handleId);

        setConnectingNodeId(nodeId);
        setConnectingHandleId(handleId);
        setValidTargetHandleIds(handle.validTargetIds);
    }

    const handleConnectEnd = () => {
        setConnectingNodeId(null);
        setConnectingHandleId(null);
        setValidTargetHandleIds(null);
    }

    const handleConnect = (connection) => {

        const { source, sourceHandle, target, targetHandle } = connection;

        //check if new edge will be a bidirectional duplicate
        const connection_exists = edges.some((edge) => {
            const forward =
            edge.source === source &&
            edge.sourceHandle === sourceHandle &&
            edge.target === target &&
            edge.targetHandle === targetHandle;

            const reverse =
            edge.source === target &&
            edge.sourceHandle === targetHandle &&
            edge.target === source &&
            edge.targetHandle === sourceHandle;

            return forward || reverse;
        });

        if (connection_exists) {
            handleDataReturnToStreamlit(nodes, edges, null);
            return;
        }

        const newEdgeId = uuidv4(); 
        const newEdges = addEdge({id: newEdgeId, ...connection, type:props.args["typeOfNewEdges"], markerStart: {},markerEnd: {}, label:"",hidden:false, animated:props.args["animateNewEdges"], deletable:true, focusable:true,zIndex:0,style:{},labelStyle:{}}, edges);
        setEdges(newEdges);
        handleDataReturnToStreamlit(nodes, newEdges, newEdgeId);
    }

    const handleNodeDragStop = (event, node) => {
        const updatedNodes = nodes.map(n => {
            if(n.id === node.id)
                return node;
            return n;
        });
        handleDataReturnToStreamlit(updatedNodes, edges, null);
    }

    return (
        <div style={{height: props.args.height}}>
            <ReactFlow
                connectionMode="loose"
                nodeTypes={nodeTypes}
                ref={ref}
                nodes={nodes}
                onNodesChange={onNodesChange}
                onNodeDragStop={handleNodeDragStop}
                edges={edges}
                onEdgesChange={onEdgesChange}
                onConnectStart={handleConnectStart}
                onConnectEnd={handleConnectEnd}
                onConnect={props.args.allowNewEdges ? handleConnect : null}
                fitView={props.args.fitView}
                style={props.args.style}
                onNodeClick={handleNodeClick}
                onEdgeClick={handleEdgeClick}
                onPaneClick={handlePaneClick}
                panOnDrag={props.args.panOnDrag}
                zoomOnDoubleClick={props.args.allowZoom}
                zoomOnScroll={props.args.allowZoom}
                zoomOnPinch={props.args.allowZoom}
                minZoom={props.args.minZoom}
                proOptions={{hideAttribution: props.args.hideWatermark}}>
            <Background/>
            {props.args["showControls"] && <Controls/>}
            {props.args["showMiniMap"] && <MiniMap pannable zoomable/>}
            </ReactFlow>
        </div>
    );
}

const ContextualStreamlitFlowComponent = (props) => {
    return (
        <ReactFlowProvider>
            <StreamlitFlowComponent {...props}/>
        </ReactFlowProvider>
    );
}

export default ContextualStreamlitFlowComponent;
