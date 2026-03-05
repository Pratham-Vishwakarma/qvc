import sys
from qvc import diff_text

old_file = "circuit1.json"
new_file = "circuit2.json"

mode = sys.argv[1]

if mode == "summary":
    print(diff_text.summary_diff(old_file, new_file))

elif mode == "detailed":
    print(diff_text.detailed_diff(old_file, new_file))