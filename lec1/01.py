def sort_word(word):
    alphabet_list = list(word)
    alphabet_list.sort()
    return "".join(alphabet_list)

def binsearch_anagram(originalword, word, dictionary):
    l = len(dictionary)
    start = 0
    end = l-1
    anagrams = []
    while(start <= end):
        mid = start + (end - start)//2
        if word == dictionary[mid][0]:
            left = mid - 1
            while left >= start and dictionary[left][0] == word:
                if(dictionary[left][1] != originalword):
                    anagrams.append(dictionary[left][1])
                left -= 1
            if(dictionary[mid][1] != originalword):
                anagrams.append(dictionary[mid][1])
            right = mid + 1
            while right <= end and dictionary[right][0] == word:
                if(dictionary[right][1] != originalword):
                    anagrams.append(dictionary[right][1])
                right += 1
            break
        elif(word < dictionary[mid][0]):
            end = mid-1
        elif(word > dictionary[mid][0]):
            start = mid+1
    
    return anagrams

        


if __name__ == "__main__":
    new_dictionary = []
    with open("./words.txt") as f:
        for line in f:
            line = line.rstrip("\n")
            sorted_word = sort_word(line)
            new_dictionary.append([sorted_word, line])
    
    new_dictionary.sort()

    input_words = list(input().split())
    words = []
    for word in input_words:
        anagrams = binsearch_anagram(word, sort_word(word), new_dictionary)
        print("word =",word,"anagrams =",anagrams)
    