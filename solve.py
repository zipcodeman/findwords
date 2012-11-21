import Queue

import itertools
import popen2
import random
import string
import sys
import dictrie

dictionary = dictrie.DictTrie("wordsEn.txt")

class ispell:
  def __init__(self):
    self._f = popen2.Popen3("ispell")
    self._f.fromchild.readline()
  def __call__(self, word):
    self._f.tochild.write(word + '\n')
    self._f.tochild.flush()
    s = self._f.fromchild.readline()
    self._f.fromchild.readline()
    if s[:8] == "word: ok":
      return None
    else:
      return (s[17:-1]).split(', ')

checker = ispell()
dims = [4,4]

letters = [
  ['p', 'l', 'm', 't'],
  ['w', 'p', 'a', 'e'],
  ['n', 'n', 'r', 'v'],
  ['i', 'n', 'a', 'l']
]

letters = []
while True:
  i = raw_input('> ')
  if i.strip() == '':
    break
  letters.append(i.split())

# for a in range(dims[0]):
  # for b in range(dims[1]):
    # letters[a][b] = random.choice(string.lowercase)

for line in letters:
  for letter in line:
    print letter,
  print

fringe = Queue.Queue()
for perm in itertools.product(range(4), repeat=2):
  fringe.put(( [perm], letters[perm[1]][perm[0]] ))

count = 0
length = 0
found = {}

while not fringe.empty():
  count += 1
  if (count % 1000) == 0:
    sys.stdout.write('\r' + "Processed %d (max length %d)" % (count, length))
    sys.stdout.flush()
  moves, word =  fringe.get()
  length = max(length, len(word))
  newmoves = []
  if moves[-1][0] > 0:
    newmoves.append((moves[-1][0] - 1, moves[-1][1]))
  if moves[-1][1] > 0:
    newmoves.append((moves[-1][0], moves[-1][1] - 1))
  if moves[-1][0] < 3:
    newmoves.append((moves[-1][0] + 1, moves[-1][1]))
  if moves[-1][1] < 3:
    newmoves.append((moves[-1][0], moves[-1][1] + 1))
  if moves[-1][0] > 0 and moves[-1][1] > 0:
    newmoves.append((moves[-1][0] - 1, moves[-1][1] - 1))
  if moves[-1][0] > 0 and moves[-1][1] < 3:
    newmoves.append((moves[-1][0] - 1, moves[-1][1] + 1))
  if moves[-1][0] < 3 and moves[-1][1] > 0:
    newmoves.append((moves[-1][0] + 1, moves[-1][1] - 1))
  if moves[-1][0] < 3 and moves[-1][1] < 3:
    newmoves.append((moves[-1][0] + 1, moves[-1][1] + 1))

  for newpos in newmoves:
    newword = word + letters[newpos[1]][newpos[0]]
    m = moves[:]
    if newpos not in moves:
      m.append(newpos)
      if dictionary.isWord(newword) and len(newword) > 2:
        if len(newword) not in found:
          found[len(newword)] = set()
        found[len(newword)].add(newword)
      if dictionary.couldBeWord(newword):
        fringe.put((m, newword))

for i in reversed(sorted(found.keys())):
  print
  print '\t'.join(sorted(found[i]))
