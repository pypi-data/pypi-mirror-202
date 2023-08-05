import os

from datetime import datetime

from .FileOutput import FileOutput
from cofense_intelligence.transforms.Stix2 import MalwareThreatReportStix
from cofense_intelligence.intelligence import MalwareThreatReport


class Stix2FileOutput(FileOutput):

    def get_file_path(self, mrti: MalwareThreatReport):
        output_path = self.verify_dirs("stix2")
        output_file = os.path.join(output_path, f'{mrti.threat_id}.json')
        return output_file

    def write_file(self, mrti: MalwareThreatReport, output_file: str):
        with open(output_file, 'w') as outfile:
            MalwareThreatReportStix(mrti=mrti).stix_bundle.fp_serialize(outfile)
