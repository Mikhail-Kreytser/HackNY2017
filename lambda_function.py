from __future__ import print_function
import json
#import requests
import urllib.request
import base64
from urllib import request, parse
import random


# --------------- Helpers that build all of the responses ----------------------
def get_gif_url(tone_id):
    opposite_tones = {
		"anger" : "calming", 
		"fear" : "animals+relaxing", 
		"indifferent" : "random", 
		"sadness": "cheer+up",
        "joy" : "funny+cats",
        "call" : "call+me"
        }

    gif_descriptor = opposite_tones[tone_id]
    urlp1 ="http://api.giphy.com/v1/gifs/search?q="
    urlp2 = "&api_key=KEY"
    url = urlp1+gif_descriptor+urlp2

    respons = urllib.request.urlopen(url)
    data = json.loads(respons.read().decode(respons.info().get_param('charset') or 'utf-8'))
    dumpedjson = json.dumps(data)
    parsed_json = json.loads(dumpedjson)
  
    list_gif_urls = []
    for val in range (0,9):
	    list_gif_urls.append((parsed_json['data'][val]['bitly_gif_url']))

    return random.choice(list_gif_urls)


def tone_analyzer(speech):

    text = '%20'.join(speech.split())

    url = "https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21&text=" + text
    usr = "19fbf368-c8be-473b-bf5e-0cc12913b1da"
    pwd = "8mEfE4eoDFkX"
    req = request.Request(url)

    authentication = "{}:{}".format(usr, pwd)
    base64string = base64.b64encode(authentication.encode('utf-8'))
    req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
    return json.loads(request.urlopen(req).read())


def wantTherapy(tones):

    base_tones = set(['anger', 'fear', 'sadness'])

    scores = tones['document_tone']['tones']
    
    largest = 0 
    emotion = None 

    for s in scores:
        if s['score'] > largest and s['tone_id'] in base_tones:
            largest = s['score']
            emotion = s['tone_id']

    if float(largest) > .80:
        return True
    return False


def biggestEmotion(tones):
    base_tones = ['sadness','anger', 'fear', 'joy']

    scores = tones['document_tone']['tones']
    
    largest = 0 
    emotion = None 

    for s in scores:
        if s['score'] > largest and s['tone_id'] in base_tones:
            largest = s['score']
            emotion = s['tone_id']
    if emotion == None:
      	return 'indifferent'
    return emotion
  
  
def sms(msg):

    url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"

    account_sid = 'account_sid'
    auth_token = 'auth_token'

    url = url.format(account_sid)

    params = {"To" : "+USER_NUMBER", "From" : "+TWILLO_NUMBER", "Body" : msg}
    data = parse.urlencode(params).encode()
    req = request.Request(url)

    authentication = "{}:{}".format(account_sid, auth_token)
    base64string = base64.b64encode(authentication.encode('utf-8'))
    req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
    request.urlopen(req, data)
    
    
def mms(link):
    url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
    account_sid = 'account_sid'
    auth_token = 'auth_token'

    url = url.format(account_sid)
    params = {"To" : "+USER_NUMBER", "From" : "+TWILLO_NUMBER", "Body" : link}
    data = parse.urlencode(params).encode()
    req = request.Request(url)

    authentication = "{}:{}".format(account_sid, auth_token)
    base64string = base64.b64encode(authentication.encode('utf-8'))
    req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
    request.urlopen(req, data)
    
    
def pow_mod(m, k, c):
    result = 1
    for i in range(0, k, +1):
        result = (result * m) % c
    return result


def pre_crypt(m, e, c):
    return pow_mod(m, e, c)


def encrypt(m):
    e = 3271
    c = 4819
    s = 0
    multy = 1
    for element in range(0, len(m), +1):
        temp = pre_crypt(ord(m[element]), e, c)
        s += temp * multy
        multy *= 100000
    return s    
    

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Anxiety Bot. " \
                    "Please tell me how you are feeling today."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me how you're feeling by saying, " \
                    "I am feeling anxious."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Anxiety Bot. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_curr_feeling_attributes(curr_feeling):
    return {"currFeeling": curr_feeling}

  
def create_reason_attributes(curr_reason):
  	return {"currReason": curr_reason}


def create_recovery_steps_attributes(stepsToRecover):
  	return {"stepsToRecover": stepsToRecover}


def set_feeling_in_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    #reply = getRES()    -causing code to crash     

    if 'feeling' in intent['slots']:
        curr_feeling = intent['slots']['feeling']['value']
        session_attributes = create_curr_feeling_attributes(curr_feeling)
        toneJSON = tone_analyzer("I am feeling " + curr_feeling)
        startTherapyBool = wantTherapy(toneJSON)
        
        if startTherapyBool:
            sms('201-310-5291 - Therapist')
            mms(get_gif_url('call'))
            speech_output = "I see you are feeling quite anxious." \
                            " It’s a normal part of life to experience occasional anxiety. " \
                            "Relax. This, of course, is easier said than done, " \
                            "but try to assess the situation and remove yourself from the cause." 
            reprompt_text = "Step away. This might just be a walk around the block, some exercise, or meditation." \
                            "Breathe deeply. Check your phone"
            should_end_session = Truea
        else:
            #sms("This is Anxiety Bot sending you a GIF")
            mms(encrypt(get_gif_url(biggestEmotion(toneJSON))))
            speech_output = "Nice to hear that. Let me show you something cool"
            reprompt_text = "Checkout your phone"
            should_end_session = True
            
        
    else:
        speech_output = "I'm not sure what your feeling is. Please try again."
        reprompt_text = "I'm not sure what your feeling is. You can tell me how you're feeling by saying, I am feeling anxious."
            
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_feeling_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "currFeeling" in session.get('attributes', {}):
        curr_feeling = session['attributes']['currFeeling']
        speech_output = "Your feeling is " + curr_feeling + \
                        "good bye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what you are feeling. " \
                        "You can say, I am feeling anxious."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()
    

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyFeelingIsIntent":
    	return set_feeling_in_session(intent, session)
    #elif intent_name = "TherapyYesNo":
    #  	return initTherapy(intent, session)
    #elif intent_name == "AnxiousBecause":
    #    return contTherapy(intent, session)
    #elif intent_name == "StepsForRecovery":
    #  	return finishTherapy(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
        

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """ 
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
