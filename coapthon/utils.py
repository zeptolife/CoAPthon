import random
import string

__author__ = 'giacomo'


def generate_random_token(size):
    return ''.join(random.choice(string.ascii_letters) for _ in range(size))


def parse_blockwise(value):
    """
    Parse Blockwise option.

    :param value: option value
    :return: num, m, size
    """

    length = byte_len(value)
    if length == 1:
        num = value & 0xF0
        num >>= 4
        m = value & 0x08
        m >>= 3
        size = value & 0x07
    elif length == 2:
        num = value & 0xFFF0
        num >>= 4
        m = value & 0x0008
        m >>= 3
        size = value & 0x0007
    else:
        num = value & 0xFFFFF0
        num >>= 4
        m = value & 0x000008
        m >>= 3
        size = value & 0x000007
    return num, int(m), pow(2, (size + 4))


def byte_len(int_type):
    """
    Get the number of byte needed to encode the int passed.

    :param int_type: the int to be converted
    :return: the number of bits needed to encode the int passed.
    """
    length = 0
    while int_type:
        int_type >>= 1
        length += 1
    if length > 0:
        if length % 8 != 0:
            length = int(length / 8) + 1
        else:
            length = int(length / 8)
    return length


def parse_uri(uri):
    t = uri.split("://")
    tmp = t[1]
    t = tmp.split("/", 1)
    tmp = t[0]
    path = t[1]
    t = tmp.split(":", 1)
    try:
        host = t[0]
        port = int(t[1])
    except IndexError:
        host = tmp
        port = 5683

    return str(host), port, path


def create_logging():
    with open("logging.conf", "w") as f:
        f.writelines("[loggers]\n")
        f.writelines("keys=root\n\n")
        f.writelines("[handlers]\n")
        f.writelines("keys=consoleHandler\n\n")
        f.writelines("[formatters]\n")
        f.writelines("keys=simpleFormatter\n\n")
        f.writelines("[logger_root]\n")
        f.writelines("level=DEBUG\n")
        f.writelines("handlers=consoleHandler\n\n")
        f.writelines("[handler_consoleHandler]\n")
        f.writelines("class=StreamHandler\n")
        f.writelines("level=DEBUG\n")
        f.writelines("formatter=simpleFormatter\n")
        f.writelines("args=(sys.stdout,)\n\n")
        f.writelines("[formatter_simpleFormatter]\n")
        f.writelines("format=%(asctime)s - %(threadName)-10s - %(name)s - %(levelname)s - %(message)s\n")
        f.writelines("datefmt=")


class Tree(object):
    def __init__(self):
        self.tree = {}

    def dump(self):
        """
        Get all the paths registered in the server.

        :return: registered resources.
        """
        return self.tree.keys()

    def with_prefix(self, path):
        ret = []
        for key in self.tree.keys():
            if path.startswith(key):
                ret.append(key)

        if len(ret) > 0:
            return ret
        raise KeyError

    def __getitem__(self, item):
        return self.tree[item]

    def __setitem__(self, key, value):
        self.tree[key] = value

    def __delitem__(self, key):
        del self.tree[key]
