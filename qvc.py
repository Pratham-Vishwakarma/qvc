import sys
from qvc import init, commit

if len(sys.argv) < 2:
    print("Usage: python qvc.py <command>")
    exit()

cmd = sys.argv[1]

if cmd == "init":
    init.run()

elif cmd == "commit":
    if len(sys.argv) < 3:
        print("Commit message missing")
    else:
        message = sys.argv[2]
        commit.run(message)

else:
    print("Unknown command")