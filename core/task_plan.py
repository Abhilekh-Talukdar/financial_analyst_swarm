import json
import re


class TaskPlanError(ValueError):
    """Raised when the supervisor returns an unsafe or unusable task plan."""


_ALLOWED_TASK_TYPES = frozenset({"news", "quant"})
_TICKER_PATTERN = re.compile(r"^[A-Z0-9^][A-Z0-9.^=-]{0,14}$")
_MAX_TASKS = 20


def parse_task_plan(content: str) -> list[dict[str, str]]:
    """Extract and validate the supervisor's JSON task array.

    The model may wrap its JSON in Markdown fences or add a short preamble.
    Only the fields consumed by the worker graph are retained.
    """
    if not isinstance(content, str) or not content.strip():
        raise TaskPlanError("response must be non-empty text")

    decoder = json.JSONDecoder()
    decoded_tasks = None
    for offset, character in enumerate(content):
        if character != "[":
            continue
        try:
            candidate, _ = decoder.raw_decode(content[offset:])
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, list):
            decoded_tasks = candidate
            break

    if decoded_tasks is None:
        raise TaskPlanError("response does not contain a valid JSON array")
    if not decoded_tasks:
        raise TaskPlanError("task plan must not be empty")
    if len(decoded_tasks) > _MAX_TASKS:
        raise TaskPlanError(f"task plan cannot contain more than {_MAX_TASKS} tasks")

    validated_tasks: list[dict[str, str]] = []
    seen_task_ids: set[str] = set()
    seen_task_targets: set[tuple[str, str]] = set()

    for position, task in enumerate(decoded_tasks, start=1):
        if not isinstance(task, dict):
            raise TaskPlanError(f"task {position} must be a JSON object")

        task_id = task.get("task_id")
        if (
            not isinstance(task_id, str)
            or not task_id.strip()
            or len(task_id.strip()) > 64
            or not task_id.strip().isprintable()
        ):
            raise TaskPlanError(
                f"task {position} must have a printable task_id of at most 64 characters"
            )
        task_id = task_id.strip()
        if task_id in seen_task_ids:
            raise TaskPlanError(f"task_id {task_id!r} is duplicated")

        task_type = task.get("task_type")
        if not isinstance(task_type, str):
            raise TaskPlanError(f"task {position} must have a supported task_type")
        task_type = task_type.strip().lower()
        if task_type not in _ALLOWED_TASK_TYPES:
            raise TaskPlanError(f"task {position} has unsupported task_type {task_type!r}")

        ticker = task.get("ticker")
        if not isinstance(ticker, str):
            raise TaskPlanError(f"task {position} must have a valid ticker")
        ticker = ticker.strip().upper()
        if not _TICKER_PATTERN.fullmatch(ticker):
            raise TaskPlanError(f"task {position} has an invalid ticker")

        task_target = (task_type, ticker)
        if task_target in seen_task_targets:
            raise TaskPlanError(f"duplicate {task_type} task for ticker {ticker}")

        seen_task_ids.add(task_id)
        seen_task_targets.add(task_target)
        validated_tasks.append(
            {"task_id": task_id, "task_type": task_type, "ticker": ticker}
        )

    if {task["task_type"] for task in validated_tasks} != _ALLOWED_TASK_TYPES:
        raise TaskPlanError("task plan must include at least one news task and one quant task")

    return validated_tasks
