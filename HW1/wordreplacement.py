sentence = input("Enter a sentence: ")
wordToReplace = input("Enter word to replace: ")
replacementWord = input("Enter replacement word: ")

word_lst = sentence.split()
#print(word_lst)
for i in range(len(word_lst)):
	if word_lst[i] == wordToReplace:
		word_lst[i] = replacementWord
		
newSentence = " ".join(word_lst)
print(newSentence)