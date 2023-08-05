import os
from .FileOutput import FileOutput


class CefFileOutput(FileOutput):

    def get_file_path(self, mrti):
        output_path = self.verify_append_dirs()
        output_file = os.path.join(output_path, "cef")
        return output_file

    def write_file(self, mrti, output_file):
        with open(output_file, 'ab') as outfile:
            outfile.write(mrti.encode('utf-8') + b'\n')
