% rebase('base.html.tpl', title='Search')
<div class="row">
  <form action="/search" method="post">

    <div class="col col-md-9">
      <div class="input-group">
        % if search_query != None:
        <input class="form-control" name="query" type="text" placeholder="Search..." autofocus value="{{search_query}}"/>
        % else:
        <input class="form-control" name="query" type="text" placeholder="Search..." autofocus/>
        % end
        <span class="input-group-btn">
          <button class="btn btn-default" type="submit">Search</button>
        </span>
      </div>
      <div class="panel-body"></div>
    </div>

    <div class="col col-md-3">
      <select class="form-control" name="engine_url">
        % for engine in search_engines:
        <option value="{{engine['url']}}">{{engine['name']}}</option>
        % end
      </select>
    </div>

  </form>
</div>

<div class="row">
  <div class="col col-md-12">
    <div class="panel-body"></div>
    <div class="panel-body"></div>
    <center><span class="text-muted">Recent Searches</span></center>
    <div class="panel-body"></div>

    % for query in queries:
    <div>
      <hr/>
      <a href="/?{{query['string_urlencoded']}}">{{query['string']}}</a>
      <span class="hidden-sm text-muted">&nbsp;&nbsp;</span>
      <small><span class="text-muted" style="color: #AEAEAE">{{query['search_engine_name']}}</span></small>
      <div class="panel-body hidden-md hidden-lg hidden-md"></div>
      <small><span class="text-muted pull-right">{{query['created_at']}}</span></small>
    </div>
    % end

  </div>
</div>
