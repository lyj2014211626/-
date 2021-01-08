import os
pid = os.getpid()
for i in range(100):
		print(i)
		if(i == 10):
				os.system('kill -9 {}'.format(pid))
				print('kill -9 {}'.format(pid))
