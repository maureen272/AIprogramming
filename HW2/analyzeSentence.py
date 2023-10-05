user_sentence = input("Enter a sentence: ")

start_idx= 0
while start_idx < len(user_sentence) and not user_sentence[start_idx].isalnum():
    start_idx += 1

end_idx = len(user_sentence) - 1
while end_idx >= 0 and not user_sentence[end_idx].isalnum():
    end_idx -= 1

sentence = user_sentence[start_idx:end_idx + 1]

words = sentence.split()


first_word = words[0]
last_word = words[-1]
print("First word: ", first_word)
print("Last word: ", last_word)

