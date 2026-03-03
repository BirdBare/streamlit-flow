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

const MemoizedMarkdown = memo(({ content }) => (
    <Markdown 
        rehypePlugins={rehypePlugins} 
        remarkPlugins={remarkPlugins}
    >
        {content}
    </Markdown>
));

const StreamlitFlowMarkdownNode = ({ data, connectingSourceHandleId }) => {    

    return (
        <>
            {buildHandles(data.handles,connectingSourceHandleId)}

            <div className="markdown-node react-flow__node-default" style={{width:"auto"}}>
                <MemoizedMarkdown content={data.content} />
            </div>
        </>
    );
};

export { StreamlitFlowMarkdownNode }