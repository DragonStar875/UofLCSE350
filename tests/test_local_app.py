import sys
import os
from unittest.mock import patch

# Prevent PyWebIO or anything else from triggering browser/server during import
os.environ["TESTING"] = "1"

# Add parent directory to path to import smartShelf
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pantry_utils
import smartShelf


def test_smartShelf_runs_without_crashing():
    """Basic smoke test: ensure smartShelf app launches main function without errors."""
    with patch('pywebio.output.put_buttons'), \
         patch('pywebio.output.put_scope'), \
         patch('pywebio.output.clear_scope'), \
         patch('smartShelf.render_expired_items'), \
         patch('smartShelf.handle_choice'), \
         patch('smartShelf.put_scope'):

        # This will now run without launching a server or browser
        smartShelf.pantry_main()

        # Test passes if pantry_main doesn't crash
        assert callable(smartShelf.pantry_main)
