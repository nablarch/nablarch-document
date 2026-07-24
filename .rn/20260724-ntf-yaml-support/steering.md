Rn version: 0.8.0

# Goal

NTF（Nablarch Testing Framework）のドキュメントを刷新する。具体的な作業内容は別途指示を受けて詳細化する。

# Acceptance criteria

- （作業指示受領後に記載）

# Assumptions

- 作業指示は本セッション中に提供される
- 変更対象は nablarch-document リポジトリ内の NTF 関連ドキュメント

# Rules

- commit and push every change; one completion marker per task
- 日本語で記述する

# Tasks

### #1: 作業指示の受領とタスク詳細化

**Purpose**: ユーザーから NTF ドキュメント刷新の具体的な作業指示を受領し、steering.md のタスクと受入基準を確定させる。

**Prerequisites**: none

**Steps**:

- [ ] ユーザーから作業指示を受け取る
- [ ] Acceptance criteria を具体化して更新する
- [ ] Tasks を作業指示に基づいて詳細化して更新する
- [ ] self-check (OK/NG per completion criterion, record in checks/task-01.md)

**Completion criteria**:

- Acceptance criteria に具体的な検証可能な条件が記載されている
- Tasks にユーザー指示に対応したタスクが分解・記載されている

### #2: Evaluation sign-off

**Purpose**: NTF ドキュメント刷新の完了を Acceptance criteria に照らして確認し、ユーザーの承認を得る。

**Prerequisites**: すべての作業タスク完了

**Steps**:

- [ ] Acceptance criteria の達成状況を確認する
- [ ] 結果をユーザーに提示して `/rn:ty`（承認）または `/rn:gm`（修正）の判定をもらう

**Completion criteria**:

- すべての Acceptance criteria が達成されていることが確認できる
- ユーザーが `/rn:ty` で承認している

# State

- **Status**: not suspended
- **Date**: 2026-07-24
- **Last completed**: (none)
- **Next**: #1 作業指示の受領とタスク詳細化
- **Notes**: 作業指示待ち。指示受領後に Acceptance criteria と Tasks を更新する。
