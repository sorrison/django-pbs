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
XML serializer.
"""
from django_pbs.serializers import base 
from django_pbs.serializers.xmlutil import SimplerXMLGenerator
from xml.dom import pulldom
import socket
from django.conf import settings


class Serializer(base.Serializer):
    """
    Serializes a QuerySet to XML.
    """

    def indent(self, level):
        if self.options.get('indent', None) is not None:
            self.xml.ignorableWhitespace('\n' + ' ' * self.options.get('indent', None) * level)

    def start_serialization(self):
        """
        Start serialization -- open the XML document and the root element.
        """
        self.xml = SimplerXMLGenerator(self.stream, self.options.get("encoding", 'utf-8'))
        self.xml.startDocument()
        self.xml.startElement("django-pbs", {
                "version" : "1.0",
                "xmlns:xlink": "http://www.w3.org/1999/xlink",
                })

    def end_serialization(self):
        """
        End serialization -- end the document.
        """
        self.indent(0)
        self.xml.endElement("django-pbs")
        self.xml.endDocument()

    def start_object(self, obj):
        """
        Called as each object is handled.
        """
        self.indent(1)
        self.xml.startElement('object', {
                "pk"    : obj._get_pk_val(),
                "xlink:href" : 'http://%s/xml%s' % (socket.gethostbyaddr(socket.gethostname())[0], obj.get_absolute_url()),
                "class" : '%s.%s' % (obj.__module__, obj.__class__.__name__),
        })

    def end_object(self, obj):
        """
        Called after handling all fields for an object.
        """
        self.indent(1)
        self.xml.endElement('object')
    

    def handle_field(self, obj, field):
        """
        Called to handle each field on an object (except for ForeignKeys and
        ManyToManyFields)
        """

        self.indent(2)
        self.xml.startElement("field", {
            "name" : field,
            "type" : type(getattr(obj, field)).__name__
        })

        # Get a "string version" of the object's data (this is handled by the
        # serializer base class).
        #if getattr(obj, field.name) is not None:
        value = self.get_string_value(obj, field)
        self.xml.characters(value)
        #else:
            #self.xml.addQuickElement("None")

        self.xml.endElement("field")


    def handle_relation(self, object, field=None):
        
        self.indent(2)
        self.xml.startElement('object', {
                "pk"    : object._get_pk_val(),
                "xlink:href" : 'http://%s/xml%s' % (socket.gethostbyaddr(socket.gethostname())[0], object.get_absolute_url()),
                "class" : '%s.%s' % (object.__module__, object.__class__.__name__),
        })
        self.xml.endElement('object')
              

    def handle_relation_list(self, object, field):
        
        self.indent(2)
        self.xml.startElement('RelationList', {
                "name"    : field,
        })
        for item in getattr(object, field):
            self.handle_relation(item)
        self.xml.endElement("RelationList")
        



class Deserializer(base.Deserializer):
    """
    Deserialize XML.
    """

    def __init__(self, stream_or_string, **options):
        super(Deserializer, self).__init__(stream_or_string, **options)
        self.event_stream = pulldom.parse(self.stream)

    def next(self):
        for event, node in self.event_stream:
            if event == "START_ELEMENT" and node.nodeName == 'object':
                self.event_stream.expandNode(node)
                return self._handle_object(node)
        raise StopIteration

    def _handle_object(self, node):
        """
        Convert an <object> node to a DeserializedObject.
        """
        # Look up the model using the model loading mechanism. If this fails,
        # bail.
        Object = self._get_object_from_node(node, "class")

        # Start building a data dictionary from the object.  If the node is
        # missing the pk attribute, bail.
        pk = node.getAttribute("pk")
        if not pk:
            raise base.DeserializationError("<object> node is missing the 'pk' attribute")

        #data = {Model._meta.pk.attname : Model._meta.pk.to_python(pk)}
        data = {}

        # Deseralize each field.
        for field_node in node.getElementsByTagName("field"):
            # If the field is missing the name attribute, bail (are you
            # sensing a pattern here?)
            field_name = field_node.getAttribute("name")
            if not field_name:
                raise base.DeserializationError("<field> node is missing the 'name' attribute")
            print field_name
            # Get the field from the Model. This will raise a
            # FieldDoesNotExist if, well, the field doesn't exist, which will
            # be propagated correctly.
            #field = Model._meta.get_field(field_name)

            
            value = getInnerText(field_node).strip()
            data[field_name] = value

        print data
        # Return a DeserializedObject so that the m2m data has a place to live.
        return base.DeserializedObject(Object(**data))

    def _get_object_from_node(self, node, attr):
        """
        Helper to look up a model from a <object model=...> or a <field
        rel=... to=...> node.
        """
        model_identifier = node.getAttribute(attr)
        if not model_identifier:
            raise base.DeserializationError(
                "<%s> node is missing the required '%s' attribute" \
                    % (node.nodeName, attr))
        try:
            Model = my_import(model_identifier)
        except TypeError:
            Model = None
        if Model is None:
            raise base.DeserializationError(
                "<%s> node has invalid model identifier: '%s'" % \
                    (node.nodeName, model_identifier))

        return Model

    #def _handle_relation_node(self, node, field):
    #    """
    #    Handle a <relation> node for a ForeignKey
    #    """
    #    # Check if there is a child node named 'None', returning None if so.
    #    if node.getElementsByTagName('None'):
    #        return None
    #    else:
    #        return field.rel.to._meta.get_field(field.rel.field_name).to_python(
    #                   getInnerText(node).strip())

 


def getInnerText(node):
    """
    Get all the inner text of a DOM node (recursively).
    """
    # inspired by http://mail.python.org/pipermail/xml-sig/2005-March/011022.html
    inner_text = []
    for child in node.childNodes:
        if child.nodeType == child.TEXT_NODE or child.nodeType == child.CDATA_SECTION_NODE:
            inner_text.append(child.data)
        elif child.nodeType == child.ELEMENT_NODE:
            inner_text.extend(getInnerText(child))
        else:
           pass
    return u"".join(inner_text)



def my_import(structured_name):
    component_names = structured_name.split('.')
    mod = __import__('.'.join(component_names[:-1]))
    for component_name in component_names[1:]:
        mod = getattr(mod, component_name)
    return mod
