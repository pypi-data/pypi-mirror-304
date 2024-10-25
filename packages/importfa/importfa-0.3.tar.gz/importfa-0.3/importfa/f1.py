import os
import sys

fa = os.path.abspath("/".join([sys.argv[0] + "/.."] + [".."] * 1))
sys.path.append(fa)
