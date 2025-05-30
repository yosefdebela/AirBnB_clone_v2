

from fabric import task
from fabric import Connection

@task
def create(c):
	co = Connection(host='NB02', user='yosef',connect_kwargs={'password': 'yosef'})
	c.local('pwd')
	co.local('mkdir yosef')
	
if __name__ == '__main__':
	create()
