# /usr/bin/python3

import pyinotify
import sys
import signal
import os
import threading
import subprocess
from my_runner import MyRunner


# TODO(asharif): add a kill switch. Write to /tmp/kill_persist and have the
# script exit.
def Main(argv):
  print('Thread: ', threading.get_ident())
  watch_dir = os.path.abspath('.')
  print('Watching dir: ', watch_dir)
  watch_manager = pyinotify.WatchManager()
  runner = MyRunner(argv[1:])
  flags = pyinotify.IN_CLOSE_WRITE
  watch_manager.add_watch(watch_dir, flags, runner.on_change)
  watch_manager.add_watch('/tmp/kill_persist', flags, runner.killfile_handler)
  notifier = pyinotify.Notifier(watch_manager)
  runner.set_notifier(notifier)
  signal.signal(signal.SIGINT, runner.signal_handler)
  # Start the first command.
  runner.on_change(None)
  notifier.loop()

if __name__ == '__main__':
  Main(sys.argv)
