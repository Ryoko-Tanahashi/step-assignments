def count_alphabets(word):
    alphabets = {}
    for alphabet in word:
        if alphabet not in alphabets:
            alphabets[alphabet] = 0
        alphabets[alphabet] += 1
    return alphabets

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

def countsearch_anagram(originalword, word_count, dictionary):
    anagrams = []
    for entry in dictionary:
        if entry[0] == originalword:
            continue
        for char, count in entry[1].items():
            if char not in word_count or word_count[char] < count:
                break
        else:
            anagrams.append(entry[0])
    return anagrams


if __name__ == "__main__":
    counted_dictionary = []
    with open("./words.txt") as f:
        for line in f:
            line = line.rstrip("\n")
            counted_dictionary.append([line, count_alphabets(line)])

    input_words = list(input().split())
    words = []
    for word in input_words:
        anagrams = countsearch_anagram(word, count_alphabets(word), counted_dictionary)
        print("word =",word,"anagrams =",anagrams)
    