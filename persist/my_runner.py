import os
import signal
import subprocess
import sys
import threading


class MyRunner:
  def __init__(self, cmd):
    self.cmd = cmd
    self.timer = None
    self.subprocess = None
    self.notifier = None
    self.exiting = False
    self.lock = threading.Lock()

  def set_notifier(self, notifier):
    self.notifier = notifier

  def signal_handler(self, sig, frame):
    print('Caught Ctrl-c.')
    self.exit_process()

  def exit_process(self):
    print('Uninstalling notifications')
    if self.notifier:
      self.notifier.stop()
    print('Killing subprocess')
    with self.lock:
      self.exiting = True
      self.kill_subprocess()
      sys.exit(0)

  def kill_subprocess(self):
    if not self.subprocess:
      print('No subprocess to kill.')
      return
    try:
      pgid = os.getpgid(self.subprocess.pid)
      print('Killing process: ', self.subprocess.pid, ' pgid: ', pgid, ' from thread: ', threading.get_ident(), ' aka: ', threading.current_thread().name)
      os.killpg(os.getpgid(self.subprocess.pid), signal.SIGTERM)
    except ProcessLookupError:
      print('Process: ', self.subprocess.pid, ' already gone.')
    except Exception as e:
      print('Caught exception: ', e)
      raise
    print('Done killing from thread: ', threading.get_ident(), ' aka: ', threading.current_thread().name)

    try:
      self.subprocess.wait(timeout=5)
    except subprocess.TimeoutExpired:
      print('WARNING: Process: ', self.subprocess.pid, ' DID NOT EXIT.')

  def run_subprocess(self):
    print('Thread: ', threading.get_ident(), ' running: ', ' '.join(self.cmd))
    my_subprocess = None
    with self.lock:
      if self.exiting:
        print('Main thread wants us to exit. Not starting subprocess.')
        return

      if self.subprocess:
        self.kill_subprocess()
      self.subprocess = subprocess.Popen(self.cmd, preexec_fn=os.setsid)
      my_subprocess = self.subprocess
      print('Starting subprocess: ', self.subprocess.pid, ' ', ' '.join(self.cmd))
    my_subprocess.communicate()
    print('Process: ', my_subprocess.pid, ' exited.')

  def killfile_handler(self, event):
    print('Exiting due to killfile write')
    self.exit_process()

  def on_change(self, event):
    # Use a timer to debounce events in case they come in quick succession.
    try:
      if self.timer:
        print('Cancelling')
        self.timer.cancel()
    except AttributeError:
      pass
    print('Scheduling from thread: ', threading.get_ident(), ' ', event)
    self.timer = threading.Timer(1, self.run_subprocess)
    self.timer.start()


