from scrapy.exporters import XmlItemExporter

class DropBlankFieldsXmlItemExporter(XmlItemExporter):
    def __init__(self, file, **kwargs) -> None:
        kwargs['export_empty_fields'] = False
        super(DropBlankFieldsXmlItemExporter, self).__init__(file, **kwargs)

    def export_item(self, item):
        self._beautify_indent(depth=1)
        self.xg.startElement(self.item_element, {})
        self._beautify_newline()
        for name, value in self._get_serialized_fields(item, default_value=''):
            # hack: drop fields with value == 'None'
            if value != 'None':
                self._export_xml_field(name, value, depth=2)
        self._beautify_indent(depth=1)
        self.xg.endElement(self.item_element)
        self._beautify_newline(new_item=True)