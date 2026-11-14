import json
import unittest

from core.task_plan import TaskPlanError, parse_task_plan


VALID_PLAN = [
    {"task_id": "news_aapl", "task_type": "news", "ticker": "AAPL"},
    {"task_id": "quant_aapl", "task_type": "quant", "ticker": "AAPL"},
]


class ParseTaskPlanTests(unittest.TestCase):
    def test_parses_plain_json_array(self):
        self.assertEqual(parse_task_plan(json.dumps(VALID_PLAN)), VALID_PLAN)

    def test_parses_markdown_fence_and_preamble(self):
        fence = chr(96) * 3
        content = f"Here is the plan:\n{fence}json\n{json.dumps(VALID_PLAN)}\n{fence}"
        self.assertEqual(parse_task_plan(content), VALID_PLAN)

    def test_normalizes_task_type_and_ticker(self):
        plan = [
            {"task_id": "news", "task_type": " NEWS ", "ticker": " aapl "},
            {"task_id": "quant", "task_type": "QUANT", "ticker": "^gspc"},
        ]
        self.assertEqual(
            parse_task_plan(json.dumps(plan)),
            [
                {"task_id": "news", "task_type": "news", "ticker": "AAPL"},
                {"task_id": "quant", "task_type": "quant", "ticker": "^GSPC"},
            ],
        )

    def test_discards_unconsumed_model_fields(self):
        plan = [
            {"task_id": "news", "task_type": "news", "ticker": "AAPL", "extra": "ignored"},
            {"task_id": "quant", "task_type": "quant", "ticker": "AAPL", "notes": "ignored"},
        ]
        expected = [
            {"task_id": "news", "task_type": "news", "ticker": "AAPL"},
            {"task_id": "quant", "task_type": "quant", "ticker": "AAPL"},
        ]
        self.assertEqual(parse_task_plan(json.dumps(plan)), expected)

    def test_rejects_empty_or_non_text_response(self):
        for content in ("", "   ", None):
            with self.subTest(content=content), self.assertRaises(TaskPlanError):
                parse_task_plan(content)

    def test_rejects_missing_or_invalid_json_array(self):
        for content in ("not json", '{"task_id": "x"}', "prefix [broken"):
            with self.subTest(content=content), self.assertRaises(TaskPlanError):
                parse_task_plan(content)

    def test_rejects_empty_plan(self):
        with self.assertRaises(TaskPlanError):
            parse_task_plan("[]")

    def test_rejects_non_object_task(self):
        content = '[1, {"task_id":"q","task_type":"quant","ticker":"AAPL"}]'
        with self.assertRaises(TaskPlanError):
            parse_task_plan(content)

    def test_rejects_missing_task_id(self):
        plan = [
            {"task_type": "news", "ticker": "AAPL"},
            {"task_id": "quant", "task_type": "quant", "ticker": "AAPL"},
        ]
        with self.assertRaises(TaskPlanError):
            parse_task_plan(json.dumps(plan))

    def test_rejects_unsupported_task_type(self):
        plan = [
            {"task_id": "news", "task_type": "sentiment", "ticker": "AAPL"},
            {"task_id": "quant", "task_type": "quant", "ticker": "AAPL"},
        ]
        with self.assertRaises(TaskPlanError):
            parse_task_plan(json.dumps(plan))

    def test_rejects_invalid_ticker(self):
        plan = [
            {"task_id": "news", "task_type": "news", "ticker": "AAPL; rm -rf /"},
            {"task_id": "quant", "task_type": "quant", "ticker": "AAPL"},
        ]
        with self.assertRaises(TaskPlanError):
            parse_task_plan(json.dumps(plan))

    def test_rejects_duplicate_ids_and_duplicate_targets(self):
        duplicate_id = [
            {"task_id": "same", "task_type": "news", "ticker": "AAPL"},
            {"task_id": "same", "task_type": "quant", "ticker": "AAPL"},
        ]
        duplicate_target = [
            {"task_id": "news1", "task_type": "news", "ticker": "AAPL"},
            {"task_id": "news2", "task_type": "news", "ticker": "AAPL"},
            {"task_id": "quant", "task_type": "quant", "ticker": "AAPL"},
        ]
        for plan in (duplicate_id, duplicate_target):
            with self.subTest(plan=plan), self.assertRaises(TaskPlanError):
                parse_task_plan(json.dumps(plan))

    def test_requires_both_worker_types(self):
        plan = [{"task_id": "news", "task_type": "news", "ticker": "AAPL"}]
        with self.assertRaises(TaskPlanError):
            parse_task_plan(json.dumps(plan))

    def test_rejects_more_than_twenty_tasks(self):
        plan = [
            {"task_id": f"news{i}", "task_type": "news", "ticker": f"T{i}"}
            for i in range(1, 21)
        ] + [{"task_id": "quant", "task_type": "quant", "ticker": "AAPL"}]
        with self.assertRaises(TaskPlanError):
            parse_task_plan(json.dumps(plan))


if __name__ == "__main__":
    unittest.main()
