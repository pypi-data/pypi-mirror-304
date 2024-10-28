from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunStreamEvent,
    NodeRunCompletedEvent,
)
from typing import Dict, Any, AsyncGenerator
from botrun_flow_lang.models.variable import InputVariable, OutputVariable
from pydantic import Field, field_validator


class AnswerNodeData(BaseNodeData):
    type: NodeType = NodeType.ANSWER
    input_variables: list[InputVariable] = Field(default_factory=list)
    output_variables: list[OutputVariable] = [OutputVariable(variable_name="answer")]

    @field_validator("output_variables")
    def validate_output_variables(cls, v):
        assert len(v) == 1, "AnswerNode must have exactly 1 output variable"
        assert (
            v[0].variable_name == "answer"
        ), "AnswerNode's output variable must be named 'answer'"
        return v


class AnswerNode(BaseNode):
    data: AnswerNodeData

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        output = variable_pool.get(self.data.input_variables[0].node_id, {}).get(
            self.data.input_variables[0].variable_name, ""
        )

        # # 如果LLM输出是流式的，我们可以直接传递它
        # if isinstance(llm_output, AsyncGenerator):
        #     async for chunk in llm_output:
        #         yield NodeRunStreamEvent(node_id=self.data.id, chunk=chunk)
        # else:
        #     # 如果不是流式的，我们可以一次性发送整个答案
        #     yield NodeRunStreamEvent(node_id=self.data.id, chunk=llm_output)

        yield NodeRunCompletedEvent(
            node_id=self.data.id,
            node_title=self.data.title,
            node_type=self.data.type.value,
            outputs={"answer": output},
        )
