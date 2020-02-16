import json
import sys
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import threading
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('L-NkgQuIroaAsmtDjGlyscro0tK238U86IwDhDWJM-H9')
service = SpeechToTextV1(authenticator=authenticator)
service.set_service_url('https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/0da1acaa-b12b-4b4c-9265-8cfefcff45c2')

models = service.list_models().get_result()
model = service.get_model('en-US_BroadbandModel').get_result()

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(join(dirname(__file__), filename),
            'rb') as audio_file:
        results = json.dumps(service.recognize(
                audio=audio_file,
                content_type='audio/wav',
                timestamps=True,
                word_confidence=True).get_result())
        print(results)




