# 文档风格

所有拉取请求都必须满足以下文档标准。关于
[自动生成的文档页面](https://leanprover-community.github.io/mathlib4_docs/)，
请参阅 [`doc-gen` 仓库](https://github.com/leanprover/doc-gen4)。

你可以使用 [Lean doc preview 页面](https://observablehq.com/@bryangingechen/github-lean-doc-preview)
预览某个 GitHub 页面或拉取请求的 markdown 处理效果。

## 头部注释

每个 mathlib 文件都应以下列内容开头：
* 一段包含版权信息的头部注释（参见[我们风格指南中的建议](style.html#header-and-imports)）；
* 导入列表（每行一个）；
* 一段包含通用文档的模块文档字符串，[使用 Markdown 和 LaTeX 编写](#latex-and-markdown)。

（参见下面的示例。）

标题使用 atx 风格的标题（带井号，不在下方加横线）。
开始与结束的分隔符 `/-!` 和 `-/` 应各自单独占一行。

文件必须有一个一级标题。其后跟随对文件内容的概述。

其他二级标题章节（按此顺序）为：
* *Main definitions*（可选，可在概述中涵盖）
* *Main statements*（可选，可在概述中涵盖）
* *Notation*（仅当本文件未引入任何记号时才省略）
* *Implementation notes*（描述重要的设计决策或接口特性，
  包括类型类的使用以及新定义的 `simp` 范式）
* *References*（对教科书、论文或维基百科页面的引用）
* *Tags*（一组关键词，在 mathlib 中进行文本搜索以查找某事物在何处涉及时可能有用）

引用应指向 [mathlib 引文文件](https://github.com/leanprover-community/mathlib4/blob/master/docs/references.bib)中的 bibtex 条目。
请参阅下面的[引用其他著作](#citing-other-works)一节。

下面的代码块是文件头部的一个示例。

```lean
/-
Copyright (c) 2018 Robert Y. Lewis. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Robert Y. Lewis
-/
module

public import Mathlib.Algebra.Order.AbsoluteValue.Basic
public import Mathlib.NumberTheory.Padics.PadicVal.Basic

/-!
# p-adic norm

This file defines the `p`-adic norm on `ℚ`.

The `p`-adic valuation on `ℚ` is the difference of the multiplicities of `p` in the numerator and
denominator of `q`. This function obeys the standard properties of a valuation, with the appropriate
assumptions on `p`.

The valuation induces a norm on `ℚ`. This norm is a nonarchimedean absolute value.
It takes values in {0} ∪ {1/p^k | k ∈ ℤ}.

## Implementation notes

Much, but not all, of this file assumes that `p` is prime. This assumption is inferred automatically
by taking `[Fact p.Prime]` as a type class argument.

## References

* [F. Q. Gouvêa, *p-adic numbers*][gouvea1997]
* [R. Y. Lewis, *A formal proof of Hensel's lemma over the p-adic integers*][lewis2019]
* <https://en.wikipedia.org/wiki/P-adic_number>

## Tags

p-adic, p adic, padic, norm, valuation
-/
```

## 文档字符串

每个定义和重要定理都必须有文档字符串。
（也鼓励在引理上添加文档字符串，尤其是当该引理具有某些数学内容
或可能在其他文件中有用时。）
这些文档字符串使用 `/--` 引入，并以 `-/` 结束，置于定义之上，标记与文本之间
可用换行或单个空格分隔。
文档字符串的后续行不应缩进。
它们同样可以包含 Markdown 和 LaTeX：参见下一节。如果文档字符串是一个完整的
句子，则应以句号结尾。具名定理，例如 **mean value theorem**，应使用粗体（即前后各加两个星号）。

文档字符串应传达定义的数学含义。它们可以与实际实现略有出入。下面是一个文档字符串示例：

```lean
/-- If `q ≠ 0`, the `p`-adic norm of a rational `q` is `p ^ (-padicValRat p q)`.
If `q = 0`, the `p`-adic norm of `q` is `0`. -/
def padicNorm (p : ℕ) (q : ℚ) : ℚ :=
  if q = 0 then 0 else (p : ℚ) ^ (-padicValRat p q)
```

一个略有出入但仍描述了数学内容的示例如下：

```lean
/-- `padicValRat` defines the valuation of a rational `q` to be the valuation of `q.num` minus the
valuation of `q.den`. If `q = 0` or `p = 1`, then `padicValRat p q` defaults to `0`. -/
def padicValRat (p : ℕ) (q : ℚ) : ℤ :=
  padicValInt p q.num - padicValNat p q.den
```

### 策略文档

策略应具有符合 [Lean 文档风格指南](https://github.com/leanprover/lean4/blob/master/doc/style.md#tactics)的文档字符串。
要点是：完整且自包含，但要简明。文档字符串应以一个完整的
句子开头，该句子以该策略为主语。（例如："`rewrite [e]` uses the expression `e` as a
rewrite rule on the main goal."）该策略的所有不同选项和形式都应出现在
项目符号列表中。"Examples:" 一节（如果有）应是一系列代码块。

### 代码检查（Linting）

`docBlame` 检查器会列出所有没有文档字符串的定义。`docBlameThm`
检查器会列出没有文档字符串的定理和引理。`tacticDocs` 检查器会列出
所有没有文档字符串的策略。

要仅运行 `docBlame` 检查器，请在你的 lean 文件末尾添加以下内容：
```
#lint only docBlame
```
要仅运行 `docBlame` 和 `docBlameThm` 检查器，请在你的 lean
文件末尾添加以下内容：
```
#lint only docBlame docBlameThm
```
要运行所有默认检查器（包括 `docBlame` 和 `tacticDocs`），请在你的 lean 文件末尾
添加以下内容：
```
#lint
```
要运行所有默认检查器（包括 `docBlame`）并运行 `docBlameThm`，请在你的
lean 文件末尾添加以下内容：
```
#lint docBlameThm
```

## LaTeX 与 Markdown

我们通常将对 Lean 声明或变量的引用放在反引号之间。写出
全限定名称（例如 `finset.card_pos` 而不只是 `card_pos`）会在我们的[在线文档](https://leanprover-community.github.io/mathlib4_docs/)中
将该名称变为一个链接。

原始 URL 应用尖括号 `<...>` 括起来，以确保它们在线时可点击。
（某些 URL，尤其是那些带括号或其他特殊符号的，
可能无法被 markdown 渲染器正确解析。）

而在谈及数学符号时，则可能更宜使用 LaTeX。可以通过三种方式在
文档字符串中包含 LaTeX：
- 使用单美元符号 `$ ... $` 以内联方式渲染数学公式，
- 使用双美元符号 `$$ ... $$` 以"显示模式"渲染数学公式，或
- 使用环境 `\begin{*} ... \end{*}`（不带美元符号）。

这些对应于我们在线文档的 [MathJax](http://docs.mathjax.org/en/latest/basic/mathematics.html) 设置。
那里 Markdown 与 LaTeX 之间的交互方式类似于
<https://math.stackexchange.com> 和 <https://mathoverflow.net> 上的情形，因此你可以把一个文档字符串粘贴到
[那里的一个编辑沙盒](https://math.meta.stackexchange.com/questions/4666/sandbox-for-drafts-of-long-complex-posts)中
以预览最终结果。另请参阅 math.stackexchange 的
[MathJax 教程](https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference)。


## 分节注释

通常会将一个文件组织成若干节，每节包含相关的声明。
通过在开头用模块文档 `/-! ... -/` 描述这些节，
这些节便能在文档中显现。

虽然这些分节注释往往会对应于 `section` 或 `namespace` 命令，
但这并非必需。你可以在一个 section 或 namespace 内部使用分节注释，也可以
让多个 section 或 namespace 跟随在一个分节注释之后。

分节注释仅用于显示和可读性。它们没有语义含义。

在分节注释内部的标题应使用三级标题 `###`。

如果注释长度超过一行，分隔符 `/-!` 和 `-/` 应各自单独占一行。

实际示例参见 [Lean/Expr/Basic.lean](https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/Lean/Expr/Basic.lean)。

```lean
namespace BinderInfo

/-! ### Declarations about `BinderInfo` -/

/-- The brackets corresponding to a given `BinderInfo`. -/
def brackets : BinderInfo → String × String
  | BinderInfo.implicit => ("{", "}")
  | BinderInfo.strictImplicit => ("{{", "}}")
  | BinderInfo.instImplicit => ("[", "]")
  | _ => ("(", ")")

end BinderInfo

namespace Name

/-! ### Declarations about `name` -/

/-- Find the largest prefix `n` of a `Name` such that `f n != none`, then replace this prefix
with the value of `f n`. -/
def mapPrefix (f : Name → Option Name) (n : Name) : Name := Id.run do
  if let some n' := f n then return n'
  match n with
  | anonymous => anonymous
  | str n' s => mkStr (mapPrefix f n') s
  | num n' i => mkNum (mapPrefix f n') i
```

## 理论文档

除了存在于 Lean 文件中的文档之外，我们还有[理论文档](../theories.html)，
其中给出跨越多个 Lean 文件的综述，
以及在形式化需要略为奇特视角的情形下提供更多数学解释，
例如可参见[拓扑文档](../theories/topology.html)。

## 引用其他著作

要在文档字符串中引用论文和书籍，首先应将引用条目添加到
BibTeX 文件：`docs/references.bib`。要使用 `bibtool` 规范化该文件，
你可以运行：

```text
bibtool --preserve.key.case=on --preserve.keys=on --print.use.tab=off --pass.comments=on -s -i docs/references.bib -o docs/references.bib
```

要确保你的引用在在线文档中成为链接，你可以使用以下
两种风格中的任意一种：

第一，你可以将 `docs/references.bib` 中使用的引用键放在方括号中：

```markdown
The proof can be found in [Boole1854].
```

在在线文档中，这会变成类似于：

> The proof can be found in [[Boo54]](https://leanprover-community.github.io/mathlib4_docs/references.html)

（该键会变为一个 [`alpha` 风格的标签](https://www.bibtex.com/s/bibliography-style-base-alpha/)，
并成为指向文档[参考文献页面](https://leanprover-community.github.io/mathlib4_docs/references.html)的链接。）

或者，你也可以通过在引用键前面的方括号中放入文本，
来为引用使用自定义文本：

```markdown
See [Grundlagen der Geometrie][hilbert1999] for an alternative axiomatization.
```

> See [Grundlagen der Geometrie](https://leanprover-community.github.io/mathlib4_docs/references.html) for an alternative axiomatization.

注意，你目前不能在链接文本中使用右方括号 `]` 符号。
因此下面的写法不会生成可用的链接：

```markdown
We follow [Euclid's *Elements* [Prop. 1]][heath1956a].
```

> We follow [Euclid's *Elements* [Prop. 1]][heath1956a].

## 语言

文档应使用英语撰写。
任何常见的拼写（例如英式、美式或澳式英语）都可接受。
不应仅为了改变所用的拼写而提交拉取请求，
但作为某个大幅增强文档的 PR 的一部分而改变拼写则是可接受的。
这与[声明名称](naming.html#spelling)的规则形成对比，
后者应使用美式英语拼写。

## 示例

以下文件作为良好文档风格的范例加以维护：

* [Mathlib.NumberTheory.Padics.PadicNorm](https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/NumberTheory/Padics/PadicNorm.lean)
* [Mathlib.Topology.Basic](https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/Topology/Basic.lean)
* [Analysis.Calculus.ContDiff.Basic](https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/Analysis/Calculus/ContDiff/Basic.lean)
