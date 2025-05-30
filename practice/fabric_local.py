from fabric import Connection
from fabric import task
from datetime import datetime
import os
#!/usr/bin/env python3

# Establish connection


# Get current working directory (proper Fabric way)
@task
def create(c):
    c = Connection(host='NB02', user='yosef', connect_kwargs={'password': 'yosef'})
    result = c.local('pwd', hide=True)
    current_dir = result.stdout.strip()
    print(f"Current directory: {current_dir}")

    # Create versions directory inside current directory
    c.local(f'mkdir -p {current_dir}/versions')
    print('Folder "versions" created')

    # List contents to verify
    c.local(f'ls -l {current_dir}')


