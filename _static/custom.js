$(function () {
  var form = $('#google-search-form');
  var q = $('#q');
  var text = $('#text');
  var url = 'nablarch.github.io/docs/LATEST/doc';
  form.submit(function (event) {
    q.val('site:' + url + ' ' + text.val());
  });
});
