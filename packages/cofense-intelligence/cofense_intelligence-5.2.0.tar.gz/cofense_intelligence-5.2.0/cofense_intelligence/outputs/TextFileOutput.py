import os,sys

from .FileOutput import FileOutput


class TextFileOutput(FileOutput):
    def get_file_path(self, mrti):
        self.logger.debug('Calling get_file_path')
        return self.verify_dirs('list')

    def write_file(self, mrti, output_dir):
        self.logger.debug('Calling write_file')
        self._write_malware(mrti, output_dir)

    def _write(self, data, file_name):
        self.logger.debug('Calling _write')
        write_mods = {2: 'ab', 3: 'a'}
        py_version = sys.version_info[0]

        if isinstance(data, list):
            output = "\n".join(data)
        elif isinstance(data, str):
            output = data
        else:
            raise TypeError("data coming into _write must be a string or a list")

        # Check for duplicates before writing
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                content = f.read()
                if isinstance(data, list) and any(x in content for x in data):
                    return
                elif isinstance(data, str) and data in content:
                    return

        with open(file_name, write_mods[py_version]) as outfile:
            try:
                if not output.endswith("\n"):
                    output += "\n"
                outfile.write(output.lstrip())

            except Exception as e:
                self.logger.error(e)
                raise e

    def _get_list(self, mrti, block_type, impact):
        self.logger.debug('Calling _get_list')
        return [item.watchlist_ioc for item in mrti.block_set if item.block_type == block_type and item.impact == impact]

    def _write_malware(self, mrti, output_dir):
        self.logger.debug('Calling _write_malware')

        block_types = ['URL', 'Domain Name', 'IPv4 Address', 'Email']
        impacts = ['Major', 'Moderate', 'Minor']

        for block_type in block_types:
            for impact in impacts:
                iocs = self._get_list(mrti=mrti,
                                      block_type=block_type,
                                      impact=impact)
                self._write(iocs, os.path.join(output_dir, f'{block_type}_{impact}.txt'))

        # Files
        files = [item.md5 for item in mrti.executable_set]
        self._write(files, os.path.join(output_dir, 'md5.txt'))

        files = [item.sha1 for item in mrti.executable_set if item.sha1]
        self._write(files, os.path.join(output_dir, 'sha1.txt'))

        files = [item.sha256 for item in mrti.executable_set if item.sha256]
        self._write(files, os.path.join(output_dir, 'sha256.txt'))

        files = [item.sha512 for item in mrti.executable_set if item.sha512]
        self._write(files, os.path.join(output_dir, 'sha512.txt'))
