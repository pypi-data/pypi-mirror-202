import base64
import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union
from urllib.parse import urljoin

from pyntone.types import AppID, CommentID, RecordID, Revision
from pyntone.types.auth import ApiTokenAuth, DiscriminatedAuth, PasswordAuth
from pyntone.types.record import (Comment, RecordForParameter, UpdateKey,
                                  UpdateKeyRecordForParameter,
                                  UpdateRecordForParameter,
                                  UpdateRecordStatusParameter)


class HttpMethod(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'

@dataclass
class KintoneRequestParams:
    app: Optional[AppID] = None
    id: Optional[RecordID] = None
    update_key: Optional[UpdateKey] = None
    record: Union[RecordForParameter, UpdateKeyRecordForParameter, None, RecordID] = None
    records: Union[list[RecordForParameter], list[UpdateKeyRecordForParameter], list[UpdateRecordForParameter], list[Union[RecordForParameter, UpdateKeyRecordForParameter]], list[Union[UpdateRecordForParameter, UpdateKeyRecordForParameter]], list[UpdateRecordStatusParameter], None] = None
    revision: Optional[Revision] = None
    revisions: Optional[list[Revision]] = None
    fields: Optional[list[str]] = None
    query: Optional[str] = None
    total_count: Optional[bool] = None
    ids: Optional[list[RecordID]] = None
    size: Union[None, int, str] = None
    requests: Optional[list] = None
    comment: Union[Comment, CommentID, None] = None
    order: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    assignees: Optional[list[str]] = None
    action: Optional[str] = None

class KintoneRequestConfigBuilder():
    def __init__(self, auth: DiscriminatedAuth, base_url: str) -> None:
        self.auth = auth
        self.base_url = base_url
    
    def build(self, method: HttpMethod, path: str, params: KintoneRequestParams) -> dict:
        config = {
            'method': method.value,
            'url': urljoin(self.base_url, path),
            'headers': self._build_headers(method, self.auth),
        }
        if method == HttpMethod.GET:
            url_params: Any = {
                'app': params.app
            }
            if params.id is not None: url_params['id'] = params.id
            if params.query is not None: url_params['query'] = params.query
            if params.fields is not None:
                for index, v in enumerate(params.fields):
                    url_params[f'fields[{index}]'] = v
            if params.total_count is not None: url_params['totalCount'] = str(params.total_count).lower()
            if params.record is not None: url_params['record'] = params.record
            if params.order is not None: url_params['order'] = params.order
            if params.offset is not None: url_params['offset'] = params.offset
            if params.limit is not None: url_params['limit'] = params.limit
            config['params'] = url_params

        elif method == HttpMethod.POST:
            payload: Any = {
                'app': params.app
            }
            if params.record is not None: payload['record'] = params.record
            if params.records is not None: payload['records'] = params.records
            if params.fields is not None: payload['fields'] = params.fields
            if params.query is not None: payload['query'] = params.query
            if params.size is not None: payload['size'] = params.size
            if params.requests is not None: payload['requests'] = params.requests
            if params.comment is not None: payload['comment'] = params.comment
            config['data'] = json.dumps(payload)
        
        elif method == HttpMethod.PUT:
            payload: Any = {
                'app': params.app
            }
            if params.id is not None: payload['id'] = params.id
            if params.update_key is not None: payload['updateKey'] = params.update_key
            if params.record is not None: payload['record'] = params.record
            if params.records is not None: payload['records'] = params.records
            if params.revision is not None: payload['revision'] = params.revision
            if params.assignees is not None: payload['assignees'] = params.assignees
            if params.action is not None: payload['action'] = params.action
            config['data'] = json.dumps(payload)

        elif method == HttpMethod.DELETE:
            payload: Any = {
                'app': params.app
            }
            if params.id is not None: payload['id'] = params.id
            if params.ids is not None: payload['ids'] = params.ids
            if params.revisions is not None: payload['revisions'] = params.revisions
            if params.comment is not None: payload['comment'] = params.comment
            if params.record is not None: payload['record'] = params.record
            config['data'] = json.dumps(payload)
        else:
            raise RuntimeError()
        
        return config
    
    def _build_headers(self, method: HttpMethod, auth: DiscriminatedAuth) -> dict[str, str]:
        if type(auth) is ApiTokenAuth:
            api_token = auth.api_token
            if type(api_token) is not str:
                api_token = ','.join(api_token)

            headers = {
                'X-Cybozu-API-Token': api_token
            }
            if method != HttpMethod.GET:
                headers['Content-Type'] = 'application/json'

            return headers
        elif type(auth) is PasswordAuth:
            password = auth.password
            user_name = auth.user_name
            b64_pass = base64.b64encode(f'{user_name}:{password}'.encode()).decode()
            headers = {
                'X-Cybozu-Authorization':b64_pass,
            }
            if method != HttpMethod.GET:
                headers['Content-Type'] = 'application/json'

            return headers
        else:
            raise NotImplementedError('Unimplemented authentication method. Please use ApiTokenAuth or PasswordAuth.')
