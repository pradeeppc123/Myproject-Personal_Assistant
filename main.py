import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
import pyttsx3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication



chatStr = ""

def send_email(subject, message, recipient_email, attachment_path=None):
    sender_email = "chigalampallip@gmail.com"
    sender_password = "wmwwqmdckomwmpfa"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
                part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                msg.attach(part)

        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print("An error occurred while sending the email:", str(e))

    finally:
        server.quit()



def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"brother: {query}\n Franky: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    if "Python" in text:
     with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.py", "w") as f:
        f.write(text)
    if "C program" in text:
     with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.c", "w") as f:
        f.write(text)
    if "java" in text:
     with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.java", "w") as f:
        f.write(text)



def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Franky"


if __name__ == '__main__':
    print('Hello i am Franky')
    say(" Hello i am Franky ")
    c=0
    d=0
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])


        if "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} bajke {min} minutes")


        elif "solve this error" in query:
             code=input("please paste the code")
             c=1
             if(c==1):
                 ai(prompt=(f"solve this error{code}"))


        elif "in detail" in query:
             jode=input("please paste the code")
             d=1
             if(d==1):
                 ai(prompt=(f"Explain each line in detail{jode}"))
        
        elif "send an email" in query.lower():
            say("Sure, please provide the subject of the email.")
            print("Listening...")
            subject = takeCommand()

            say("Great! Now, please provide the message of the email.")
            print("Listening...")
            message = takeCommand()

            say("Enter the email address")
            recipient_email = input()

            say("Do you want to attach a file? Say 'yes' or 'no'.")
            print("Listening...")
            attach_file_response = takeCommand()

            if "yes" in attach_file_response.lower():
                say("Please provide the path of the file to attach.")
                attachment_path = input()  # Collect the attachment file path
                send_email(subject, message, recipient_email, attachment_path)
            else:
                 send_email(subject, message, recipient_email)






        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "bye".lower() in query.lower():
            say("Bye Bye ")
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""
            print("clear")

        else:
            print("Chatting...")
            chat(query)
