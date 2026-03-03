import { Handle, Position } from 'reactflow';

function canRender(connectingNodeId, nodeId, connectingHandleId, validTargetHandleIds,handleId) {
    return (
        (connectingNodeId === null && connectingHandleId === null) ||
        ((connectingNodeId === nodeId) && (connectingHandleId === handleId)) ||
        ((connectingNodeId !== nodeId) && (validTargetHandleIds.length === 0)) ||
        ((connectingNodeId !== nodeId) && (validTargetHandleIds.includes(handleId)))
        );
}

function positionHandle(position, total_handles, iteration) {
  if (position === Position.Left || position === Position.Right) {
    return { top: `${(iteration + 1) * (100.0 / (total_handles + 1))}%` };
  } else {
    return { left: `${(iteration + 1) * (100.0 / (total_handles + 1))}%` };
  }
}

function buildHandles(nodeId, handles, connectingNodeId,connectingHandleId,validTargetHandleIds) {

    const top_handles = handles.filter(obj => obj.position === "top")
    const bottom_handles = handles.filter(obj => obj.position === "bottom")
    const left_handles = handles.filter(obj => obj.position === "left")
    const right_handles = handles.filter(obj => obj.position === "right")

    return (
        <>
            {[...top_handles].map((handleData, i) => (
                <Handle
                    id={handleData.id}
                    key={i}
                    position={Position.Top}
                    isConnectableStart = {handleData.isConnectableStart}
                    isConnectableEnd = {handleData.isConnectableEnd && canRender(connectingNodeId,nodeId,connectingHandleId,validTargetHandleIds,handleData.id)}
                    style={{ 
                        ...handleData.style, 
                        ...positionHandle(Position.Top, top_handles.length, i),
                        opacity: canRender(connectingNodeId,nodeId,connectingHandleId,validTargetHandleIds,handleData.id) ? 1 : 0,}}
                />
            ))}
            {[...bottom_handles].map((handleData, i) => (
                <Handle
                    id={handleData.id}
                    key={i}
                    position={Position.Bottom}
                    isConnectableStart = {handleData.isConnectableStart}
                    isConnectableEnd = {handleData.isConnectableEnd && canRender(connectingNodeId,nodeId,connectingHandleId,validTargetHandleIds,handleData.id)}
                    style={{ 
                        ...handleData.style, 
                        ...positionHandle(Position.Bottom, bottom_handles.length, i),
                        opacity: canRender(connectingNodeId,nodeId,connectingHandleId,validTargetHandleIds,handleData.id) ? 1 : 0,}}
                />
            ))}
            {[...left_handles].map((handleData, i) => (
                <Handle
                    id={handleData.id}
                    key={i}
                    position={Position.Left}
                    isConnectableStart = {handleData.isConnectableStart}
                    isConnectableEnd = {handleData.isConnectableEnd && canRender(connectingNodeId,nodeId,connectingHandleId,validTargetHandleIds,handleData.id)}
                    style={{ 
                        ...handleData.style, 
                        ...positionHandle(Position.Left, left_handles.length, i),
                        opacity: canRender(connectingNodeId,nodeId,connectingHandleId,validTargetHandleIds,handleData.id) ? 1 : 0,}}
                />
            ))}
            {[...right_handles].map((handleData, i) => (
                <Handle
                    id={handleData.id}
                    key={i}
                    position={Position.Right}
                    isConnectableStart = {handleData.isConnectableStart}
                    isConnectableEnd = {handleData.isConnectableEnd && canRender(connectingNodeId,nodeId,connectingHandleId,validTargetHandleIds,handleData.id)}
                    style={{ 
                        ...handleData.style, 
                        ...positionHandle(Position.Right, right_handles.length, i),
                        opacity: canRender(connectingNodeId,nodeId,connectingHandleId,validTargetHandleIds,handleData.id) ? 1 : 0,}}
                />
            ))}
        </>
    );
};

export { buildHandles }