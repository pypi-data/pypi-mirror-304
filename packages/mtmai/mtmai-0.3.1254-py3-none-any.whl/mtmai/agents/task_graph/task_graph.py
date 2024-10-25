from fastapi.encoders import jsonable_encoder
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import tools_condition

import mtmai.chainlit as cl
from mtmai.agents.assisant.nodes.assisant_node import (
    PrimaryAssistantNode,
    primary_assistant_tools,
    route_assistant,
)
from mtmai.agents.ctx import init_mtmai_http_context, mtmai_context
from mtmai.agents.graphutils import (
    create_tool_node_with_fallback,
    is_internal_node,
    is_skip_kind,
    pop_dialog_state,
)
from mtmai.agents.task_graph.nodes.task_entry_node import TaskEntryNode
from mtmai.agents.task_graph.task_state import TaskState
from mtmai.chainlit import context
from mtmai.core.coreutils import is_in_dev
from mtmai.core.logging import get_logger

logger = get_logger()


class TaskGraph:
    def __init__(self):
        pass

    @classmethod
    def name(cls):
        return "taskrunner"

    async def build_graph(self):
        wf = StateGraph(TaskState)

        wf.add_node("entry", TaskEntryNode())
        wf.add_edge("entry", "assistant")
        wf.set_entry_point("entry")

        wf.add_node("assistant", PrimaryAssistantNode())

        wf.add_conditional_edges(
            "assistant",
            tools_condition,
        )

        wf.add_node(
            "tools",
            create_tool_node_with_fallback(primary_assistant_tools),
        )
        wf.add_conditional_edges(
            "tools",
            route_assistant,
            {
                "assistant": "assistant",
                # "error": END,
            },
        )
        wf.add_node("leave_skill", pop_dialog_state)
        wf.add_edge("leave_skill", "assistant")

        return wf

    async def compile_graph(self) -> CompiledGraph:
        graph = (await self.build_graph()).compile(
            checkpointer=await mtmai_context.get_graph_checkpointer(),
            # interrupt_after=["human_chat"],
            interrupt_before=[
                # "human_chat",
                # "update_flight_sensitive_tools",
                # "develop_sensitive_tools",
                # "book_car_rental_sensitive_tools",
                # "book_hotel_sensitive_tools",
                # "book_excursion_sensitive_tools",
            ],
            debug=True,
        )

        if is_in_dev():
            image_data = graph.get_graph(xray=1).draw_mermaid_png()
            save_to = "./.vol/assistant_graph.png"
            with open(save_to, "wb") as f:
                f.write(image_data)
        return graph

    async def chat_start(self):
        init_mtmai_http_context()
        user_session = cl.user_session
        user = user_session.get("user")
        thread_id = context.session.thread_id
        # await cl.Message(content="欢迎使用博客文章生成器").send()
        graph = await TaskGraph().compile_graph()
        user_session.set("graph", graph)

        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
            }
        }
        await self.run_graph(thread, {"messages": []})

    async def on_chat_resume(self):
        thread_id = context.session.thread_id
        logger.info("on_chat_resume", thread_id)

    async def on_message(self, message: cl.Message):
        try:
            user_session = cl.user_session
            thread_id = context.session.thread_id

            graph: CompiledGraph = user_session.get("graph")
            if not graph:
                cl.Message(content="工作流初始化失败").send()
                raise ValueError("graph 未初始化")
            thread: RunnableConfig = {
                "configurable": {
                    "thread_id": thread_id,
                }
            }
            pre_state = await graph.aget_state(thread, subgraphs=True)
            if not pre_state.next:
                logger.info("流程已经结束")
                await context.emitter.emit(
                    "logs",
                    {
                        "message": "流程已经结束",
                    },
                )
                cl.Message(content="流程已经结束").send()
                return
            await graph.aupdate_state(
                thread,
                {
                    **pre_state.values,
                    "user_input": message.content,
                },
                # as_node="primary_assistant",
            )
            await self.run_graph(thread)
        except Exception as e:
            import traceback

            error_message = f"An error occurred: {str(e)}\n\nDetailed traceback:\n{traceback.format_exc()}"
            logger.error(error_message)
            await cl.Message(content=error_message).send()

    async def run_graph(
        self,
        thread: RunnableConfig,
        inputs=None,
    ):
        user_session = cl.user_session
        graph = user_session.get("graph")
        if not graph:
            raise ValueError("graph 未初始化")

        async for event in graph.astream_events(
            inputs,
            version="v2",
            config=thread,
            subgraphs=True,
        ):
            kind = event["event"]
            node_name = event["name"]
            data = event["data"]

            if not is_internal_node(node_name):
                if not is_skip_kind(kind):
                    logger.info("[event] %s@%s", kind, node_name)
            # if kind == "on_chat_model_end":
            #     output = data.get("output")
            #     if output:
            #         chat_output = output.content
            #         if chat_output:
            #             await cl.Message("node_name:"+node_name+"\n"+chat_output).send()

            if kind == "on_chain_end":
                output = data.get("output")

                if node_name == "on_chat_start_node":
                    thread_ui_state = output.get("thread_ui_state")
                    if thread_ui_state:
                        await context.emitter.emit(
                            "ui_state_upate",
                            jsonable_encoder(thread_ui_state),
                        )

                if node_name == "LangGraph":
                    logger.info("中止节点")
                    if (
                        data
                        and (output := data.get("output"))
                        and (final_messages := output.get("messages"))
                    ):
                        for message in final_messages:
                            message.pretty_print()
                        await context.emitter.emit(
                            "logs",
                            {
                                "on": "中止",
                                "node_name": node_name,
                                "output": message.pretty_print(),
                            },
                        )

            if kind == "on_tool_start":
                await context.emitter.emit(
                    "logs",
                    {
                        "on": kind,
                        "node_name": node_name,
                    },
                )

            if kind == "on_tool_end":
                output = data.get("output")
                await context.emitter.emit(
                    "logs",
                    {
                        "on": kind,
                        "node_name": node_name,
                        "output": jsonable_encoder(output),
                    },
                )
