from cd2t.types.base import BaseDataType
from cd2t.types.any import AnyDataType
from cd2t.References import References, ReferenceElement, OPT
from cd2t.results import WrongValueFinding, UniqueErrorFinding, FindingsList
from cd2t.schema import SchemaError
import re


class IDList(BaseDataType):
    type = 'idlist'
    matching_classes = [dict]
    support_reference = True
    options = [
        # option_name, required, class
        ('minimum', False, int, None),
        ('maximum', False, int, None),
        ('elements', True, dict, None),
        ('id_type', False, str, 'string'),
        ('id_minimum', False, int, None),
        ('id_maximum', False, int, None),
        ('allowed_ids', False, list, None),
        ('not_allowed_ids', False, list, list()),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.minimum = None
        self.maximum = None
        self.elements = None
        self.element_type = None
        self.id_type = 'string'
        self.id_minimum = None
        self.id_maximum = None
        self.allowed_ids = None
        self.not_allowed_ids = list()
    
    def build_schema(self, schema :dict, path :str,
                     data_types :dict, subschemas :dict,
                     subpath :list):
        self.__init__()
        path = path + '{id}'
        self.load_reference_option(schema, path)
        self.load_schema_options(schema, path)
        if self.id_type not in ['string', 'integer']:
            raise SchemaError("id_type '%s' is not valid" % self.id_type, path)
        if 'type' in self.elements.keys():
            element_type_name = self.elements['type']
            if element_type_name not in data_types:
                raise SchemaError("Elements data type '%s' not found" % element_type_name, path)
            self.element_type = data_types[element_type_name]()
        elif self.elements:
            raise SchemaError("'type' not found in elements schema", path)
        else:
            self.element_type = AnyDataType()
        # Save recursively detected data type (i.e. from 'schema' --> subschema)
        self.element_type = self.element_type.build_schema(
            schema=self.elements, path=path,
            data_types=data_types, subschemas=subschemas, subpath=subpath)
        return self
    
    def build_sub_references(self, data :any, path :str, references :References):
        for id, element in data.items():
            self.element_type.build_references(data=element,
                                            path=path + '{id}',
                                            references=references)
    
    def autogenerate_data(self, data :any, path :str, references :References):
        FL = FindingsList()
        if not self.data_matches_type(data):
            return data, FL
        new_dict = dict()
        for id, element in data.items():
            new_path = path + '{}' + str(id)
            _data, _FL = self.element_type.autogenerate_data(data=element,
                                                            path=new_path,
                                                            references=references)
            new_dict[id] = _data
            FL += _FL
        return new_dict, FL

    def verify_data(self, data :any, path :str, references=References()) -> FindingsList:
        FL = FindingsList()
        path = path + '{}'
        if self.minimum and len(data) < self.minimum:
            FL.append(WrongValueFinding(
                        path=path,
                        message='Attribute count is lower than minimum %d' % self.minimum))
        elif self.maximum is not None and len(data) > self.maximum:
            FL.append(WrongValueFinding(
                        path=path,
                        message='Attribute count is greater than maximum %d' % self.maximum))

        for id, element in data.items():
            _FL = FindingsList()
            id_path = path + str(id)
            if self.id_type == 'string':
                if not isinstance(id, str):
                    _FL.append(WrongValueFinding(
                        path=id_path, message="Attribute is not a string"))
                elif self.id_minimum and len(id) < self.id_minimum:
                    _FL.append(WrongValueFinding(
                        path=id_path,
                        message="String length of attribute is lower than minimum %d" %
                                self.id_minimum))
                elif self.id_maximum is not None and len(id) > self.id_maximum:
                    _FL.append(WrongValueFinding(
                        path=id_path,
                        message="String length of attribute is greater than maximum %d" %
                                self.id_maximum))
                else:
                    not_allowed = False
                    for regex in self.not_allowed_ids:
                        if re.match(regex, id):
                            _FL.append(WrongValueFinding(
                                path=id_path,
                                message="Attribute is not allowed"))
                            not_allowed = True
                    if not not_allowed and self.allowed_ids:
                        allowed = False
                        for regex in self.allowed_ids:
                            if re.match(regex, id):
                                allowed = True
                                break
                        if not allowed:
                            _FL.append(WrongValueFinding(
                                    path=id_path,
                                    message="Attribute does not match any allowed value"))
                    
            else: # id_type == 'integer'
                if not isinstance(id, int):
                    _FL.append(WrongValueFinding(
                        path=id_path, message="Attribute is not a integer"))
                elif self.id_minimum and id < self.id_minimum:
                    _FL.append(WrongValueFinding(
                        path=id_path,
                        message="Attribute is lower than minimum %d" % self.id_minimum))
                elif self.id_maximum is not None and id > self.id_maximum:
                    _FL.append(WrongValueFinding(
                        path=id_path,
                        message="Attribute is greater than maximum %d" % self.id_maximum))
                elif id in self.not_allowed_ids:
                    _FL.append(WrongValueFinding(
                        path=id_path,
                        message="Attribute is not allowed"))
                elif self.allowed_ids and id not in self.allowed_ids:
                    _FL.append(WrongValueFinding(
                        path=id_path,
                        message="Attribute is not an allowed value"))

            if not _FL:
                FL += (self.element_type.validate_data(
                    data=element, path=id_path, references=references))
            else:
                FL += _FL
        return FL

    def verify_reference(self, data :any, path :str, references=References()) -> FindingsList:
        if not self.data_matches_type(data) or OPT.NONE in self.ref_OPT:
            return []
        results = list()
        for id in data.keys():
            id_path = path + '{}' + id
            element = ReferenceElement(self.ref_key, id_path, id, self.ref_OPT)
            other = references.same_unique(element)
            if other is not None:
                if references.namespace != other.namespace:
                    _path = "%s > %s" % (other.namespace, other.path)
                else:
                    _path = other.path
                results.append(UniqueErrorFinding(
                    path=id_path, message="ID '%s' already used at '%s'" % (str(id), _path)))
            else:
                references.add_element(element)
        return results
