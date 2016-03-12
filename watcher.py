#!/usr/bin/python

import sys, time, logging, subprocess, os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler  

class BuilderHandler(PatternMatchingEventHandler):
    patterns = ["*.py", "*.html"]

    def __init__(self, script):
        PatternMatchingEventHandler.__init__(self)
        self.script = script

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug
        subprocess.call(self.script)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


def main():
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    if len(sys.argv) < 2:
        print "USAGE: watcher.py scriptname dirname"
        return
    script = os.path.abspath(sys.argv[1])
    event_handler = BuilderHandler(script)
    path = sys.argv[2] if len(sys.argv) > 1 else '.'
    path = os.path.abspath(path)
    print "Watching for changes in " + path
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()