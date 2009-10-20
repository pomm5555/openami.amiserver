from supay import Daemon
import time, sys, os

t_name='testd'
t_pid_dir='/var/run'
t_stdin=os.path.abspath(".")+'/logs'
t_stdout=os.path.abspath(".")+'/logs'
t_stderr=os.path.abspath(".")+'/logs'
print os.path.abspath(".")+'/logs'

def get():
    return Daemon(t_name, t_pid_dir, t_stdin, t_stdout, t_stderr)

def run():
    daemon = get()
    print os.path.abspath(".")
    daemon.start()
    while True:
        do_something()
    daemon.stop()


def stop():
    daemon = get()
    daemon.stop()


def stat():
    daemon = get()
    print "daemon stats"
    daemon.status()


# daemon routine
def do_something():
    time.sleep(5)
    print "hello from daemon"


# cli interface
def display_help():
    print "Usage:\npython amiServer.py <argument>"
    print "arguments:\n\tstart\tstarts the daemon\n\tstop\t stops the daemon\n\tstat\t displays status information"

if __name__ == "__main__":
    if sys.argv.__len__() == 2:
        if sys.argv[1].__eq__("start"):
            run()
        elif sys.argv[1].__eq__("stop"):
            stop()
        elif sys.argv[1].__eq__("stat"):
            stat()
        else:
            display_help()
    else:
        display_help()

