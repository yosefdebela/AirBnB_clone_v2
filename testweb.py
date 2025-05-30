
from dotenv import load_dotenv
import os
from fabric import Connection
load_dotenv()
web01 = os.getenv('web01')
web02 = os.getenv('web02')
key_path = os.getenv('file_path')
password = os.getenv('password')

def list():
    c = Connection(host='web01', user='ubuntu', connect_kwargs={"key_filename":key_path, "password": password})
    return c.run('ls -l /etc')

if __name__ == "__main__":
    result = list()
    print(result.stdout.strip())

    print(result.ok)
    print(result.failed)
    print(result.connection)
    print(result.command)
    print(result.return_code)
    print(result.exited)  # This is the same as result.return_code