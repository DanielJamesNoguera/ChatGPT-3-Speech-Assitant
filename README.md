# ChatGPT-3-Speech-Assitant
This is a quick Speech -> ChatGPT-3 -> Speech wrapper I made for OpenAI's ChatGPT-3.

This will also render an image through Replicate if you say the word 'picture'.

All the code you need is in main.py, make sure you install the necessary modules via pip;
speech_recognition
openai
replicate
pyttsx3

To begin head over to https://beta.openai.com/login/ and make an account. Then generate an API key. Once you have this add it on line 7. (If you want to do this probably create an environment variable, I'm just lazy)

If you want to use the image generation via Replicate then head over to https://replicate.com/account make an account and create an API key. If you want to skip this step then use main_no_image.py instead of main.py

Then simply execute the file by opening your terminal and running the python file:
py main.py (or main_no_image.py)

It will print the speech it detects from your mic, send that to the openAI API and then play the response through your default speakers.

Enjoy.
