import os
import sys

fa = os.path.abspath("/".join([sys.argv[0] + "/.."] + [".."] * 8))
sys.path.append(fa)
