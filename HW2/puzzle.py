input_str = input("Starting word: ")

starting_word = input_str
crossed= (starting_word[::2])
remaining= (starting_word[1::2])

print("Crossed out letters:", crossed)
print("Remaining letters:", remaining)
