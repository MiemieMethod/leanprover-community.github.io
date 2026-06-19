# 转换策略模式

在策略块内部，可以使用关键字 `conv` 进入转换模式（conversion mode）。该模式允许深入到假设和目标内部，甚至深入其中的 `fun` 绑定子内部，以施加重写或化简步骤。

这类似于其他定理证明器（如 HOL4、HOL Light 或 Isabelle）中的转换策略组合子（tactic combinators）。

## 基本导航与重写

作为第一个例子，让我们证明
`example (a b c : ℕ) : a * (b * c) = a * (c * b)`（本文中的例子多少有些刻意，因为 `Tactic.Ring` 中的 `ring` 策略可以立即完成它们）。最朴素的初次尝试是进入策略模式并尝试 `rw [mul_comm]`。但这会在交换项中出现的第一个乘法之后，把目标变成 `b * c * a = a * (c * b)`。有几种方法可以修正这一问题，其中一种是使用更精确的工具：转换模式。下面的代码块在每一行之后展示了当前的目标。注意目标以 `|` 为前缀，而普通模式中的目标以 `⊢` 为前缀（尽管如此，这些目标仍被称为"目标"）。

```lean
example (a b c : ℕ) : a * (b * c) = a * (c * b) := by
  conv =>           -- | a * (b * c) = a * (c * b)
    lhs             -- | a * (b * c)
    congr           -- | a and | b * c
    · skip          -- | a
    · rw [mul_comm] -- | c * b
```

上面的代码片段展示了三个导航命令：
* `lhs` 导航到关系（此处为等式）的左侧，还有一个 `rhs` 导航到右侧。
* `congr` 创建与当前头部函数（此处头部函数为乘法）的参数数量相同的多个目标
* `skip` 转到下一个目标

一旦到达相关的目标，我们便可像在普通模式中那样使用 `rw`。注意，若当前目标变为 `x = x`（在严格的句法意义下，定义等价是不够的：此时需要用 `rfl` 或 `trivial` 来收尾），Lean 会尝试求解它。

供参考，我们可以把 "conv => lhs .." 写成 "conv_lhs => .."：

```lean
example (a b c : ℕ) : a * (b * c) = a * (c * b) := by
  conv_lhs =>
    congr
    · skip
    · rw [mul_comm]
```

使用转换模式的第二个主要理由是在绑定子下进行重写。假设我们想证明 `example (fun x : ℕ ↦ 0 + x) = (fun x ↦ x)`。最朴素的初次尝试是进入策略模式并尝试 `rw [zero_add]`。但这会令人沮丧地失败：
```text
tactic 'rewrite' failed, did not find instance of the pattern in the target expression
  0 + ?a
⊢ (fun x ↦ 0 + x) = fun x ↦ x
```

解决方法是：
```lean
example : (fun x : ℕ ↦ 0 + x) = (fun x ↦ x) := by
  conv_lhs =>     -- | fun x ↦ 0 + x
    ext x         -- | 0 + x
    rw [zero_add] -- | x
```
其中 `ext` 是进入 `fun` 绑定子内部的导航命令。注意这个例子多少有些刻意，我们也可以这样做：
```lean
example : (fun x : ℕ ↦ 0 + x) = (fun x ↦ x) := by
  funext x; rw [zero_add]
```

以上所有这些也可用于重写局部上下文中的某个假设 `H`，方法是使用 `conv at H`。

## 模式匹配

使用上述命令进行导航可能很繁琐。我们可以利用模式匹配将其简化，如下所示：

```lean
example (a b c : ℕ) : a * (b * c) = a * (c * b) := by
  conv in (b * c) => -- | b * c
    rw [mul_comm]    -- | c * b
```

我们可以把这个证明写成一行：

```lean
example (a b c : ℕ) : a * (b * c) = a * (c * b) := by
  conv in (b * c) => rw [mul_comm]
```

当然，也允许使用通配符：

```lean
example (a b c : ℕ) : a * (b * c) = a * (c * b) := by
  conv in (_ * c) => rw [mul_comm]
```

在所有这些情况中，只有第一个匹配会受到影响。在转换模式内部，还可以使用 `for` 命令来进行更复杂的模式匹配。下面的代码仅对 `b * c` 的第二个和第三个出现位置执行重写：

```lean
example (a b c : ℕ) : (b * c) * (b * c) * (b * c) = (b * c) * (c * b) * (c * b) := by
  conv in (occs := 2 3) (b * c) =>
    · rw [mul_comm]
    · rw [mul_comm]
```

我们可以用 "all_goals" 把这个证明写成一行：

```lean
example (a b c : ℕ) : (b * c) * (b * c) * (b * c) = (b * c) * (c * b) * (c * b) := by
  conv in (occs := 2 3) (b * c) => all_goals rw [mul_comm]
```

## 转换模式中的其他策略

除了使用 `rw` 进行重写之外，还可以使用 `simp`、`dsimp`、`change` 和 `whnf`。`change` 是一个有用的工具——它允许将一个项更改为与之定义等价的某物，颇像策略模式中的 `show` 命令。`whnf` 命令意为"归约到弱头范式（weak head normal form）"，将在 [Metaprogramming in Lean 4](https://leanprover-community.github.io/lean4-metaprogramming-book/main/04_metam.html#weak-head-normalisation) 第 4 节中加以解释。

mathlib 为 `conv` 提供的扩展，例如 `ring` 和 `norm_num`，可以通过 [`Mathlib.Tactic.HelpCmd`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/HelpCmd.html) 中的 `#help conv` 命令找到。
