__author__ = 'kth'


def build_entity(xml_node):
    attrs = {}
    clazz_name = xml_node.tag.capitalize()
    sub_entity = {}
    for child_node in xml_node:
        if len(child_node) > 0:
            entity = build_entity(child_node)
            if child_node.tag in sub_entity.keys():
                if type(sub_entity[child_node.tag]) is list:
                    sub_entity[child_node.tag].append(entity)
                else:
                    t = sub_entity[child_node.tag]
                    sub_entity[child_node.tag] = [t, entity]
            else:
                sub_entity[child_node.tag] = entity
        else:
            attrs[child_node.tag] = child_node.text
    for att in xml_node.attrib.keys():
        attrs[att] = xml_node.attrib[att]
    entity_clazz = MetaEntity(clazz_name, (object,), attrs)
    for s in sub_entity.keys():
        attr_name = s
        if type(sub_entity[s]) is list:
            attr_name = '%s%s' % (attr_name, 's')
        setattr(entity_clazz, attr_name, sub_entity[s])
    return entity_clazz()

def proxy_call(instance, item):
    try:
        return super(type(instance), instance).__getattribute__(item)
    except AttributeError:
        return EmptyEntity()

class MetaEntity(type):
    def __init__(cls, name, bases, dct):
        super(MetaEntity, cls).__init__(name, bases, dct)
        setattr(cls, "__getattribute__", proxy_call)

class EmptyEntity:

    __metaclass__ = MetaEntity

    def next(self):
        raise StopIteration

    def __iter__(self):
        return self
