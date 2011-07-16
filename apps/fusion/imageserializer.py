"""
XML serializer with an extra field to indicate if an image has related fusions
"""

from django.core.serializers import xml_serializer

class Serializer(xml_serializer.Serializer):
    def end_object(self, obj, *args, **kwargs):
        hasfusions = obj.then.count() > 0
        self.indent(2)
        self.xml.startElement("field", {
            "name" : 'hasfusion',
            "fusioncount" : str(obj.then.count()),
            "latitude" : str(obj.then.all()[0].latitude()) if hasfusions else str(obj.latitude),
            "longitude" : str(obj.then.all()[0].longitude()) if hasfusions else str(obj.longitude),
        })

        # Get a "string version" of the object's data.
        if hasfusions:
            self.xml.characters('true')
        else:
            self.xml.characters('false')

        self.xml.endElement("field")

        return super(Serializer, self).end_object(obj, *args, **kwargs)
