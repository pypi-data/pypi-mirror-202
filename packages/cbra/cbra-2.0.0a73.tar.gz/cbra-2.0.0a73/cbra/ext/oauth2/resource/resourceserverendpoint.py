# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import cbra.core as cbra
from cbra.core.conf import settings
from cbra.core.iam import NullAuthorizationContext
from cbra.types import IAuthorizationContext
from ..params import RequestAccessToken
from ..resourceserversubjectresolver import ResourceServerSubjectResolver
from .resourceserverauthorizationcontext import ResourceServerAuthorizationContext


class ResourceServerEndpoint(cbra.Endpoint):
    __module__: str = 'cbra.ext.oauth2.endpoints'
    principal: RequestAccessToken # type: ignore
    required_scope: set[str] = set()
    subjects: ResourceServerSubjectResolver

    def get_trusted_issuers(self) -> set[str]:
        return settings.OAUTH2_TRUSTED_ISSUERS

    async def authenticate(self) -> None:
        self.ctx = await self.setup_context()
    
    async def setup_context(self) -> IAuthorizationContext:
        if self.principal.is_anonymous():
            assert self.request.client is not None
            return NullAuthorizationContext(
                remote_host=self.request.client.host
            )
        await self.verify_token()
        return ResourceServerAuthorizationContext(
            self.request,
            await self.subjects.resolve(self.principal)
        )
    
    async def verify_token(self):
        await self.principal.verify(
            request=self.request,
            scope=self.required_scope,
            trusted_issuers=self.get_trusted_issuers()
        )