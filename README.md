# HackNY2017

- Install the APK
- Add hack17RSA.py to /AppInventor/assets
- Set up the Amazon Skill

##Inspiration
In today's world, there have been signs of increasing levels of anxiety and no one knows quite why. However, one fact that we know for sure is that people tend to reach out to people less because they fear judgment from the people who they might reach out to. Therefore, we've decided to make a bot that is easily accessible and will not judge you for what you will be telling the bot.

##What it does
The bot aims to listen to first listen to the key word of I am feeling ____. Then it evaluates how you might be feeling by sending a request to the IBM Watson Tone Analyser to evaluate how you might be really feeling by the words that you might be using. Depending on how high your level of sadness, anger, frustration or anxiety might be, it'll send you a comforting text message to your phone via Twilio and a GIF via GIPHY that might give a laugh.

##How we built it
We built this by using AWS with Alexa and coded everything in Python. Due to our lack of resources of being able to setup an environment to download the helper libraries on python, we used requests to the request on the API's that used such as GIPHY API, Twilio API, and IBM Tone Analyser. In addition, we are encrypting the gifs by an RSA algorithm so that you won't be concerned about people knowing what kind of gifs you might be receiving depending how you are feeling.

##Challenges we ran into
We ran into problems as mentioned before where we didn't have enough time to setup the AWS development on our local machines and had to hack everything in one large file. This caused a problem in both workflow and neatness.

##Accomplishments that we're proud of
We are proud of how this actually works and how this can be extended into other potential projects. In addition, by training Alexa with more skills, it can be used to lead into a dynamic conversation if extended further.

##What we learned
We learned that it was at first difficult to set a plan in motion with a limited amount of time.

##Built With
python
alexa
amazon-web-services
twilio
giphy-api
encryption

