import os
import argparse
import signal
import daemon
import lockfile
import bottle
from contextlib import contextmanager

@contextmanager
def __locked_pidfile(filename):
    # Acquire the lockfile
    lock = lockfile.FileLock(filename)
    lock.acquire(-1)
    
    # Write out our pid
    realfile = open(filename, "w")
    realfile.write(str(os.getpid()))
    realfile.close()

    # Yield to the daemon
    yield
    
    # Cleanup after ourselves
    os.remove(filename)
    lock.release()


def daemon_run(host="localhost", port="8080", pidfile=None, logfile=None):
    """
    Get the bottle 'run' function running in the background as a daemonized
    process. 

    :host: The host interface to listen for connections on. Enter 0.0.0.0
           to listen on all interfaces. Defaults to localhost.
    :port: The host port to listen on. Defaults to 8080.
    :pidfile: The file to use as the process id file. Defaults to "bottle.pid"
    :logfile: The file to log stdout and stderr from bottle to. Defaults to "bottle.log"

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "stop"])
    args = parser.parse_args()

    if pidfile is None:
        pidfile = os.path.join(
            os.getcwd(),
            "bottle.pid"
        )
    
    if logfile is None:
        logfile = os.path.join(
            os.getcwd(),
            "bottle.log"
        )

    if args.action == "start":
        log = open(logfile,"w+")
        context = daemon.DaemonContext( 
            pidfile=__locked_pidfile(pidfile),
            stdout=log,
            stderr=log
        )
        
        with context:
            bottle.run(host=host, port=port)
    else:
        with open(pidfile,"r") as p:
            pid = int(p.read())
            os.kill(pid, signal.SIGTERM)

if __name__ == "__main__":
    daemon_run()
