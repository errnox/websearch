% rebase('base.html.tpl', title='Search Engines')
<div class="row">
  <div class="col col-md-8 col-md-offset-2">
    <h4 class="text-muted">Search Engines</h4>
    <div class="panel-body"></div>
    <form action="/engines" method="post">
      <textarea class="form-control" cols="30" rows="10" name="lines" autofocus>
% for engine in engines:
{{engine['name']}} {{engine['url']}}
% end
</textarea>
      <div class="panel-body"></div>
      <button class="btn btn-success" type="submit">Update</button>
      <a class="btn btn-link" href="/">Cancel</a>
    </form>

    <div class="panel-body"></div>
    <div class="panel-body"></div>

    <hr/>
    <b>Heads Up</b>
    <div class="panel-body"> </div>
    <p>
      Each line in this text box represents one search engine and
      looks like this: "&lt;Name&gt; &lt;URL&gt;". Note that there is
      at least one space between "&lt;Name&gt;" and "&lt;URL&gt;". The
      lines at the top are ranked higher and will be presented at the
      top of the selection menu. "&lt;Name&gt;" may, however, include
      spaces. "{}" indicates where the search string should be placed.
    </p>
    <p>
      Here is an example:
    </p>
    <pre>DuckDuckGo https://duckduckgo.com/html?q={}
Wikipedia Search http://en.wikipedia.org/wiki/?search={}
GitHub http://www.github.com/search?q={}
StackOverflow Search http://stackoverflow.com/search?q={}
Info.com http://info.com/{}</pre>
  </div>
</div>
