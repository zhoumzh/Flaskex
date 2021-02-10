import os
import sys


def kill_process_by_name():
    n = "app.py"
    cmd = "ps -e | grep 'app.py'"
    f = os.popen(cmd)
    txt = f.readlines()
    if len(txt) == 0:
        print("no process !")
        return
    else:
        for line in txt:
            columns = line.split()
            pid = columns[0]
            cmd = "kill -9 %d" % int(pid)
            rc = os.system(cmd)
            if rc == 0:
                print("exec \"%s\" success!!" % cmd)
            else:
                print("exec \"%s\" failed!!" % cmd)
        return


def update_codes():
    print(sys.path[0])
    os.system("cd " + sys.path[0])
    lines = os.popen("git pull").readlines()
    print(lines)


def start():
    lines = os.popen("nohup py app.py > app.log &").readlines()
    print(lines)


if __name__ == "__main__":
    update_codes()
    kill_process_by_name()
    start()
