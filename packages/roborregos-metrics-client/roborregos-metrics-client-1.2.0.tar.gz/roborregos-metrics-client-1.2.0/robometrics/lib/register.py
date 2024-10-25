import os
import threading


class Register(object):
    @classmethod
    def add_process_async(cls, pid: int):
        with open('/tmp/worker', 'w') as f:
            f.write(str(pid))
        print(f"Process {pid} registered.")

    @classmethod
    def register_async(cls, pid: int):
        t = threading.Thread(target=cls.add_process_async, args=(pid,))
        t.start()

    @classmethod
    def add_process(cls, pid: int):
        with open('/tmp/worker', 'w') as f:
            f.write(str(pid))

    @classmethod
    def unregister_process(cls, pid: int):
        with open('/tmp/worker', 'w') as f:
            f.write(str(-1*pid))

    @classmethod
    def auto_register(cls):
        pid = os.getpid()
        cls.add_process(pid)

    @classmethod
    def async_auto_register(cls):
        pid = os.getpid()
        cls.register_async(pid)

    @classmethod
    def auto_unregister(cls):
        pid = os.getpid()
        cls.unregister_process(pid)
