import sys
from pathlib import PurePath
PARENT_DIRECTORY = PurePath(__file__).parents[1]
sys.path.append(str(PARENT_DIRECTORY))
