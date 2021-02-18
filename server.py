import os
import sys


def kill_process_by_name():
    cmd = "ps -ef | grep 'app.py'"
    print("准备杀掉现有进程...", cmd)
    f = os.popen(cmd)
    txt = f.readlines()
    for line in txt:
        print(line)
    if len(txt) == 0:
        print("no process !")
        return
    else:
        for line in txt:
            columns = line.split()
            pid = columns[1]
            cmd = "kill -9 %d" % int(pid)
            rc = os.system(cmd)
            if rc == 0:
                print("exec \"%s\" success!!" % cmd)
            else:
                print("exec \"%s\" failed!!" % cmd)
        return


def update_codes():
    print(sys.path[0])
    print("准备更新代码...")
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
