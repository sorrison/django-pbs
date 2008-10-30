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

"""
YAML serializer.

Requires PyYaml (http://pyyaml.org/), but that's checked for in __init__.
"""

import datetime
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import yaml

class Serializer(PythonSerializer):
    """
    Convert a queryset to YAML.
    """
    def end_serialization(self):
        self.options.pop('stream', None)
        self.options.pop('fields', None)
        yaml.dump(self.objects, self.stream, **self.options)

    def getvalue(self):
        return self.stream.getvalue()

def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of YAML data.
    """
    if isinstance(stream_or_string, basestring):
        stream = StringIO(stream_or_string)
    else:
        stream = stream_or_string
    for obj in PythonDeserializer(yaml.load(stream)):
        yield obj

