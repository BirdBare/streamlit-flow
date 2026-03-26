import React, { memo } from 'react';
import Markdown from 'react-markdown'
import rehypeHighlight from 'rehype-highlight';
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw';
import rehypeKatex from 'rehype-katex';
import remarkMath from 'remark-math';
import 'katex/dist/katex.min.css';
import 'highlight.js/styles/github.css';
import {
    BaseEdge,
    EdgeLabelRenderer,
    getStraightPath,
    getBezierPath,
    getSimpleBezierPath,
    getSmoothStepPath,
} from 'reactflow';

const remarkPlugins = [remarkGfm, remarkMath];
const rehypePlugins = [rehypeHighlight, rehypeRaw, rehypeKatex];

const MemoizedMarkdown = memo(({ markdown }) => (
    <Markdown 
        rehypePlugins={rehypePlugins} 
        remarkPlugins={remarkPlugins}
    >
        {markdown}
    </Markdown>
));

const StreamlitFlowMarkdownEdge = ({ id, data, sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition }) => {
    const getPath = {
        straight: getStraightPath,
        smoothstep: getSmoothStepPath,
        simplebezier: getSimpleBezierPath,
        bezier: getBezierPath
    }

    const [edgePath, labelX, labelY] = getPath[data.lineType]({
        sourceX,
        sourceY,
        targetX,
        targetY,
        sourcePosition,
        targetPosition
        });

    console.log(data.markdown)

    return (
        <>
            <BaseEdge id={id} path={edgePath} />
            <EdgeLabelRenderer>
                {data?.markdown?.trim() && (
                    <div className="nodrag nopan react-flow__edge-label react-flow__edge-label-inner markdown-edge"
                        style={{
                            position: "absolute",
                            transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
                            pointerEvents: "all",  
                            ...data.markdownStyle
                    }}>
                        <MemoizedMarkdown markdown={data.markdown} />
                    </div>
                )}
            </EdgeLabelRenderer>
        </>
    );
};

export { StreamlitFlowMarkdownEdge }