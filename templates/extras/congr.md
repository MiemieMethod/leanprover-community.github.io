# 如何使用 congr()

`congr()` 是一个项繁释器（term elaborator），它利用*同余性*（congruence）来构造关于相等、`HEq` 与 `Iff` 的证明。
最典型的同余引理称为 [`congr`](https://leanprover-community.github.io/mathlib4_docs/find/?pattern=congr#doc)，
它断言：当两个表达式（此处为两个函数应用）的各个组成部分相等（此处为函数本身及其参数）时，这两个表达式相等。
```lean
theorem congr {f₁ f₂ : α → β} {a₁ a₂ : α} (h₁ : f₁ = f₂) (h₂ : a₁ = a₂) : f₁ a₁ = f₂ a₂
```
同余引理使我们能够将多个相等证明串联起来，构成一个更大的证明。
与其手动地使用 `congr` 及其特化版本 [`congrFun`](https://leanprover-community.github.io/mathlib4_docs/find/?pattern=congrFun#doc) 和 [`congrArg`](https://leanprover-community.github.io/mathlib4_docs/find/?pattern=congrArg#doc) 来组合证明，
`congr()` 繁释器能以更少的语法噪声为你完成这一工作。

基本用法示例：

```lean
import Mathlib.Tactic.TermCongr

example (a b : Nat) (h : a = b) : 4 * (37 + a) = 4 * (37 + b) :=
  congr(4 * (37 + $h))
```

这里，传给 `congr()` 的表达式中，除了我们书写 `$h` 的位置之外，其余各部分都同时出现在等式的两侧。
语法 `$h` 的含义是：`congr()` 将 `h` 的左端 `a` 插入到所得等式的左侧，将 `h` 的右端 `b` 插入到所得等式的右侧。
`$h` 是[反引用](https://lean-lang.org/doc/reference/latest/Notations-and-Macros/Macros/#quasiquotation)（antiquotation）的一个例子。
在本文后面，我们将介绍 `congr()` 所使用的引用与反引用的完整语法。

`congr()` 支持 `Eq`、`Iff` 与 `HEq`，并能根据需要在它们之间相互转换：

```lean
example (a b : Nat) (h : a = b) : 4 * (37 + a) = 0 ↔ 4 * (37 + b) = 0 :=
  congr(4 * (37 + $h) = 0)

example (p q : Prop) [Decidable p] [Decidable q] (h : p ↔ q) :
    (if p then 1 else 0) = if q then 1 else 0 :=
  congr(if $h then 1 else 0)

example (a b : Nat) (h : a = b) [NeZero a] [NeZero b] : (37 : Fin a) ≍ (37 : Fin b) :=
  congr((37 : Fin $h))
```

## 语法

与其他繁释器和宏一样，括号总是紧贴 `congr()` 书写，中间不留空格。
`congr(...)` 与 `congr (...)` 含义不同：前者是我们正在讨论的项繁释器，而后者则是库中的 [`congr`](https://leanprover-community.github.io/mathlib4_docs/find/?pattern=congr#doc) 引理应用于参数 `(...)`。

括号内放置的是一个[*准引用*](https://lean-lang.org/doc/reference/latest/Notations-and-Macros/Macros/#quasiquotation)（quasiquoted）表达式。
除了普通表达式的语法之外，你还可以插入*反引用*，从而使其内容可以变化。
反引用有两种：

* `$ident`，如上面例子中的 `$h`，用于引用单个变量。
* `$(term)`，可以在项的位置插入一整个表达式。

每当 `congr()` 遇到一个反引用时，它就将该反引用的内容当作一个表达式来处理。
只要该表达式能够在当前上下文中被繁释，它可以任意复杂：

```lean
example (a b : Nat) (h : a = b) : 4 * (37 + a) = 4 * (37 + b) :=
  congr(4 * (37 + $h))

example (a b : Nat) (h : a = b) : 4 * (37 + a) = 4 * (37 + b) :=
  congr(4 * (37 + $(h)))

example (a b : Nat) (h : a = b) : 4 * (37 + a) = 4 * (37 + b) :=
  congr(4 * (37 + $(h.symm.symm)))

example (a b : Nat) (h : a = b) : 4 * (37 + a) = 4 * (37 + b) :=
  congr($(by rfl) * ($(by grind) + $(by simp [h])))
```

反引用内部的表达式可以引用局部变量，当你的证明尚未完全应用时这一点很有用：
```lean
example (f g : Nat → Nat) (h : ∀ i, f i = g i) (a : Nat) : f a = g a :=
  congr($(h a))

-- Make sure to apply the proof inside the antiquotation brackets.
-- The example below fails, because `h` is expected to be an equality of functions.
example (f g : Nat → Nat) (h : ∀ i, f i = g i) (a : Nat) : f a = g a :=
  congr($h a) -- Error: function expected.

-- The local variables can be bound inside the `congr` expression:
example (f g : Nat → Nat) (h : ∀ i, f i = g i) : (fun a => f a) = (fun a => g a) :=
  congr(fun a => $(h a))

-- Since `fun a => f a` is equal to `f`, this is a tricky proof of function extensionality:
example (f g : Nat → Nat) (h : ∀ i, f i = g i) : f = g :=
  congr(fun a => $(h a))
```

## 证明

根据期望类型的不同，`congr()` 将产生一个 `Eq`、`HEq` 或 `Iff`。
为简单起见，本节中我们假设 `congr()` 产生的是相等。
我们将 `congr(t)` 中的项 `t` 称为*模式*（pattern），将 `congr(t)` 的类型称为*结果*（result）。
若模式中不含反引用，则 `congr(t)` 等价于 `rfl : t = t`。
对于任何一个反引用，结果的左侧将包含该反引用类型的左端，
结果的右侧将包含该反引用类型的右端。

`congr()` 对模式进行两次处理：一次作为左侧，一次作为右侧。
被引用的表达式按常规方式繁释，直到 `congr()` 遇到一个反引用为止：
这些反引用首先在不带期望类型的情况下被繁释，
以便确定其左端与右端。
若此次繁释得到一个带有洞（hole）的类型，则这些洞会被推迟，留待之后通过与目标的合一（unification）来求解。

换言之，`congr()` 利用期望类型来填补模式中的洞：

```lean
example (a b : Nat) (h : a = b) : 1 + a = 1 + b := by
  have : 1 + _ = _ := congr(_ + $h)
  exact this
```

这意味着反引用可以按需推迟，例如仅在最后才调用 `assumption` 策略：
```lean
example (a b : Nat) (h : a = b) : 4 * (37 + a) = 4 * (37 + b) :=
  congr(4 * (37 + $(by assumption)))
```

但若缺少期望类型而反引用仍需被填补，则它会带着元变量（metavariable）运行，从而可能做出错误的猜测：
```lean
example (a b c : Nat) (h : a = b) (h2 : b = c) : 1 + a = 1 + b := by
  have : 1 + _ = _ := congr(_ + $(by assumption -- Goal: `?m.55 = ?m.56`, filled with `h2 : b = c`))
  exact this -- Error: `this` has type `1 + b = 1 + c`
```

当模式被繁释两次后，它会与期望类型进行合一，
以填补大多数剩余的洞。
最后，将左侧与右侧相互匹配，
并适当地插入同余引理或反引用内部的证明。
`congr()` 对 `Subsingleton` 与命题外延性有专门的支持，
使其能够处理依赖于诸如 `Decidable` 与 `Fintype` 等单元素类型类（subsingleton class）的函数。

根据上下文，`congr()` 能够在 `Eq`、`HEq` 或 `Iff` 的证明之间相互转换。
默认情况下，`congr()` 会产生一个 `Eq` 的证明。当期望类型有所暗示时，它会使用 `HEq` 或 `Iff`：
```lean
example (p q : Prop) [Decidable p] [Decidable q] (h : p ↔ q) : (if p then 1 else 0) = (if q then 1 else 0) := by
  have := congr($h)
  -- No expected type given above, so `this : p = q`.
  exact congr(if $this then 1 else 0)

example (p q : Prop) [Decidable p] [Decidable q] (h : p ↔ q) : (if p then 1 else 0) = (if q then 1 else 0) := by
  have : _ ↔ _ := congr($h)
  -- `Iff` expected above, so `this : p ↔ q`.
  exact congr(if $this then 1 else 0)
```

`congr()` 能够深入绑定子（binder）内部。如果你的相等尚未完全应用，请务必使用正确的语法将其应用于绑定子内部：

```lean
example (f g : Nat → Nat) (s t : Finset Nat) (hfg : ∀ i, f i = g i) (hst : s = t) :
    ∑ i ∈ s, f i = ∑ i ∈ t, g i :=
  congr(∑ i ∈ $hst, $(hfg i))

-- Equivalent to:
example (f g : Nat → Nat) (s t : Finset Nat) (hfg : f = g) (hst : s = t) :
    ∑ i ∈ s, f i = ∑ i ∈ t, g i :=
  congr(∑ i ∈ $hst, $hfg i)
```

## 相关功能

有许多类似 `congr()` 的工具可用于构造涉及相等的证明。

* [`congrm`](https://leanprover-community.github.io/mathlib4_docs/tactics.html#Mathlib.Tactic.congrM) 是 `congr()` 在策略模式下的等价物。除了 `congr()` 所支持的反引用之外，传给 `congrm` 的项还可以包含 `?_` 占位符，这些占位符将转化为新的证明目标。[`congrm?`](https://leanprover-community.github.io/mathlib4_docs/tactics.html#tacticCongrm?) 是一个交互式小部件（widget），通过点击子表达式将其转化为洞来生成 `congrm` 调用。
* [`congr`](https://leanprover-community.github.io/mathlib4_docs/tactics.html#Lean.Parser.Tactic.congr) 与 [`congr!`](https://leanprover-community.github.io/mathlib4_docs/tactics.html#Congr!.congr!) 策略利用同余规则来证明相等。`congr()` 繁释器从表达式各个小部分的证明出发，利用同余规则将它们组装成整个表达式的一个证明；而 `congr` 与 `congr!` 策略则反其道而行之，利用同余规则将整个表达式的相等目标拆解为若干小部分。`congr!` 比 `congr()` 更强大，因为它能够使用自定义的同余引理。
* 三角符号 `▸` 是一个用于在表达式类型内部进行重写的宏。若 `h : a = b` 且目标为 `4 * (37 + a) = 4 * (37 + b)`，则 `h ▸ _` 中的洞的期望类型为 `4 * (37 + a) = 4 * (37 + a)`。因此 `h ▸ rfl` 可以闭合这一目标，正如 `congr(4 * (37 + $h))` 一样。与 `congr()` 不同，三角符号是由外向内工作的：如果我们在没有期望类型的情况下写 `have := h ▸ rfl`，最终会得到一个假设 `this : a = b`。
* 诸如 `rw` 与 `simp` 之类的重写策略可以利用形如 `h : a = b` 的假设来证明形如 `4 * (37 + a) = 4 * (37 + b)` 的目标，办法是将等式两侧都重写为相同的形式，再用 `rfl` 闭合目标。与 `congr()` 不同，这些策略也是由外向内工作的：如果缺少目标类型，它们就会失败。`simp` 比 `congr()` 更强大，因为它使用了一个更强大的同余引理生成器。

## 局限性

`congr()` 无法处理所有可能的表达式：它只能组合你所传入的那些确切的相等。
下面的例子之所以成功，是因为通过处处使用 `h : a = b` 进行重写，`(37 : Fin a)` 可以被转化为 `(37 : Fin b)`：

```lean
example (a b : Nat) (h : a = b) [NeZero a] [NeZero b] : (37 : Fin a) ≍ (37 : Fin b) :=
  congr((37 : Fin $h))
```

另一方面，下面的例子会失败，因为通过使用 `h : x ≍ y` 进行重写，无法将 `(37 + _ : Fin a)` 转化为 `(37 + _ : Fin b)`。

```lean
example (a b : Nat) [NeZero a] [NeZero b] (x : Fin a) (y : Fin b) (h : x ≍ y) :
    37 + x ≍ 37 + y :=
  congr(37 + $h) -- Error: could not generate congruence between `a` and `b`.
```

我们需要自行构造 `a = b` 的证明，并将其插入到表达式中正确的位置，才能让 `congr()` 工作：

```lean
-- import Mathlib.Data.Fin.Embedding to make this work
example (a b : Nat) [NeZero a] [NeZero b] (x : Fin a) (y : Fin b) (h : x ≍ y) :
    37 + x ≍ 37 + y :=
  have hab : a = b := Fin.equiv_iff_eq.mp ⟨type_eq_of_heq h ▸ Equiv.refl _⟩
  congr(Add.add (α := Fin $hab) 37 $h)
```

## 缺陷

在极少数情况下，内部元数据或可化简（reducible）包装会从所生成的项中泄漏出来，暴露于合一过程之中。
用户看不到这些内容，但某些策略的模式匹配可能配置得过于严格，从而被它们绊倒。
如果你注意到某个策略在使用 `congr()` 之后无法应用，请在 Lean 社区的 Zulip 聊天上报告该问题。
