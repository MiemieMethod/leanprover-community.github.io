# 学习 Lean 4

学习 Lean 有许多途径，具体取决于你的背景和
偏好。它们都既有趣又有收获，但同样也颇有难度，
偶尔还会令人沮丧。证明助手目前仍然不易上手，
你不能指望通过一个下午的
学习就变得熟练。

本页列出的所有资源都关于 Lean 4。
其中有些有 Lean 3 版本，但现阶段已没有必要学习 Lean 3。

## 动手实践

* 无论你的背景如何，如果你想立刻上手，可以来玩
  [Natural Number Game](https://adam.math.hhu.de/#/g/hhu-adam/NNG4)。
  这是一个在线交互式 Lean 教程，
  专注于证明自然数上基本运算的各种性质。
  [Lean Game Server](https://adam.math.hhu.de/#/) 托管了多种学习游戏，包括
  集合论、逻辑以及 Robo（一个关于本科数学的故事）。

* 若想更快节奏地入门，你可以获取
  [Glimpse of Lean 教程](https://github.com/PatrickMassot/GlimpseOfLean)。
  它包含四个基础文件，涵盖使用 Lean 进行证明的一些
  基本方面，随后是关于初等分析、
  抽象拓扑和数理逻辑的若干独立专题文件。

* 你可以下载 [策略速查表（PDF）](https://leanprover-community.github.io/papers/lean-tactics.pdf)，作为最常用策略的参考。

* 如果你希望直接从源代码学习，
  [Lean API 文档](https://leanprover-community.github.io/mathlib4_docs/)
  不仅包含 `Mathlib`，还涵盖 `Std`、`Batteries`、`Lake` 以及核心编译器。
  由于 Lean 的许多部分都是以语法扩展的形式定义的，这是现存最接近
  完整参考手册的资料。
  
* 如果你想亲自动手并为 mathlib 做贡献，但不知道有什么合适的项目可以
  入手，那么在 [GitHub Issues](https://github.com/leanprover-community/mathlib4/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20label%3A%22good%20first%20issue%22) 上有一长串容易上手的 issue。
  如果你正在处理某个 issue，请在该 GitHub issue 下回复，说明你正在
  处理它，以尽量减少重复劳动。

## 书籍

如果你更喜欢阅读书籍（带练习），有许多免费可得的 Lean 书籍
已被证明对初学者很有帮助。
它们以 HTML 或 PDF 形式提供，但通常意在 VSCode 中交互式阅读，
随读随做 Lean 练习：

* 面向数学的标准参考是
  [Mathematics in Lean](https://leanprover-community.github.io/mathematics_in_lean/)。
  你可以[将其下载为 PDF](https://leanprover-community.github.io/mathematics_in_lean/mathematics_in_lean.pdf)，
  但也请参阅
  [VSCode 使用说明](https://leanprover-community.github.io/mathematics_in_lean/C01_Introduction.html#getting-started)。

* [The Mechanics of Proof](https://hrmacbeth.github.io/math2001/) 同样面向数学。
  它的节奏比 *Mathematics in Lean* 更平缓，面向数学经验较少的
  读者。

* 如果你更偏好关于类型论基础的内容，标准参考是
  [Theorem Proving in Lean](https://lean-lang.org/theorem_proving_in_lean4/)。

* 一本面向计算机科学/编程的书籍是
  [The Hitchhiker's Guide to Logical Verification](https://raw.githubusercontent.com/blanchette/logical_verification_2023/main/hitchhikers_guide.pdf)。
  它也包含关于 Lean 类型论的有用信息，并配有一个带练习的 VSCode 项目。

如果你想要更专注于 Lean 本身而非如何使用 Lean 的内容，那么你
可以阅读[参考手册](https://lean-lang.org/doc/reference/latest/)（[旧版手册](https://lean-lang.org/lean4/doc/)）。

## （元）编程与策略编写

* 如果你对 Lean 作为一门编程语言感兴趣，那么你应该阅读
  [Functional programming in Lean](https://lean-lang.org/functional_programming_in_lean/)。
* 如果你特别想实现自定义策略，那么你可以从对初学者友好的
  [Tactic Programming Guide](https://github.com/mirefek/lean-tactic-programming-guide) 开始。
* 若要更深入地学习策略和元编程，我们推荐
  [Metaprogramming in Lean 4](https://github.com/arthurpaulino/lean4-metaprogramming-book)
  （至少在确认你已掌握 Functional programming in Lean 中关于单子的章节之后）。

## 关于基础的更多内容

如果你对 Lean 的基础感兴趣，可以先阅读
[这里](https://leanprover-community.github.io/lean-perfectoid-spaces/type_theory.html)
一份非常粗略的概述。
如果你想要更多细节，可以阅读 Rijke 的 [Introduction to Homotopy Type Theory](https://arxiv.org/pdf/2212.11082) 的第一部分，或
[HoTT book](https://homotopytypetheory.org/book/) 的第一章，并忽略
其中任何提到一价性（univalence）的内容。

如果你对 Lean 内核的具体细节感兴趣，想为 Lean 编写自己的外部类型检查器，或导出证明，你可以在 [Type Checking in Lean 4](https://ammkrn.github.io/type_checking_in_lean4/) 中阅读更多内容。

另一个可能有用的资源是
Coq 文档中的[这个页面](https://coq.github.io/doc/master/refman/language/cic.html)。
Coq 的基础与 Lean 的基础极为接近。
需要牢记的最相关的差异是：
* Lean 的 `Prop` 是证明无关的（proof-irrelevant），因此它更接近于上述页面中的
  `SProp`。
* Lean 中的宇宙*不是*累积的（cumulative）。然而，任何类型都可以被提升
  到更高的宇宙。
* Lean 原生支持商类型及其相关的约简
  规则（参见 *Theorem proving in Lean* 的[这一
  节](https://lean-lang.org/theorem_proving_in_lean4/axioms_and_computation.html#quotients)）。

如果你能读懂上述 Coq 文档，那么你就已经准备好阅读
Mario Carneiro 的[这篇论文](https://github.com/digama0/lean-type-theory/releases)，
它精确地描述了 Lean 的类型论。

请注意，理解类型论基础对于使用 Lean 而言完全不是必需的。

## 聚会

许多聚会曾帮助欢迎新人加入 Lean 社区。
以下这些附有在线讲座的链接及其他可能感兴趣的材料。
请注意，2022 年以前的所有项目都使用 Lean 3，但它们可能仍包含相关信息。
* [Lean for the Curious Mathematician 2023](https://lftcm2023.github.io/tutorial/index.html)
* [Formalization of mathematics 2023](https://www.msri.org/summer_schools/1021)
* [Lean for the Curious Mathematician 2022](https://icerm.brown.edu/topical_workshops/tw-22-lean/)
* [Lean for the Curious Mathematician 2020](https://leanprover-community.github.io/lftcm2020/)

更多活动可在[活动](events.html)页面找到。
我们还有一个 [YouTube 频道](https://www.youtube.com/channel/UCWe5B7Ikr0AI9727doEUxPg/playlists)，
其中包含来自上述会议的视频播放列表，以及其他包含 Lean 相关内容的会议。
