import numpy as np
from typing import *
import string
from dataclasses import dataclass
import unittest

# Make a fresh hash table with the given size, containing no elements
class HashTable:
    def __init__(self, size = 128):
        self.size = size
        self.table = [None] * size
        self.numEl = 0

# Reads given stop words file and converts into a format readable by other functions
def readStopWords(fileName: str) -> List[str]:
    file = open(fileName, "r")
    raw = file.readlines()
    res = []
    for i in raw:
        temp = i.replace('\n', "")
        res.append(temp)
    file.close()
    return res

# Reads given text file and converts it into a format readable by other functions
def readText(fileName: str) -> List[str]:
    file = open(fileName, "r")
    res = file.readlines()
    file.close()
    return res

# Given a word and length of hash table, returns a key
def h(word: str, length: int) -> int:
    key = 0
    effLen = min(len(word) - 1, 7)
    for i in range(0,  effLen):
        key += ord(word[i].lower())*31**(effLen-1-i)
    return int(key % length)

# Make a hash table with given size
def make_hash(size: int = 128) -> HashTable:
    ht = HashTable(size)
    return ht

# Return the size of the given hash table
def hash_size(ht: HashTable) -> int:
    return ht.size

# Return the number of elements in the given hash table
def hash_count(ht:HashTable) -> int:
    return ht.numEl

# Does the hash table contain a mapping for the given word?
def has_key(ht: HashTable, word: str) -> bool:
    index = h(word, ht.size)
    i = 1
    ans = ht.table[index]
    while ans is not None and ans[0] != word:
        if index + i*(i+1)/2 > ht.size:
            index = index + i * (i + 1) / 2 - ht.size
            ans = ht.table[int(index)]
        else:
            ans = ht.table[int(index + i*(i+1)/2)]
        i += 1
    return ans is not None
# What line numbers is the given key mapped to in the given hash table?
# this list should not contain duplicates, but need not be sorted.
def lookup(ht, word: str) -> List[int]:
    index = h(word, ht.size)
    res = ht.table[index]
    i = 1
    while res is not None and res[0] != word:
        if index + (i * (i + 1) / 2) > ht.size:
            index += (i * (i + 1) / 2) - ht.size
            res = ht.table[int(index)]
        else:
            index += i * (i + 1) / 2
            res = ht.table[int(index)]
        i += 1
    if res is not None:
        return res[1:]
    else:
        return "Word not in table"


# Add a mapping from the given word to the given line number in
# the given hash table
def add(ht: HashTable, word: str, line: int) -> None:
    index = h(word, ht.size)
    if ht.table[index] is None:
        ht.table[index] = [word, line]
        ht.numEl += 1
    elif word in ht.table[index]:
        if line not in ht.table[index]:
            ht.table[index].append(line)
    else:
        i = 1
        while ht.table[index] is not None and word not in ht.table[index]:
            index += int((i * (i + 1))/2)
            index %= ht.size
            i += 1
        if ht.table[index] is None:
            ht.table[index] = [word, line]
            ht.numEl += 1
        elif word in ht.table[index]:
            if line not in ht.table[index]:
                ht.table[index].append(line)
            ht.numEl += 1
            if word == "and":
                print("Else", line, index, ht.table[index])
    if ht.numEl != 0 and ht.numEl / ht.size > 0.5:
        tempTable = make_hash(ht.size * 2)
        for i in ht.table:
            if i is not None:
                reHash(tempTable, i)
        ht.table = tempTable.table
        ht.size *= 2

# In the event of a table expansion takes a keys value and adds it to an expanded array
def reHash(ht: HashTable, arr: List) -> None:
    index = h(arr[0], ht.size)
    if ht.table[index] is None:
        ht.table[index] = arr
        ht.numEl += 1
    else:
        i = 1
        while ht.table[index] is not None and arr[0] not in ht.table[index]:
            index += int((i * (i + 1)) / 2)
            i += 1
        ht.table[index] = arr
        ht.numEl += 1

# What are the words that have mappings in this hash table?
# this list should not contain duplicates, but need not be sorted.
def hash_keys(ht: HashTable) -> List[str]:
    res = []
    for i in ht.table:
        if i is not None and i[0] not in res:
            res.append(i[0])
    return res

# Given a list of stop words and a list of strings representing a text,
# return a hash table
def make_concordance(stop_words: List[str], text: List[str]) -> HashTable:
    ht = make_hash(128)
    lineNum = 1
    for i in text:
        noAp = i.replace("'", '')
        rem = noAp.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
        split = rem.split(' ')
        words = []
        for k in split:
            if k.isalpha():
                words.append(k.lower())
        for j in words:
            if j not in stop_words:
                add(ht, j, lineNum)
        lineNum += 1
    return ht

# Formats a given concordance table into the result desired by the assignment
def make_result(cd: HashTable) -> None:
    keys = hash_keys(cd)
    f = open("result.txt", "w+")
    for key in keys:
        f.write(key + ": " + ' '.join(map(str,lookup(cd, key))) + "\n")
    f.close

class test_methods(unittest.TestCase):

    def test_h(self):
        self.assertEqual(h("", 128), 0)

        self.assertEqual(h("test", 128), 34)
        self.assertEqual(h("test", 256), 34)
        self.assertEqual(h("test", 2048), 34)

        self.assertEqual(h("sevenLetterWord", 128), 70)
        self.assertEqual(h("sevenLetterWord", 128), h("sevenLetterWordTwo", 128))

    def test_make_hash(self):
        self.assertEqual(make_hash(128).table, HashTable(128).table)
        self.assertNotEqual(make_hash(256).table, HashTable(1024).table)
        self.assertEqual(make_hash().size, make_hash(128).size)

    def test_hash_size(self):
        self.assertEqual(hash_size(HashTable(256)), 256)
        self.assertEqual(hash_size(HashTable()), 128)

    def test_hash_count(self):
        self.assertEqual(hash_count(HashTable(256)), 0)
        test = HashTable()
        add(test, "testOne", 1)
        add(test, "testTwo", 2)
        add(test, "testThree", 3)
        add(test, "testFour", 4)
        self.assertEqual(hash_count(test), 4)

    def test_has_key(self):
        test = HashTable()
        add(test, "testOne", 1)
        add(test, "testTwo", 2)
        add(test, "testThree", 3)
        add(test, "testFour", 4)
        self.assertTrue(has_key(test, "testOne"))
        self.assertFalse(has_key(test, "testFive"))

    def test_lookup(self):
        test = HashTable()
        add(test, "testOne", 1)
        add(test, "testOne", 2)
        add(test, "testTwo", 2)
        add(test, "testThree", 3)
        add(test, "testFour", 4)
        self.assertEqual(lookup(test, "testOne"), [1, 2])
        self.assertEqual(lookup(test, "testTwo"), [2])

        self.assertNotEqual(lookup(test, "testOne"), [1])
        self.assertNotEqual(lookup(test, "testThree"), [4])

    def test_add(self):
        test = HashTable()
        add(test, "testOne", 1)
        add(test, "testOne", 2)
        add(test, "testTwo", 2)
        add(test, "testTwo", 2)

        test2 = HashTable()
        add(test2, "testOne", 1)
        add(test2, "testOne", 2)
        add(test2, "testTwo", 2)

        self.assertEqual(test.table, test2.table)

        add(test, "testThree", 3)
        add(test, "testFour", 4)

        self.assertNotEqual(test.table, test2.table)

    def test_reHash(self):
        test = HashTable()
        add(test, "testOne", 1)
        add(test, "testTwo", 2)
        add(test, "testThree", 3)
        add(test, "testFour", 4)

        test2 = HashTable()
        for i in test.table:
            if i is not None:
                reHash(test2, i)

        self.assertEqual(test.table, test2.table)

        add(test, "testFive", 5)

        self.assertNotEqual(test.table, test2.table)

    def test_hash_keys(self):
        test = HashTable()
        add(test, "testOne", 1)
        add(test, "testTwo", 2)

        self.assertTrue("testOne", "testTwo" in hash_keys(test))
        self.assertTrue(len(hash_keys(test)) == 2)

        self.assertFalse("testThree" in hash_keys(test))
        self.assertFalse(len(hash_keys(test)) == 1)

    def make_concordance(self):
        test = make_concordance(
            ["the", "a", "but"],
        ["The hIstOry test was$#$ so easy@", "but there-might have been a trick question or 2", "I guess we'll see", "History will show"])

        self.assertEqual(hash_keys(test), ['i', 'been', 'history', 'question', 'trick', 'guess', 'have', 'there', 'test', 'show', 'was', 'see', 'easy', 'will', 'well', 'or', 'so', 'might'])
        self.assertEqual(test.size, 128)
        self.assertEqual(test.numEl, 18)
        self.assertTrue(["Math", 1] not in test.table)
        self.assertTrue(lookup(test, "history"), [1, 4])
        self.assertTrue(lookup(test, "easy"), [1])

        self.assertFalse(lookup(test, "trick"), [1])
        self.assertFalse(lookup(test, "history"), [4])
        self.assertNotEqual(test.size, 256)
        self.assertNotEqual(test.numEl + 1, len(hash_keys(test)))
