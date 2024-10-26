from urllib.parse import urlparse

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from mtmai.agents.task_graph.task_state import TaskState
from mtmai.chainlit import context as clctx
from mtmai.core.db import get_async_session
from mtmai.core.logging import get_logger
from mtmai.crud import crud_task

logger = get_logger()


class TaskEntryNode:
    def __init__(self):
        pass

    async def __call__(self, state: TaskState, config: RunnableConfig):
        logger.info(f"task entry node: {state}")

        if not state.scheduleId:
            scheduleId, taskId = await self.detect_client_info()
            state.scheduleId = scheduleId
            state.taskId = taskId

        async with get_async_session() as session:
            sched = await crud_task.get_schedule(session=session, id=state.scheduleId)

        # cl_thread_id = clctx.session.thread_id

        # db_task = await crud_task.(cl_thread_id)
        # if not db_task:
        #     logger.info(f"启动新任务 {cl_thread_id}")
        if state.user_input:
            return {
                "next": "assistant",
                "messages": [HumanMessage(content=state.user_input)],
            }
        return {
            "next": "assistant",
        }

    async def detect_client_info(self):
        """
        通过函数js 函数获取客户端的基本信息
        """
        js_code_get_detail_info = """
var results = {};
results.fullUrl=window.location.href;
results.cookie=document.cookie;
results.title=document.title;
results.body=document.body.innerText;
(function() { return results; })();
"""
        js_eval_result = await clctx.emitter.send_call_fn(
            "js_eval", {"code": js_code_get_detail_info}
        )
        logger.info("js_eval_result %s", js_eval_result)

        client_url = js_eval_result.get("fullUrl")
        logger.info("client_url %s", client_url)

        # Parse the URL to extract scheduleId and taskId

        parsed_url = urlparse(client_url)
        path_segments = parsed_url.path.split("/")

        scheduleId = None
        taskId = None

        if len(path_segments) >= 5 and path_segments[2] == "schedule":
            scheduleId = path_segments[3]

        if len(path_segments) >= 7 and path_segments[5] == "task":
            taskId = path_segments[6]

        logger.info(f"Extracted scheduleId: {scheduleId}, taskId: {taskId}")

        # Store the extracted IDs in the user session for later use
        # cl.user_session.set("scheduleId", scheduleId)
        # cl.user_session.set("taskId", taskId)
        return scheduleId, taskId
