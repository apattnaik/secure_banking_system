import os, sys
sys.path.append('.')
print(sys.path)
print(os.getcwd())

import app

import unittest
from tests import *

print("Running tests...")

unittest.main()
