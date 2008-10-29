import os

class MoabServer(object):

    def __init__(self, server):
        self.server = str(server)




    def showstart(self, procs, time):
	
	procs = str(procs)
	time = str(time)
	

	command = 'showstart --host=%s %s@%s' % (self.server, procs, time)
	print command	

        result = os.popen(command).readlines()
	

        if result[0] == '\n':
            return result[1]

        return result[2]


	

    def mshow(self):

        command = "mshow --host=%s -a --flags=future |head -7" % self.server

        result = os.popen(command).readlines()

        result[0].split(' ')
        
        
        
        
