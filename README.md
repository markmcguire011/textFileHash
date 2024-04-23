# Text File Hash Project

## Course Information
- **Course Name:** CSC 202
- **Instructor:** Adnan Awan
- **Term:** 2023-24 Fall Quarter

## Overview

In this project we used Python in order to analyze a text file. Provided a file of stop words, we filtered the original text based on this list and then created a hashmap with the words that remained. For the result text file we accessed this hashmap and expressed in a specified format the line numbers where each word occured in the text.

The project description we were provided is included below. 

I recieved full credit for this assignment.

## Instructions

The goal of this assignment is to process a textual data file to
generate a word concordance with line numbers for each main word.  A
Hash Table ADT is perfect to store the word concordance with the word
being the key and a list of its line numbers being the associated value
for the key. Since the concordance should only keep track of the “main”
words, there will be another file containing words to ignore, namely a
stop-words file (stop_words.txt).  The stop-words file will contain a
list of stop words (e.g., “a”, “the”, etc.) -- these words will not be
included in the concordance even if they do appear in the data file.
You should also not include strings that represent numbers. e.g. “24” or
“2.4” should not appear.

### Sample Text File

```
This is a sample data ((text)) file, to be 
processed by your word-concordance program!!!

A REAL data file is MUCH bigger. Gr8!
```

### Sample Stop-Words File

```
a
about
be
by
can
do
i
in
is
it
of
on
the
this
to
was
```

### Sample Result File

```
bigger: 4
concordance: 2
data: 1 4
file: 1 4
much: 4
processed: 2
program: 2
real: 4
sample: 1
text: 1
word: 2
your: 2
```

Notes: 

1. Words are defined as sequences of characters delimited by any non-letter (whitespace, punctuation).
1. There is no distinction made between upper and lower case letters (CaT is the same word as cat)
1. Blank lines are counted in line numbering.


The general algorithm for the word-concordance program is:

1. Read the stop-words file into your implementation of a hash table
   containing the stop words. For the initial table size, start with
   default of 128 and let the table grow as described below, if
   necessary. Note: You should use the same hash table implementation
   for the stop-words and the concordance. In the case of the
   stop-words, you just won’t use the line number information (can
   either store the actual line number from the file, or just use a
   default value).
1. The word-concordance will be in a separate hash table from the stop
   words hash table. Process the input file one line at a time to build
   the word-concordance.  This hash table should only contain the
   non-stop words as the keys (use the stop words hash table to "filter
   out" the stop words).  Associated with each key is its value where
   the value consists of a list containing the line numbers where the
   key appears.  DO NOT INCLUDE DUPLICATE LINE NUMBERS.
1. Generate a text file containing the concordance words printed out in
   alphabetical order along with their line numbers.  One word per line
   (followed by a colon), and spaces separating items on each line:
   
   data: 1 4
   
   Note there is no space after the last line number - make sure to match the sample output files.

It is strongly suggested that the logic for reading words and assigning
line numbers to them be developed and tested separately from other
aspects of the program.  This could be accomplished by reading a sample
file and printing out the words recognized with their corresponding line
numbers without any other word processing.

### Collision resolution:

Your implementation should use Open Addressing using quadratic probing for collision resolution.

Note that you do not have to support deletion of items from your hash table.

The hash function should take a string containing one or more characters
and return an integer.  Here is the hash function you should use:

h(str) = ∑_(i=0)^(n-1)〖ord(str[i])* 〖31〗^(n-1-i) 〗  where n = the minimum of len(str) and 8  

In order to keep the number of multiplications down, you should use Horner's rule to
compute the output of this hash function for each key.

Also, your hash table size should have the capability to grow if the
input file is large.  After insertion of an item, if the load factor
exceeds 0.5, you should grow the hash table size.

Start with a default hash table size of 128. When increases are necessary, double
the size of the table.

Use the probing sequence

(i * (i + 1))/2


### Removing Punctuation

It is recommended that you process the input file one line at a time.

For each line in the input file, do the following:

* Remove all occurrences of the apostrophe character (‘) (so the word "don't" would simply become "dont")
* Convert all characters in string.punctuation to spaces.
* Split the string into tokens using the .split() method.
* Each token that returns True when the isalpha() method is called should be considered a “word”.  All other tokens should be ignored.

### Using Python data structures

Please do not use a Python `dict` for this assignment, that ... is a hash table,
so that's pretty much the whole assignment done right there.

On the other hand, it's okay for you to use Python lists for this assignment,
specifically in order to track the list of lines where a word occurs.

### Testable Functions

In order to make your code testable, we're requiring a set of functions. This
should not dictate your internal implementations; each of these should be
a very easy "add-on" to any implementation of the project.


```
# Make a fresh hash table with the given size, containing no elements
def make_hash(size: int) -> HashTable:
  pass

# Return the size of the given hash table
def hash_size(ht: HashTable) -> int:
  pass

# Return the number of elements in the given hash table
def hash_count(ht: HashTable) -> int:
  pass

# Does the hash table contain a mapping for the given word?
def has_key(ht: HashTable, word: str) -> bool:
  pass

# What line numbers is the given key mapped to in the given hash table?
# this list should not contain duplicates, but need not be sorted.
def lookup(ht: HashTable, word: str) -> List[int]:
  pass

# Add a mapping from the given word to the given line number in
# the given hash table
def add(ht: HashTable, word: str, line: int) -> None:
  pass

# What are the words that have mappings in this hash table?
# this list should not contain duplicates, but need not be sorted.
def hash_keys(ht: HashTable) -> List[str]:
  pass

# given a list of stop words and a list of strings representing a text,
# return a hash table
def make_concordance(stop_words: List[str], text: List[str]) -> HashTable:
  pass
```

Note that nearly all of these methods should not require traversing the
whole hash table. The exceptions are: `hash_keys`, `make_concordance`,
and (occassionally) `add` (when a resize is required).

All of these should be defined in the file `main.py`, in such a way that
one can write 

```
from main import make_hash, hash_size, hash_count, has_key, lookup, add, hash_keys, make_concordance
```

### Implementation Report

Your project must include a short implementation writeup or
"lab report", containing the following information:

* instructions on how to call your program with a text of the user's choice.
* the data definitions, and first lines & purpose statements of every
  function & method that you wrote.
* A description of running the program on a large text file (> 1 Megabyte),
  including the total length of the output, and a quasi-random chunk of
  five consecutive lines of the output. Choose one of these lines, and verify
  by hand that the given word does in fact occur in the specified locations
  within the file.
* the name of an animal that does not occur anywhere in your source text.

This writeup should be in the form of a pdf with the name "writeup.pdf",
submitted as part of your Git repo.