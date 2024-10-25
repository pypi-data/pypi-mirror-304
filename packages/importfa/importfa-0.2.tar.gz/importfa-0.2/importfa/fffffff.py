import os
import sys

fa = os.path.abspath("/".join([sys.argv[0] + "/.."] + [".."] * 7))
sys.path.append(fa)
