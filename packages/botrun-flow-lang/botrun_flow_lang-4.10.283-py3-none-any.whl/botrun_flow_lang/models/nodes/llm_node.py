from pydantic import BaseModel, Field
from typing import List, Dict, Any, AsyncGenerator
from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
import litellm
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunStreamEvent,
    NodeRunCompletedEvent,
)


class LLMModelConfig(BaseModel):
    completion_params: Dict[str, Any] = Field(default_factory=dict)
    mode: str
    name: str
    provider: str


class LLMNodeData(BaseNodeData):
    type: NodeType = NodeType.LLM
    model: LLMModelConfig
    prompt_template: List[Dict[str, str]]
    context: Dict[str, Any] = Field(default_factory=dict)
    vision: Dict[str, bool] = Field(default_factory=dict)


class LLMNode(BaseNode):
    data: LLMNodeData

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        messages = self.prepare_messages(variable_pool)

        stream = await litellm.acompletion(
            model=self.data.model.name,
            messages=messages,
            stream=True,
            **self.data.model.completion_params
        )

        full_response = ""
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                yield NodeRunStreamEvent(
                    node_id=self.data.id,
                    node_title=self.data.title,
                    node_type=self.data.type.value,
                    chunk=content,
                )

        yield NodeRunCompletedEvent(
            node_id=self.data.id,
            node_title=self.data.title,
            node_type=self.data.type.value,
            outputs={"llm_output": full_response},
        )

    def prepare_messages(self, variable_pool):
        messages = []
        for message in self.data.prompt_template:
            content = self.replace_variables(message["content"], variable_pool)
            messages.append({"role": message["role"], "content": content})
        return messages
