

from hmd_meta_types import Relationship, Noun, Entity
from hmd_lang_audit.audit_record import AuditRecord
from hmd_meta_types.entity import Entity
from datetime import datetime
from typing import List, Dict, Any

class AuditRecordAuditsEntity(Relationship):

    _entity_def = \
        {'name': 'audit_record_audits_entity', 'namespace': 'hmd_lang_audit', 'metatype': 'relationship', 'ref_from': 'hmd_lang_audit.audit_record', 'ref_to': 'hmd_meta_types.entity', 'attributes': {}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return AuditRecordAuditsEntity._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(AuditRecordAuditsEntity._entity_def)


    @staticmethod
    def ref_from_type():
        return AuditRecord

    @staticmethod
    def ref_to_type():
        return Entity

    

    