import sys
from qvc import diff_text

mode = sys.argv[1]

if mode == "summary":
    print(diff_text.summary_diff())

elif mode == "detailed":
    print(diff_text.detailed_diff())