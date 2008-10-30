# Copyright 2008 VPAC
#
# This file is part of django-pbs.
#
# django-pbs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-pbs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-pbs  If not, see <http://www.gnu.org/licenses/>.

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
        
        
        
        
