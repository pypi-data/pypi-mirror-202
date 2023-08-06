"""Welcome to the Garden - We're so glad you're here <3 """
__version__ = "v0.4.11"
import sys
from pathlib import Path

from golem_garden.api import main

base_package_path = Path(__file__).parent.parent
sys.path.insert(0, str(base_package_path))  # add parent directory to sys.path

from golem_garden.user_interface.command_line_interface import chat_with_golem

