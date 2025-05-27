import sys

def count_alphabets(word):
    alphabets = {}
    for alphabet in word:
        if alphabet not in alphabets:
            alphabets[alphabet] = 0
        alphabets[alphabet] += 1
    return alphabets

def score_word(word):
    scores = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    total = 0
    for char in word:
        total += scores[ord(char) - ord('a')]
    return total

def countsearch_anagram(originalword, word_count, dictionary):
    maxscore = 0
    for entry in dictionary:
        if entry[0] == originalword:
            continue
        for char, count in entry[1].items():
            if char not in word_count or word_count[char] < count:
                break
        else:
            score = score_word(entry[0])
            if score > maxscore:
                maxscore = score
                maxword = entry[0]
    return maxword


def main(data_file, output_file):
    counted_dictionary = []
    with open('lec1/words.txt') as f:
        for line in f:
            line = line.rstrip("\n")
            counted_dictionary.append([line, count_alphabets(line)])

    words = []
    with open(data_file) as f:
        for line in f:
            words.append(line)

    output = []
    for word in words:
        output.append(countsearch_anagram(word, count_alphabets(word), counted_dictionary))

    with open(output_file, 'w') as f:
        for word in output:
            print(word, file=f) 

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s data_file your_answer_file" % sys.argv[0])
        exit(1)
    main(sys.argv[1], sys.argv[2])
