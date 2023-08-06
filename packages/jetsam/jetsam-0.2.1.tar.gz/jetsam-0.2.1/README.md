# Jetsam
- True daemonizer using native C calls  
- Currently only compatible with `*nix` file systems 
- <u>Extra Paranoid Edition</u> uses that **double fork magic!** 
> jetsam definition: floating debris ejected from a ship 

## C Extension 
To showcase a C library being used as a _native python module_

## Example 
```python
import time
import logging
import jetsam
from jetsam import daemon

# jetsam will log pids and errors from daemons
# to a single log file. It will also update the file
# with the current status of the daemon
#
#   function_name:pid:status
#
jetsam.set_logfile("user_daemon.log")  # defaults to /tmp/jetsam.log


@daemon
def func():
    logging.basicConfig(filename="func.log", level=logging.DEBUG, filemode="w")
    while True:
        time.sleep(1)
        logging.debug("I am running in my own interpreter!")


func()  # detachs from current interpreter each function immediately returns 

print("simulate long running process...")
time.sleep(3)

jetsam.end_daemon(func)

print("Eject and forget with jetsam!")
```
