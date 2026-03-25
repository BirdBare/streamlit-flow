import React, { memo } from 'react';
import Markdown from 'react-markdown'
import rehypeHighlight from 'rehype-highlight';
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw';
import rehypeKatex from 'rehype-katex';
import remarkMath from 'remark-math';
import 'katex/dist/katex.min.css';
import 'highlight.js/styles/github.css';
import {buildHandles} from "./StreamlitFlowHandle.jsx"

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

const StreamlitFlowMarkdownNode = ({id, data, connectingNodeId,connectingHandleId, validTargetHandleIds }) => {    

    return (
        <>
            {buildHandles(id, data.handles,connectingNodeId,connectingHandleId,validTargetHandleIds)}

            <div className="markdown-node react-flow__node-default" style={{width:"auto"}}>
                <MemoizedMarkdown markdown={data.markdown} />
            </div>
        </>
    );
};

export { StreamlitFlowMarkdownNode }