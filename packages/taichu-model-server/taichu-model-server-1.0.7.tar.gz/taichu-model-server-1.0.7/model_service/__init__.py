__version__ = "1.0.4"

import os
import sys
src_path = os.path.abspath(os.path.dirname(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from model_service import *