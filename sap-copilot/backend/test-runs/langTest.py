import unittest
from unittest.mock import patch
import sys
import os

# Add the correct path to import lang.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lang import get_llm
from langchain.chat_models.base import BaseChatModel


class TestLangModule(unittest.TestCase):

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "fake_api_key"})
    def test_get_llm_success(self):
        llm = get_llm()
        self.assertIsInstance(llm, BaseChatModel)

    @patch.dict(os.environ, {}, clear=True)
    def test_get_llm_missing_api_key(self):
        with self.assertRaises(EnvironmentError) as context:
            get_llm()
        self.assertIn("Missing GOOGLE_API_KEY", str(context.exception))


if __name__ == "__main__":
    unittest.main()
