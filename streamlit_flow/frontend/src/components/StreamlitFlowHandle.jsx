import { Handle, Position } from 'reactflow';

const handlePosMap = {
    'top': Position.Top,
    'right': Position.Right,
    'bottom': Position.Bottom,
    'left': Position.Left,
};

function positionHandle(position, total_handles, iteration) {
  if (position === Position.Left || position === Position.Right) {
    return { top: `${(iteration + 1) * (100.0 / (total_handles + 1))}%` };
  } else {
    return { left: `${(iteration + 1) * (100.0 / (total_handles + 1))}%` };
  }
}

function buildHandles(handles) {

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
                    isConnectableEnd = {handleData.isConnectableEnd}
                    style={{ ...handleData.style, ...positionHandle(Position.Top, top_handles.length, i)}}
                />
            ))}
            {[...bottom_handles].map((handleData, i) => (
                <Handle
                    id={handleData.id}
                    key={i}
                    position={Position.Bottom}
                    isConnectableStart = {handleData.isConnectableStart}
                    isConnectableEnd = {handleData.isConnectableEnd}
                    style={{ ...handleData.style, ...positionHandle(Position.Bottom, bottom_handles.length, i)}}
                />
            ))}
            {[...left_handles].map((handleData, i) => (
                <Handle
                    id={handleData.id}
                    key={i}
                    position={Position.Left}
                    isConnectableStart = {handleData.isConnectableStart}
                    isConnectableEnd = {handleData.isConnectableEnd}
                    style={{ ...handleData.style, ...positionHandle(Position.Left, left_handles.length, i)}}
                />
            ))}
            {[...right_handles].map((handleData, i) => (
                <Handle
                    id={handleData.id}
                    key={i}
                    position={Position.Right}
                    isConnectableStart = {handleData.isConnectableStart}
                    isConnectableEnd = {handleData.isConnectableEnd}
                    style={{ ...handleData.style, ...positionHandle(Position.Right, right_handles.length, i)}}
                />
            ))}
        </>
    );
};

export { buildHandles }