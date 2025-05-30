#!/usr/bin/env python3
from fabric import Connection


def list_files():
    # Connect to localhost (add user/key if needed)
    c = Connection(host='localhost', user='root',  port=4444, connect_kwargs={'key_filename': '/home/yosef/.ssh/school'})

    # Run command (use full path for system directories)
    result = c.run('ls -la /etc', hide=False)
    print(result.stdout)


if __name__ == '__main__':
    list_files()