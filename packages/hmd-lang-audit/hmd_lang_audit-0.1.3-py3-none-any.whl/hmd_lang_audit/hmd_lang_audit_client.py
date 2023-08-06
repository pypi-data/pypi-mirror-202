# The code in this file is generated automatically.
# DO NOT EDIT!
from hmd_graphql_client.hmd_base_client import BaseClient
from typing import List
from hmd_schema_loader.hmd_schema_loader import get_default_loader, get_schema_root


from .audit_record import AuditRecord



from hmd_meta_types.entity import Entity

from .audit_record_audits_entity import AuditRecordAuditsEntity

def get_client_loader():
    return get_default_loader("hmd_lang_audit")

def get_client_schema_root():
    return get_schema_root("hmd_lang_audit")

class HmdLangAuditClient:
    def __init__(self, base_client: BaseClient):
        self._base_client = base_client

    # Generic upsert...
    def upsert(self, entity):
        return self._base_client.upsert_entity(entity)

    # Generic delete...
    def delete(self, entity):
        self._base_client.delete_entity(entity.get_namespace_name(), entity.identifier)

    # Nouns...

    # hmd_lang_audit_audit_record
    def get_audit_record_hmd_lang_audit(self, id_: str) -> AuditRecord:
        return self._base_client.get_entity(AuditRecord.get_namespace_name(), id_)

    def delete_audit_record_hmd_lang_audit(self, id_: str) -> None:
        self._base_client.delete_entity(AuditRecord.get_namespace_name(), id_)

    def upsert_audit_record_hmd_lang_audit(self, entity: AuditRecord) -> AuditRecord:
        if not isinstance(entity, AuditRecord):
            raise Exception("entity must be an instance of AuditRecord")
        return self._base_client.upsert_entity(entity)

    
    def search_audit_record_hmd_lang_audit(self, filter_: dict) -> List[AuditRecord]:
        return self._base_client.search_entity(AuditRecord.get_namespace_name(), filter_)


    # Relationships...

    # hmd_lang_audit_audit_record_audits_entity
    def delete_audit_record_audits_entity_hmd_lang_audit(self, id_: str) -> None:
        self._base_client.delete_entity(AuditRecordAuditsEntity.get_namespace_name(), id_)

    def upsert_audit_record_audits_entity_hmd_lang_audit(self, entity: AuditRecordAuditsEntity) -> AuditRecordAuditsEntity:
        if not isinstance(entity, AuditRecordAuditsEntity):
            raise Exception("entity must be an instance of AuditRecordAuditsEntity")
        return self._base_client.upsert_entity(entity)

    def get_from_audit_record_audits_entity_hmd_lang_audit(self, entity: AuditRecord) -> List[AuditRecordAuditsEntity]:
        if not isinstance(entity, AuditRecord):
            raise Exception("entity must be an instance of AuditRecord")
        return self._base_client.get_relationships_from(entity, AuditRecordAuditsEntity.get_namespace_name())

    def get_to_audit_record_audits_entity_hmd_lang_audit(self, entity: Entity) -> List[AuditRecordAuditsEntity]:
        if not isinstance(entity, Entity):
            raise Exception("entity must be an instance of Entity")
        return self._base_client.get_relationships_to(entity, AuditRecordAuditsEntity.get_namespace_name())


