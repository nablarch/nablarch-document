============================
設計指針
============================

----------------------
業務画面JSPの記述
----------------------
Nablarchでの画面開発のワークフローでは、設計段階から各業務画面のJSPを作成する。
これらのJSPでは画面項目定義書の記述レベルと同じ抽象度をもったカスタムタグを記述する。
以下は業務画面JSPの記述例である。

.. code-block:: jsp

      <t:page_template
          title="ユーザ情報登録"
          confirmationPageTitle="ユーザ情報登録確認">
        <jsp:attribute name="contentHtml">
        <n:form>
          <field:block title="ユーザ基本情報">
            <field:text title="ログインID"
                        required="true"
                        maxlength="20"
                        hint="半角英数記号20文字以内"
                        sample="test01">
            </field:text>
            <field:password title="パスワード"
                            required="true"
                            maxlength="20"
                            sample="password">
            </field:password>
            <field:password title="パスワード（確認用）"
                            required="true"
                            maxlength="20"
                            sample="password">
            </field:password>
            <field:hint>半角英数記号20文字以内</field:hint>
          </field:block>
          <button:block>
            <button:back
                  label="一覧照会画面へ"
                  size="4">
              </button:back>
              <button:check
                  uri="/action/ss11AC/W11AC02Action/RW11AC0202">
              </button:check>
          </button:block>
        </n:form>
        </jsp:attribute>
      </t:page_template>
 

このソースコードを見ると、各業務画面のJSPソースコードから画面の見た目に関する情報が全て排除されていることがわかる。
このソース中の各カスタムタグがどのように画面上に表示されるのかを規定するのが **UI標準**
であり、その標準に沿った画面表示を実現する共通部品群が :doc:`../internals/jsp_page_templates` と
:doc:`../internals/jsp_widgets` である。

:doc:`../internals/jsp_page_templates` は画面の全体構成および、画面間で共通のヘッダー・サイドメニューなどの
領域の描画を行うUI部品である。
:doc:`../internals/jsp_widgets` は各業務画面中で使用する
ボタン、検索結果テーブル、テキスト入力などの描画を行うUI部品である。

業務画面JSPでは、画面表示に関する実装は全て :doc:`../internals/jsp_page_templates` と
:doc:`../internals/jsp_widgets` を通じて行う。 [#]_ 
これにより、各画面の開発者が全く意識しなくとも、UI標準に準拠した画面表示となることが保証される。

.. [#]
  業務画面JSPに直接記述したHTMLは、そのまま画面上に描画される。
  このため :doc:`../internals/jsp_widgets` として提供されていない画面要素がある場合は、
  一旦HTMLとして記述し、仕様が固まった後で共通化するといったことが可能である。


以下はこの構造をあらわした概念図である。

.. figure:: ../_image/app_jsp.png
     :scale: 85 
     :align: center

ここで作成した業務画面JSPは、以下の特性をもつ。

  **ブラウザで直接開くことが可能**
    各設計担当者に業務画面JSPを確認するためのサーバー環境を用意させるのはかなり難しいので、
    本機能で作成したJSPファイルはHTMLと同様に直接ブラウザで確認することが可能となっている。

    詳細は :doc:`../internals/inbrowser_jsp_rendering` を参照すること。


  **画面項目一覧を表示しその内容をExcelの設計書に貼りこむことが可能**
    業務画面JSPのローカル表示時に、画面内の入出力項目を **システム機能設計書/画面項目一覧**
    の書式で画面上に表示でき、その内容をコピー&ペーストで設計書に貼りこむことが可能である。


  **マルチブラウザ・マルチデバイスでの表示が可能**
    **UI標準** では、マルチブラウザ・マルチデバイスをサポートしており、
    各デバイスでどのような表示になるかについて、詳細に定義している。
    そこで記述している仕様は全て :doc:`../internals/jsp_page_templates` と
    :doc:`../internals/jsp_widgets` 側の実装により吸収されるため、
    各業務画面ではその実装について気にする必要はない。


  **開発工程以降もそのまま流用できる**
    設計工程で作成したJSPファイルは、必要最小限の修正(入力項目の **name** 属性追加など)により
    開発工程以降もそのまま流用することが可能である。



--------------------------------------------
UI標準と共通部品
--------------------------------------------
上述したように、本機能では各画面のJSPを最小の工数で作成できるだけでなく、
インターフェース標準への準拠、デモ用の表示、画面項目定義の出力、
マルチデバイスへの対応などを単一のソースコードで実現することができる。

しかし、これらの機能を実現している :doc:`../internals/jsp_page_templates` および
:doc:`../internals/jsp_widgets` の修正には、高い技術と知識が必要となる。
特に、PJごとの要求に沿ってUI標準のカスタマイズを行った際、
その内容に沿った共通部品の修正を行う担当者の存在はPJを進める上で必須である。


