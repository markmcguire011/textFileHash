from main import *

stopWords = readStopWords("./text/stopWords.txt")
text = readText("./text/test.txt")
mc = make_concordance(stopWords, text)

make_result(mc)