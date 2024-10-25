import os
import sys

fa = os.path.abspath("/".join([sys.argv[0] + "/.."] + [".."] * 4))
sys.path.append(fa)
