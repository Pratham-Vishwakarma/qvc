def main():
    import sys
    from qvc import init, add, commit, diff_text, diff_param

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
            target = "Test_code3.py"  # default file name

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
        if len(sys.argv) < 4:
            print("Usage: python qvc.py diff <text|param> <summary|detailed>")
        else:
            diff_type = sys.argv[2]
            mode = sys.argv[3]

            if diff_type == "text":
                if mode == "summary" or mode == ".":
                    print(diff_text.summary_diff())
                elif mode == "detailed":
                    print(diff_text.detailed_diff())
                else:
                    print("Unknown diff mode")

            elif diff_type == "param":
                if mode == "summary" or mode == ".":
                    print(diff_param.summary_param_diff())
                elif mode == "detailed":
                    print(diff_param.detailed_param_diff())
                else:
                    print("Unknown diff mode")

            else:
                print("Unknown diff type")

    else:
        print("Unknown command")