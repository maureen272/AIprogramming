word = input("Enter word to translate: ")

vowels = "aeiou"

if word[0] in vowels:
	pigLatinWord = word + "way"
	
else:
	tmp = ""
	index = 0
	
	while index < len(word) and word[index] not in vowels:
		tmp += word[index]
		index += 1
		
	pigLatinWord = word[index:] + tmp + "ay"
	
	
print(f"The word in Pig Latin is {pigLatinWord}.")