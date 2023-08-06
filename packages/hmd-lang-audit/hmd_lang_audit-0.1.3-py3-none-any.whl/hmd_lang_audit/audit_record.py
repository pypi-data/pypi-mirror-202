

from hmd_meta_types import Relationship, Noun, Entity

from datetime import datetime
from typing import List, Dict, Any

class AuditRecord(Noun):

    _entity_def = \
        {'name': 'audit_record', 'namespace': 'hmd_lang_audit', 'metatype': 'noun', 'attributes': {'event_type': {'type': 'string', 'description': 'Type of event being audited, i.e. database access, operation call', 'required': True}, 'event_subtype': {'type': 'string', 'description': 'Sub-type of event being audited, i.e. postgres, global graph'}, 'user_email': {'type': 'string', 'description': 'Email address of user performing the action'}, 'action': {'type': 'string', 'description': 'Action type of event being audited, i.e. insert, delete'}, 'started_at': {'type': 'timestamp', 'description': 'Start time of the event being audited', 'required': True}, 'ended_at': {'type': 'timestamp', 'description': 'End time of the event being audited', 'required': True}, 'outcome': {'type': 'string', 'description': 'Outcome of event, e.g. success, failure, critical error'}, 'outcome_description': {'type': 'string', 'description': 'Longer description of the event outcome'}, 'correlation_id': {'type': 'string', 'description': 'Unique ID to trace calls across services'}}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def entity_definition():
        return AuditRecord._entity_def

    @staticmethod
    def get_namespace_name():
        return Entity.get_namespace_name(AuditRecord._entity_def)


    

    
        
    @property
    def event_type(self) -> str:
        return self._getter("event_type")

    @event_type.setter
    def event_type(self, value: str) -> None:
        self._setter("event_type", value)
    
        
    @property
    def event_subtype(self) -> str:
        return self._getter("event_subtype")

    @event_subtype.setter
    def event_subtype(self, value: str) -> None:
        self._setter("event_subtype", value)
    
        
    @property
    def user_email(self) -> str:
        return self._getter("user_email")

    @user_email.setter
    def user_email(self, value: str) -> None:
        self._setter("user_email", value)
    
        
    @property
    def action(self) -> str:
        return self._getter("action")

    @action.setter
    def action(self, value: str) -> None:
        self._setter("action", value)
    
        
    @property
    def started_at(self) -> datetime:
        return self._getter("started_at")

    @started_at.setter
    def started_at(self, value: datetime) -> None:
        self._setter("started_at", value)
    
        
    @property
    def ended_at(self) -> datetime:
        return self._getter("ended_at")

    @ended_at.setter
    def ended_at(self, value: datetime) -> None:
        self._setter("ended_at", value)
    
        
    @property
    def outcome(self) -> str:
        return self._getter("outcome")

    @outcome.setter
    def outcome(self, value: str) -> None:
        self._setter("outcome", value)
    
        
    @property
    def outcome_description(self) -> str:
        return self._getter("outcome_description")

    @outcome_description.setter
    def outcome_description(self, value: str) -> None:
        self._setter("outcome_description", value)
    
        
    @property
    def correlation_id(self) -> str:
        return self._getter("correlation_id")

    @correlation_id.setter
    def correlation_id(self, value: str) -> None:
        self._setter("correlation_id", value)
    

    
    
        
    def get_from_audit_record_audits_entity_hmd_lang_audit(self):
        return self.from_rels["hmd_lang_audit.audit_record_audits_entity"]
    