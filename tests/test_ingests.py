import os
import parse
from utils import PipelineCache


def test_all_ingests_are_modules():
    discovered = PipelineCache(auto_discover=True)._modules
    expected = [
        path
        for path in os.listdir("ingest/")
        if path not in ["__init__.py", "__pycache__"]
    ]
    assert sorted(discovered) == sorted(expected)


def test_all_ingests_define_tests():
    modules = PipelineCache(auto_discover=True)._modules
    test_dirs = [f"ingest/{module}/tests/" for module in modules]
    for test_dir in test_dirs:
        assert os.path.isdir(test_dir)
        pattern = parse.compile("test_{}.py")
        tests = list(filter(lambda f: pattern.parse(f), os.listdir(test_dir)))
        assert len(tests) >= 1
