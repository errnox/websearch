import string
import time
import urllib
import webbrowser

import bottle as bo
import sqlite3


class WebApp (object):
  def __init__(self):
    self.name = 'Websearch'
    self.db = 'db/db.sqlite3'

  def get_static(self, filename):
    return bo.static_file(filename, root='static/')

  def get_index(self):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    r = c.execute('''
SELECT q.created_at, q.string, q.search_engine_name
FROM query q
ORDER BY q.created_at DESC
LIMIT 10;
''').fetchall()
    queries = []
    for row in r:
      created_at = time.strftime(
        '%a %d %b %Y %H:%M:%S', time.gmtime(row[0]))
      string = row[1]
      urlencoded = urllib.urlencode({'search': string})
      search_engine_name = row[2]
      queries.append({'created_at': created_at, 'string': string,
                      'string_urlencoded': urlencoded,
                      'search_engine_name': search_engine_name})

    r2 = c.execute('''
SELECT s.name, s.url
FROM search_engine s
ORDER BY rank ASC;
''').fetchall()

    search_engines = []
    for row in r2:
      search_engines.append({'name': row[0], 'url': row[1]})

    conn.commit()
    conn.close()

    search_query = bo.request.query.get('search')

    return bo.template(
      'index.html.tpl',
      queries=queries,
      search_query=search_query,
      search_engines=search_engines)

  def get_search(self):
    bo.redirect('/')

  def post_search(self):
    query = bo.request.forms.get('query')
    search_engine_url = bo.request.forms.get('engine_url')
    created_at = time.time()

    if string.strip(query) != '':
      conn = sqlite3.connect(self.db)
      c = conn.cursor()

      r = c.execute('''
SELECT s.url, s.name
FROM search_engine s
WHERE s.url = ?
LIMIT 1;
''', (search_engine_url,)).fetchone()

      url_template = r[0]
      search_engine_name = r[1]
      url_encoded = urllib.quote_plus(query)
      webbrowser.open(url_template.format(url_encoded))

      c.execute('''
INSERT INTO query (created_at, string, url_template, url, search_engine_name)
VALUES (?, ?, ?, ?, ?)
''', (created_at, query, url_template, url_encoded, search_engine_name))
      conn.commit()
      conn.close()

    bo.redirect('/')

  def get_engines(self):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    r = c.execute('''
SELECT s.name, s.url
FROM search_engine s
ORDER BY rank;
''').fetchall()
    engines = []
    for row in r:
      engines.append({'name': row[0], 'url': row[1]})
    conn.commit()
    conn.close()
    return bo.template('engines.html.tpl', engines=engines)

  def post_engines(self):
    s = bo.request.forms.get('lines')
    lines = string.split(s, '\n')
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    c.execute('''
DELETE FROM search_engine;
''')
    conn.commit()
    for rank, line in enumerate(lines):
      if string.strip(line) != '':
        splitted = string.split(line)
        url = splitted[-1]
        name = string.join(splitted[:-1])
        c.execute('''
INSERT INTO search_engine (name, url, rank) VALUES (?, ?, ?)
''', (name, url, rank))
        conn.commit()
    conn.close()
    bo.redirect('/')


if __name__ == '__main__':
  web_app = WebApp()
  app = bo.default_app()

  app.get(
    '/assets/<filename:path>',
    name='get_static',
    callback=web_app.get_static)

  app.get(
    '/',
    name='get_index',
    callback=web_app.get_index)

  app.get(
    ['/search', '/search/'],
    name='get_search',
    callback=web_app.get_search)
  app.post(
    ['/search', '/search/'],
    name='post_search',
    callback=web_app.post_search)

  app.get(
    ['/engines', '/engines/'],
    name='get_engines',
    callback=web_app.get_engines)
  app.post(
    ['/engines', '/engines/'],
    name='post_engines',
    callback=web_app.post_engines)

  app.run(host='localhost', port=4321, reloader=True, debug=True)
