class Trie:
  def __init__(self):
    self._trie = {}

  def addWord(self, word):
    current = self._trie
    for character in word:
      if character not in current:
        current[character] = {}
      current = current[character]
    current['word'] = True

  def couldBeWord(self, prefix):
    current = self._trie
    for c in prefix:
      if c not in current:
        return False
      current = current[c]
    return True

  def isWord(self, word):
    current = self._trie
    for character in word:
      if character not in current:
        return False
      current = current[character]
    if 'word' in current:
      return current['word']
    return False

  def __str__(self):
    return str(self._trie)

class DictTrie(Trie):
  def __init__(self, filename):
    Trie.__init__(self)
    for line in open(filename, 'r'):
      self.addWord(line.strip())
