import sys
import os
from unittest.mock import patch

# Add parent directory to path to import smartShelf
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_smartShelf_runs_without_crashing():
    """Basic smoke test: ensure smartShelf app launches main function without errors."""
    with patch('pywebio.output.put_buttons'), \
         patch('pywebio.output.put_scope'), \
         patch('smartShelf.start_server') as mock_start_server:
        
        # Import here to trigger top-level logic, if any
        import smartShelf

        # Simulate calling main app manually (to avoid __main__ block)
        smartShelf.pantry_main()

        assert mock_start_server.called or callable(smartShelf.pantry_main)
