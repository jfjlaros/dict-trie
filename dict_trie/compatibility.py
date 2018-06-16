from itertools import imap


class iMap(imap):
    def __next__(cls):
        return cls.next()


map = iMap
