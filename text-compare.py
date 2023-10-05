import Levenshtein

# Original text (ground truth)
original_text = "This is the original text."

# Text converted from audio
audio_text = "This is the orignal text."

# Calculate the Levenshtein distance
distance = Levenshtein.distance(original_text, audio_text)

# Set a threshold for similarity (adjust as needed)
threshold = 5

# Provide feedback based on the distance
if distance == 0:
    feedback = "Perfect! Your pronunciation matches the original text exactly."
elif distance <= threshold:
    feedback = "Good job! Your pronunciation is very close to the original text."
else:
    feedback = "You might want to work on your pronunciation. There are significant differences from the original text."

# Print the feedback and Levenshtein distance
print("Feedback:", feedback)
print("Levenshtein Distance:", distance)
