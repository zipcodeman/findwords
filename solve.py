import Queue

import itertools
import random
import string
import sys
import dictrie
import time

dictionary = dictrie.DictTrie("allwords.txt")

class Word:
  def __init__(self, position, grid):
    self._p = position
    self._grid = grid
    self._word = grid[self._p[1]][self._p[0]]
    self._path = [position]

  @staticmethod
  def possibleMoves(position):
    x, y = position
    successors = []
    for i in range(3):
      xdel = i - 1
      for j in range(3):
        ydel = j - 1
        if xdel != 0 or ydel != 0:
          successors.append((x + xdel, y + ydel))
    return successors

  def copy(self):
    retval = Word(self._p, self._grid)
    retval._word = self._word
    retval._path = self._path[:]
    return retval

  def generateSuccessors(self):
    moves = Word.possibleMoves(self._p)
    retval = []
    for move in moves:
      x, y = move
      if y >= 0 and y < len(self._grid):
        if x >= 0 and x < len(self._grid[y]):
          if (x, y) not in self._path:
            n = self.copy()
            n._path.append((x, y))
            n._p = (x, y)
            n._word += self._grid[y][x]
            retval.append(n)
    return retval

  def getWord(self):
    return self._word

  def __len__(self):
    return len(self._word)

  def __str__(self):
    row = '+--+--+--+--+\n'
    retval = self._word + '\n'
    retval += row
    y = 0
    for r in self._grid:
      x = 0
      retval += '|'
      for c in r:
        if (x, y) in self._path:
          retval += '% 2d|' % (self._path.index((x, y)) + 1)
        else:
          retval += '% 2s|' % '  '
        x += 1
      retval += '\n'
      retval += row
      y += 1
    return retval

dims = [4,4]

letters = []
while True:
  i = raw_input('> ')
  if i.strip() == '':
    break
  letters.append(i.split())

for line in letters:
  for letter in line:
    print letter,
  print

fringe = Queue.Queue()
for perm in itertools.product(range(4), repeat=2):
  fringe.put(Word(perm, letters))

count = 0
length = 0
found = {}

while not fringe.empty():
  count += 1
  if (count % 100) == 0:
    sys.stdout.write('\r' + "Processed %d (max length %d)" % (count, length))
    sys.stdout.flush()
  word =  fringe.get()
  length = max(length, len(word))

  newmoves = word.generateSuccessors()

  for new in newmoves:
    if dictionary.isWord(new.getWord()) and len(new) > 2:
      if len(new) not in found:
        found[len(new)] = set()
      found[len(new)].add(new)
    if dictionary.couldBeWord(new.getWord()):
      fringe.put(new)

for i in reversed(sorted(found.keys())):
  print
  print
  print len(found[i])
  for element in found[i]:
    print element.getWord() + '\t',
