# Simp

## 概述

在本文档中，我们将介绍 Lean 4 中化简器策略 [`simp`](https://leanprover-community.github.io/mathlib4_docs/Init/Tactics.html#Lean.Parser.Tactic.simp)
以及相关策略 [`dsimp`](https://leanprover-community.github.io/mathlib4_docs/Init/Tactics.html#Lean.Parser.Tactic.dsimp)
的基本用法。

我们将给出一些避免“非终结性 `simp`”的建议，并简要描述 `simp`
和 `dsimp` 的配置选项。

## 引言

Lean 拥有一个称为 `simp` 的“化简器”，它会查询一个称为 *`simp` 引理* 的事实数据库，
以（期望地）化简假设和目标。该化简器是所谓的 *条件项重写系统*：
它所做的全部工作就是反复将形如 `A` 的子项替换（或 *重写*）为 `B`，
对所有适用的形如 `A = B` 或 `A ↔ B` 的事实皆如此。
化简器会机械地不断重写，直到再也无法重写为止。所有
`simp` 引理都是有方向的：左端始终被右端替换，而绝不会反过来。

理想情况下，这个事实数据库应当能将表达式化简
为某种范式（normal form）。
在实践中，这往往无法实现（范式可能不存在，或者
可能不存在一组能产生范式的重写规则），
但我们仍尽可能地力求逼近这一理想。
更进一步，我们希望这个事实数据库是 *合流的*（confluent），
即化简器考虑重写的顺序并不影响结果。
同样，我们也尽可能地力求接近合流。

虽然这套系统能够完全自动地证明许多简单的命题，但证明所有简单命题
并不在它的职责范围之内，尽管这或许令人失望。

下面是一个示例（使用了 mathlib）。

```lean
import Mathlib.Algebra.Group.Defs

variable (G : Type) [Group G] (a b c : G)

example : a * a⁻¹ * 1 * b = b * c * c⁻¹ := by
  simp
```

人类会如何求解这个目标呢？他们会注意到 `a * a⁻¹ = 1`、
`1 * 1 = 1`，等等，直到将该示例化简
为 `b = b`，而这显然成立。

化简器所做的也正是如此。事实上，如果你在该示例上方加上
`set_option trace.Meta.Tactic.simp.rewrite true`，那么 `simp` 下方就会出现
一条蓝色波浪下划线（在 VS Code 中），
点击它便会显示 `simp` 所执行的
重写序列：
```
[Meta.Tactic.simp.rewrite] @mul_right_inv:1000, a * a⁻¹ ==> 1

[Meta.Tactic.simp.rewrite] @mul_one:1000, 1 * 1 ==> 1

[Meta.Tactic.simp.rewrite] @one_mul:1000, 1 * b ==> b

[Meta.Tactic.simp.rewrite] @mul_inv_cancel_right:1000, b * c * c⁻¹ ==> b

[Meta.Tactic.simp.rewrite] @eq_self:1000, b = b ==> True
```
`simp?` 策略是提取 `simp` 所应用的引理列表的一种有用方式。
它会建议
```lean
simp only [mul_right_inv, mul_one, one_mul, mul_inv_cancel_right]
```
这是一次使用了这特定四条引理的 `simp` 调用。

若要查看化简过程中那些成功以及失败的重写，
你可以使用更为详尽的选项 `set_option trace.Meta.Tactic.simp true`。

## Simp 引理

那么 Lean 的化简器是如何知道 `a * a⁻¹ = 1` 的呢？这是因为
在 `Mathlib.Algebra.Group.Defs` 中有一条被标注了
`simp` 属性的引理：

```lean
@[simp] lemma mul_right_inv (a : G) : a * a⁻¹ = 1 := ...
```

我们将标注了 `simp` 属性的引理称为“`simp` 引理”。下面
是 mathlib 中更多 `simp` 引理的例子：

```lean
@[simp] theorem Nat.dvd_one {n : ℕ} : n ∣ 1 ↔ n = 1 := ...
@[simp] theorem mul_eq_zero {a b : ℕ} : a * b = 0 ↔ a = 0 ∨ b = 0 := ...
@[simp] theorem List.mem_singleton {a b : α} : a ∈ [b] ↔ a = b := ...
@[simp] theorem Set.setOf_false : {a : α | False} = ∅ := ...
```

当化简器试图化简某个项 `T` 时，它会查阅
系统在那一时刻已知的 `simp` 引理；若遇到一条适用的、形如
`A = B` 或 `A ↔ B` 的引理，且 `A` 作为子表达式出现在 `T` 中，
它就会将 `T` 中 `A` 的那个实例重写为 `B`，
然后再从头开始。注意 `simp` 从最内层的项开始，向外
推进：它会先化简函数的参数，
然后再化简函数本身。此外，`simp` 内部具有一定的
机巧，使其能够避免每次都考虑 *所有* `simp`
引理（截至 2026 年 2 月，mathlib 中有四万余条这样的引理）。

化简器只在一个方向上应用 `simp` 引理：若 `A = B` 是一条 `simp`
引理，那么 `simp` 会将 `A` 替换为 `B`，但不会将
`B` 替换为 `A`。因此一条 `simp` 引理应当具有这样的性质：其
右端比左端更简单。特别地，
在这种情形下，`=` 和 `↔` 不应被视为对称的运算符。下面将是
一条糟糕透顶的 `simp` 引理（假如它竟被允许的话）：

```lean
@[simp] lemma mul_right_inv_bad (a : G) : 1 = a * a⁻¹ := ...
```

将 `1` 替换为 `a * a⁻¹` 并不是一个合理的默认推进
方向。更糟糕的是那种会使表达式无限制增长的引理，
它会导致 `simp` 永远循环下去：

```lean
@[simp] lemma even_worse_lemma: (1 : G) = 1 * 1⁻¹ := ...
```

在做出一个新定义时，通常也会同时引入
若干 `simp` 引理，以将涉及该定义的表达式化为
某种合理的形式。一个例子是 mathlib 中的
[Data.Complex.Basic](https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/Data/Complex/Basic.lean)，
其中有将近 100 条 `simp` 引理。尽管诸如
```lean
@[simp] lemma add_re (z w : ℂ) : (z + w).re = z.re + w.re := rfl
```
这样的定理依定义为真，它们仍被引入，因为它们赋予 `simp` 化简表达式并进而利用已有事实的能力。
例如这一条就把复数加法转化为实数加法。
如果你允许 `simp` 使用实数加法的交换律，那么它便能够
经由 `z.re + w.re = w.re + z.re` 自动证明 `(z + w).re = (w + z).re`，
而这正是复数加法可交换之证明的一半。

Lean 内核本身就是一个针对 lambda 演算的重写系统，它有着明确的
推进进展之概念。有鉴于此，一类有用的
`simp` 引理是那些在此意义上让 `simp` 能够部分求值
表达式的引理。例如，假设你有一个结构类型 `Foo`，并
用该类型定义一个结构 `myFoo`，
```lean
structure Foo where n : ℕ

def myFoo : Foo where n := 37
```
那么如果你添加一条 `simp` 引理 `myFoo.n = 37`，就赋予了化简器
对 `myFoo` 求值 `Foo.n` 投影的能力，从而省去
展开 `myFoo` 定义的麻烦（默认情况下 `simp` 并不展开大多数定义）。
创建这类 `simp` 引理是如此常见，以至于有
[一个属性](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/Simps/Basic.html#simpsAttr)
能自动为你创建它们：
```lean
@[simps] def myFoo : Foo where n := 37
```
这会生成引理 `@[simp] lemma myFoo_n : myFoo.n = 37`。

## 基本用法

* `simp` 试图利用 Lean 在那一时刻已知的所有 `simp` 引理来化简目标。

* `simp [h1, h2]` 使用所有 `simp` 引理，外加 `h1` 和 `h2`（它们既可以是局部假设，也可以是出于某种原因未被标注为 `simp` 的其他引理）。

* `simp [← h]` 使用所有 `simp` 引理，并以反向形式 `B = A` 使用 `h : A = B`（即 `simp` 将 `B` 重写为 `A`）。

* `simp [-thm]` 阻止 `simp` 使用名为 `thm` 的 `simp` 引理。

* `simp [*]` 使用所有 `simp` 引理，外加当前所有局部假设，来尝试化简目标。

* `simp at h` 试图利用所有 `simp` 引理来化简 `h`。

* `simp [h1] at h2 ⊢` 试图利用 `h1` 和所有 `simp` 引理来化简 `h2` 和目标（注意：在 VS Code 中用 `\|-`、`\goal` 或 `\vdash` 输入 `⊢`）。

* `simp [*] at *`：试图利用所有假设和所有 `simp` 引理来化简目标和所有假设。有时值得一试。

* `simp only [h1, h2, ..., hn]` 告诉 `simp` 只使用引理 `h1`、`h2`、……，而非整套 simp 引理。
（在证明中途使用 `simp only [...]` 是可以接受的，因为后续对 `simp` 集合的改动不会破坏该证明。）

* `simp [↓h1]` 在进入子项 *之前* 使用 `h1`。通常情况下，`simp` 在进入子项 *之后* 才使用引理。

* `simp [↑h1]` 在进入子项 *之后* 使用 `h1`。此语法用于标注了 `simp↓` 的引理。

注意，某些 `simp` 引理带有必须满足的附加假设。
例如，一条关于在等式两端消去某因子的定理，
只在该因子非零这一假设下方才成立。若 `h`
是假设 `P` 的一个证明，且 `P → A = B` 是一条 `simp` 引理，那么
`simp [h]` 会将目标中的 `A` 替换为 `B`。`simp` 会考虑
附加假设这一事实，正是它被称为
*条件* 项重写系统的原因。

## Simp 范式

有时同一件事有若干种表述方式。例如，
若 `n : ℕ`，则假设 `n ≠ 0`、`0 ≠ n`、`n > 0`、`0 < n`、
`1 ≤ n` 和 `n ≥ 1` 在逻辑上都是等价的。这对于
化简器这类重写系统可能造成困扰。原因在于
化简器是通过 *语法相等*（syntactic equality）来寻找子项的。如果
化简器正在处理项 `T`，且 `A = B` 是一条 `simp` 引理，
那么除非 `T` 的某个子项 `A'` 与 `A` 在语法上完全相同
（大致而言：它们具有字面上相同的文本表示），否则 `simp` 一般
不会注意到该规则适用，因而不会
将其重写为 `B`。类似地，若某条形如 `A = B` 的 `simp` 引理以 `n` 的非零性（以某一种方式表述）作为前提条件，而 `h`
是 `n` 非零性（以另一种方式表述）的一个证明，那么 `simp [h]` 可能
不会将 `A` 替换为 `B`。

mathlib 中处理这个问题的方式，是一劳永逸地为某事物的表达方式
固定一个 *`simp` 范式*（例如以 `0 < n` 表示非零性），
然后在陈述引理时始终坚持采用这一变体。这样
就免去了为每一种变体编写重复引理的麻烦。为帮助化简器，
往往会有一些规范化引理，其唯一目的就是把表达式化为
`simp` 范式。

一般而言，如果你在写一条引理，你应当知道表达引理中各想法的“范式”
方式。`#simp` 命令可以帮助你
了解这一点：对表达式 `e` 写下 `#simp e`，便会用
适用的 `simp` 引理化简该表达式。
如果你在写一条关于自己所作定义的引理，
请思考那些可以用多于一种方式表达的想法的范式。

`simp` 范式的一个例子，是表达类型的某个子集非空性的方式。
若 `α : Type` 且 `s : Set α`，则
`s` 的非空性既可表示为 `s.Nonempty`，也可表示为 `s ≠ ∅`。
在 mathlib 中，人们努力坚持以 `s.Nonempty` 作为范式
形式。

另一个例子：每个有限集 `s : Finset α` 都可以被强制转换
为 `Set α`，因此对 `a : α` 而言，`a ∈ s` 和
`a ∈ (s : Set α)` 都可表示同一含义。有限集中
隶属关系的 simp 范式是 `a ∈ s`，而且还有一条
规范化 `simp` 引理
```lean
@[simp] lemma mem_coe {a : α} {s : Finset α} : a ∈ (s : Set α) ↔ a ∈ s := ...
```
用于将 `a ∈ (s : Set α)` 的出现替换为正确的范式。

由于化简器是从内向外工作的——先化简函数的参数，
再化简函数本身——因此一条 `simp`
引理在其左端，函数的参数应当处于 simp 范式。例如，若 `g 0` 可被
化简，那么 `@[simp] lemma foo : f (g 0) = 0` 将永远不会被使用。
Batteries 的 `simpNF` [linter](https://leanprover-community.github.io/mathlib4_docs/Batteries/Tactic/Lint/Frontend.html) 会检查这一点
（你可以通过在文件末尾加上 `#lint`，自行对某个模块运行 mathlib 的 linter）。

## `simpa`

`simpa` 策略是 `simp` 的一种变体，用于完成证明——作为一个“收尾”策略，若它
无法关闭目标，就会失败。其基本用法是
```lean
simpa [h1, h2] using e
```
其中 `[h1, h2]` 指可选的 `simp` 引理列表（语法与 `simp` 相同），
而 `e` 是一个表达式。`e` 通常是某个假设的名字。
`e` 的类型与目标都会被化简，若两者被化简为同一事物，`simpa` 即告成功。

下面是一个简单的 `simpa` 示例：
```lean
example (n : ℕ) (h : n + 1 - 1 ≠ 0) : n + 1 ≠ 1 := by
  simpa using h
```
若不用 `simpa`，我们或许会写 `simp at ⊢ h; exact h`。
所谓“非终结性 `simp`”，即那些不关闭目标的 `simp` 用法，
最好加以避免（参见下一节），而 `simpa` 正是避免它们的一种方式。

如果没有 `using` 子句，那么 `simpa` 转而执行以下三个步骤：

1. 化简目标。
2. 如果局部上下文中有一个名为 `this` 的假设，则化简其类型。
3. 应用 `assumption` 策略。

第 2 步是为了支持这样一种模式：`simpa` 紧跟在 `have : P` 或 `suffices : P` 之后，
因为这两者都默认以 `this` 作为它们所引入假设的名字。

## 非终结性 `simp`

随着 `simp` 引理被添加进库（或从库中移除），`simp`
的行为也会随时间变化。这意味着使用
`simp` 的证明可能失效，而且，除非你了解 `simp` 引理集合是如何
变化的，否则修复一个证明可能颇为困难。

例如，如果一个证明长这样
```lean
  ...
  simp
  rw [foo_eq_bar]
  ...
```
之后某人给 `foo_eq_bar` 加上了 `@[simp]` 属性，
那么这次重写如今就会失败。

虽然在初始开发期间，于证明中途使用 `simp` 是没问题的，
但经验法则是：当每个 `simp` 都完整地关闭一个目标时，
Lean 代码更易于维护。当这样一个 `simp` 日后
失效时，这能确保我们知道原本意图的目标是什么。

有几种在证明中途使用 `simp` 的“被认可”方式：

1) `simp only [h1, h2, ..., hn]` 将 `simp` 约束为只使用给定列表中的
引理，因而它不受 `simp` 引理集合
变化的影响。提示：用 `simp?` 来
自动生成一个合适的 `simp only`。

2) 使用形如 `have h : P := by ...; simp` 的构造来引入一个
由 `simp` 证明的假设。`have` 表达式可能处于
证明中途，但其中的 `simp` 关闭的是它所引入的目标。

3) 如果 `simp` 将你的目标变为 `P`，那么你可以写
```lean
  suffices : P by simpa
```
这会在当前目标之后添加一个新目标 `P`，引入一个新
假设 `this : P`，同时化简目标和 `this`，
然后试图用 `this` 关闭目标。`simpa` 策略 *要求*
目标被关闭，这与 `simp` 不同，从而更容易知道它何时失效。
源代码中显式写出的 `P` 有助于找到修复方法。

非终结性 `simp` 可能出现的一种情形，是在形如 `simp at ⊢ h; exact h` 的策略序列中。
这些可以用 `simpa using h` 来替代。

## `dsimp`

`dsimp` 是 `simp` 的一个变体，它只使用“定义性的”`simp`
引理。这些 `simp` 引理的证明是 `rfl`，
也就是说，其两端依定义相等的引理。

与 `simp` 一样，建议你不要在证明中途使用它。
不过，如果 `dsimp` 将你的目标变为 `h`，那么 `change h`
很可能会做同样的事。`dsimp` 的另一种常见用法是
```lean
dsimp only
```
它是 `dsimp only []` 的简写，即一个带空 `simp` 引理集合的 `dsimp`。
这可以安全地在证明中途使用，并且它可以是
整理目标的一种有用方式：除其他作用外，它会对 lambda 表达式做 beta 归约
（它会把 `(fun x => f x) 37` 变成 `f 37`），并且会归约结构投影
（它会把 `{ toFun := f, ... }.toFun` 变成 `f`）。

## 更高级的特性

### 析消器（Discharger）

Lean 有以下定理：

```lean
theorem Nat.max_eq_left {a b : ℕ} (h : b ≤ a) : max a b = a
```

然而，仅凭此定理，`simp` 无法证明以下目标。

```lean
example : max (1 : ℕ) 0 = 1 := by
  simp only [Nat.max_eq_left]
-- simp made no progress
```

这是因为 `simp` 未能解决附带条件 `(0 : ℕ) ≤ 1`；这可以通过命令 `set_option trace.Meta.Tactic.simp.discharge true` 看到。

```lean
[Meta.Tactic.simp.discharge] @Nat.max_eq_left discharge ❌
      0 ≤ 1
```

这个附带条件可以简单地用 `decide` 解决：

```lean
example : (0 : ℕ) ≤ 1 := by
  decide
```

如何在 `simp` 中使用这个策略来解决附带条件呢？答案如下：

```lean
example : max (1 : ℕ) 0 = 1 := by
  simp (disch := decide) only [Nat.max_eq_left]
```


### 完整语法

以下是 `dsimp` 策略的完整语法：

> `dsimp` (`?`)? (`!`)? (`(config :=` config `)`)? (`(disch :=` discharger `)`)? (`only`)? (`[`引理列表`]`)? (`at` locations)?

其中 “( ... )?” 表示表达式中可选的部分。引理列表与 `rw` 的类似，但
此外 `-lemma_name` 表示某条引理被排除在 `simp` 引理集合之外。
配置选项将在后续小节中描述。

如果存在 `!`，它会向配置选项添加 `autoUnfold := true`。
如果存在 `?`，它会使 `simp` 建议一组足以完成任务的 `simp` 引理。

以下是 `simp` 策略的完整语法：

> `simp` (`?`)? (`!`)? (`(config :=` config `)`)? (`(disch :=` discharger `)`)? (`only`)? (`[`由 `*` 和引理构成的列表`]`)? (`at` locations)?

以下是 `simpa` 策略的完整语法：

> `simpa` (`?`)? (`!`)? (`(config :=` config `)`)? (`(disch :=` discharger `)`)? (`only`)? (`[`由 `*` 和引理构成的列表`]`)? (`using` expr)?

其含义与 `simp` 相同，但 `using` 可以接受任意表达式，而不仅限于 `at` 所要求的局部常量。

### 自定义 simp 属性

使用命令 [`register_simp_attr`](https://leanprover-community.github.io/mathlib_docs/commands.html#mk_simp_attribute)，
你可以创建自己的类似 `@[simp]` 的属性，但有一个关键区别：
被 `@[new_attr]` 标注的引理 _不_ 在默认的 `simp` 引理集合中。
相反，它们应当被显式纳入：`simp [new_attr]`。这往往可以替代冗长的
`simp only [...]` 调用，并使代码更易读。一些常见用法的例子包括
[`enat_to_nat_top`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/Attr/Register.html#Parser.Attr.enat_to_nat_top) 和
[`coassoc_simps`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/Attr/Register.html#Parser.Attr.coassoc_simps)。

### 配置选项

`simp` 和 `dsimp` 都可以接受额外的配置选项。
例如，`simp +singlePass` 在将 `singlePass` 配置选项设为 true 的情况下运行 `simp`；`simp -singlePass` 则会显式地将该选项设为 false。
可以用 `singlePass` 来避免某些原本可能发生的循环。
对于取值的选项，你可以使用具名参数语法，如 `simp (maxSteps := 37)`。
这会将失败前所允许的最大步数设为 37。

Lean 核心文件 `Init/MetaTypes.lean` 在
[`Lean.Meta.DSimp.Config`](https://leanprover-community.github.io/mathlib4_docs/Init/MetaTypes.html#Lean.Meta.DSimp.Config) 和 [`Lean.Meta.Simp.Config`](https://leanprover-community.github.io/mathlib4_docs/Init/MetaTypes.html#Lean.Meta.Simp.Config) 结构中揭示了其他配置选项。
它们中的大多数对普通用户而言并不十分相关。下表
复现了这些选项，其中某个配置选项
对 `simp` 或 `dsimp` 的默认值分别给在
相应的列中——若没有给出默认值，则表示该选项不可用。
默认值 “max” 指 `Lean.Meta.Simp.defaultMaxSteps`，目前为 `100000`。

| 选项 | `simp` | `dsimp` | 描述 |
| --- | --- | --- | --- |
| `maxSteps` | max | | 失败前所允许的最大步数 |
| `maxDischargeDepth` | 2 | | 对附带条件递归应用化简时的最大递归深度 |
| `contextual` | `false` | | 基于当前子表达式的上下文使用额外的 `simp` 引理（见下面的示例） |
| `memoize` | `true` | | 对子项的化简进行缓存 |
| `singlePass` | `false` | | 每个子项至多访问一次 |
| `zeta` | `true` | `true` | 进行 zeta 归约：`let x := a; b` ↝ `b[x := a]` |
| `beta` | `true` | `true` | 进行 beta 归约：`(fun x => a) y` ↝ `a[x := y]` |
| `eta` | `true` | `true` | 允许 eta 等价：`(fun x => f x)` ↝ `f`（目前尚未实现） |
| `etaStruct` | `.all` | `.all` | 配置如何判定两个结构实例之间的定义相等性。参见 [`Lean.Meta.EtaStructMode`](https://leanprover-community.github.io/mathlib4_docs/Init/MetaTypes.html#Lean.Meta.EtaStructMode) 的文档 |
| `iota` | `true` | `true` | 归约递归子：`Nat.recOn (succ n) Z R` ↝ `R n (Nat.recOn n Z R)` |
| `proj` | `true` | `true` | 归约投影：`Prod.fst (a, b)` ↝ `a` |
| `decide` | `false` | `false` | 通过推断 `Decidable p` 实例并将其归约，把命题 `p` 重写为 `True` 或 `False` |
| `arith` | `false` | | 化简简单的算术表达式 |
| `autoUnfold` | `false` | `false` | 使用方程编译器生成的所有方程引理进行归约 |
| `dsimp` | `true` | | 当为 `true` 时，若不存在能让 `simp` 访问依值参数的同余定理，则对这些参数切换为 `dsimp`。当 `dsimp` 为 `false` 时，则不访问该参数。 |
| `failIfUnchanged` | `true` | `true` | 若未应用任何化简则失败 |
| `ground` | `false` | | 归约基项（ground term）。当一个项不含自由变量或元变量时，它是基项。 |
| `unfoldPartialApp` | `false` | `false` | 当我们请求展开 `f` 时，即使是 `f` 的部分应用也予以展开 |
| `zetaDelta` | `false` | `false` | 展开局部定义。即，给定包含条目 `x : t := e` 的局部上下文，自由变量 `x` 归约为 `e`。 |

`autoUnfold` 将方程/模式匹配编译器生成的
方程引理添加到 `simp` 引理集合中。

`contextual` 选项赋予 `simp` 这样的能力：基于某个子表达式
所处的上下文，将假设视为额外的 `simp`
引理。例如，当它化简某个蕴含式的后件时，
会临时把前件添加为一条 `simp` 引理。下面这个示例
就需要用到这一点：
```lean
example {x y : ℕ} : x = 0 → y = 0 → x = y := by
  simp +contextual
```
