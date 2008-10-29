"""
Module for abstract serializer/unserializer base classes.
"""

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import datetime
from django_pbs.jobs.models import Job
from django_pbs.servers.models import Server, Node, Queue, RelationList

relations = [Server, Job, Node, Queue,]

class SerializationError(Exception):
    """Something bad happened during serialization."""
    pass

class DeserializationError(Exception):
    """Something bad happened during deserialization."""
    pass

class Serializer(object):
    """
    Abstract serializer base class.
    """

    def serialize(self, obj_list, **options):
        """
        Serialize a queryset.
        """
        self.options = options

        self.stream = options.get("stream", StringIO())
        self.selected_fields = options.get("fields")

        self.start_serialization()
        for obj in obj_list:
            self.start_object(obj)
            for field in obj.__dict__:
                field_type = getattr(obj, field).__class__
                if field_type in relations:
                    self.handle_relation(obj, field)
                elif field_type == RelationList:
                    self.handle_relation_list(obj, field)
                else:
                    self.handle_field(obj, field)
            self.end_object(obj)
        self.end_serialization()
        return self.getvalue()

    def get_string_value(self, obj, field):
        """
        Convert a field's value to a string.
        """

        if isinstance(getattr(obj, field), datetime.date):
            value = getattr(obj, field).strftime("%Y-%m-%d %H:%M:%S")
        else:
            value = str(getattr(obj, field))
        return value

    def start_serialization(self):
        """
        Called when serializing of the queryset starts.
        """
        raise NotImplementedError

    def end_serialization(self):
        """
        Called when serializing of the queryset ends.
        """
        pass

    def start_object(self, obj):
        """
        Called when serializing of an object starts.
        """
        raise NotImplementedError

    def end_object(self, obj):
        """
        Called when serializing of an object ends.
        """
        pass

    def handle_field(self, obj, field):
        """
        Called to handle each individual (non-relational) field on an object.
        """
        raise NotImplementedError


    def getvalue(self):
        """
        Return the fully serialized queryset (or None if the output stream is
        not seekable).
        """
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()



class Deserializer(object):
    """
    Abstract base deserializer class.
    """

    def __init__(self, stream_or_string, **options):
        """
        Init this serializer given a stream or a string
        """
        self.options = options
        if isinstance(stream_or_string, basestring):
            self.stream = StringIO(stream_or_string)
        else:
            self.stream = stream_or_string

    def __iter__(self):
        return self

    def next(self):
        """Iteration iterface -- return the next item in the stream"""
        raise NotImplementedError

class DeserializedObject(object):
    """
    A deserialized model.

    Basically a container for holding the pre-saved deserialized data along
    .


    """

    def __init__(self, obj):
        self.object = obj

    def __repr__(self):
        return "<DeserializedObject: %s>" % str(self.object)

