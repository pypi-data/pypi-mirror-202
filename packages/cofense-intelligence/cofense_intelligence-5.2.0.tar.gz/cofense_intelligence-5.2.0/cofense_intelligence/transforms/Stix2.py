from typing import Optional
from datetime import datetime

from stix2 import Bundle, File, URL, DomainName, IPv4Address, EmailAddress, \
    Relationship, Identity, Incident, TLP_AMBER, ExternalReference

from cofense_intelligence.intelligence import MalwareThreatReport


class MalwareThreatReportStix(MalwareThreatReport):
    def __init__(self, mrti: MalwareThreatReport):
        super().__init__(mrti.json)
        self._mrti = mrti

        self._author: Optional[Identity] = None
        self._incident: Optional[Incident] = None
        self._threathq_external_reference: Optional[ExternalReference] = None

        self._stix_objects: list = []
        self._tags: list = []
        self._stix_bundle: Optional[Bundle] = None
        self._confidence: int = 100

        self._block_obj = {
            "URL": URL,
            "Domain Name": DomainName,
            "IPv4 Address": IPv4Address,
            "Email": EmailAddress
        }

    @property
    def tags(self) -> list:
        if not self._tags:
            self._create_tags()
        return self._tags

    @property
    def stix_bundle(self) -> Bundle:
        if not self._stix_bundle:
            self._stix_bundle = Bundle(*self.stix_objects, allow_custom=True)
        return self._stix_bundle

    @property
    def author(self) -> Identity:
        if not self._author:
            self._create_author()
        return self._author

    @property
    def incident(self) -> Incident:
        if not self._incident:
            self._create_incident()
        return self._incident

    @property
    def threathq_ref(self) -> ExternalReference:
        if not self._threathq_external_reference:
            self._create_threathq_external_reference()
        return self._threathq_external_reference

    @property
    def stix_objects(self) -> list:
        if not self._stix_objects:
            self._gather_stix()
        return self._stix_objects

    def _create_author(self):
        self._author = Identity(
            type='identity',
            name="Cofense Intelligence",
            identity_class="organization",
            description="CofenseIntel",
            confidence=self._confidence
        )
        self._stix_objects.append(self._author)

    def _create_incident(self):
        self._incident = Incident(
            name=self.label,
            description=self.executive_summary,
            object_marking_refs=[TLP_AMBER],
            labels=self.tags,
            created=datetime.fromtimestamp(self.first_published/1000),
            created_by_ref=self.author,
            confidence=self._confidence,
            external_references=[self.threathq_ref],
        )
        self._stix_objects.append(self._incident)

    def _create_threathq_external_reference(self):
        self._threathq_external_reference = ExternalReference(
            source_name="Cofense Intelligence",
            description="Cofense Intelligence",
            external_id=self.threat_id,
            url=f"https://threathq.com/active-threat-reports/m-{self.threat_id}"
        )

    def _create_tags(self):
        self._tags.extend(f"family:{x}" for x in self.malware_families)
        self._tags.extend(f"delivery:{x}" for x in self.delivery_mechs)
        self._tags.extend(f"brand:{x}" for x in self.brands)

    def _gather_stix(self):
        self._gather_network_stix()
        self._gather_file_stix()

    def _gather_network_stix(self):
        for block in self.block_set:
            self._get_block_stix(block)

    def _gather_file_stix(self):
        for exe in self.executable_set:
            self._get_file_stix(exe)

    def _add_incident_relation(self, observable):
        custom_properties = {
            "x_opencti_score": self._confidence,
            "x_opencti_created_by_ref": self.author.id,
        }

        incident_relation = Relationship(
            relationship_type="related-to",
            created_by_ref=self.author.id,
            source_ref=observable.id,
            target_ref=self.incident.id,
            object_marking_refs=[TLP_AMBER],
            allow_custom=True,
            confidence=self._confidence,
            custom_properties=custom_properties
        )
        self._stix_objects.append(incident_relation)

    def _get_block_stix(self, block):
        labels = []
        if hasattr(block, "malware_family") and block.malware_family:
            labels.append(f"family:{block.malware_family}")
        if hasattr(block, "delivery_mech") and block.delivery_mech:
            labels.append(f"delivery:{block.delivery_mech}")

        custom_properties = {
            "x_opencti_score": self._confidence,
            "x_opencti_created_by_ref": self.author.id,
            "description": f"From Cofense Intelligence Threat Report {self.threat_id}",
            "x_opencti_create_indicator": True,
            "confidence": self._confidence,
            "external_references": [self.threathq_ref]
        }

        observable_obj = self._block_obj[block.block_type](
            value=block.watchlist_ioc,
            custom_properties=custom_properties,
        )

        self._stix_objects.append(observable_obj)
        self._add_incident_relation(observable=observable_obj)

    def _get_file_stix(self, exe):
        labels = []
        if hasattr(exe, "malware_family") and exe.malware_family:
            labels.append(f"family:{exe.malware_family}")
        if hasattr(exe, "delivery_mech") and exe.delivery_mech:
            labels.append(f"delivery:{exe.delivery_mech}")

        custom_properties = {
            "labels": labels,
            "x_opencti_score": self._confidence,
            "x_opencti_created_by_ref": self.author.id,
            "description": f"From Cofense Intelligence Threat Report {self.threat_id}",
            "x_opencti_create_indicator": True,
            "confidence": self._confidence,
            "external_references": [self.threathq_ref]
        }

        file_obj = File(
            name=exe.file_name,
            type='file',
            hashes={
                "MD5": str(exe.md5),
                **({"SHA-1": str(exe.sha1)} if exe.sha1 else {}),
                **({"SHA-256": str(exe.sha256)} if exe.sha256 else {}),
                **({"SHA-512": str(exe.sha512)} if exe.sha512 else {})
            },
            custom_properties=custom_properties
        )

        self._add_incident_relation(file_obj)
        self._stix_objects.append(file_obj)
