# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack import resource
from openstack import utils


class ProfileType(resource.Resource):
    resource_key = 'profile_type'
    resources_key = 'profile_types'
    base_path = '/profile-types'

    # Capabilities
    allow_list = True
    allow_fetch = True

    # Properties
    #: Name of the profile type.
    name = resource.Body('name', alternate_id=True)
    #: The schema of the profile type.
    schema = resource.Body('schema')
    #: The support status of the profile type
    support_status = resource.Body('support_status')

    def type_ops(self, session):
        url = utils.urljoin(self.base_path, self.id, 'ops')
        resp = session.get(url)
        return resp.json()
