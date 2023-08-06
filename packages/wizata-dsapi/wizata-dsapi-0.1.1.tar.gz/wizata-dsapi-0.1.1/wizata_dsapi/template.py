import uuid
import json
from .api_dto import ApiDto


class Template(ApiDto):

    def __init__(self, template_id=None, key=None, name=None, properties=None):
        if template_id is None:
            self.template_id = uuid.uuid4()
        else:
            self.template_id = template_id
        self.key = key
        self.name = name
        self.properties = properties

    def api_id(self) -> str:
        """
        Id of the Template (template_id)

        :return: string formatted UUID of the template.
        """
        return str(self.template_id).upper()

    def endpoint(self) -> str:
        """
        Name of the endpoints used to manipulate templates.
        :return: Endpoint name.
        """
        return "Templates"

    def from_json(self, obj):
        """
        Load the Template entity from a dictionary.

        :param obj: Dict version of the Template.
        """
        if "id" in obj.keys():
            self.template_id = uuid.UUID(obj["id"])
        if "key" in obj.keys() and obj["key"] is not None:
            self.key = obj["key"]
        if "name" in obj.keys() and obj["name"] is not None:
            self.name = obj["name"]
        if "properties" in obj.keys() and obj["properties"] is not None:
            if isinstance(obj["properties"], str):
                self.properties = json.loads(obj["properties"])
            else:
                self.properties = obj["properties"]

    def to_json(self):
        """
        Convert the template to a dictionary compatible to JSON format.

        :return: dictionary representation of the Template object.
        """
        obj = {
            "id": str(self.template_id)
        }
        if self.key is not None:
            obj["key"] = str(self.key)
        if self.name is not None:
            obj["name"] = str(self.name)
        if self.properties is not None:
            obj["properties"] = json.dumps(self.properties)
