import speech_recognition as sr
import Levenshtein
from flask import jsonify

# from pydub import AudioSegment

def text_compare(original_text, audio_text):
    # Calculate the Levenshtein distance
    # distance = Levenshtein.distance(original_text, audio_text)

    # # Set a threshold for similarity (adjust as needed)
    # threshold = 5

    # # Provide feedback based on the distance
    # if distance == 0:
    #     feedback = "Perfect! Your pronunciation matches the original text exactly."
    # elif distance <= threshold:
    #     feedback = "Good job! Your pronunciation is very close to the original text."
    # else:
    #     feedback = "You might want to work on your pronunciation. There are significant differences from the original text."

    # # Print the feedback and Levenshtein distance
    # print("Feedback:", feedback)
    # print("Levenshtein Distance:", distance)

    # Calculate the Levenshtein distance
    distance = Levenshtein.distance(original_text.lower(), audio_text.lower())  # Convert to lowercase for case-insensitive comparison

    # Set a threshold for similarity (adjust as needed)
    threshold = 5

    # Provide feedback based on the distance
    if distance == 0:
        feedback = "Excellent! Your pronunciation matches the original text exactly."
    elif distance <= threshold:
        feedback = "Good job! Your pronunciation is very close to the original text."
    else:
        feedback = "Your pronunciation needs improvement. Here are some suggestions:\n"

        # Split the original and audio text into words
        original_words = original_text.split()
        audio_words = audio_text.split()

        # Compare each word in the text
        for i in range(min(len(original_words), len(audio_words))):
            original_word = original_words[i]
            audio_word = audio_words[i]

            word_distance = Levenshtein.distance(original_word.lower(), audio_word.lower())

            if word_distance > 0:
                feedback += f"- Replace '{audio_word}' with '{original_word}' in this context.\n"

        # Provide overall feedback based on Levenshtein distance
        if distance <= threshold + 2:
            feedback += "Overall, your pronunciation is close to the original text."
        else:
            feedback += "Overall, your pronunciation differs significantly from the original text."

    # Print the feedback, Levenshtein distance, and suggestions
    # print("Feedback:")
    # print(feedback)
    # print("Levenshtein Distance:", distance)
    return {"feedback": feedback, "distance": distance}


def audio_check_old(audio_file, original_text):
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
    # Load the audio file
    with sr.AudioFile(audio_file) as source:
        # Adjust for ambient noise (optional)
        print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
        recognizer.adjust_for_ambient_noise(source)
        
        # print("Listening to the audio...")
        # original_text = "The speaker is speaking too quickly or too slowly. Google Speech Recognition is trained on a variety of speech speeds, but it may not be able to accurately transcribe audio that is outside of its expected range."
        
        try:
            # Record audio data from the file
            audio_data = recognizer.record(source)
            print("Audio recorded successfully.")
            
            # Recognize the audio and convert to text
            audio_text = recognizer.recognize_google(audio_data, language="en-US")
            print("Recognized text:")
            # print(audio_text)
            result = text_compare(original_text, audio_text)
            print("Comparison Done")
            return result

        
        except sr.RequestError as e:
            return {"error": f"Could not request results from Google Speech Recognition service; {e}"}
        except sr.UnknownValueError:
            return { "error" : "Google Speech Recognition could not understand the audio."}
    
    # # recognizer.adjust_for_ambient_noise(source)
    # print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
    
    # # print("Listening to the audio...")
    # # original_text = "The speaker is speaking too quickly or too slowly. Google Speech Recognition is trained on a variety of speech speeds, but it may not be able to accurately transcribe audio that is outside of its expected range."
    
    # try:
    #     # Record audio data from the file
    #     audio_data = recognizer.record(source)
    #     print("Audio recorded successfully.")
        
    #     # Recognize the audio and convert to text
    #     audio_text = recognizer.recognize_google(audio_data, language="en-US")
    #     print("Recognized text:")
    #     # print(audio_text)
    #     result = text_compare(original_text, audio_text)
    #     print("Comparison Done")
    #     return result

    
    # except sr.RequestError as e:
    #     return {"error": f"Could not request results from Google Speech Recognition service; {e}"}
    # except sr.UnknownValueError:
    #     return { "error" : "Google Speech Recognition could not understand the audio."}



def audio_check(audio, original_text):
    recognizer = sr.Recognizer()
    audio_data = sr.AudioData(audio.raw_data, audio.frame_rate, audio.frame_width)

    try:
        audio_text = recognizer.recognize_google(audio_data=audio_data)
        result = text_compare(original_text, audio_text)
        print("Comparison Done")
        return jsonify(result), 200
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Could not request results; {e}"}), 500