import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

dataset = (
    "Hey, You got a lottery worth of $1000000!",
    "Can we have a lunch today?",
    "Congratulations, you won a prize in RummyCircle!",
    "An amount of $10000 has been credited to your Poker Account",
    "Your meeting will start at 5:00PM Today",
    "it's an important call for you"
)

label = (1, 0, 1, 1, 0, 0)

max_words, word_len = 1000, 50

tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
tokenizer.fit_on_texts(dataset)
sequences = tokenizer.texts_to_sequences(dataset)
padded_sequences = pad_sequences(sequences, maxlen=word_len, padding='post', truncating='post')

# print(sequences)



# Constructing a Neural Network

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=max_words, output_dim=16, input_length=word_len),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(16, activation='relu'), # adding hidden layer with 16 nodes (depend on output dimension)
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

training_sequence = np.array(padded_sequences)
training_label = np.array(label)

model.fit(training_sequence, training_label, epochs=10)

def check_is_spam(email, threshold=0.5):
    sequence = tokenizer.texts_to_sequences([email])
    padded_sequence = pad_sequences(sequence, maxlen=word_len, padding='post', truncating='post')
    prediction = model.predict(padded_sequence)[0][0]
    if prediction > threshold:
        print(f"Probably Spam mail, Score: {prediction:.2f}")
    else:
        print(f"Probably Not a Spam mail, Score: {prediction:.2f}")

check_is_spam("hey, congratulations you won a lottery of $200")
check_is_spam("You have meeting today at 3:00 PM")
