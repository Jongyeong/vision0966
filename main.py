#!/usr/bin/env python

# Copyright 2016 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Identifies the landmark for the given image."""

import argparse
import time
import base64
import json
import sys
sys.path.insert(0, '/libr')
from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials


# [START get_vision_service]
# The url template to retrieve the discovery document for trusted testers.
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build(
        'vision', 'v1', credentials=credentials,
        discoveryServiceUrl=DISCOVERY_URL)

    return service

# [START identify_landmark]
def identify_logo(gcs_uri, max_results=10):
    batch_request = [{
        'image': {
            'source': {
                'gcs_image_uri': gcs_uri
            }
        },
        'features': [{
            'type': 'LOGO_DETECTION',
            'maxResults': max_results,
            }]
        }]
    service = get_vision_service();
    request = service.images().annotate(body={
        'requests': batch_request,
        })
    response = request.execute()
    return response['responses'][0].get('logoAnnotations', None)
# [END identify_landmark]


# [START main]
def main(gcs_uri):
    if gcs_uri[:5] != 'gs://':
        raise Exception('Image uri must be of the form gs://bucket')
    g_url = [gcs_uri+'/'+str(i)+'.jpg' for i in range(1, 8)]
    for gcs_url in g_url:
      	print len(g_url
        annotations = identify_logo(gcs_url)
        if not annotations:
            print('No Logo identified')
        else:
            print('\n'.join(a['description'] for a in annotations))
# [END main]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Identifies the Logo in the given image.')
    parser.add_argument(
        'gcs_uri', help=('The Google Cloud Storage uri to the image to identify'
                         ', of the form: gs://bucket_name'))
    args = parser.parse_args()

    main(args.gcs_uri)