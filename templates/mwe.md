# 最小工作示例

## 摘要

在 Zulip 上发布代码时，请包含所有的 `import`、`open`、`universe` 和 `variable`，这样他人只需复制粘贴你发布的内容，就能看到与你相同的问题。

确保你做到这一点的最佳方式，是把你打算发布的代码片段复制粘贴到一个空的 Lean 文件中，或粘贴到 [lean web 编辑器](https://live.lean-lang.org/)中，并检查它能否编译通过。

## 示例

### 不好的示例：

```lean
#check (univ : Set X)
```

### 好的示例：

```lean
import Mathlib

universe u

variable (X : Type u)

open Set

#check (univ : Set X)
```

### 不好的示例：

```text
Goal state:
/-
a b : blah,
h : a.fst < b.fst,
h2 : a.fst < b.snd
⊢ false
-/
```

### 好的示例：

```lean
def blah : Type := Nat × Nat

example (a b : blah) (h : a.fst < b.fst) (h2 : a.fst < b.snd) : False := by
  /-
  a b : blah,
  h : a.fst < b.fst,
  h2 : a.fst < b.snd
  ⊢ False
  -/
  done
```

提示：如果你正在使用 [mathlib](https://github.com/leanprover-community/mathlib4)（例如使用 `import Mathlib`），有一个名为 [`extract_goal`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/ExtractGoal.html) 的策略，可以帮助你把当前目标格式化为一个独立的示例。你可以从 `extract_goal` 的输出中移除多余的变量和假设，以进一步精简你的示例。

注意，你仍然需要按上文所述包含相应的 `import`、`open`、`universe` 和 `variable`。

## 形式化定义

**最小工作示例**是一段代码片段，它可以被复制粘贴到一个空的 Lean 文件中，并仍然保持相同的特性（工作），且不包含不必要的细节（最小）。

[这里](https://stackoverflow.com/help/minimal-reproducible-example)是 StackOverflow 关于制作 MWE 的指南。

请确保你的代码片段具备：

- 正确的 imports；以及
- 所有相关的定义 / 定理。

你的示例抛出编译器错误或警告是没有问题的。特别地，你的代码包含关键字 `sorry` 也是没有问题的（事实上，用 `sorry` 替换无关的证明是精简示例的一种好方法）。MWE 的要点在于，你的代码*在空白文件中应当抛出与你看到的相同的错误*，这样人们才能针对你困惑的那个确切错误来帮助你。

## 我如何知道我的代码是不是 MWE？

你应当通过把代码片段复制粘贴到一个新的 Lean 文件中，或粘贴到 [lean web 编辑器](https://live.lean-lang.org/)中，看看是否得到预期的行为，来*测试*这一点。这正是那些试图帮助你的人会做的事！

## 如果我问的是关于[自然数游戏（Natural Number Game）](https://adam.math.hhu.de/#/g/hhu-adam/NNG4)之类游戏的问题怎么办？

如果你的示例来自自然数游戏或任何此类基于浏览器的 Lean 演示，那么你可以添加一个指向该网页的链接，而不必去寻找正确的 imports。例如，说“我正处于自然数游戏的[这个关卡](https://adam.math.hhu.de/#/g/leanprover-community/nng4/world/Addition/level/2)，我的证明脚本是 _某某_”，会比说“我正处于自然数游戏的 Addition World 第 2 关，我的证明脚本是 _某某_”有用得多。

如果你在 Zulip 上发布代码片段，请确保它被三重反引号包围。

````text
```
def myNat : Nat := 5
```
````

## 精简代码的技巧
- 在 MWE 中，简单的 `import Mathlib` 是一个完全合适的 import。
- 出于制作 MWE 的目的，你可以把所有 `theorem` 和 `lemma`（你正在处理的那个之外）的证明替换为 `sorry`。Lean 会给你一些额外的警告，但这些警告是无害的。

- 移除所有与你看到的问题无关的声明（`def`、`theorem`、`lemma`、`example` 等）。一般来说，如果你能注释掉某段代码而不抛出错误，那么它就可以被移除。

- 删除一些代码之后，你接着可以删除所有仅在那里被引用的声明。通过重复这一过程几次，你或许能把一个很长的文件缩短到只有几行。
- 最后，你可以在代码中加入像 `-- HERE`、`-- TODO`、`-- ERROR: yada yada` 之类的注释，以将注意力引导到你 MWE 中的某个特定部分。

---

## Lean 的缺陷报告和功能请求

*本节面向为 Lean 本身提交缺陷报告或功能请求的资深用户。如果你是在 Zulip 上提问的初学者，上文的建议已经足够——你无需关心本节内容。*

在报告 Lean 中的意外行为时（无论是缺陷还是功能请求），让你的示例尽可能精确且可复现会很有帮助。有两种技术尤其有价值：`#guard_msgs` 和 `lean-minimizer` 项目。

### 使用 `#guard_msgs` 来捕获预期输出

`#guard_msgs` 命令让你能够将预期的编译器输出直接嵌入到代码中。这使你的示例毫不含糊：任何运行它的人都会立即看到他们能否复现该问题。

#### 基本用法

预期输出放在 `#guard_msgs` **之前的一个文档注释**中，并且必须完全匹配：

```lean
/-- info: Nat.add : Nat → Nat → Nat -/
#guard_msgs in
#check Nat.add
```

如果输出不匹配，`#guard_msgs` 会向你展示一个 diff：

```lean
-- This fails because #check Nat.mul produces different output
/-- info: Nat.add : Nat → Nat → Nat -/
#guard_msgs in
#check Nat.mul
```

`#guard_msgs` 提供了一个代码操作（code action），当文档注释与输出不匹配时，它会添加或更新该文档注释。（特别地，在设置时无需手动复制粘贴文本！）

#### 记录错误

```lean
/--
error: Application type mismatch: The argument
  true
has type
  Bool
but is expected to have type
  Nat
in the application
  Nat.succ true
---
info: sorry.succ : Nat
-/
#guard_msgs in
#check Nat.succ true
```

#### 使用 `drop` 来忽略消息类别

使用 `drop info` 或 `drop warning` 来忽略整类消息：

```lean
#guard_msgs (drop info) in
#check Nat.add
```

#### 使用 `substring` 进行部分匹配

当你只关心输出的一部分时，使用 `#guard_msgs (substring := true)`。文档注释只需包含出现在实际输出中某处的文本即可：

```lean
/-- Nat.add -/
#guard_msgs (substring := true) in
#check Nat.add
```


#### 记录超时

将 `set_option maxHeartbeats` 与 `#guard_msgs (substring := true)` 结合使用：

```lean
set_option maxHeartbeats 1 in
/-- maximum number of heartbeats (1) has been reached -/
#guard_msgs (substring := true) in
example : True := by trivial
```


#### 用 `pp.mvars` 稳定元变量名

错误消息中常常包含像 `?m.47` 这样的元变量名，它们在不同的运行之间会发生变化。使用 `set_option pp.mvars.anonymous false` 将它们替换为稳定的 `?_` 占位符：

```lean
set_option pp.mvars false in
/--
error: Type mismatch
  rfl
has type
  ?_ = ?_
but is expected to have type
  1 + 1 = 3
-/
#guard_msgs in
example : 1 + 1 = 3 := rfl
```


### 不依赖 Mathlib 的精简

对于提交给 Lean 仓库的缺陷报告，不依赖 Mathlib 的示例要可操作得多。一个不依赖 Mathlib 的示例：

- 使得二分查找哪个 Lean 提交引入了回归（regression）变得更容易
- 排除了缺陷在 Mathlib 而非 Lean 中的可能性
- 在开发者迭代修复时编译速度更快

当然，制作一个不依赖 Mathlib 的示例可能很繁琐。[**lean-minimizer**](https://github.com/kim-em/lean-minimizer) 可以帮助自动化这一过程。它的工作方式是反复尝试移除或简化你代码中的各个部分——包括内联和移除 imports——同时保留你试图演示的那个错误。这个过程可能需要一段时间，但其结果往往是一个极小的、自包含的示例，使缺陷一目了然。

对于依赖 Mathlib 的代码，[**mathlib-minimizer**](https://github.com/kim-em/mathlib-minimizer) 是一个便利项目，它把 lean-minimizer 与作为依赖的 Mathlib 捆绑在一起，因此你可以运行该精简器而无需自己设置依赖项。
