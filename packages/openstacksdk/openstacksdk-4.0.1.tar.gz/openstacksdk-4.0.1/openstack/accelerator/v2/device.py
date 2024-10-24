# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from openstack import resource


class Device(resource.Resource):
    resource_key = 'device'
    resources_key = 'devices'
    base_path = '/devices'
    # capabilities
    allow_create = False
    allow_fetch = True
    allow_commit = False
    allow_delete = False
    allow_list = True
    #: The timestamp when this device was created.
    created_at = resource.Body('created_at')
    #: The hostname of the device.
    hostname = resource.Body('hostname')
    #: The ID of the device.
    id = resource.Body('id')
    #: The model of the device.
    model = resource.Body('model')
    #: The std board information of the device.
    std_board_info = resource.Body('std_board_info')
    #: The type of the device.
    type = resource.Body('type')
    #: The timestamp when this device was updated.
    updated_at = resource.Body('updated_at')
    #: The UUID of the device.
    uuid = resource.Body('uuid', alternate_id=True)
    #: The vendor ID of the device.
    vendor = resource.Body('vendor')
    #: The vendor board information of the device.
    vendor_board_info = resource.Body('vendor_board_info')
