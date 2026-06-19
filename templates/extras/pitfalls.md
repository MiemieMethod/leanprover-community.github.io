# 常见的 Lean 陷阱

本文档列举了 Lean 用户经常犯的一些错误，以及 Lean 中可能导致错误的一些反直觉特性。

如果你在本文档中发现了错误，或者希望补充某些内容，请在 Zulip 上提出，或者在[本网站的代码仓库](https://github.com/leanprover-community/leanprover-community.github.io)中提交 issue 或拉取请求。

## 目录
- [自动隐式参数](#automatic-implicit-parameters)
- [忘记 Mathlib 缓存](#forgetting-the-mathlib-cache)
- [用 `have` 来表示数据](#using-have-for-data)
- [在绑定子下进行改写](#rewriting-under-binders)
- [指望策略展开定义](#trusting-tactics-to-unfold-definitions)
- [使用 `b > a` 而非 `a < b`](#using-b-gt-a-instead-of-a-lt-b)
- [混淆 `Prop` 与 `Bool`](#confusing-prop-and-bool)
- [未检查相异性](#not-checking-for-distinctness)
- [未考虑 0 的情形](#not-accounting-for-0)
- [除以 0](#division-by-0)
- [整数除法](#integer-division)
- [自然数减法](#natural-number-subtraction)
- [其他偏函数](#other-partial-functions)
- [`Fin` 中算术的回绕](#wrapping-arithmetic-in-fin)
- [实数幂](#real-power)
- [`Fin n → ℝ` 中的距离](#distance-in-fin-n--%E2%84%9D)
- [意外的双重 `iInf` 或 `iSup`](#accidental-double-iinf-or-isup)
- [试图从命题的证明中提取数据](#trying-to-extract-data-from-proofs-of-propositions)
- [处理类型的相等](#working-with-equality-of-types)
- [为已存在的实例引入参数](#parameters-for-instances-that-already-exist)
- [把 `Set` 当作类型使用](#using-sets-as-types)
- [Sort _](#sort-_)
- [试图证明关于 Float 的性质](#trying-to-prove-properties-about-float)
- [`native_decide`](#native_decide)
- [Panic 不会中止程序](#panic-does-not-abort)
- [Lean 3 代码](#lean-3-code)
- [非终结性 simp](#non-terminal-simp)
- [忽略警告](#ignoring-warnings)
- [易混淆的 Unicode 字符](#ambiguous-unicode-characters)
- [结构字段中的默认值](#default-values-in-structure-fields)

## 自动隐式参数

默认情况下，Lean 的[自动隐式参数](https://lean-lang.org/doc/reference/latest///Definitions/Headers-and-Signatures/#automatic-implicit-parameters)特性（简称 `autoImplicit`）会将未绑定的变量转换为隐式参数。例如，当启用该特性时，
```lean
theorem my_theorem : a + 1 = 1 + a := by omega
```
是
```lean
theorem my_theorem {a : Nat} : a + 1 = 1 + a := by omega
```
的简写。

这个特性可以使你的代码更加简洁，但它也意味着定理陈述中的任何笔误都可能使该定理陈述变得错误。
例如，下面的陈述
```lean
theorem my_theorem (n : Nat) (h : 1 ≤ n) : 0 < m := sorry
```
是错误的，因为 `m` 是一个自动隐式参数。
自动隐式特性使得人们很难察觉到本该输入 `n` 时却输入了 `m`。
在较新的 Lean 版本中，你应该能在文本编辑器中 `my_theorem` 旁边看到一个内联的 `{m}`，这表明 `m` 正充当一个自动隐式参数；留意这些标注是值得的，因为它们能帮助你发现无意中使用了 `autoImplicit` 的情况。

问题也可能以难以预料的方式表现出来。
例如，如果你尚未导入 `Mathlib.Data.Nat.Notation`，那么在
```lean
theorem my_theorem : ∃ (a b : ℕ), a ≠ b := sorry
```
中，`ℕ` 实际上是一个自动隐式变量，可以是任何类型，因此这个陈述实际上是错误的：
```lean
example : False := Exists.elim (my_theorem (ℕ := False)) (fun f _ ↦ f)
```

自动隐式参数默认在全局启用，但如果你在 Mathlib 上工作，它们会被禁用。
如果你是 Lean 新手，我建议你禁用它们，转而使用 `variable` 命令。
这可以通过在每个 Lean 文件顶部 `import` 语句之后添加
```lean
set_option autoImplicit false
```
来实现，或者在你的 `lakefile.toml` 或 `lakefile.lean` 中全局禁用它。

## 忘记 Mathlib 缓存

如果你正在 `Mathlib` 上工作，或者在一个依赖于 `Mathlib` 的项目上工作，那么首次打开一个依赖于 `Mathlib` 的文件，或者在终端中运行 `lake build`，可能需要一个多小时才能完成。
当 Lean 文件首次被编译时，Lean 会将编译结果缓存到 `.olean` 文件中，从而使后续运行更快。

在终端中运行 `lake exe cache get`，或者[在 VSCode 中调用 "Project: Fetch Mathlib Build Cache"](https://github.com/leanprover/vscode-lean4/blob/master/vscode-lean4/manual/manual.md#project-actions)，会从中央服务器下载 `Mathlib` 的 `.olean` 文件，从而使你无需自行编译它们，可以节省一个多小时的计算时间。
（如果 `lake exe cache get` 不起作用，你可能想试试 `lake exe cache get!`。）
如果你发现你的项目在 VSCode 中编译或启动花费了异常长的时间，可能是因为你忘记运行这个命令了。

请注意，解压后编译版本的 Mathlib 超过 5 GB，因此在下载缓存之前，请确保你有足够的存储空间，并且连接到了合适的网络（而不是例如有每月流量限制的手机热点）。

## 用 `have` 来表示数据

有时在证明中引入一个新变量来表示一个较为复杂的表达式会很方便。
例如，假设你有一个复杂的谓词 `MyPredicate`，并希望在证明中设 `x := 37 * n + 42 * m + 76`。
如果你用 `have` 来做这件事，然后证明 `h : MyPredicate x`，你会发现没有办法用 `h` 来完成目标。
```lean
example (n m : Nat) : MyPredicate (37 * n + 42 * m + 76) := by
  have x : Nat := 37 * n + 42 * m + 76
  have h : MyPredicate x := ...
  /- Tactic state is now:
  n m x : Nat
  h : MyPredicate x
  ⊢ MyPredicate (37 * n + 42 * m + 76)
  Now what? -/
```
此外，如果你的证明依赖于 `x` 的具体取值，你可能根本无法证明 `MyPredicate x`。

这里的问题在于，当你用 `have` 在证明中创建一个新变量时，Lean 会忘记你赋给 `have` 的值。
因此，在执行 `have x : Nat := 37 * n + 42 * m + 76` 之后，命题
`x = 37 * n + 42 * m + 76` 现在就无法证明了。

解决办法是，每当你引入一个并非证明的新变量时，使用 `let` 而非 `have`。
注意在下面的策略状态中，`x` 是如何附带一个值的。
```lean
example (n m : Nat) : MyPredicate (37 * n + 42 * m + 76) := by
  let x : Nat := 37 * n + 42 * m + 76
  have h : MyPredicate x := ...
  /- Tactic state is now:
  n m : Nat
  x : Nat := 37 * n + 42 * m + 76
  h : MyPredicate x
  ⊢ MyPredicate (37 * n + 42 * m + 76)
  -/
```
这意味着在证明的其余部分中，`x` 在定义上等于
`37 * n + 42 * m + 76`。
因此，`h` 的类型在定义上等于目标，所以我们可以用 `exact h` 完成证明，而无需进行任何手动转换。
如果你确实想要一个 `x = 37 * n + 42 * m + 76` 的证明，你可以用 `have hx : x = 37 * n + 42 * m + 76 := rfl` 来获得它，其中 `rfl` 之所以是这一事实的有效证明，正是由于定义上的相等。

你可能还会对 `set` 策略感兴趣，它类似于 `let`，但还会自动替换证明状态中该表达式的所有出现之处。

## 在绑定子下进行改写

人们有理由期望 `rw` 在下面的例子中把 `0 + i ^ 2` 改写为 `i ^ 2`，但不幸的是 `rw` 失败了：
```lean
import Mathlib.Algebra.BigOperators.Group.Finset.Defs

example (s : Finset Nat) : ∑ i ∈ s, (0 + i ^ 2) = ∑ i ∈ s, i ^ 2 := by
  rw [Nat.zero_add]
  /-
  tactic 'rewrite' failed, did not find instance of the pattern in the target expression
    0 + ?n
  s : Finset ℕ
  ⊢ ∑ i ∈ s, (0 + i ^ 2) = ∑ i ∈ s, i ^ 2
  -/
```
这是因为 `∑ i ∈ s, (0 + i ^ 2)` 是 `Finset.sum s (fun i ↦ 0 + i ^ 2)` 的简写，而 `rw` 有时无法在 `fun` 表达式内部进行改写，因为它无法改写像 `0 + i ^ 2` 这样含有绑定变量的子表达式。

在这种情况下，你可以使用 `simp_rw [Nat.zero_add]` 来执行改写，但在某些情况下，你可能需要使用[转换模式](https://leanprover.github.io/theorem_proving_in_lean4/The-Conversion-Tactic-Mode/)进行精确的改写：
```lean
example (s : Finset Nat) : ∑ i ∈ s, (0 + i ^ 2) = ∑ i ∈ s, i ^ 2 := by
  conv =>
    lhs
    congr
    · rfl
    · intro i
      rw [Nat.zero_add]
```

## 指望策略展开定义

Lean 中一个常见的错误是试图使用诸如 `rw` 和 `simp` 之类的策略，期望它们能“看穿” `def` 和 `let` 语句。
例如，在下面的例子中，你可能希望 `rw` 能意识到 `x` 只不过是 `0 + n` 的简写，并将其改写为 `n`，但这并不会发生：
```lean
theorem mythm (n : Nat) : True := by
  let x := 0 + n
  have : x = n := by
    rw [Nat.zero_add]
    /-
    tactic 'rewrite' failed, did not find instance of the pattern in the target expression
      0 + ?n
    n : Nat
    x : Nat := 0 + n
    ⊢ x = n
    -/
```
类似地，`simp` 在这里也会失败，并给出错误信息 “simp made no progress”。

这里的解决办法是，先 `unfold x` 或使用 `change 0 + n = n`，然后再调用 `rw [Nat.zero_add]` 或 `simp`。
你也可以用 `simp [x]` 代替 `simp`。
最后，如果 `x` 是一个 `def` 而非 `let`，你可以执行 `rw [x]`，这等价于 `rw [show x = 0 + n from rfl]`。
请注意，对 `x` 使用 `let` 而非 `have` 是很重要的；参见上文关于用 `have` 来表示数据的章节。

话虽如此，理解为什么这从一开始就是个问题是值得的。
回想一下，Lean 中主要有三种相等的概念：命题相等、定义相等和句法相等。
命题相等是传统数学中通常意义上的相等概念，Lean 中的命题 `a = b` 指的就是命题相等。
相比之下，定义相等和句法相等不是你能够证明或否证的东西；两个表达式要么在定义上相等，要么不相等，它们要么在句法上相等，要么不相等。

一种粗略的思考方式是：如果两个项在 Lean 中以相同的方式书写，那么它们就是句法相等的；如果对两个项调用 `#reduce` 会得到相同的表达式，那么它们就是定义相等的。
例如，当 `n` 是一个未知的自然数时：
- `n + 0` 与 `n + 0` 既句法相等，又定义相等，也命题相等。
- `n + 0` 与 `n` 定义相等且命题相等，但不句法相等。这是因为 `Nat.add` 是按第二个参数递归定义的，所以即便 Lean 不知道 `n` 是什么，它也能把 `n + 0` 归约为 `n`。
- `0 + n` 与 `n` 命题相等，但既不定义相等也不句法相等。这是因为当 `n` 未知时，Lean 不知道如何归约 `0 + n`，所以这个陈述必须用归纳法来证明。

更多信息，请参见 https://b-mehta.github.io/formalising-mathematics-notes/Part_1/equality.html

不幸的是，在 Lean 中，句法相等与定义相等之间的界限往往是模糊的。
需要记住的重要一点是，某些策略（例如 `exact`）在定义相等的意义下工作，而另一些策略（例如 `rw` 和 `simp`）则在句法相等的意义下工作。
尽管 Lean 的核心类型检查器只关心定义相等，但策略可以自由地利用关于项的句法的额外信息来辅助其运作。

## 使用 `b > a` 而非 `a < b`

大多数情况下，`a < b` 与 `b > a` 在 Lean 中是定义相等的。
但鉴于上面关于不要指望策略展开定义的讨论，即便两个项在定义上相等，它们仍然可能并非在所有情形下都可以互换。
例如，下面这个改写会失败，因为 `Nat.mod_eq_iff_lt` 的右端是 `m < n`，而非 `n > m`：
```lean
example {n m : Nat} (h₁ : m % n = m) (h₂ : n ≠ 0) : n > m := by
  rw [←Nat.mod_eq_iff_lt h₂]
```

在 Mathlib 中，`a < b` 优先于 `b > a`。
事实上，`>` 在 Mathlib 中几乎从不出现。
这意味着，如果你想避免一直使用 `gt_iff_lt`，你应该在代码中处处优先使用 `a < b` 而非 `b > a`。
类似地，你应该优先使用 `a ≤ b` 而非 `b ≥ a`。
除了像 `∀ ε > 0, ∃ δ > 0, _` 这样 `>` 与 `∀` 或 `∃` 相连的表达式之外，通常最好完全不使用 `>` 或 `≥`。

## 混淆 `Prop` 与 `Bool`

类型 `Prop` 和 `Bool` 都刻画了某物为真或为假的概念，
但它们在 Lean 中的行为大相径庭。
`Prop` 是*命题*的全集，命题是具有真值的数学陈述，
而 `Bool` 是*布尔值*的类型；它恰好由两个元素 `true` 和 `false` 组成。
请注意，`True` 和 `False` 是*命题*，而 `true` 和 `false` 是*布尔值*。

在期望命题的地方使用布尔值，或反之，可能导致一些反直觉的错误。此外，由于布尔值可以被隐式强制转换为命题，由此产生的问题可能并不会立即显现。
例如，`a = b` 是一个命题，而 `a == b` 是一个布尔值（参见 `BEq` 类型类），混淆它们会引发问题。
确保你充分掌握了 `Prop` 与 `Bool` 之间的区别是值得的。

在 Lean 中，`Prop` 和 `Bool` 都是类型，但 `Prop` 同时也是一个全集，而 `Bool` 只是一个包含两个元素的普通类型。
这意味着，如果 `p : Prop` 且 `q : Bool`，那么 `h : p` 可能是合法的，但 `h : q` 永远不合法。
另一方面，你可以在 `match` 语句中使用 `Bool` 类型的项，但你不能对 `Prop` 类型的项进行 `match`（在 `Prop` 上的等价操作是 `by_cases hp : p` 策略，或者“依值”的 if-then-else 语句 `if hp : p then ... else ...`）。
`Bool` 在数学中很少使用，但当 `Lean` 被用作编程语言时，它的使用要频繁得多。

直观地说，命题是一个可能被证明或被否证的数学陈述。
如果 `p` 是一个命题，那么说 `h : p` 是有意义的，它意味着 `h` 是 `p` 的一个证明。
另一方面，如果 `q` 是一个布尔值，那么 `q` 实实在在地等于 `true` 或 `false` 之一；“证明” `q` 是没有意义的，因为 `q` 是一个值，而非一个陈述。

如果你有一个布尔值 `q`，你可以通过写 `q = true` 将它转换为一个命题。
反之，如果 `p` 是一个命题，并且 Lean 能合成出 `Decidable p` 的一个实例，那么你可以通过写 `decide p` 将 `p` 转换为一个布尔值。
（这里，项 `decide` 不应与策略 `decide` 相混淆。）
由于公理 `Classical.choice` 可以为任意命题 `p` 产生一个 `Decidable p` 实例，因此任何命题都可以被转换为布尔值，从而 `Prop` 与 `Bool` 在*经典意义下是等价的*。

尽管如此，在 `Prop` 与 `Bool` 之间保持区分仍然是有意义的。
在 mathlib 中，`Prop` 与 `Bool` 在类型类上可能被赋予不同的实例；例如，`Prop` 被赋予 Sierpiński 空间（以 `{True}` 为开集）作为其拓扑，而 `Bool` 被赋予离散拓扑。

## 未检查相异性

考虑下面这个鸽笼原理的陈述，它说的是：如果 $f : A \to B$ 是有限集之间的一个函数且 $|A| > |B|$，那么在 $A$ 中存在两个相异的元素被 $f$ 映射到 $B$ 中同一个元素：
```lean
import Mathlib.Data.Fintype.Card

variable {A B : Type*} [Fintype A] [Fintype B]

theorem pigeonhole_principle (f : A → B) (h : Fintype.card B < Fintype.card A) : ∃ (x y : A), f x = f y := by
  let a : A := Classical.choice <| Fintype.card_pos_iff.mp (by omega)
  exact ⟨a, a, rfl⟩
```
如果你看一下这个证明，你会注意到它太过简单了。
注意，该定理的陈述忘记要求 `x` 与 `y` 相异，所以我们要做的只是证明存在某个元素 `a : α`，然后根据定义就有 `f(a) = f(a)`。
这并非 Lean 特有的问题，但在 Lean 中它比在非形式化数学中更容易在日后引发麻烦。

## 未考虑 0 的情形

考虑下面这个费马大定理的陈述：
```lean
theorem flt (a b c n : Nat) (h : 3 ≤ n) : a ^ n + b ^ n ≠ c ^ n := sorry
```
不幸的是，这个陈述是错误的：
```lean
example : False := flt 0 0 0 3 le_rfl rfl
```

记住，在 Lean 中，`0 : ℕ`，你应该在你的定理陈述中考虑到这一情形。
（这也是一个使用 Mathlib 定义本可以提供帮助的例子：
Mathlib 已经为费马大定理的陈述提供了一个定义 `FermatLastTheorem`，它包含错误的可能性要小得多。）

## 除以 0

在 Lean 中，`n / 0 = 0`。这与其他编程语言不同，在那些语言中除以零通常会导致异常。

这意味着像下面这样的陈述
```lean
import Mathlib.Data.Real.Basic

theorem my_theorem : ∃! (x : ℝ), x / (1 + x) = 0 := sorry
```
实际上是错误的，因为在 Lean 中，方程 `x / (1 + x) = 0` 在实数上有两个解：
```lean
example : False := by
  suffices h : (0 : ℝ) = -1 by aesop
  apply my_theorem.unique <;> simp
```

除法之所以这样表现，是因为 Lean 是一门纯函数式语言，所以所有函数都必须是全函数——函数不能抛出异常。
在 Lean 中，处理偏函数 $f : A \rightharpoonup B$ 的推荐方式是改为定义一个函数 $g : A \to B$，使得只要 $x \in \text{dom}(f)$，就有 $g(x) = f(x)$。
$g$ 在 $A \setminus \text{dom}(f)$ 上的取值是任意的，通常被选取为能给出最良好的代数性质的值（这些值常被称为“垃圾值”）。

也可以改为像这样定义除法
```lean
def div (a b : ℝ) (h : b ≠ 0) : ℝ := ...
```
但在实践中，每次想要对两个数做除法时都提供分母非零的证明会很快变得繁琐。
相比之下，涉及除法的*定理*通常会带有一个表明分母非零的假设。
建议你为自己的定理添加确保分母非零的假设，除非你已经仔细考虑过分母为零的情形。
更多信息，请参见[这篇 Xena 项目博文](https://xenaproject.wordpress.com/2020/07/05/division-by-zero-in-type-theory-a-faq/)。

## 整数除法

在 Lean 中对两个 `Int` 或 `Nat` 做除法时，结果总是向下取整（这与大多数语言略有不同，那些语言是向零取整的）。
这是为了使用除法不会导致所处理的数的类型发生改变。
例如，下面的陈述是错误的：
```lean
import Mathlib.Algebra.Field.Rat
import Mathlib.Algebra.Order.Ring.Rat

def thm₁ (n : ℤ) (h : 2 < n) : (1 / n) < (1 / 2) := by
  /-
  ===================
  Found a counter-example!
  n := 3
  guard: 2 < 3
  issue: 0 < 0 does not hold
  (0 shrinks)
  -------------------
  -/
  plausible
```

但与此同时，你可能并不想依赖这种行为。例如，下面这个定理实际上是成立的：
```lean
def thm₂ (n : ℚ) (h : 2 < n) : (1 / n) < (1 / 2) := by
  simp [inv_strictAnti₀ rfl h]
```
在这个例子中，`<` 的左端是一个有理数，所以 Lean 将右端也解释为有理数，于是整数除法就不再适用了。
这与下面发生的情况类似：
```lean
#eval (1 / 2) + 0 -- 0
#eval (1 / 2) + (0 : ℚ) -- (1 : Rat)/2
```

如果你习惯了像 Java 这样的语言，你可能会对此感到惊讶——在 Java 中 `(1 / 2) + 0.0` 求值为 `0.0`，因为在 Java 中括号外的类型信息通常不会影响括号内的运算。

一般来说，判断整数除法是否存在是很困难的。
此外，Lean 在最近这个例子中的行为在未来也有可能改变。

如果你对此有所顾虑，你可能想考虑在文件顶部附近添加 `set_option pp.numericTypes true`，这样数值字面量在 infoview 中显示时就会被标注上其相应的类型（例如 `ℕ`、`ℤ`、`ℚ`、`ℝ`、`ℂ`）。

## 自然数减法

自然数的减法在 `0` 处截断，因为我们希望自然数减法的返回类型是 `Nat`。也就是说，我们有
```lean
#eval 5 - 3 -- 2
#eval 5 - 7 -- 0
#eval 10 - 100 + 100 -- 100
#eval 5 - 13 + 11 + 0 -- 11
```
正如上面整数除法一节中所解释的，类型标注会影响所执行的运算：
```lean
#eval 10 - 100 + (100 : Int) -- 10
#eval 5 - 13 + 11 + (-0) -- 3
```

截断减法也被称为 [monus](https://en.wikipedia.org/wiki/Monus)。

自然数减法可能出现的一个场合是：如果你有一个谓词 `P : Nat → Prop`，并想证明对所有 `n ≥ 1` 都有 `P n` 成立。
如果你试图证明
```lean
theorem mythm {n : Nat} (hn : 1 ≤ n) : P n := ...
```
你可能会发现 `mythm` 的证明需要你频繁地用到 `n - 1`。
尽管这里并未发生截断，但这个陈述证明起来仍可能很繁琐，因为自动化往往不能很好地处理自然数减法。
在许多情况下，改为证明
```lean
theorem mythm (n : Nat) : P (n + 1) := ...
```
是更明智的，因为这完全避免了自然数减法。
更一般地，你常常可以把一个涉及自然数减法的陈述重述为一个不涉及它的陈述。
此外，在很多情况下，`mythm` 的后一种表述比前一种表述更易于使用。

## 其他偏函数

你还应该意识到，Mathlib 中许多其他函数也使用了垃圾值。
例如，
- 当 `f` 在 `s` 内于 `x` 处不可微时，`deriv f s x = 0`。
类似地，当 `f` 在给定点处不可微时，Fréchet 导数 `fderiv` 返回零线性映射。
你可能需要在定理的假设中加入 `HasDerivAt` 或 `HasFDerivAt`。
- “拓扑和” `tsum f`，也记作 `∑' i, f i`，计算一个级数的和，或者在该和不收敛时返回 0。
考虑为涉及 `∑' i, f i` 的定理加入 `Summable f` 假设。
  - 注意，由于 `tsum` 不假设定义域上有序结构，只有无条件收敛的级数才被视为 `Summable`。
  直观地说，如果级数求和的次序无关紧要，那么它就是无条件收敛的。
  例如，交错调和级数*不是* `Summable` 的，因为它只是条件收敛的。
  （由 [Riemann 级数定理](https://en.wikipedia.org/wiki/Riemann_series_theorem)可知，一个实值级数*无条件收敛*当且仅当它*绝对收敛*。
  一般而言，无条件收敛比绝对收敛更弱：如果 $(e_n)_{n \in \mathbb{N}}$ 是一个可数无穷维 Hilbert 空间的一组标准正交基，那么 $\sum (e_n)/n$ 无条件收敛，但不绝对收敛。）
- `tprod f`（记作 `∏' i, f i`）与 `tsum` 类似，但其垃圾值是 `1` 而非 `0`。
- `Nat.sqrt x` 取 $\sqrt{x}$ 的下取整。
- `Real.sqrt x` 对负数输入返回 `0`。
- `Real.log x` 在 $x \ne 0$ 时实际上表示 $\log_e |x|$，并在 $x = 0$ 时为 $0$。
这比将其对所有负的 $x$ 都设为 $0$ 给出了更好的代数性质。
- 当集合为空或无上界时，`Real.sSup` 和 `Real.iSup` 为 0；同样地，当集合为空或无下界时，`Real.sInf` 和 `Real.iInf` 为 0。
这与 `Real.sqrt` 配合得很好：它意味着对所有 $x \in \mathbb{R}$ 都有 $\sqrt{x} = \sup \{y \mid y^2 < x\}$，因为当 $x \le 0$ 时两端都为 $0$。

## `Fin` 中算术的回绕

`Fin` 中的算术在上溢或下溢时会回绕：
```lean
#eval (7 : Fin 10) + 6 -- 3
#eval (7 : Fin 10) * 6 -- 2
#eval (2 : Fin 10) - 8 -- 4
```
这对字面量也适用：
```lean
#eval (15 : Fin 10) -- 5
#eval (10 : Fin 10) -- 0
```
请注意，尽管对于正的 `n`，`Fin n` 使用与 `ZMod n` 相同的加法、减法和乘法概念，但它们并不完全相同，因为 `Fin n` 是有序的而 `ZMod n` 是无序的，并且 `Fin n` 使用截断的整数除法，而 `ZMod n` 在 $n$ 为素数时使用 $\mathbb{Z}/n\mathbb{Z}$ 上“数学上正确”的除法概念。
此外，`Fin 0` 是空的，而 `ZMod 0 = Int`（这是为了使 `ZMod n` 始终是一个特征为 `n` 的环，因为空类型不能成为环）。

`Fin` 之所以使用回绕算术而非诸如饱和算术之类的东西，原因之一是它被用来表示像 `UInt32` 这样的原生定宽整数类型，而 `Fin` 上的运算需要与机器原生算术的上溢和下溢相一致。

## 实数幂

`Real.rpow x y` 对负的 `x` 的定义有些任意。
具体来说，它被定义为复指数函数的实部，而复指数函数本身也有些任意，因为它依赖于复对数。
这赋予了该函数良好的解析性质，但也意味着对负数取根会有些反直觉。
例如，`(-125 : ℝ) ^ (1/3 : ℝ)` 的值是 $5\cos(\pi/3)$，而非你可能预期的 $-5$。

## `Fin n → ℝ` 中的距离

在许多情况下，`Fin n → ℝ` 是在 Lean 中表示 $\mathbb{R}^n$ 的推荐方式。
这种类型的向量可以用 `![x,y,z,...]` 记法书写。
但请注意，在 Lean 中，如果 $(S_i)_{i \in I}$ 是一族有限多个（伪）度量空间，那么 $\prod_{i \in I}S_i$ 使用 $L^\infty$ 度量：
$$
\text{dist}(\textbf{x},\textbf{y}) = \sup\left\{ \text{dist}(x_i,y_i) \mid i \in I\right\}
$$
而 `Fin n → ℝ` 是这种情形的一个特例。

这意味着 $(1,0)$ 与 $(0,1)$ 之间的距离实际上是 $1$：
```lean
import Mathlib.Analysis.InnerProductSpace.PiL2

example : dist ![(1 : ℝ),0] ![0,1] = 1 := by
  rw [dist_pi_eq_iff (by positivity)]
  constructor
  · use 0
    simp
  · intro b
    fin_cases b <;> simp
```

要改用标准的欧几里得度量（也称为 $L^2$ 度量），你必须使用 `EuclideanSpace ℝ (Fin n)`，它是 `WithLp 2 (Fin n → ℝ)` 的缩写。这种类型的向量可以用 `!₂[x,y,z,...]` 记法书写。
```lean
example : dist !₂[(1 : ℝ),0] !₂[0,1] = √2 := by
  norm_num [EuclideanSpace.dist_eq]
```

这样做的一个后果是，`Fin n → ℝ` 并未被注册为内积空间，因为与该内积相对应的范数会与已有的 $L^\infty$ 范数相冲突。
如果你需要把 $\mathbb{R}^n$ 作为内积空间，请使用 `EuclideanSpace ℝ (Fin n)`。

## 意外的双重 `iInf` 或 `iSup`

你可能期望 `⨅ x > 2, (x : ℝ) ^ 2` 等于 `4`，因为 `(2,∞)` 在 `fun x : ℝ ↦ x ^ 2` 下的像是 `(4,∞)`。但在 Lean 中，这个表达式实际上等于 `0`：

```lean
import Mathlib.Data.Real.Archimedean
import Mathlib.Order.ConditionallyCompleteLattice.Indexed

-- The infimum of x^2 on (2,∞) is ... 0?
example : ⨅ x > 2, (x : ℝ) ^ 2 = 0 := by
  set f := fun x : ℝ ↦ ⨅ (h : x > 2), x ^ 2
  have hf₁ (x : ℝ) : f x = if _ : x > 2 then x ^ 2 else sInf ∅ := ciInf_eq_ite
  have hf₂ : f 0 = 0 := by simp [hf₁]
  have hf₃ (x : ℝ) : 0 ≤ f x := by
    rw [hf₁]
    split_ifs <;> simp [sq_nonneg]
  apply le_antisymm
  · rw [←hf₂]
    refine ciInf_le ?_ 0
    rw [bddBelow_iff_exists_le 0]
    use 0
    simp [hf₃]
  · simp [le_ciInf, hf₃]
```

其原因在于，`⨅ x > 2, (x : ℝ) ^ 2` 是 `⨅ (x : ℝ) (h : x > 2), x ^ 2` 的简写，而后者又是 `⨅ (x : ℝ), ⨅ (h : x > 2), x ^ 2` 的简写。
注意：
- 当 `x > 2` 时，`⨅ (h : x > 2), x ^ 2` 表示 `⨅ (h : True), x ^ 2`，它等于 `x ^ 2`。
- 当 `x ≤ 2` 时，`⨅ (h : x > 2), x ^ 2` 表示 `⨅ (h : False), x ^ 2`，它等于
`sInf (∅ : Set ℝ)`。
在传统数学中，实数上的 $\inf \varnothing$ 通常是无定义的，或者被定义为等于 $+\infty$。但在 Lean 中，`sInf (∅ : Set ℝ) = 0`（解释参见上面关于偏函数的章节）。

所以，总结来说，`⨅ x > 2, (x : ℝ) ^ 2` 等于 `⨅ (x : ℝ), f x`，其中
$$
f(x) = \begin{cases} x^2 &\text{ for } x > 2 \\ 0 &\text{ for } x \le 2 \end{cases}
$$
而这个函数的下确界是 `0`。

集合也会出现类似的情况。`⨅ x ∈ s, f x` 是 `⨅ x, ⨅ (_ : x ∈ s), f x` 的简写，它可能与 `⨅ x : ↑s, f ↑x`（其中索引类型是被强制转换为类型的 `s`）不同。
此外，本节中的一切对 `iSup` 的适用程度与对 `iInf` 的一样。

`⨅` 和 `⨆` 之所以这样表现，是为了与诸如 `∀` 和 `∃` 之类的其他绑定子保持一致：
`∀ x ∈ s, p x` 是 `∀ x, ∀ h : x ∈ s, p x` 的简写，`∃ x ∈ s, p x` 是 `∃ x, ∃ h : x ∈ s, p x` 的简写。
然而，关于未来是否可能改变这种行为，已经有过一些讨论：参见 [Zulip 上的这则讨论](https://leanprover.zulipchat.com/#narrow/channel/287929-mathlib4/topic/sup.20and.20inf.20over.20sets/with/472565284)。

## 试图从命题的证明中提取数据

给定一个证明 `h : ∃ n : Nat, p n`，你可能希望提取出使得 `p n` 成立的那个特定的 `n`。
或者给定一个项 `q : Nonempty Nat`，你可能希望获得用于构造 `q` 的那个特定的 `Nat`。
在上述每种情况下，从 `h` 或 `q` 中提取一个*任意的* `n : Nat` 都是可能的，但获得 `h` 或 `p` 的构造中所用的那个*特定的* `n` 则是不可能的。

要理解其原因，首先回想一下 Lean 有一个单一的全集层级 `Sort 0`、`Sort 1`、`Sort 2`、`Sort 3`、……，
并且 `Prop` 是 `Sort 0` 的简写，`Type` 是 `Sort 1` 的简写，`Type 1` 是 `Sort 2` 的简写，如此等等。
之所以要区分 `Prop` 和 `Type u`，是因为 `Prop` 具有一些特殊行为，有时需要我们把它与其余的全集区别对待。
`Prop` 最重要的两个特殊性质是*非直谓性*和*证明无关性*。
在本节中，我将主要讨论证明无关性的后果。

本质上，证明无关性表明每个命题至多有一个证明；也就是说，同一命题的任意两个证明都相等。
另一种表述方式是，每个命题都是一个*子单元集*——一个具有零个或一个元素的类型。
证明无关性在 Lean 中的实现方式是：如果 `P : Prop` 且 `p : P` 且 `q : P`，那么 `p` 与 `q` 在定义上相等，因此 `rfl : p = q`。
这是 Lean 类型论中的一条内置规则，不应与 `propext` 相混淆，后者是一条公理，表明如果 `P Q : Prop` 且 `P ↔ Q`，那么 `P = Q`。

要明白为什么需要这条规则，回想一下子类型 `{x : X // p x}` 的一个元素形如 `{ val := x, property := h }`，其中 `x` 是 `X` 的一个元素，`h` 是 `p x` 的一个证明。如果我们定义
```lean
def x : {n : Nat // 4 < n} := { val := 8, property := Nat.lt_of_sub_eq_succ rfl }
def y : {n : Nat // 4 < n} := { val := 8, property := by omega }
```
那么 `x` 与 `y` 具有相同的值，但具有不同的证明。
我们希望 `x` 与 `y` 尽管证明不同却仍然相等，而且如果它们甚至定义相等的话就非常方便了，正是证明无关性使这成为可能：
```lean
example : x = y := rfl
```

由于证明无关性，当一个证明 `h : ∃ n : Nat, p n` 被构造出来时，它“遗忘”了用来证明它的是哪个 `n`。
如果存在某个函数 `f : (∃ n : Nat, p n) → Nat` 能提取出 `h` 的构造中所用的自然数，那么我们就可以构造两个不同的证明 `h₁ h₂ : ∃ n : Nat, p n`，使得 `f h₁ ≠ f h₂`，但由证明无关性又有 `h₁ = h₂`。
这会产生矛盾，所以不存在这样的 `f`。

更一般地，当你定义一个属于 `Prop` 的归纳类型 `T` 时，`T.rec` 的返回类型只被允许属于 `Prop`。
实际上，这意味着虽然函数
```lean
def swap {P Q : Prop} (h : P ∨ Q) : Q ∨ P :=
  match h with
  | Or.inl hp => Or.inr hp
  | Or.inr hq => Or.inl hq
```
是被允许的，因为该 match 表达式的返回类型属于 `Prop`，但函数
```lean
def bad {P Q : Prop} (h : P ∨ Q) : Nat :=
  match h with
  | Or.inl hp => 1
  | Or.inr hq => 2
```
则是不被允许的，因为该 match 表达式的返回类型属于 `Type`。
请注意，某些归纳命题——称为*句法子单元集*——通过一种称为*子单元集消去*的机制而豁免于这一限制。

如果你确实必须从命题中提取数据，有几种方法可供选择：
- 如果你是在某个命题的证明过程中提取数据（而不是在一个属于 `Type` 或更高层级的 `def` 中），那么诸如 `cases` 和 `obtain` 之类的策略会像往常一样工作。你也可以应用诸如 `Exists.elim` 和 `Nonempty.elim` 之类的消去子，它们只允许你消去到命题。
- 如果你只是需要从一个证明 `h : Nonempty α` 中提取一个*任意的* `α`，你可以使用公理 `Classical.choice` 来做到这一点。请注意，除了 `Classical.choice` 的输出属于 `α` 这一事实之外，关于该输出无法证明任何性质。例如，如果你对一个证明 `h : Nonempty Nat` 使用 `Classical.choice` 以产生一个元素 `n : Nat`，那么诸如 `n = 37` 之类的陈述在 Lean 中既不可证也不可否。
此外，如果你编写的代码的行为依赖于 `n` 的值，那么你将被迫把这样的代码标记为 `noncomputable`。
- 如果你拥有的是一个元素 `h : ∃ n : Nat, p n`，那么你可以使用 `Classical.choose` 来获得一个元素 `n : Nat`，并使用 `Classical.choose_spec` 来获得 `p n` 的一个证明。
`Classical.choose` 和 `Classical.choose_spec` 在内部是通过使用 `Classical.choice` 产生 `{n : Nat // p n}` 的一个元素来定义的，所以关于可计算性的相同限制也适用。
- 如果你需要依赖于 `∃ n : Nat, p n` 的证明中所用的那个*特定的*值，你或许应该完全避免使用 `Exists` 类型，而是给出 `{n : Nat // p n}` 的一个元素。
`∃ n : Nat, p n` 与 `{n : Nat // p n}` 都由一个 `n : Nat` 和一个 `p n` 的证明组成；它们唯一的区别在于该类型属于哪个全集。
- 如果你是在 `Nat` 上工作，并且你有一个 `h : ∃ n : Nat, p n`，其中 `p` 是一个 `DecidablePred`，那么你可以使用 `Nat.find` 和 `Nat.find_spec`，其用法类似于 `Classical.choose` 和 `Classical.choose_spec`。
`Nat.find` 是可计算的，尽管它可能并不特别高效，因为求值 `Nat.find h` 会从 0 开始按顺序检查每一个自然数，直到找到满足 `p` 的最小者。

## 处理类型的相等

类型的相等在 Lean 的类型论中表现得很糟糕。
如果 `A` 与 `B` 是 `Type u` 中两个不同的归纳类型或结构，并且 `A` 与 `B` 具有相同的基数，那么陈述 `A = B` 在 Lean 中既不可证也不可否。
例如，`Int = Nat` 既不可证也不可否。
更多信息，请阅读 Jason Rute 和 Andrej Bauer 对这个问题的回答：https://proofassistants.stackexchange.com/q/4046

粗略地说，你唯一能够证明两个类型相等的情形，是它们由相同的不可约类型定义而来。例如，当 `n = m` 时 `Fin n = Fin m` 是可证的，但 `Fin 2 = Bool` 则不可证。
你唯一能够证明两个类型*不*相等的情形，是它们具有不同的基数。所以，`Fin 3 ≠ Bool` 是可证的，但 `Fin 2 ≠ Bool` 则不可证。
例外是 `Prop`，对它而言，公理 `propext` 可以被理解为表明：如果两个 `Prop` 具有相同的基数，那么它们相等。

如果你*确实*能够证明 `A = B`，那么你可以使用 `cast` 把 `A` 的一个元素转换为 `B` 的一个元素。
但对 `cast` 的依赖往往会在日后引发问题，并可能导致表现糟糕的 `HEq`。
通常，与其处理类型的相等，处理某种合适的同构类型（如果你不涉及任何代数或拓扑结构，则用 `Equiv`）要好得多。
另外，如果你处理的是 `α` 的若干 `Subtype` 之间的相等，你或许应该改为处理 `Set α` 的元素。
`Set α` 中的相等表现良好。

## 为已存在的实例引入参数

一个常见的错误是为已经存在的实例引入 `variable` 或参数。
例如，在下面的定理陈述中，注意 `[Ring ℤ]` 是多余的，因为 `ℤ` 已经有一个可用的 `Ring` 实例。
```lean
import Mathlib.Algebra.Equiv.TransferInstance
import Mathlib.Algebra.Field.ZMod
import Mathlib.Algebra.Polynomial.Cardinal

theorem my_theorem [Ring ℤ] : CharZero ℤ := sorry
```

事实上，按照所陈述的，这个陈述说的是 $\mathbb{Z}$ 上*每一个*环的特征都为 0，而这是错误的，因为存在特征非零的可数无穷环（例如 $(\mathbb{Z}/2\mathbb{Z})[X]$）。
下面的证明由 Bhavik Mehta 给出：
```lean
open Cardinal in
theorem bad : False := by
  have e1 : #(Polynomial (ZMod 2)) = ℵ₀ := by simpa using (Cardinal.nat_lt_aleph0 2).le
  have e2 : #ℤ = ℵ₀ := by simp
  obtain ⟨e⟩ := Cardinal.eq.1 (e2.trans e1.symm)
  let i : Ring ℤ := e.ring
  cases @Nat.cast_injective _ _ my_theorem 2 0 rfl
```

这种情况的一个症状是，你可能会遇到在 infoview 中看起来完全相同但实际上并不相等的表达式，导致诸如 `rfl`、`apply` 和 `rw` 之类的策略带着晦涩的信息失败。
例如，下面的策略状态显示目标是证明 `dist 0 1 = dist 0 1`，而你必须深入点击右侧 `dist` 函数的三层，才能发现它使用了错误的实例。
```lean
import Mathlib.Topology.MetricSpace.Basic

example [inst : MetricSpace ℝ] : dist (0 : ℝ) 1 = inst.dist (0 : ℝ) 1 := by
  /-
  Tactic state:
  1 goal
  inst : MetricSpace ℝ
  ⊢ dist 0 1 = dist 0 1
  -/
  sorry
```
在这个特定的例子中，尝试 `rfl` 会给你如下错误信息
```
tactic 'rfl' failed, the left-hand side
  @dist ℝ (@PseudoMetricSpace.toDist ℝ Real.pseudoMetricSpace) 0 1
is not definitionally equal to the right-hand side
  @dist ℝ (@PseudoMetricSpace.toDist ℝ MetricSpace.toPseudoMetricSpace) 0 1
inst : MetricSpace ℝ
⊢ dist 0 1 = dist 0 1
```
由此你可以断定这两个类型类并不匹配。当诸如 `congr` 或 `convert` 之类的策略生成子目标时，往往值得在那些目标上运行 `rfl`，以查看它们是否是由不匹配的类型类实例引起的。

在实际代码中，你大概不会无意间写出 `inst.dist`，但在更复杂的例子中，错误的实例可能会以难以察觉的方式表现出来。

感谢 Edward van de Meent 建议我纳入这个主题并找出了一个误导性的陈述，也感谢 Bhavik Mehta 完成了第一个例子为 `False` 的证明细节。

## 把 `Set` 当作类型使用

在 Lean 中，`Set X` 被定义为 `X → Prop`，所以集合是谓词，而非类型。然而，存在一个从 `Set X` 到 `Type u` 的隐式强制转换，因此如果你有参数 `(X : Type) (s : Set X) (a : s)`，那么 `(a : s)` 实际上表示 `(a : {x : X // x ∈ s})`。
这里，`{x : X // x ∈ s}` 是 `Subtype (fun x ↦ x ∈ s)` 的记法。

也就是说，`a` 实际上是一个对 `⟨x, hx⟩`，其中 `x : X` 且 `hx` 是 `x ∈ s` 的一个证明。
所以，`a` 实际上并不是 `X` 的一个元素，但你可能没意识到这一点，因为还存在另一个从 `{x : X // x ∈ s}` 到 `X` 的隐式强制转换，它使得 `a` 在某些（但并非所有）情形下表现得像 `X` 的一个元素。

这会导致各种各样的问题。例如，
```lean
import Mathlib.Data.Set.Basic

example (s : Set ℕ) (n : s) : 0 + n = n := by
  sorry
```
无法编译，因为 Lean 不知道 `0 + n` 是什么意思，因为从技术上讲 `n` 并不是一个自然数。
你必须写 `(n : ℕ)` 才能使这个加法成立。

此外，如果你试图对 `n` 进行归纳来证明这个，你可能会发现你的策略并没有做你所期望的事。
```lean
import Mathlib.Data.Set.Basic
import Mathlib.Tactic

example (s : Set ℕ) (n : s) : 0 + (n : ℕ) = n := by
  /- Tactic state before:
  s : Set ℕ
  n : ↑s
  ⊢ 0 + ↑n = ↑n
  -/
  induction' n with d hd
  /- Tactic state after:
  s : Set ℕ
  d : ℕ
  hd : d ∈ s
  ⊢ 0 + ↑⟨d, hd⟩ = ↑⟨d, hd⟩
  -/
```
这里，该策略并没有把 `n` 当作自然数来进行归纳；相反，它拆解了 `Subtype` 的两个分量。
如果你改用未加撇号的 `induction` 策略，你会得到一条 “invalid alternative name 'zero', expected 'mk'” 的错误信息。

注意策略状态中 `↑` 的出现。它表示一个强制转换，这是 `n` 的类型可能并非你所想的那样的一条线索。

由于这些问题以及其他原因，如果你有一个参数 `(s : Set X)` 并且想假设 `a` 是 `s` 的一个元素，那么添加两个参数 `(a : X) (ha : a ∈ S)` 往往比写 `(a : s)` 更好。
类似地，如果你想让 `t` 成为 `s` 的一个子集，你应该声明 `(t : Set X) (h : t ⊆ s)`，而非 `(t : Set s)`。
这种从 `Set` 到类型的强制转换通常应当只保留给那些你需要把一个 `Set` 传递给另一个要求类型作为输入的函数的情形。

Mathlib 的代数库正是基于这一考虑设计的。例如，
`Subgroup` 是这样定义的
```lean
structure Subgroup (M : Type*) [Group M] where
  carrier : Set M
  mul_mem {a b} : a ∈ carrier → b ∈ carrier → a * b ∈ carrier
  one_mem : (1 : M) ∈ carrier
  inv_mem {x} : x ∈ carrier → x⁻¹ ∈ carrier
```
这是为了让你在拥有一个 `H : Subgroup G` 时，可以通过声明 `x : G` 和 `hx : x ∈ H` 来处理 `H` 的元素，而不必写 `x : H` 并应对 `x` 实际上并不具有类型 `G` 的问题。

## Sort _

写 `Sort _` 和 `Type _` 会让 Lean 自动填入全集层级参数。
有时，这会导致 Lean 把全集层级特化得比你预期的更窄。
例如，在
```lean
import Mathlib.Data.Countable.Defs

example (α : Sort _) (x y : α) (_ : Countable α := inferInstance) : x = y := by
  rfl
```
中，`inferInstance` 默认参数找到了 `Prop.countable`，这导致 `Sort _` 被限制为 `Prop`。
于是，`α : Prop`，这意味着由证明无关性，`x : α` 与 `y : α` 在定义上相等。

在较旧的 Lean 版本中，这种行为甚至更容易被触发，因为 `:=` 之后的代码可能会影响 `Sort _` 是什么。
例如，下面的代码可以在 Lean 4.8.0 中编译：
```lean
example {α : Sort _} (x y : α) : x = y := by
  have := α ∧ α -- Force α to have type Prop
  rfl
```

由于这种行为，建议你要么使用 `Sort*` 或 `Type*`（它们是 `Sort _` 和 `Type _` 的更严格版本，会迫使 Lean 每次使用时都生成一个新的全集参数），要么显式地指定全集参数。

## 试图证明关于 Float 的性质

默认情况下，输入像 `5.42` 这样的数会创建一个类型为 `Float` 的项，而非 `Rat` 或 `Real`。
证明关于 `Float` 的性质是非常困难的。
这是因为在 Lean 的数学部分中，`Float` 被定义为一个不透明类型，而 `Float = Unit` 与 Lean 的核心类型论是相容的（只要不使用 `native_decide`）。
但在计算上，`Float` 遵循 IEEE 754 *binary64* 格式，这类似于 C 中的 `double` 或 Rust 中的 `f64`。
（关于 32 位浮点数，参见 `Float32`。）
这意味着要证明关于 `Float` 的任何有意义的内容，你都必须使用 `native_decide`，而这是一个有风险的策略（参见本文档中关于 `native_decide` 的章节）。

此外，由于浮点数的行为，`0.1 + 0.2 == 0.3` 求值为 `false`。
（解释参见 <https://0.30000000000000004.com/>。）

所以，如果你对把 Lean 用作编程语言不感兴趣，或者想要证明关于你所处理的数的复杂性质，你应该避免使用 `Float`，转而使用诸如 `Rat` 或 `Real` 之类的其他数值类型。

## `native_decide`

`native_decide`（也写作 `decide +native`）类似于 `decide` 策略，区别在于它使用 `#eval` 来运行判定过程，而非在内核中对其进行归约。
这有可能比 `decide` 快得多，而且它是证明关于 `Float` 及其他一些不透明类型的性质的唯一途径，但它是有风险的，因为它信任 Lean 编译器，而编译器比 Lean 内核复杂得多，也更有可能包含错误。

具体来说，使用 `native_decide` 会使你的定理依赖于 `Lean.ofReduceBool` 公理，该公理表明 Lean 编译器是可信的。
你可以通过使用 `#print axioms` 来检查一个证明是否依赖于这条公理。
除了信任编译器之外，`Lean.ofReduceBool` 还信任所有的 `@[extern]` 和 `@[implemented_by]` 注解以及对编译器的其他扩展。
由于在 Lean 核心中有数百个这样的注解，目前 `native_decide` 几乎可以肯定有能力证明 `False`。
它还会信任你自己的 `@[extern]` 和 `@[implemented_by]` 注解，而不会对它们加以追踪：
```lean
def m := 37

@[implemented_by m]
def n := 22

#reduce n -- 22
#eval n -- 37

theorem bad : False := by
  have : n = 22 := by decide
  have : n = 37 := by native_decide
  contradiction

#print axioms bad -- 'bad' depends on axioms: [Lean.ofReduceBool]
```

贡献给 Mathlib 的代码不允许使用 `native_decide`。

## Panic 不会中止程序

如果你把 Lean 用作编程语言，请注意 `panic!` 宏默认并不会触发崩溃；相反，它只是打印一条错误信息并让代码继续运行。
这同样适用于像 `Option.get!` 这样的函数。`panic` 之所以这样表现，是因为它是一个安全函数，并且在形式上等价于 `default`。

如果你用 panic 来防护潜在危险的 `IO` 操作或防止数据损坏，这可能会很危险。
你可能想考虑把环境变量 `LEAN_ABORT_ON_PANIC` 设为 `1`，尽管对于环境变量难以控制的面向用户的应用而言，这可能并不足够。

## Lean 3 代码

互联网上能找到大量的 Lean 3 代码，而 LLM 也经常生成 Lean 3 代码而非 Lean 4 代码。
如果你在阅读旧的 Lean 代码，或者在使用 LLM，并且你看到诸如以下的细节
- 类型名以小写字母开头，例如 `nat` 和 `rat`
- 不以库名开头的小写 import，例如 `import data.real.basic`（其 Lean 4 等价形式是 `import Mathlib.Data.Real.Basic`）。
- 使用 `begin` 和 `end` 来包围策略模式，而非使用 `by`
- 在引入 2 个或更多变量或全集时使用复数命令，例如 `variables` 和 `universes`
- 不带方括号的 `rw` 策略
- `refl` 策略（在 Lean 4 中拼作 `rfl`）

那么你所阅读的代码很可能是 Lean 3 代码（或者，如果你在使用 LLM，它可能是 Lean 3 与 Lean 4 不连贯的混合体）。
Lean 3 和 Lean 4 是非常不同的语言，所以 Lean 3 代码在 Lean 4 中无法工作。

## 非终结性 simp

这是你初次编写证明时无需担心的事情，但如果你想整理一个证明，或许是为了能将其添加到像 mathlib 这样的库中，那么请注意，在策略块的中间使用 `simp` 被认为是不良实践。
在下面的例子中
```lean
example : ... := by
  ...
  simp
  rw [...]
  exact h
```
对 `simp` 的使用被认为是*非终结性的*。

非终结性 `simp` 会带来可维护性问题。
一般来说，随着越来越多的引理被添加到 mathlib，`simp` 会随时间变得越来越强大，这意味着当库中其他部分的代码发生改变时，`simp` 之后的目标状态可能随之改变，从而有可能破坏 `simp` 之后的任何策略，例如本例中的 `rw`。
在较少见的从 mathlib 中移除引理的情况下，终结性 `simp` 和非终结性 `simp` 都可能被破坏，但修复一个终结性 `simp` 调用通常要容易得多。

为避免非终结性 `simp`，你可以使用诸如 `simpa` 或 `simp_rw` 之类的 simp 变体，把 `simp` 与其后的策略合并起来；或者你可以通过使用 `simp?` 来“压缩”你的 simp 调用。
请注意，只要 `simp` 能完整地关闭一个目标，它出现在证明中间是没有问题的。
例如，尽管下面例子中的 `simp`
```lean
  induction n with
  | zero =>
    simp
  | succ d hd =>
    ...
```
位于证明中间，但它不被视为非终结性 simp，因为它完整地关闭了一个目标。

更多信息，请参见[这些关于非终结性 simp 的笔记](simp.html#non-terminal-simps)。

## 忽略警告

请密切关注你的 Lean 文件中的警告。
一个已完成的定理中出现的未使用变量警告，可能意味着并非所有假设都被用到了，而这通常表明该定理陈述是错误的。
类似地，如果你自己并没有输入 `sorry`，却出现一条声明使用了 sorry 的警告，这可能表明某个策略失败了，并悄悄地用一个合成的 sorry 关闭了证明。

如果你确信某条警告不适用，你可以通过适当地使用 `set_option` 来禁用它。
这比忽略警告、把判断哪些警告是预期的、哪些是你应当关注的留给他人（或未来的你自己！）去猜测，是更好的编程实践。

请注意，`#lint` 命令（定义于 `Batteries` 中）能检测一些常见问题，例如句法上的恒真式。
它只会检查 `#lint` 命令之上的文件部分，因此应当在文件末尾运行它。

## 易混淆的 Unicode 字符

Lean 大量使用非 ASCII 的 Unicode 字符，但这样做的一个副作用是，许多字符看起来相似，但在 Lean 中却具有非常不同的功能。
如果你使用带有 Lean 4 扩展的 VSCode，你可以将鼠标悬停在不熟悉的字符上，以查看如何输入它们的说明。

一些经常被混淆的字符包括：

字符 | Unicode 名称 | 输入方式 | 在 Lean 中的用途
--- | --- | --- | ---
`\|` | Vertical Line (U+007C) | ASCII 字符 | 集合构造记法；模式匹配，绝对值
`∣` | Divides (U+2223) | `\\|`、`\dvd`、`\mid`、`\shortmid` | 整除
`Π` | Greek Capital Letter Pi (U+03A0) | `\p`、`\P`、`\Pi` | 依值函数类型：`Π x : α, β x` 是 `(x : α) → β x` 的另一种写法
`∏` | N-Ary Product (U+220F) | `\prod` | 带索引的乘积：参见 `BigOperators.bigprod`
`⊓` | Square Cap (U+2293) | `\inf`、`\meet`、`\glb`、`\sqcap` | 两个元素的下确界：`a ⊓ b` 表示 `min a b`。参见 `Min` 类型类，即便序不是线性的也会用到它
`⨅` | N-Ary Square Intersection Operator (U+2A05) | `\infi`、`\Glb`、`\Inf`、`\Meet`、`\Sqcap`、`\bigglb`、`\biginf`、`\bigmeet`、`\bigsqcap` | 带索引的下确界运算，需要 `InfSet` 类型类。
`Σ` | Greek Capital Letter Sigma (U+03A3) | `\S`、`\GS`、`\Sigma` | `Sigma`（即依值对／依值和）类型
`∑` | N-Ary Summation (U+2211) | `\sum` | 带索引的求和：参见 `BigOperators.bigsum`
`×` | Multiplication Sign (U+00D7) | `\x`、`\times`、`\multiplication` | 类型的笛卡尔积
`x` | Latin Small Letter X (U+0078) | ASCII 字符 | 无特殊功能
`X` | Latin Capital Letter X (U+0058) | ASCII 字符 | 通常无特殊功能；当 `Polynomial` 命名空间打开时，表示多项式变量／不定元
`*` | Asterisk (U+002A) | ASCII 字符 | 乘法
`∨` | Logical Or (U+2228) | `\v`、`\or`、`\vee` | 或符号：`a ∨ b` 表示 `Or a b`
`\/` | | ASCII 字符 | 或符号 `∨` 的 ASCII 替代写法
`v` | Latin Small Letter V (U+0076) | ASCII 字符 | 无特殊功能
`·` | Middle Dot (U+00B7) | `\.`、`\centerdot` | 在策略模式中缩进并聚焦于子目标；匿名函数语法，例如 `(· + 2)`，它是 `fun x ↦ x + 2` 的简写
`•` | Bullet (U+2022) | `\smul`、`\bub`、`\bu` | 标量乘法或左作用（参见 `HSMul` 和 `SMul` 类型类）
`⬝` | Black Very Small Square (U+2B1D) | `\cdot`、`\dot`、`\tr`、`\con` | 仅用于 `u ⬝ᵥ w = dotProduct u w`（用 `\_v` 输入 `ᵥ`）
`→` | Rightwards Arrow (U+2192) | `\r`、`\imp`、`\->`、`\to`、`\r-`、`\rightarrow` | 函数类型 `A → B`
`->` | | ASCII 字符 | 函数类型中 `→` 的 ASCII 替代写法
`↦` | Rightwards Arrow From Bar (U+21A6) | `\mapsto`、`\\|->`、`\r-\|` | 用于 Lambda 绑定子，例如 `fun x : Nat ↦ x + 2`
`=>` | | ASCII 字符 | 模式匹配；`↦` 的 ASCII 替代写法
`⟶` | Long Rightwards Arrow (U+27F6) | `\hom`、`\-->`、`\longrightarrow`、`\r--` | `a ⟶ b` 是范畴或箭图中从 `a` 到 `b` 的态射的类型：参见 `Quiver.Hom`。
`↪` | Rightwards Arrow With Hook (U+21AA) | `\hookrightarrow` | `α ↪ β` 是从 `α` 到 `β` 的单射函数的类型：参见 `Function.Embedding`
`=` | Equals Sign (U+003D) | ASCII 字符 | 对象之间的相等：参见 `Eq`
`==` | | ASCII 字符 | 布尔相等：参见 `BEq`。布尔相等是类型相关的，但如果存在 `LawfulBEq` 实例，则 `BEq` 与 `Eq` 一致。
`≃` | Asymptotically Equal To (U+2243) | `\equiv`、`\~-`、`\simeq` | 双射：`α ≃ β = Equiv α β` 是配有双侧逆的从 `α → β` 的函数的类型；`≃o`、`≃r` 等则指特定种类的同构。
`≅` | Approximately Equal To (U+2245) | `\iso`、`\~=`、`\cong` | 范畴中的同构；当 `open scoped Congruent` 生效时，转而指 `Congruent`。
`≈` | Almost Equal To (U+2248) | `\~~`、`\approx`、`\thickapprox` | 类型相关的等价记法：参见 `HasEquiv`。通常指一个由类型类推断出的 `Setoid` 实例
`~` | Tilde (U+007E) | ASCII 字符 | `List`、`Array` 和 `Vector` 的置换等价关系；对其他类型有某些特殊含义
`≡` | Identical To (U+2261) | `\==` | `a ≡ b [MOD n]` 表示 `Nat.ModEq n a b`，`a ≡ b [ZMOD n]` 表示 `Int.ModEq n a b`。对其他类型有某些特殊含义

## 结构字段中的默认值

用户常常以为结构字段中 `:=` 的使用意味着“此字段被定义为具有此值”。但事实并非如此！相反，这是为结构字段提供默认值的方式。具体来说，这些值可以被覆盖。

```
structure foo : Type where
  n : Nat := 37 -- I want n to always be 37...

def X : foo where
  n := 42 -- ...but that's not the way to do it

#eval X.n -- 42

def Y : foo where -- only if `n` is not supplied does the default value kick in.

#eval Y.n -- 37
```

如果你确实想要类似这样的效果，请改试下面的做法：

```
structure foo : Type where

def foo.n : Nat := 37

def X : foo where

#eval X.n -- 37
```
