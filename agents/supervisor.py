import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from core.state import GlobalState
from core.prompts import get_prompt, SUPERVISOR_FALLBACK
from core.task_plan import TaskPlanError, parse_task_plan


logger = logging.getLogger(__name__)
llm = ChatOpenAI(model="gpt-4o", temperature=0)  # Using GPT-4o for better JSON adherence

FALLBACK_TASKS = [
    {"task_id": "fallback_news_aapl", "task_type": "news", "ticker": "AAPL"},
    {"task_id": "fallback_quant_aapl", "task_type": "quant", "ticker": "AAPL"},
]


def supervisor_node(state: GlobalState):
    """Takes the query and generates a validated list of sub-tasks."""
    query = state["query"]

    prompt_template = get_prompt("supervisor_prompt", SUPERVISOR_FALLBACK)
    system_prompt = prompt_template.format(query=query)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Generate the task plan in JSON.")
    ]
    response = llm.invoke(messages)

    try:
        tasks = parse_task_plan(response.content)
    except TaskPlanError as exc:
        logger.warning(
            "Supervisor returned an invalid task plan (%s); using the default AAPL plan.",
            exc,
        )
        tasks = [task.copy() for task in FALLBACK_TASKS]

    return {"tasks": tasks, "completed_tasks": []}
