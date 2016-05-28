from flask import Flask, render_template, request
import googleapiclient.discovery
import oauth2client.client.GoogleCredentials

DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/result', methods='POST')
def end():
    gcs_uri = request.form['gcs_uri']
    g_url = ['gs://'+gcs_uri + '/' + str(i) + '.jpg' for i in range(1,
                                                                    100)]
    for gcs_url in g_url:
        annotations = identify_logo(gcs_url)
        if not annotations:
            break
        else:
            result = [a['description'] for a in annotations]
    return render_template('result.html', result=result)


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
    service = get_vision_service()
    req = service.images().annotate(body={
        'requests': batch_request,
        })
    response = req.execute()
    return response['responses'][0].get('logoAnnotations', None)


if __name__ == '__main__':
    app.run()


def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials,
                           discoveryServiceUrl=DISCOVERY_URL)


if __name__ == '__main__':
    app.run()
