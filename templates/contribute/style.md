# 库风格指南

除了[命名约定](naming.html)之外，
Lean 库中的文件通常还遵循以下指南和约定。
统一的风格使得浏览库和阅读内容更加容易，
但这些只是指南，而非僵化的规则。

### 变量约定

- `u`、`v`、`w`、…… 用于宇宙
- `α`、`β`、`γ`、…… 用于一般类型
- `a`、`b`、`c`、…… 用于命题
- `x`、`y`、`z`、…… 用于一般类型的元素
- `h`、`h₁`、……     用于假设
- `p`、`q`、`r`、…… 用于谓词和关系
- `s`、`t`、……      用于列表
- `s`、`t`、……      用于集合
- `m`、`n`、`k`、…… 用于自然数
- `i`、`j`、`k`、…… 用于整数

具有数学内涵的类型使用通常的数学记号来表示，
通常用大写字母
（`G` 表示群，`R` 表示环，`K` 或 `𝕜` 表示域，`E` 表示向量空间，……）。
在较旧的文件中并未遵循这一约定，那里所有类型都使用希腊字母。
我们欢迎对这些文件中类型变量进行重命名的拉取请求。

### Unicode 用法

请使用特殊的 Unicode 字符，尤其是[数学符号](https://en.wikipedia.org/wiki/Mathematical_operators_and_symbols_in_Unicode)，凡是有助于形成良好记号并提升可读性之处皆可使用。
请避免使用以下字符：
- 改变文本方向的字符
- 不可见字符（空格和换行符除外）
- 修饰其他字符的字符

Mathlib 有一个 linter，它会对照[允许列表](https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/Tactic/Linter/TextBased/UnicodeLinter.lean)检查所有字符，必要时可向该列表添加新字符。

### 行长度

每行长度不应超过 100 个字符。这使得文件
更易于阅读，尤其是在小屏幕或小窗口中。
如果你使用 VS Code 进行编辑，会有一个
指示 100 字符上限的可视标记。

### 文件头与导入

文件头应包含版权信息、所有对该文件做出
重要贡献的作者列表，以及对内容的描述。
将 `module` 关键字单独放在文件头之后的一行，空一行，
然后将所有 `public import` 归为一组，再空一行，
然后将所有 `import` 归为一组。
请尽量在每个导入块内保持字母顺序。

```lean
/-
Copyright (c) 2024 Joe Cool. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Joe Cool
-/
module

public import Mathlib.Logic.Defs

import Mathlib.Algebra.Group.Defs
import Mathlib.Data.Nat.Basic
```

（提示：如果你在 VS Code 中编辑 mathlib，可以输入 `copy`
然后按 <kbd>TAB</kbd> 来生成版权头的框架。）

关于作者列表：即使只有一位作者，也使用 `Authors`。
行尾不要加句点，并使用逗号（`, `）分隔所有作者姓名
（因此不要在倒数第二位与最后一位作者之间使用 `and`）。
我们对于哪些贡献有资格列入其中并没有严格的规则。
总的思路是，列在那里的人应当是当我们对该 Lean 代码的
设计或开发有疑问时会去联系的人。

注意还有一些不太常见的关键字组合，例如 `public meta import` 或
`import all`。
鉴于它们较为罕见，我们尚未规定它们在导入语句中的相对位置。

### 模块文档字符串

在版权头和导入之后，
请添加一个模块文档字符串（以 `/-!` 和 `-/` 分隔），其中包含

- 文件的标题，
- 内容的摘要（主要定义和定理、证明技巧等……）
- 文件中使用的记号（如果有的话）
- 对文献的引用（如果有的话）

总的来说，模块文档字符串应当看起来像这样：
```markdown
/-!
# Foos and bars

In this file we introduce `foo` and `bar`,
two main concepts in the theory of xyzzyology.

## Main results

- `exists_foo`: the main existence theorem of `foo`s.
- `bar_of_foo_of_baz`: a construction of a `bar`, given a `foo` and a `baz`.
  If this doc-string is longer than one line, subsequent lines should be indented by two spaces
  (as required by markdown syntax).
- `bar_eq`    : the main classification theorem of `bar`s.

## Notation

 - `|_|` : The barrification operator, see `bar_of_foo`.

## References

See [Thales600BC] for the original account on Xyzzyology.
-/
```

新的参考文献条目应添加到 `docs/references.bib` 中。

更多建议和示例请参阅我们的[文档要求](doc.html)。

### 定义和定理的结构

所有声明（例如 `def`、`lemma`、`theorem`、`class`、`structure`、`inductive`、`instance` 等）
和命令（例如 `variable`、`open`、`section`、`namespace`、`notation` 等）都被视为
顶层内容，这些词应当在文档中靠左对齐。特别地，打开一个
命名空间或节并不会导致该命名空间或节的内容缩进。
（注意：在 VS Code 中，将鼠标悬停在任何声明上，例如 `def Foo ...`，会显示完全
限定的名称，例如若 `Foo` 是在命名空间 `MyNamespace` 打开的情况下声明的，则显示 `MyNamespace Foo`。）

这些指南适用于以 `def`、`lemma` 和 `theorem` 开头的声明。
对于“定理陈述”，也应理解为“定义的类型”；对于“证明”，也应理解为
“定义体”。

在“:”、“:=”或中缀运算符两侧使用空格。将它们置于换行之前，
而不是放在下一行的开头。

下文中，凡是未明确指出量的“缩进”都意为
“额外缩进 2 个空格”。

在陈述定理之后，我们将后续证明中的各行缩进 2 个空格。
```lean
open Nat
theorem nat_case {P : Nat → Prop} (n : Nat) (H1 : P 0) (H2 : ∀ m, P (succ m)) : P n :=
  Nat.recOn n H1 (fun m IH ↦ H2 m)
```

如果定理陈述需要多行，则将后续各行缩进 4 个空格。
证明仍然只缩进 2 个空格（*而非* 6 = 4 + 2）。
当以策略模式提供证明时，`by` 放在第一个策略*之前*的那一行；
然而，`by` 不应单独占一行。
实践中这意味着你会经常在定理陈述末尾看到 `:= by`。
```lean
import Mathlib.Data.Nat.Basic

theorem le_induction {P : Nat → Prop} {m}
    (h0 : P m) (h1 : ∀ n, m ≤ n → P n → P (n + 1)) :
    ∀ n, m ≤ n → P n := by
  apply Nat.le.rec
  · exact h0
  · exact h1 _

def decreasingInduction {P : ℕ → Sort*} (h : ∀ n, P (n + 1) → P n) {m n : ℕ} (mn : m ≤ n)
    (hP : P n) : P m :=
  Nat.leRecOn mn (fun {k} ih hsk => ih <| h k hsk) (fun h => h) hP
```

当一个证明项接受多个参数时，有时将某些参数放在后续行上
会更清晰，且往往是必要的。在这种情况下，
缩进每个参数。更一般地，每当一个项跨越多行时，
都适用这条规则，即额外缩进 2 个空格。
```lean
open Nat
axiom zero_or_succ (n : Nat) : n = zero ∨ n = succ (pred n)
theorem nat_discriminate {B : Prop} {n : Nat} (H1: n = 0 → B) (H2 : ∀ m, n = succ m → B) : B :=
  Or.elim (zero_or_succ n)
    (fun H3 : n = zero ↦ H1 H3)
    (fun H3 : n = succ (pred n) ↦ H2 (pred n) H3)
```
不要让括号成为“孤儿”；让它们与其参数保持在一起。

这里有一个较长的示例。
```lean
import Mathlib.Init.Data.List.Lemmas

open List
variable {T : Type}

theorem mem_split {x : T} {l : List T} : x ∈ l → ∃ s t : List T, l = s ++ (x :: t) :=
  List.recOn l
    (fun H : x ∈ [] ↦ False.elim ((mem_nil_iff _).mp H))
    (fun y l ↦
      fun IH : x ∈ l → ∃ s t : List T, l = s ++ (x :: t) ↦
      fun H : x ∈ y :: l ↦
      Or.elim (eq_or_mem_of_mem_cons H)
        (fun H1 : x = y ↦
          Exists.intro [] (Exists.intro l (by rw [H1]; rfl)))
        (fun H1 : x ∈ l ↦
          let ⟨s, (H2 : ∃ t : List T, l = s ++ (x :: t))⟩ := IH H1
          let ⟨t, (H3 : l = s ++ (x :: t))⟩ := H2
          have H4 : y  ::  l = (y :: s) ++ (x :: t) := by rw [H3]; rfl
          Exists.intro (y :: s) (Exists.intro t H4)))
```
声明的所有参数的类型都应显式给出，
即使 Lean 能够自行推断出这些类型信息。
这使得在像 GitHub 这样的网页上看到该定义时更易于理解。
出于同样的原因，所有声明的返回类型也应给出
（Lean 仅对定理强制要求这一点）。
因此你应当遵循此例中 `GoodStatement` 的风格：
```lean
def BadStatement (n) := ∃ k, n + k = 3
def GoodStatement (n : ℕ) : Prop := ∃ k : ℕ, n + k = 3
```

一个简短的声明可以写在单行上：
```lean
open Nat
theorem succ_pos : ∀ n : Nat, 0 < succ n := zero_lt_succ

def square (x : Nat) : Nat := x * x
```

当论证简短时，可以将 `have` 放在单行上。
```lean
example (n k : Nat) (h : n < k) : ... :=
  have h1 : n ≠ k := ne_of_lt h
  ...
```
当论证过长时，你应当将其放在下一行，
额外缩进 2 个空格。
```lean
example (n k : Nat) (h : n < k) : ... :=
  have h1 : n ≠ k :=
    ne_of_lt h
  ...
```
当 `have` 的论证使用策略模式时，无论论证是否
跨越多行，`by` 都应放在同一行上。
```lean
example (n k : Nat) (h : n < k) : ... :=
  have h1 : n ≠ k := by apply ne_of_lt; exact h
  ...

example (n k : Nat) (h : n < k) : ... :=
  have h1 : n ≠ k := by
    apply ne_of_lt
    exact h
  ...
```

当参数本身长到需要换行时，对第一行之后的每一行
都使用额外的缩进，如下例所示：
```lean
import Mathlib.Data.Nat.Basic

theorem Nat.add_right_inj {n m k : Nat} : n + m = n + k → m = k :=
  Nat.recOn n
    (fun H : 0 + m = 0 + k ↦ calc
      m = 0 + m := Eq.symm (zero_add m)
      _ = 0 + k := H
      _ = k     := zero_add _)
    (fun (n : Nat) (IH : n + m = n + k → m = k) (H : succ n + m = succ n + k) ↦
      have H2 : succ (n + m) = succ (n + k) := calc
        succ (n + m) = succ n + m   := Eq.symm (succ_add n m)
        _            = succ n + k   := H
        _            = succ (n + k) := succ_add n k
      have H3 : n + m = n + k := succ.inj H2
      IH H3)
```

在类或结构定义中，字段缩进 2 个空格，
此外每个字段都应有一个文档字符串，如下所示：

```lean
structure PrincipalSeg {α β : Type*} (r : α → α → Prop) (s : β → β → Prop) extends r ↪r s where
  /-- The supremum of the principal segment -/
  top : β
  /-- The image of the order embedding is the set of elements `b` such that `s b top` -/
  down' : ∀ b, s b top ↔ ∃ a, toRelEmbedding a = b

class Module (R : Type u) (M : Type v) [Semiring R] [AddCommMonoid M] extends
    DistribMulAction R M where
  /-- Scalar multiplication distributes over addition from the right. -/
  protected add_smul : ∀ (r s : R) (x : M), (r + s) • x = r • x + s • x
  /-- Scalar multiplication by zero gives zero. -/
  protected zero_smul : ∀ x : M, (0 : R) • x = 0
```

后续的声明之间应以单个换行符分隔。
对于一组类似的单行声明则可作例外。
```lean
theorem foo : True :=
  sorry

theorem bar : False :=
  sorry

@[simp] theorem one_lt_two : 1 < 2 := sorry
@[simp] theorem two_lt_three : 2 < 3 := sorry
```

在定义中使用一个接受多个参数的构造子时，
各参数对齐排列，如下所示：

```lean
theorem Ordinal.sub_eq_zero_iff_le {a b : Ordinal} : a - b = 0 ↔ a ≤ b :=
  ⟨fun h => by simpa only [h, add_zero] using le_add_sub a b,
   fun h => by rwa [← Ordinal.le_zero, sub_le, add_zero]⟩
```

`@[to_additive]` 和 `@[to_dual]` 属性是两种自动化机制，
它们分别为代数中的乘法陈述生成相应的加法版本，
以及为序论/范畴论中的陈述生成相应的对偶版本。
在适用的情况下，应当使用这些属性，
而不是手写第二个陈述。
```lean
@[to_additive] -- generates `add_rotate`
theorem mul_rotate {G : Type*} (a b c : G) : a * b * c = b * c * a := sorry

-- `to_additive` can't be used here because `ℝ` can't be additivised.
theorem mul_rotate' (a b c : ℝ) : a * b * c = b * c * a := sorry
```


### 实例

在提供结构的项或类的实例时，应当使用 `where`
语法，以避免需要包围的花括号，如下所示：

```lean
instance instOrderBot : OrderBot ℕ where
  bot := 0
  bot_le := Nat.zero_le
```

如果已经存在一个实例 `instBot`，则可以写成

```lean
instance instOrderBot : OrderBot ℕ where
  __ := instBot
  bot_le := Nat.zero_le
```

### 冒号左侧的假设

一般而言，如果证明以引入这些变量开始，
那么将参数放在冒号左侧
比放在全称量词或蕴含式中更受青睐。例如：

```lean
example (n : ℝ) (h : 1 < n) : 0 < n := by linarith
```

优于

```lean
example (n : ℝ) : 1 < n → 0 < n := fun h ↦ by linarith
```

而

```lean
example (n : ℕ) : 0 ≤ n := Nat.zero_le n
```

优于

```lean
example : ∀ (n : ℕ), 0 ≤ n := Nat.zero_le
```

注意模式匹配并不算作证明以引入变量开始。
例如，下面就是将假设放在冒号右侧的一个有效用例：

```lean
lemma zero_le : ∀ n : ℕ, 0 ≤ n
  | 0 => le_rfl
  | n + 1 => add_nonneg (zero_le n) zero_le_one
```

### 绑定子

在绑定子之后使用空格。此外，一般应显式写出绑定子的类型，
即使 Lean 并不需要这一信息。
```lean
example : ∀ α : Type, ∀ x : α, ∃ y : α, y = x :=
  fun (α : Type) (x : α) ↦ Exists.intro x rfl
```

### 匿名函数

Lean 为声明匿名函数提供了若干优雅的语法选项。对于非常简单的
函数，可以使用居中的点作为函数参数，例如用 `(· ^ 2)`
表示平方函数。然而，有时需要按名称引用
参数（例如，如果它们在函数体中出现多次）。
Lean 对此的默认写法是 `fun x => x * x`，但 `↦` 箭头（通过 `\mapsto` 输入）
同样有效。在 mathlib 中，美观打印器显示 `↦`，我们在
源代码中也稍微更倾向于使用它。lambda 记号 `λ x ↦ x * x` 虽然在
语法上有效，但在 mathlib 中不被允许，而应使用 `fun` 关键字。

### 计算

在如何书写计算式证明上有一定的灵活性，尽管 `calc` 本身的
语法要求会强制施加一些规则。不过，仍有一些一般性的
指南。

与 `by` 一样，`calc` 关键字应放在计算开始*之前*的那一行上，
而计算内容则缩进。无论涉及哪些关系（例如
`=` 或 `≤`），都应在各行之间对齐。用作各项占位符以指示
计算延续的下划线 `_` 应当左对齐。

至于论证部分，不必对齐 `:=` 符号，但如果表达式足够短，
对齐会显得美观。第一个关系两侧的项既可以
放在一行，也可以放在不同行上，这可根据表达式的大小来决定。

下面是一个适当风格的示例，它能更轻松地容纳较长的表达式：

```lean
import Init.Data.List.Basic

open List

theorem reverse_reverse : ∀ (l : List α), reverse (reverse l) = l
  | []     => rfl
  | a :: l => calc
    reverse (reverse (a :: l))
      = reverse (reverse l ++ [a]) := by rw [reverse_cons]
    _ = reverse [a] ++ reverse (reverse l) := reverse_append _ _
    _ = reverse [a] ++ l := by rw [reverse_reverse l]
    _ = a :: l := rfl
```

下面这种风格有一个显著优势，即所有行都可互换，这在例如
VSCode 中编辑证明时尤为有用：

```lean
import Init.Data.List.Basic

open List

theorem reverse_reverse : ∀ (l : List α), reverse (reverse l) = l
  | []     => rfl
  | a :: l => calc
        reverse (reverse (a :: l))
    _ = reverse (reverse l ++ [a]) := by rw [reverse_cons]
    _ = reverse [a] ++ reverse (reverse l) := reverse_append _ _
    _ = reverse [a] ++ l := by rw [reverse_reverse l]
    _ = a :: l := rfl
```

如果表达式和证明都相对较短，下面这种风格也是一个选择：

```lean
import Init.Data.List.Basic

open List

theorem reverse_reverse : ∀ (l : List α), reverse (reverse l) = l
  | []     => rfl
  | a :: l => calc
    reverse (reverse (a :: l)) = reverse (reverse l ++ [a])         := by rw [reverse_cons]
    _                          = reverse [a] ++ reverse (reverse l) := reverse_append _ _
    _                          = reverse [a] ++ l                   := by rw [reverse_reverse l]
    _                          = a :: l                             := rfl
```

### 策略模式

正如我们已经提到的，在打开一个策略块时，
`by` 放在策略块开始所在行*之前*那一行的末尾，
而不是单独占一行。
策略块内的所有内容都缩进，如下所示：

```lean
theorem continuous_uncurry_of_discreteTopology [DiscreteTopology α] {f : α → β → γ}
    (hf : ∀ a, Continuous (f a)) : Continuous (uncurry f) := by
  apply continuous_iff_continuousAt.2
  rintro ⟨a, x⟩
  change map _ _ ≤ _
  rw [nhds_prod_eq, nhds_discrete, Filter.map_pure_prod]
  exact (hf a).continuousAt
```

可以混用项模式和策略模式，如下所示：
```lean
theorem Units.isUnit_units_mul {M : Type*} [Monoid M] (u : Mˣ) (a : M) :
    IsUnit (↑u * a) ↔ IsUnit a :=
  Iff.intro
    (fun ⟨v, hv⟩ => by
      have : IsUnit (↑u⁻¹ * (↑u * a)) := by exists u⁻¹ * v; rw [← hv, Units.val_mul]
      rwa [← mul_assoc, Units.inv_mul, one_mul] at this)
    u.isUnit.mul
```

当新目标作为附带条件或步骤出现时，它们被缩进，并在前面加上
一个聚焦点 `·`（通过 `\.` 输入）；该点本身不缩进。
```lean
import Mathlib.Algebra.Group.Basic

theorem exists_npow_eq_one_of_zpow_eq_one' [Group G] {n : ℤ} (hn : n ≠ 0) {x : G} (h : x ^ n = 1) :
    ∃ n : ℕ, 0 < n ∧ x ^ n = 1 := by
  cases n
  · simp only [Int.ofNat_eq_coe] at h
    rw [zpow_ofNat] at h
    refine ⟨_, Nat.pos_of_ne_zero fun n0 ↦ hn ?_, h⟩
    rw [n0]
    rfl
  · rw [zpow_negSucc, inv_eq_one] at h
    refine ⟨_ + 1, Nat.succ_pos _, h⟩
```

某些策略，例如 `refine`，可以创建*具名的*子目标，这些子目标
可以使用 `case` 以任意所需的顺序证明。这一特性
也有助于提升可读性。然而，并不强制要求
使用它来代替聚焦点（`·`）。

```lean
example {p q : Prop} (h₁ : p → q) (h₂ : q → p) : p ↔ q := by
  refine ⟨?imp, ?converse⟩
  case converse => exact h₂
  case imp => exact h₁
```

经常使用 `t0 <;> t1` 来执行 `t0`，然后对所有新目标执行 `t1`。
要么将这些策略写在一行，要么将后续策略缩进。

```lean
  cases x <;>
    simp [a, b, c, d]
```

对于单行策略证明（或嵌入在项中的简短策略证明），
可以使用 `by tac1; tac2; tac3`，用分号代替
换行加缩进。

一般而言，你应当每行只放一个策略调用，除非你正在用一个
完全能放进单行的证明来闭合目标。对应于单个数学思想的
简短策略序列也可以放在一行，用分号分隔，例如 `cases bla; clear h`
或 `induction n; simp` 或 `rw [foo]; simp_rw [bar]`，但即便在这些
情形下，仍更倾向于使用换行。

```lean
example : ... := by
  by_cases h : x = 0
  · rw [h]; exact hzero ha
  · rw [h]
    have h' : ... := H ha
    simp_rw [h', hb]
    ...
```

非常简短的目标可以立即使用 `swap` 或 `pick_goal`（如有需要）来闭合，
以避免在证明其余部分中产生额外的缩进。

```lean
example : ... := by
  rw [h]
  swap; exact h'
  ...
```

我们通常使用一个空行来分隔定理和定义，
但这也可以省略，例如，为了将若干
简短的定义归为一组，或将一个定义和记号归为一组。

### 压缩 simp 调用

除非性能特别差或证明会因此中断，否则*终结性 `simp` 调用*
（如果一个 `simp` 调用闭合了当前目标，或其后仅跟随诸如
`ring`、`field_simp`、`aesop` 之类的灵活策略，则它是终结性的）不应被*压缩*（即被 `simp?` 的输出所替换）。

主要有两个原因：
1. 压缩后的 `simp` 调用可能比对应的未压缩调用长好几行，
  因而把添加到未压缩 `simp` 调用中用以闭合目标的那些关键引理这一有用信息
  淹没在大量基础 simp 引理之中。
2. 压缩后的 `simp` 调用按名称引用许多引理，这意味着当其中某个
  引理被重命名时它就会中断。引理重命名发生得足够频繁，
  以至于这在维护层面上是个值得关注的问题。

### 性能剖析

在为 mathlib 做贡献时，作者应当注意其贡献对性能的影响。
Lean FRO 维护着基准测试基础设施，
可以通过在 PR 上评论 `!bench` 来访问。

作者应确保其贡献不会导致显著的
性能退化。特别地，如果该 PR 触及了语言的重要组成部分，
例如添加新的类、实例或 `simp` 引理、更改导入、
创建新定义，或将 `def` 转为 `abbrev`，那么作者应当
主动对其更改进行基准测试。尤其是非平凡的 `refactor` PR
应当进行基准测试，任何显著的负面结果都必须在评审过程中加以解释。

### 透明度与 API 设计

Lean 作为一个实践中高性能的证明助手，其核心在于避免
对非常大的项进行定义性相等的检查。在繁释器（elaborator，
即将语法转换为项的语言组件）中，
透明度（transparency）的概念是避免在不必要时
展开大型定义的主要机制。除 `opaque` 定义外，透明度
共有三个级别：
- `reducible` 定义总是被展开
- `semireducible` 定义（默认）在诸如 `rw` 和 `simp` 之类的主要策略中通常不被展开，
    但稍加努力即可展开，例如显式调用 `rfl` 或 `erw`。在计算用于将实例存入
    实例缓存或将 simp 引理存入 simp 缓存的键时，semireducible 定义也不会被展开。
- `irreducible` 定义永远不会被展开，除非用户显式
    请求（例如使用 `unfold` 策略，或使用 `unseal` 命令）。

`def` 默认创建 `semireducible` 定义，`abbrev` 创建
`reducible`（且 `@[inline]`）定义。

在设计定义时，作者应当对定义的透明度级别加以思考。
考虑暴露定义的底层项将如何
影响实例搜索和化简。mathlib 的默认做法是，定义
应当是 `semireducible`，除非有充分的理由不这样做，且该理由
应当在 PR 描述中清楚地说明。这会给
贡献者带来额外负担，他们将需要声明形如
```lean4
instance : Foo myDef := inferInstanceAs (Foo underlyingTermOfMyDef)
```
的新实例，并复用 API 引理，尤其是供 `simp` 使用的引理，例如
```lean4
@[simp] lemma myDef_bar_eq_bizz (x : X) : myDef.bar = bizz :=
    underlyingTermOfMyDef_bar_eq_bizz
```

如果意在使 API 边界完全封闭，则使用形如
```lean4
structure myDef where
    underlying : underlyingTerm
```
的类型同义词是库的惯例，以代替 `irreducible` 定义。这些结构包装器
意在用于那些与某个现有类型等价、但在数学语义上明显
有别的类型，例如 `Option` 和 `WithTop`。

内核并没有类似的透明度概念，因此其
展开规则是不同的。在某些情况下，作者也想
阻止内核进行展开。Mathlib 为此提供了一个命令
`irreducible_def`。只有当剖析表明确有
必要时才应使用它。

在诸如 `simp` 或 `rw` 这类以 reducible 透明度运作的策略之后
使用 `erw` 或 `rfl`，表明缺失了某些 API。
请考虑向 API 添加必要的引理以避免这种情况。

库中存在着滥用定义性透明度的现有情形，
例如 `erw` 和多余的 `rfl`。我们非常欢迎移除这些的 PR，但其 PR
描述应当清楚地说明移除是如何实现的，尤其要说明
底层项的变化，并且必须对其更改进行基准测试。
请将此视为改进相关组件 API 设计的
机会。

### 空白与定界符

Lean 对空白敏感，一般而言我们选择一种避免
为代码加定界符的风格。例如，在书写策略时，可以将
它们写成 `tac1; tac2; tac3`，用 `;` 分隔，以覆盖默认的
空白敏感性。然而，如上所述，除少数特殊情况外，我们通常都尽量避免
这样做。

类似地，有时可以通过明智地使用 `<|`
运算符（或它的近亲 `|>`）来避免使用括号。注意：虽然 `$` 是 `<|`
的同义词，但在 mathlib 中不允许使用它，而应使用 `<|`，以保持一致性，
也因为它与 `|>` 的对称性。这些运算符的作用是
为 `<|` 右侧的所有内容加括号（注意 `(` 的弯曲方向与 `<`
相同），或为 `|>` 左侧的所有内容加括号（且 `)` 的弯曲方向与
`>` 相同）。

`|>` 用法的一个常见例子出现在点记号中，当 `.`
之前的项是一个被应用于某些参数的函数时。例如，
`((foo a).bar b).baz` 可以重写为 `foo a |>.bar b |>.baz`

`<|` 用法的一个常见例子是，当用户提供的项
是一个被应用于多个参数的函数，而其最后一个参数是策略模式下的证明，
尤其是跨越多行的证明时。在这种情况下，
使用 `<| by ...` 代替 `(by ...)` 是很自然的，如下所示：

```lean
import Mathlib.Tactic

example {x y : ℝ} (hxy : x ≤ y) (h : ∀ ε > 0, y - ε ≤ x) : x = y :=
  le_antisymm hxy <| le_of_forall_pos_le_add <| by
    intro ε hε
    have := h ε hε
    linarith
```

当使用策略 `rw` 或 `simp` 时，左箭头 `←` 之后应有一个空格。
例如 `rw [← add_comm a b]` 或 `simp [← and_or_left]`。
（在策略名称及其参数之间也应有一个空格，例如 `rw [h]`。）
这条规则同样适用于 `do` 记号：`do return (← f) + (← g)`

### 声明内部的空行

不鼓励在声明内部使用空行，并且有一个 linter 会强制
要求它们不出现。这有助于在整个 mathlib 中
维持统一的代码风格。

不过，我们鼓励你为代码添加注释：即便是一句短短的话，
也比一个置于证明中间的空行所传达的*多得多*！

### 规范形式

某些陈述是等价的。例如，要求某个类型的子集 `s`
非空有若干等价的方式。再举一个例子，给定
`a : α`，`Option α` 中对应的元素既可以等价地写成
`Some a`，也可以写成 `(a : Option α)`。一般而言，我们尽量确定
一种标准形式，称为规范形式，并在定理的陈述和
结论中都使用它。在上述例子中，这将分别是 `s.Nonempty`（它
让我们能使用点记号）和 `(a : Option α)`。通常会注册一些 simp 引理，
以将其他等价形式转换为规范形式。

这条规则有一种特殊情况。在带有最小元素的类型中，
要求 `hlt : ⊥ < x` 与 `hne : x ≠ ⊥` 是等价的，由于两者各有利弊，
并不清楚哪一个作为规范形式更好。在带有最大元素的类型中，
`hlt : x < ⊤` 与 `hne : x ≠ ⊤` 也出现类似的情形。由于从 `hlt`
转换到 `hne` 非常容易（根据所需的方向使用 `hlt.ne` 或 `hlt.ne'`），
而反向转换则更为冗长，因此我们在定理的*假设*中使用 `hne`
（因为这是更容易检验的假设），而在定理的*结论*中使用 `hlt`
（因为这是更强有力可用的结果）。
这条规则的一个常见用法是在自然数上，那里 `⊥ = 0`。

### 注释

使用模块文档定界符 `/-! -/` 来提供节标题和
分隔符，因为它们会被纳入自动生成的文档，
并使用 `/- -/` 来书写更具技术性的注释（例如 TODO 和
实现说明），或证明中的注释。
使用 `--` 来书写简短的或行内的注释。

声明的文档字符串以 `/-- -/` 定界。
当一个声明的文档字符串跨越多行时，不要缩进
后续各行。

更多建议和示例请参阅我们的[文档要求](doc.html)。

### 错误或追踪消息中的表达式

在所有打印出的消息中（例如在 linter、自定义繁释器或其他元程序中），
名称和内插数据应当要么
- 内联并以反引号包围（例如 `m!"`{foo}` must have type `{bar}`"`），要么
- 单独占一行并缩进（例如通过 `indentD`）

第二种风格产生如下的输出
```
Could not find model with corners for domain
  src
nor codomain
  tgt
of function
  f
```

mathlib 并非所有部分都已遵循这条规则；那属于 bug（我们欢迎修复此问题的 PR）。

### 弃用

删除、重命名或更改声明可能导致依赖这些
定义的下游项目编译失败。
任何正在被移除的公开暴露的定理和定义都应当通过保留旧声明
并附加 `@[deprecated]` 属性来平稳过渡。
这会向下游项目警示该更改，并给予他们机会，在这些声明被删除之前
作出调整。
被重命名的定义应当使用一个弃用的 `alias` 指向新名称。
否则，当被弃用的定义没有直接替代品时，应当
用一条消息来弃用该定义，如下所示：

```lean4
theorem new_name : ... := ...
@[deprecated (since := "YYYY-MM-DD")] alias old_name := new_name

@[deprecated "This theorem is deprecated in favor of using ... with ..." (since := "YYYY-MM-DD")]
theorem example_thm ...
```

`@[deprecated]` 属性要求给出弃用日期，以及一个指向新声明的别名，
或一条字符串，用以说明在不再提供新版本时如何从旧定义过渡开。

[`deprecate to`](/mathlib4_docs/Mathlib/Tactic/DeprecateTo.html) 命令和
`scripts/add_deprecations.sh` 脚本可以帮助生成别名定义。

对于带有 `to_additive` 属性的声明，其弃用应确保该弃用
也正确地被打上 `to_additive` 标签，如下所示：
```lean4
@[to_additive] theorem Group_bar {G} [Group G] {a : G} : a = a := rfl

-- Two deprecations required to include the `deprecated` tag on both the additive
-- and multiplicative versions
@[deprecated (since := "YYYY-MM-DD")] alias AddGroup_foo := AddGroup_bar
@[to_additive existing, deprecated (since := "YYYY-MM-DD")] alias Group_foo := Group_bar
```

我们允许、但不鼓励贡献者同时将声明 X 重命名为 Y 以及将 W 重命名为 X。
在这种情况下，X 不需要弃用属性，但 W 需要。

具名实例不需要弃用。被弃用的声明可以在 6 个月后删除。

### 避免 `nonrec`

`nonrec` 关键字告诉 Lean 假定声明体中那些貌似递归的调用
实际上并非递归，而是去其他命名空间中查找同名的声明。
当递归调用与*某个命名空间中*的另一个声明冲突时，请避免使用 `nonrec`，因为此时将该命名空间添加到那个声明上更具信息量（对 Lean 和用户都是如此）。如果它与根命名空间中的某个声明冲突，那么 `nonrec` 和 `_root_.[...]` 都是可以接受的。有时，避免使用 `nonrec` 需要放弃在该声明体内使用点记号。
（目前 Mathlib 中有许多地方违反了这条规则。）
