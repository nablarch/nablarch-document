$(function () {
  var form = $('#google-search-form');
  var version = $('#document-version').val();
  var q = $('#q');
  var text = $('#text');
  var url = 'nablarch.github.io/docs/' + version + '/doc';
  form.submit(function (event) {
    q.val('site:' + url + ' ' + text.val());
  });
});
