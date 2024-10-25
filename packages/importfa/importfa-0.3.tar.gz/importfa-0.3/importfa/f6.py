import os
import sys

fa = os.path.abspath("/".join([sys.argv[0] + "/.."] + [".."] * 6))
sys.path.append(fa)
