from main import *

stopWords = readStopWords("stopWords.txt")
text = readText("test.txt")
mc = make_concordance(stopWords, text)

make_result(mc)