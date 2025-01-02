import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
from bs4 import BeautifulSoup

engine = pyttsx3.init()


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("You:", "Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            print("You:", "Recognizing...")
            query = recognizer.recognize_google(audio)
            print("You:", f"You said: {query}\n")
            return query
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand what you said.")
            return ""
        except sr.RequestError:
            speak("Sorry, I couldn't reach the speech recognition service.")
            return ""


def perform_task(query, context):
    query = query.lower()
    if "hello" in query:
        speak("Hello! How can I help you?")
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}")
    elif "date" in query:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "search" in query:
        search_query = query.replace("search", "").strip()
        search_web(search_query)
    elif "weather" in query:
        get_weather()
    elif "feedback" in query:
        provide_feedback(context)
    else:
        speak("I'm sorry, I didn't understand that command.")


def search_web(query):
    try:
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('div', class_='BNeawe UPmit AP7Wnd')
        if search_results:
            first_result = search_results[0].get_text()
            speak(f"Here are the search results for {query}: {first_result}")
        else:
            speak("Sorry, I couldn't find any relevant information for your query.")
    except requests.RequestException:
        speak("Sorry, I couldn't perform the search due to a network error.")


def get_weather():
    try:
        weather_url = "https://www.google.com/search?q=weather"
        response = requests.get(weather_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_info = soup.find('div', class_='BNeawe iBp4i AP7Wnd').get_text()
        speak("Here is the current weather:")
        speak(weather_info)
    except requests.RequestException:
        speak("Sorry, I couldn't fetch the weather information due to a network error.")


def provide_feedback(context):
    speak("How was your experience with the voice assistant? Any suggestions or issues you'd like to share?")
    feedback = recognize_speech()
    if feedback:
        print("You:", "User feedback:", feedback)
        context["feedback"] = feedback
        speak("Thank you for your feedback!")
    else:
        speak("Sorry, I couldn't understand your feedback. Please try again.")
        provide_feedback(context)


def main():
    context = {} 
    speak("Initializing voice assistant...")
    while True:
        query = recognize_speech()
        if query:
            if "exit" in query:
                speak("Goodbye!")
                break
            perform_task(query, context)

if __name__ == "__main__":
    main()
