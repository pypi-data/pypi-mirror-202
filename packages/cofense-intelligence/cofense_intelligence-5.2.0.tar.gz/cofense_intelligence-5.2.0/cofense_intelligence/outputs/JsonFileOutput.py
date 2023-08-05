import json, os
from datetime import datetime
from .FileOutput import FileOutput

class JsonFileOutput(FileOutput):

    def get_file_path(self, mrti):
        output_path = self.verify_dirs("json")

        output_file = os.path.join(output_path, str(mrti.threat_id) + '.json')

        return output_file

    def write_file(self, mrti, output_file):
        with open(output_file, 'w') as outfile:
            outfile.write(json.dumps(mrti.json))
