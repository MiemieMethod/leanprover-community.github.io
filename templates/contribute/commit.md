# 拉取请求标题与描述规范

我们采用以下规范来撰写拉取请求的标题与描述。

## 格式

注意:"Title:" 与 "Description:" 并不会实际出现

```markdown
  Title:
  <type>(<optional-scope>): <subject>

  Description:
  <body>
  <NEWLINE>
  <footer>
  <NEWLINE>
  <dependencies>
```

`<type>` 为:

 - feat (feature,新功能)
 - fix (bug fix,缺陷修复)
 - doc (documentation,文档)
 - style (formatting, missing semicolons, ...,格式调整、缺失的分号等)
 - refactor (重构)
 - test (when adding missing tests,补充缺失的测试时)
 - chore (maintain,维护)
 - perf (performance improvement, optimization, ...,性能改进、优化等)
 - ci (for changes to github workflows, other automation,对 github workflows 及其他自动化的修改)

`<optional-scope>` 是包含所修改模块的某个模块名或目录名。
它并非必须包含,但当 `<subject>` 不足以说明时可能会有用。
`Mathlib` 目录前缀总是省略。
例如,它可以是

- Data/Nat/Basic
- Algebra/Group/Defs
- Topology/Constructions

`<subject>` 有以下约束:

- 使用祈使语气、现在时态:用 "change" 而非 "changed" 或 "changes"
- 首字母不大写
- 结尾不加句点(.)

`<body>` 有以下约束:

- 与 ``<subject>`` 一样,使用祈使语气、现在时态
- 包含本次修改的动机,并与之前的行为作对比

`<footer>` 是可选的,可能包含两项内容:

- 破坏性变更(Breaking changes):所有破坏性变更都必须在 footer
  中提及,并附上变更的描述、理由以及迁移说明
- 引用 issue(Referencing issues):已关闭的缺陷应在 footer 中单独
  成行列出,并以 "Closes" 关键字为前缀,例如:Closes #123, #456

`<dependencies>` 如果本 PR 依赖于其他 PR,则应以复选框格式列出,
即 `- [ ] depends on: #XXXX`

## 示例

一个无需 `<scope>` 的示例可能是:

```markdown
feat: have library search use the whole range for replacement

previously `apply? using h` would replace to `refine blah using h` rather than `refine blah`.

This also changes the diagnostic message to be on the whole syntax `apply? using h` rather than just the `apply?` bit, which seems fine to me.
```

而一个包含 `<scope>` 确实能增加价值的示例:

```markdown
doc(CategoryTheory/EssentialImage): typo and punctuation

Fix a typo, add two periods.
```

一个带有依赖 PR 的示例:

```markdown
feat: the norm on `Unitization` is a C⋆-norm

This shows that C⋆-algebras are always `RegularNormedAlgebra`s, so that their `Unitization` is equipped with a norm. Moreover, we show this norm is a C⋆-norm.

---

- [ ] depends on: #5330
- [ ] depends on: #5741
- [ ] depends on: #5742
- [ ] depends on: #5743
```
