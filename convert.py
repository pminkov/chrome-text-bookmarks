"""
Usage:

1. Export bookmarks from chrome into an html.
2. python ./convert.py < ./bookmarks_5_17_16.html
3. Text appears.
"""

import sys

from HTMLParser import HTMLParser

class BookmarksHTMLParser(HTMLParser):
  indent = 0
  in_anchor = False
  cur_href = ''

  def is_list(self, tag):
    return tag.lower() == 'dl'

  def is_term(self, tag):
    return tag.lower() == 'dt'

  def is_anchor(self, tag):
    return tag.lower() == 'a'
  
  def handle_starttag(self, tag, attrs):
    if self.is_list(tag):
      self.indent += 2

    if self.is_anchor(tag):
      self.in_anchor = True

      for (k, v) in attrs:
        if k == 'href':
          self.cur_href = v
      

  def handle_endtag(self, tag):
    if self.is_list(tag):
      self.indent -= 2

    if self.is_anchor(tag):
      self.in_anchor = False
      

  def handle_data(self, rawdata):
    data = rawdata.strip()
    if not self.in_anchor:
      if data:
        ind = ' ' * self.indent
        print '%s[ %s ]' % (ind, data)
    else:
      if data:
        ind = ' ' * self.indent
        print '%s%s [%s]' % (ind, data, self.cur_href)


if __name__ == '__main__':
  input_str = sys.stdin.read()
  input_str = input_str.replace('&#39;', "'")
  parser = BookmarksHTMLParser()
  parser.feed(input_str)
