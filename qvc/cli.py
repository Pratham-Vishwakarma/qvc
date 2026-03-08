def main():
    import sys
    from qvc import init, add, commit, diff_text

    if len(sys.argv) < 2:
        print("Usage: python qvc.py <command>")
        exit()

    cmd = sys.argv[1]

    if cmd == "help":
        print("init : Intialize the qvc project\nadd : Add the circuit data to staging area\ncommit : Commit the circuit data to database")

    elif cmd == "init":
        init.initialize()

    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: python qvc.py <command> <file.py>")
            sys.exit(1)

        target = sys.argv[2]

        if target == ".":
            target = "Test_code2.py"  # default file name

        qc = add.load_circuit_from_file(target)
        added_file = add.generate(qc)
        add.stage(added_file)

    elif cmd == "commit":
        if len(sys.argv) < 3:
            print("Commit message missing")
        else:
            message = sys.argv[2]
            commit.commits(message)
    
    elif cmd == "diff":
        if len(sys.argv) < 3:
            print("Usage: python qvc.py diff <summary|detailed>")
        else:
            mode = sys.argv[2]
            if mode == "summary" or mode == ".":
                print(diff_text.summary_diff())
            elif mode == "detailed":
                print(diff_text.detailed_diff())
            else:
                print("Unknown diff mode")

    else:
        print("Unknown command")