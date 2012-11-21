import pytest
import os

from dictrie import *

@pytest.fixture(scope="module",
                params=['antidisestablishmentarianism', 'a', 'mitochondria'])
def word(request):
  return request.param

class TestSearch:
  def test_oneword(self, word):
    #testword = 'antidisestablishmentarianism'
    f = open('testdict.txt', 'w')
    f.write(word)
    f.close()
    t = DictTrie('testdict.txt')

    soFar = ''
    assert t.couldBeWord(soFar)
    for character in word:
      soFar += character
      assert t.couldBeWord(soFar)

    assert t.isWord(word)

    os.remove('testdict.txt')
