YUI.add("yuidoc-meta", function(Y) {
   Y.YUIDoc = { meta: {
    "classes": [
        "jQuery",
        "jsp",
        "jsp.taglib.box",
        "jsp.taglib.button",
        "jsp.taglib.column",
        "jsp.taglib.device",
        "jsp.taglib.function",
        "jsp.taglib.html",
        "jsp.taglib.jsp",
        "jsp.taglib.jstl",
        "jsp.taglib.layout",
        "jsp.taglib.listsearchresult",
        "jsp.taglib.nablarch",
        "jsp.taglib.tab",
        "jsp.taglib.table",
        "jsp.taglib.template",
        "nablarch.ui",
        "nablarch.ui.AutoSpan",
        "nablarch.ui.AutoSum",
        "nablarch.ui.Collapsible",
        "nablarch.ui.ContextMenu",
        "nablarch.ui.DatePicker",
        "nablarch.ui.LightBox",
        "nablarch.ui.ListBuilder",
        "nablarch.ui.SlideMenu",
        "nablarch.ui.Tab",
        "nablarch.ui.TabLink",
        "nablarch.ui.TabindexOrder",
        "nablarch.ui.ToggleCheckbox",
        "nablarch.ui.Tooltip",
        "nablarch.ui.TreeList",
        "nablarch.ui.TreeMenu",
        "nablarch.ui.Widget",
        "nablarch.ui.event.AjaxAction",
        "nablarch.ui.event.Listener",
        "nablarch.ui.event.ShowDialog",
        "nablarch.ui.event.SubWindowListener",
        "nablarch.ui.event.ToggleAction",
        "nablarch.ui.event.WindowClose",
        "nablarch.ui.event.WriteAction",
        "nablarch.ui.selector",
        "nablarch.util.BigDecimal",
        "nablarch.util.BigDecimal.NaN",
        "nablarch.util.Consumer",
        "nablarch.util.DateUtil",
        "nablarch.util.SimpleDateFormat"
    ],
    "modules": [
        "devtool",
        "jsp",
        "jsp.taglib",
        "nablarch.ui",
        "nablarch.ui.device",
        "nablarch.util"
    ],
    "allModules": [
        {
            "displayName": "devtool",
            "name": "devtool",
            "description": "モック画面JSP開発用ツール起動スクリプト\n\n以下の使用例のようにJSPの先頭にDOCTYPE宣言とJSPコメントで囲ったスクリプトタグを\n記述することで、JSPのローカルレンダリング等の各種開発用機能が有効となる。"
        },
        {
            "displayName": "jsp",
            "name": "jsp",
            "description": "ページ上JSPソースコードをブラウザ上でモックレンダリングするjQuery拡張。\n\n各JSPタグを対応するHTMLタグに変換する処理は、 `jsp/taglib/(タグリブ名).js` に\nディスパッチされる。\n例えば、 `<c:if>` の変換は `jsp/taglib/jstl.js` で行なわれる。"
        },
        {
            "displayName": "jsp.taglib",
            "name": "jsp.taglib",
            "description": "一覧検索画面表示用タグ `<listSearchResult:xxx>` タグのエミュレーションを行う。\n\n`js/jsp/tagfile` 配下に存在するタグファイルをロードする。"
        },
        {
            "displayName": "nablarch.ui",
            "name": "nablarch.ui"
        },
        {
            "displayName": "nablarch.ui.device",
            "name": "nablarch.ui.device",
            "description": "iOSビューポート制御不具合修正\n================================================\niOSデバイスにおいて、viewportをdevice-widthに設定しかつユーザによる拡大・縮小を禁止\nした場合に、デバイスの縦横表示の切替をくりかえすと、画面の表示がすこしずつ拡大して\nいくという問題がある。(iOS6/iOS7での発生を確認)\n\n本スクリプトでは、この問題を回避するためのものである。"
        },
        {
            "displayName": "nablarch.util",
            "name": "nablarch.util",
            "description": "ユーティリティ関数など"
        }
    ]
} };
});