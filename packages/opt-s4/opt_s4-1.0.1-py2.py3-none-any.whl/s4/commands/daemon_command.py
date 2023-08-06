#! -*- encoding: utf-8 -*-
from collections import defaultdict

from s4.commands import Command
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import time

# Don't crash on import if the underlying operating system does not support INotify
try:
    from inotify_simple import flags
    from s4.inotify_recursive import INotifyRecursive

    supported = True
except (OSError, ModuleNotFoundError):
    supported = False


# class DaemonCommand(Command):
#     def run(self, terminator=lambda x: False):
#         if not supported:
#             self.logger.info("Cannot run INotify on your operating system")
#             self.logger.info(
#                 "Only Linux machines are officially supported for this command"
#             )
#             return
#
#         all_targets = list(self.config["targets"].keys())
#         if not self.args.targets:
#             targets = all_targets
#         else:
#             targets = self.args.targets
#
#         if not targets:
#             self.logger.info("No targets available")
#             self.logger.info('Use "add" command first')
#             return
#
#         for target in targets:
#             if target not in self.config["targets"]:
#                 self.logger.info("Unknown target: %s", target)
#                 return
#
#         notifier = INotifyRecursive()
#         watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY
#
#         watch_map = {}
#
#         for target in targets:
#             entry = self.config["targets"][target]
#             path = entry["local_folder"]
#             self.logger.info("Watching %s", path)
#             for wd in notifier.add_watches(path.encode("utf8"), watch_flags):
#                 watch_map[wd] = target
#
#             # Check for any pending changes
#             worker = self.get_sync_worker(target)
#             worker.sync(conflict_choice=self.args.conflicts)
#
#         index = 0
#
#         while not terminator(index):
#             index += 1
#
#             to_run = defaultdict(set)
#
#             for event in notifier.read(read_delay=self.args.read_delay):
#                 target = watch_map[event.wd]
#
#                 # Don't bother running for .index
#                 if event.name not in (".index", ".s4lock"):
#                     to_run[target].add(event.name)
#
#             for target, keys in to_run.items():
#                 worker = self.get_sync_worker(target)
#
#                 # Should ideally be setting keys to sync
#                 self.logger.info("Syncing {}".format(worker))
#                 worker.sync(conflict_choice=self.args.conflicts)


# override by Minghuan Ma
class DaemonCommand(Command):

    """
    One-way continuous sync from localpath to s3 path (uses a file watcher called watchdog)
    """

    def run(self, terminator=lambda x: False):
        print("Daemon command running")

        all_targets = list(self.config["targets"].keys())
        if not self.args.targets:
            targets = all_targets
        else:
            targets = self.args.targets

        if not targets:
            self.logger.info("No targets available")
            self.logger.info('Use "add" command first')
            return

        for target in targets:
            if target not in self.config["targets"]:
                self.logger.info("Unknown target: %s", target)
                return

        for target in targets:
            entry = self.config["targets"][target]
            path = entry["local_folder"]

            # do sync at begainning
            worker = self.get_sync_worker(target)
            # conflict_choice参数："1"/"2"/"ignore"
            # conflict_choice="1": 如果某些文件s3dir有, localdir没有, 删除s3路径上的差别文件
            # conflict_choice="2": 如果某些文件s3dir有, localdir没有, 将差别文件下拉到localdir
            # conflict_choice="ignore": 忽略差别文件
            worker.sync(conflict_choice="ignore")

            event_handler = FileWatchHandler(worker, self.args)
            observer = Observer()
            observer.schedule(event_handler, path, recursive=True)
            observer.start()
            self.logger.info("Watching %s", path)

            try:
                while True:
                    time.sleep(2)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()


class FileWatchHandler(PatternMatchingEventHandler):

    def __init__(self, sync_worker, args):
        super().__init__(ignore_patterns=[".index", ".s4lock"])
        self.sync_worker = sync_worker
        self.args = args

    def on_any_event(self, event):

        if event.is_directory:
            return

        print("Watchdog received [{}] event for [{}] - [{}]"
              .format(event.event_type, "directory" if event.is_directory else "file", event.src_path))
        self.sync_worker.sync(conflict_choice=self.args.conflicts)