#!/usr/bin/env python

from django_pbs.moab import MoabServer


if __name__ == "__main__":
	s = MoabServer('edda-m.vpac.org')

	print s.mshow()
	print s.showstart(10, 10)

	print s.showstart(50, 20)
	


