import { Handle, Position } from 'reactflow';

function canRender(connectingSourceHandleId,validSourceIds) {
    return (connectingSourceHandleId === null || 
            validSourceIds === null || 
            validSourceIds.includes(connectingSourceHandleId));

}

function positionHandle(position, total_handles, iteration) {
  if (position === Position.Left || position === Position.Right) {
    return { top: `${(iteration + 1) * (100.0 / (total_handles + 1))}%` };
  } else {
    return { left: `${(iteration + 1) * (100.0 / (total_handles + 1))}%` };
  }
}

function buildHandles(handles, connectingSourceHandleId) {

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
                    isConnectableEnd = {handleData.isConnectableEnd && canRender(connectingSourceHandleId,handleData.validSourceIds)}
                    style={{ 
                        ...handleData.style, 
                        ...positionHandle(Position.Top, top_handles.length, i),
                        display: canRender(connectingSourceHandleId, handleData.validSourceIds) ? 1 : 0,}}
                />
            ))}
            {[...bottom_handles].map((handleData, i) => (
                <Handle
                    id={handleData.id}
                    key={i}
                    position={Position.Bottom}
                    isConnectableStart = {handleData.isConnectableStart}
                    isConnectableEnd = {handleData.isConnectableEnd && canRender(connectingSourceHandleId,handleData.validSourceIds)}
                    style={{ 
                        ...handleData.style, 
                        ...positionHandle(Position.Bottom, bottom_handles.length, i),
                        opacity: canRender(connectingSourceHandleId, handleData.validSourceIds) ? 1 : 0,}}
                />
            ))}
            {[...left_handles].map((handleData, i) => (
                <Handle
                    id={handleData.id}
                    key={i}
                    position={Position.Left}
                    isConnectableStart = {handleData.isConnectableStart}
                    isConnectableEnd = {handleData.isConnectableEnd && canRender(connectingSourceHandleId,handleData.validSourceIds)}
                    style={{ 
                        ...handleData.style, 
                        ...positionHandle(Position.Left, left_handles.length, i),
                        opacity: canRender(connectingSourceHandleId, handleData.validSourceIds) ? 1 : 0,}}
                />
            ))}
            {[...right_handles].map((handleData, i) => (
                <Handle
                    id={handleData.id}
                    key={i}
                    position={Position.Right}
                    isConnectableStart = {handleData.isConnectableStart}
                    isConnectableEnd = {handleData.isConnectableEnd && canRender(connectingSourceHandleId,handleData.validSourceIds)}
                    style={{ 
                        ...handleData.style, 
                        ...positionHandle(Position.Right, right_handles.length, i),
                        opacity: canRender(connectingSourceHandleId, handleData.validSourceIds) ? 1 : 0,}}
                />
            ))}
        </>
    );
};

export { buildHandles }