import random
f=open("D:\words.txt",'r')
words=f.readlines()
#words=data.split()
word=random.choice(words)
word=word.upper()
total_chances=7
guessed_word='_'*len(word)
while total_chances!=0:
    print(guessed_word)
    letter=input("Guess a letter: ").upper()
    if letter in word:
        for index in range(len(word)):
            if word[index]==letter:
                guessed_word=guessed_word[:index]+letter+guessed_word[index+1:]
        if guessed_word==word:
            print("congo u won!")
            break
    else:
        total_chances-=1
        print("incorrect guess")
        print("remaining chances ",total_chances)
print("game over")
print("all the chances are over")
print("the correct word is ",word)
