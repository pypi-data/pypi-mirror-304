from queue import Queue


class ReplacingQueue(Queue):
    def __init__(self, maxsize):
        super().__init__(maxsize=maxsize)

    def put(self, item):
        if self.full():
            self.get()
        super().put(item)
