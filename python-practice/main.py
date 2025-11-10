from collections import Counter

def foo(input):
    sentence1 = input[0].strip().split(' ')
    sentence2 = input[1].strip().split(' ')

    counts = Counter(sentence1) + Counter(sentence2)
    return [w for w, c in counts.items() if c == 1]    

def main():
    foo(["", "The quick brown fox jumps over the lazy dog"])


# [3, 3, 4]
#  3, 2, 2, 3]
# [2, 2, 2, 2, 2]


if __name__ == "__main__":
    main()


