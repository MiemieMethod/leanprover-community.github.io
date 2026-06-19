# 你证明它了吗？

[Lean](https://lean-lang.org/) 是一个计算机程序，
它能够以超越人类的水平验证数学证明。但 Lean 是
一个复杂的程序。某人声称自己证明了一条定理，
不能仅仅附上一段 Lean 代码；这段代码必须符合若干
基本准则。下面我们简要列出这些准则，
然后再逐一详细说明。

## 验证 Lean 证明的准则

* 你的代码是否位于一个格式正确的 Lean 仓库中？单独一个 Lean 文件是不够的。
* 仓库能否编译？换言之，`lake build` 是否无错误地返回？
* 证明是否正在被检查？换言之，证明主定理的那个文件
  是否被构建过程所编译？
* 证明所用的内容是否不超出 Lean 的标准公理？
  换言之，`#print axioms my_proof` 是否返回 `[propext, Classical.choice, Quot.sound]` 的一个子集？
* 你的工作是否证明了你所声称证明的内容？

下面我们逐一详细说明这些准则。

## 你的代码是否位于一个仓库中？

Lean 是一个发展迅速的软件，每月都有新的
发布。Lean 的数学库 `mathlib`
通常每天都会合并许多提交。在
当前阶段，该软件仍处于“快速推进”阶段，
对向后兼容性几乎没有保证。这在
实践中意味着，你电脑上某个随机目录下的一个 Lean
文件中的独立代码片段，可能在你的机器上能够编译，
但在别人的机器上却不行（甚至在以后的某个时刻在你自己的机器上也不行）——
因为所用的 Lean 或 `mathlib` 版本不同。

为解决这个问题，Lean 代码需要成为
一个*仓库*（也称为*项目*）的一部分。例如，
[mathlib](https://github.com/leanprover-community/mathlib4)
就是一个存储在 GitHub 上的 Lean 项目。一个 Lean 项目附带
各种系统文件，这些文件精确地确定了你的代码所使用的
Lean 版本（以及诸如 Mathlib 之类的其他依赖库的版本），
这意味着其他人可以独立地编译你的代码。

如果你在 VS Code 中使用 Lean，创建新 Lean 项目
最简单的方法是点击由 Lean 扩展提供的 `∀` 符号，
然后选择 “New Project”。

或者，你也可以在命令行中创建新的 Lean 项目。命令
```lean 
lake new my_project math
```
会创建一个名为 `my_project` 的新项目，并依赖于
Lean 的数学库。

## 仓库能否编译？证明是否正在被检查？

一个名为 `Foobar` 的项目的典型设置是：
它在项目的根目录下有一个 `Foobar.lean` 文件，
该文件导入项目中所有相关的
文件。如果你定理的实际证明
位于 `Foobar/MainResult.lean` 中，那么文件
`Foobar.lean` 中应该有一行写着
`import Foobar.MainResult`。在通常情况下，
`lake build` 随后就会构建 `Foobar/MainResult.lean`，
而该命令需要无错误地编译。

还有其他更高级的方式来设置仓库，
但如果你了解这些方式，那么你也会
非常清楚构建过程检查你的证明意味着什么。

## 证明是否只使用了数学的公理？

Lean 是一个灵活的软件。可以
用 `axiom` 命令向系统中添加新的公理（包括错误的公理），
或用 `sorry` 策略跳过证明。
此外还有其他滥用系统的方法。
归根结底，在执行 `#print axioms my_proof` 之后，
系统应当返回 `[propext, Classical.choice, Quot.sound]`
（或这些公理的某个子集）。用户自定义的公理，
或 `sorryAx`（表明某个证明被省略了）
都说明你的证明是不完整的。

## 你的工作是否证明了你所声称证明的内容？

这是一个重要的问题，而且比看上去更为复杂。

* 用户有可能混淆一个结果的*陈述*
和它的*证明*。在 Lean 中很容易定义并命名
`2+2=5` 这一*陈述*；但这并不构成
对 `2+2=5` 的*证明*！

* 把一个看起来很复杂的陈述定义并命名为
`TheRiemannHypothesis` 是非常容易的，而它尽管
名字如此，实际上却并不是黎曼猜想的陈述。
因此，对该陈述的证明当然也不是
对真正的黎曼猜想的证明。

* Lean 的语法极其灵活。可以
覆盖 Lean 对自然数或其上基本运算的
标准定义，然后声称你
证明了一个*看起来*像费马大定理的陈述，
但它其实根本不是。

Lean 的数学库
`Mathlib` 提供了若干著名数学
定理和猜想的陈述，例如[费马大定理](https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Basic.html#FermatLastTheorem)
和[黎曼猜想](https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/LSeries/RiemannZeta.html#RiemannHypothesis)。
这些陈述都已经过 Mathlib 维护者团队的检查，
确认它们是相应数学陈述在 Lean 语言中的
正确翻译。

如果你声称
证明了一条 `Mathlib` 中尚未陈述的定理，那么
验证过程中必不可少的一部分就是要有一位 Lean
专家能够确认：你所证明内容的*陈述*
确实对应于你所提出的数学论断，
并且你在陈述该命题的同时也确实*证明*了它。
