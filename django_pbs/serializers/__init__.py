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
Interfaces for serializing Django objects.

Usage::

    from django.core import serializers
    json = serializers.serialize("json", some_query_set)
    objects = list(serializers.deserialize("json", json))

To add your own serializers, use the SERIALIZATION_MODULES setting::

    SERIALIZATION_MODULES = {
        "csv" : "path.to.csv.serializer",
        "txt" : "path.to.txt.serializer",
    }

"""

from django.conf import settings

# Built-in serializers
BUILTIN_SERIALIZERS = {
    "xml"    : "django_pbs.serializers.xml_serializer",
}


_serializers = {}

def register_serializer(format, serializer_module):
    """Register a new serializer by passing in a module name."""
    module = __import__(serializer_module, {}, {}, [''])
    _serializers[format] = module

def unregister_serializer(format):
    """Unregister a given serializer"""
    del _serializers[format]

def get_serializer(format):
    if not _serializers:
        _load_serializers()
    return _serializers[format].Serializer

def get_serializer_formats():
    if not _serializers:
        _load_serializers()
    return _serializers.keys()

def get_deserializer(format):
    if not _serializers:
        _load_serializers()
    return _serializers[format].Deserializer

def serialize(format, queryset, **options):
    """
    Serialize a queryset (or any iterator that returns database objects) using
    a certain serializer.
    """
    s = get_serializer(format)()
    s.serialize(queryset, **options)
    return s.getvalue()

def deserialize(format, stream_or_string):
    """
    Deserialize a stream or a string. Returns an iterator that yields ``(obj,
    m2m_relation_dict)``, where ``obj`` is a instantiated -- but *unsaved* --
    object, and ``m2m_relation_dict`` is a dictionary of ``{m2m_field_name :
    list_of_related_objects}``.
    """
    d = get_deserializer(format)
    return d(stream_or_string)

def _load_serializers():
    """
    Register built-in and settings-defined serializers. This is done lazily so
    that user code has a chance to (e.g.) set up custom settings without
    needing to be careful of import order.
    """
    for format in BUILTIN_SERIALIZERS:
        register_serializer(format, BUILTIN_SERIALIZERS[format])
    if hasattr(settings, "SERIALIZATION_MODULES"):
        for format in settings.SERIALIZATION_MODULES:
            register_serializer(format, settings.SERIALIZATION_MODULES[format])
