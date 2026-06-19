# Mathlib 命名约定

本指南针对 Lean 4 编写。

## 文件名

mathlib 中的 `.lean` 文件一般应采用 `UpperCamelCased` 命名。
一个（极为罕见的）例外是以某个特定小写对象命名的文件，例如 `lp.lean` 用于专门讨论空间 $\ell_p$（而非 $L^p$）的文件。
此类例外应先在 Zulip 上讨论。

## 一般约定

### 大小写

与 Lean 3 不同（在 Lean 3 中约定所有声明都使用 `snake_case`），
在 Lean 4 下的 mathlib 中，我们根据以下命名方案，混合使用 `snake_case`、`lowerCamelCase` 和
`UpperCamelCase`。

1. `Prop` 的项（例如证明、定理名）使用 `snake_case`。
2. `Prop` 与 `Type`（或 `Sort`）（归纳类型、结构、类）使用 `UpperCamelCase`。
存在一些罕见的例外：某些结构的字段目前被错误地小写化了（见下面关于类 `LT` 的示例）。
3. 函数的命名方式与其返回值相同（例如，类型为 `A → B → C` 的函数，其命名方式如同它是类型 `C` 的一个项）。
4. 所有其他 `Type` 的项（基本上就是其余的一切）使用 `lowerCamelCase`。
5. 当一个以 `UpperCamelCase` 命名的事物作为某个以 `snake_case` 命名的事物的一部分时，它以 `lowerCamelCase` 引用。
6. 像 `LE` 这样的首字母缩写词作为一个整体写成全大写或全小写，取决于其首字符本应是什么。
7. 规则 1-6 以同样的方式适用于结构的字段或归纳类型的构造子。

为保持局部命名的对称性，存在一些罕见的例外：例如，我们使用 `Ne` 而非 `NE`，以遵循 `Eq` 的范例；`outParam` 的输出是 `Sort` 但并不采用 `UpperCamelCase`。其他一些例外包括区间（`Set.Icc`、`Set.Iic` 等），其中 `I`
被大写，尽管按照约定它本应是 `lowerCamelCase`。任何此类例外都应在 Zulip 上讨论。

#### 示例

```lean
-- follows rule 2
structure OneHom (M : Type _) (N : Type _) [One M] [One N] where
  toFun : M → N -- follows rule 4 via rule 3 and rule 7
  map_one' : toFun 1 = 1 -- follows rule 1 via rule 7

-- follows rule 2 via rule 3
class CoeIsOneHom [One M] [One N] : Prop where
  coe_one : (↑(1 : M) : N) = 1 -- follows rule 1 via rule 6

-- follows rule 1 via rule 3
theorem map_one [OneHomClass F M N] (f : F) : f 1 = 1 := sorry

-- follows rules 1 and 5
theorem MonoidHom.toOneHom_injective [MulOneClass M] [MulOneClass N] :
  Function.Injective (MonoidHom.toOneHom : (M →* N) → OneHom M N) := sorry

-- follows rule 2
class HPow (α : Type u) (β : Type v) (γ : Type w) where
  hPow : α → β → γ -- follows rule 3 via rule 6; note that rule 5 does not apply

-- follows rules 2 and 6
class LT (α : Type u) where
  lt : α → α → Prop -- this is an exception to rule 2

-- follows rules 2 (for `Semifield`) and 4 (for `toIsField`)
theorem Semifield.toIsField (R : Type u) [Semifield R] :
    IsField R -- follows rule 2

-- follows rules 1 and 6
theorem gt_iff_lt [LT α] {a b : α} : a > b ↔ b < a := sorry

-- follows rule 2; `Ne` is an exception to rule 6
class NeZero : Prop := sorry

-- follows rules 1 and 5
theorem neZero_iff {R : Type _} [Zero R] {n : R} : NeZero n ↔ n ≠ 0 := sorry
```

### 拼写

声明名使用美式英语拼写。因此，例如我们使用
`factorization`、`Localization` 和 `FiberBundle`，而不使用
`factorisation`、`Localisation` 或 `FibreBundle`。
这与[文档](doc.html#language)的规则形成对比，文档允许使用其他常见的英语拼写。

### 符号的名称

在将定理的陈述翻译成文字时，常使用下面的对照表。

#### 逻辑

| symbol | shortcut | name                      | notes                                                               |
|--------|----------|---------------------------|---------------------------------------------------------------------|
| `∨`    | `\or`    | `or`                      |                                                                     |
| `∧`    | `\and`   | `and`                     |                                                                     |
| `→`    | `\r`     | `of` / `imp`              | 结论先陈述，假设常常省略 |
| `↔`    | `\iff`   | `iff`                     | 有时连同 iff 的右侧一并省略 |
| `¬`    | `\n`     | `not`                     |                                                                     |
| `∃`    | `\ex`    | `exists` / `bex`          | `bex` 表示 "bounded exists"（有界存在） |
| `∀`    | `\fo`    | `all` / `forall` / `ball` | `ball` 表示 "bounded forall"（有界全称） |
| `=`    |          | `eq`                      | 常常省略 |
| `≠`    | `\ne`    | `ne`                      |                                                                     |
| `∘`    | `\o`     | `comp`                    |                                                                     |

`ball` 与 `bex` 仍在 Lean core 中使用，但不应在 mathlib 中使用。

#### 集合

| symbol                      | shortcut    | name                 | notes                                         |
|-----------------------------|-------------|----------------------|-----------------------------------------------|
| `∈`                         | `\in`       | `mem`                |                                               |
| `∉`                         | `\notin`    | `notMem`             |                                               |
| `∪`                         | `\cup`      | `union`              |                                               |
| `∩`                         | `\cap`      | `inter`              |                                               |
| `⋃`                         | `\bigcup`   | `iUnion` / `biUnion` | `i` 表示 "indexed"（带索引），`bi` 表示 "bounded indexed"（有界带索引） |
| `⋂`                         | `\bigcap`   | `iInter` / `biInter` | `i` 表示 "indexed"（带索引），`bi` 表示 "bounded indexed"（有界带索引） |
| `⋃₀`                        | `\bigcup\0` | `sUnion`             | `s` 表示 "set"（集合） |
| `⋂₀`                        | `\bigcap\0` | `sInter`             | `s` 表示 "set"（集合） |
| `\`                         | `\\`        | `sdiff`              |                                               |
| `ᶜ`                         | `\^c`       | `compl`              |                                               |
| <code>{x &#124; p x}</code> |             | `setOf`              |                                               |
| `{x}`                       |             | `singleton`          |                                               |
| `{x, y}`                    |             | `pair`               |                                               |

#### 代数

| symbol | shortcut              | name          | notes                                                       |
| ------ | --------------------- | ------------- | ----------------------------------------------------------- |
| `0`    |                       | `zero`        |                                                             |
| `+`    |                       | `add`         |                                                             |
| `-`    |                       | `neg` / `sub` | `neg` 用于一元函数，`sub` 用于二元函数 |
| `1`    |                       | `one`         |                                                             |
| `*`    |                       | `mul`         |                                                             |
| `^`    |                       | `pow`         |                                                             |
| `/`    |                       | `div`         |                                                             |
| `•`    | `\bu`                 | `smul`        |                                                             |
| `⁻¹`   | `\-1`                 | `inv`         |                                                             |
| `⅟`    | `\frac1`              | `invOf`       |                                                             |
| `∣`    | <code>\\&#124;</code> | `dvd`         |                                                             |
| `∑`    | `\sum`                | `sum`         |                                                             |
| `∏`    | `\prod`               | `prod`        |                                                             |

#### 格

| symbol | shortcut | name                       | notes                            |
|--------|----------|----------------------------|----------------------------------|
| `<`    |          | `lt` / `gt`                |                                  |
| `≤`    | `\le`    | `le` / `ge`                |                                  |
| `⊔`    | `\sup`   | `sup`                      | 二元运算符 |
| `⊓`    | `\inf`   | `inf`                      | 二元运算符 |
| `⨆`    | `\supr`  | `iSup` / `biSup` / `ciSup` | `c` 表示 "conditionally complete"（条件完备） |
| `⨅`    | `\infi`  | `iInf` / `biInf` / `ciInf` | `c` 表示 "conditionally complete"（条件完备） |
| `⊥`    | `\bot`   | `bot`                      |                                  |
| `⊤`    | `\top`   | `top`                      |                                  |

符号 `≤` 与 `<` 有一个特殊的命名约定。
在 mathlib 中，我们几乎总是使用 `≤` 与 `<` 而非 `≥` 与 `>`，因此我们可以用 `le`/`lt` 和 `ge`/`gt` 来为 `≤` 与 `<` 命名。
使用 `ge`/`gt` 有几个理由：

1. 当 `≤` 或 `<` 的参数以不同顺序出现时，我们使用 `ge`/`gt`。
  对于定理名中第一次出现的 `≤`/`<`，我们使用 `le`/`lt`，
  随后用 `ge`/`gt` 来表示参数被交换了。
2. 我们使用 `ge`/`gt` 以匹配另一个关系（如 `=` 或 `≠`）的参数顺序。
3. 我们使用 `ge`/`gt` 来描述参数被交换后的 `≤` 或 `<` 关系。
4. 当 `≤` 或 `<` 的第二个参数“更具变动性”时，我们使用 `ge`/`gt`。
```lean
-- follows rule 1
theorem lt_iff_le_not_ge [Preorder α] {a b : α} : a < b ↔ a ≤ b ∧ ¬b ≤ a := sorry
theorem not_le_of_gt [Preorder α] {a b : α} (h : a < b) : ¬b ≤ a := sorry
theorem LT.lt.not_ge [Preorder α] {a b : α} (h : a < b) : ¬b ≤ a := sorry

-- follows rule 2
theorem Eq.ge [Preorder α] {a b : α} (h : a = b) : b ≤ a := sorry
theorem ne_of_gt [Preorder α] {a b : α} (h : b < a) : a ≠ b := sorry

-- follows rule 3
theorem ge_trans [Preorder α] {a b : α} : b ≤ a → c ≤ b → c ≤ a := sorry

-- follows rule 4
theorem le_of_forall_gt [LinearOrder α] {a b : α} (H : ∀ (c : α), a < c → b < c) : b ≤ a := sorry
```

### 强制转换

强制转换（coercion）以其底层函数命名。
```lean
-- Named after `Subtype.val`
theorem Subtype.val_injective {p : α → Prop} : ((↑) : {a : α // p a} → α).Injective := sorry

-- Named after `ENNReal.ofNNReal`
theorem ENNReal.ofNNReal_injective : ((↑) : ℝ≥0 → ℝ≥0∞).Injective := sorry

-- Named after `DFunLike.coe`
theorem DFunLike.coe_injective {F α : Sort*} {β : α → Sort*} [DFunLike F α β] :
    ((↑) : F → ∀ a, β a).Injective := sorry

-- Named after `SetLike.coe`
theorem SetLike.coe_injective {α β : Type*} [SetLike α β] :
    ((↑) : α → Set β).Injective := sorry
```
当类型支持多种自然的强制转换时，这有助于消歧义，
其动机在于强制转换是可约的（reducible）。
在 Lean 3 中并非如此，因此许多名称仍然是错误的。

### 点号

点号用于命名空间，也用于自动生成的名称，
例如递归子（recursor）、消去子（eliminator）和结构投影。它们也可以
手动引入，例如在投影记法很有用的场合。因此，它们用于以下所有情形。

注意：由于 `And` 是一个（值为 `Prop` 的二元函数），按照命名约定它采用 `UpperCamelCase`，
因此其命名空间为 `And.*`。
这看起来似乎与对照表中 `∧` --> `and` 相矛盾，但因为
大驼峰式的类型在定理名中出现时会被转为小驼峰式，
所以该对照表整体上仍然有效。同样的情形适用于
`Or`、`Iff`、`Not`、`Eq`、`HEq`、`Ne` 等。

逻辑联结词的引入（intro）、消去（elim）和析构（destruct）规则，
无论它们是否自动生成：

- `And.intro`
- `And.elim`
- `And.left`
- `And.right`
- `Or.inl`
- `Or.inr`
- `Or.intro_left`
- `Or.intro_right`
- `Iff.intro`
- `Iff.elim`
- `Iff.mp`
- `Iff.mpr`
- `Not.intro`
- `Not.elim`
- `Eq.refl`
- `Eq.rec`
- `Eq.subst`
- `HEq.refl`
- `HEq.rec`
- `HEq.subst`
- `Exists.intro`
- `Exists.elim`
- `True.intro`
- `False.elim`

投影记法有用的场合，例如：

- `And.symm`
- `Or.symm`
- `Or.resolve_left`
- `Or.resolve_right`
- `Eq.symm`
- `Eq.trans`
- `HEq.symm`
- `HEq.trans`
- `Iff.symm`
- `Iff.refl`

即使对于并非归纳类型的类型，使用点号记法也是有益的。例如，我们使用：

- `LE.trans`
- `LT.trans_le`
- `LE.trans_lt`

### 公理化描述

某些定理使用公理化名称来描述，而非
描述其结论。

- `def`（用于展开定义）
- `refl`
- `irrefl`
- `symm`
- `trans`
- `antisymm`
- `asymm`
- `congr`
- `comm`
- `assoc`
- `left_comm`
- `right_comm`
- `mul_left_cancel`
- `mul_right_cancel`
- `inj`（injective，单射）

### 变量约定

- `u`、`v`、`w`、…… 用于宇宙
- `α`、`β`、`γ`、…… 用于一般类型
- `a`、`b`、`c`、…… 用于命题
- `x`、`y`、`z`、…… 用于一般类型的元素
- `h`、`h₁`、…… 用于假设
- `p`、`q`、`r`、…… 用于谓词和关系
- `s`、`t`、…… 用于列表
- `s`、`t`、…… 用于集合
- `m`、`n`、`k`、…… 用于自然数
- `i`、`j`、`k`、…… 用于整数

具有数学内涵的类型用通常的数学记法表示，
常常使用大写字母
（`G` 表示群，`R` 表示环，`K` 或 `𝕜` 表示域，`E` 表示向量空间，……）。
在较旧的文件中并未遵循这一约定，那里所有类型都使用希腊字母。
欢迎提交重命名这些文件中类型变量的拉取请求。

## 标识符与定理名

我们采用以下命名准则，以便用户
更容易猜出定理的名称，或借助 tab 补全找到它。诸如合取或
析取这样的运算的常见“公理化”性质，被放在以该
运算名称开头的命名空间中：

```lean
import Mathlib.Logic.Basic

#check And.comm
#check Or.comm
```

特别地，这包括逻辑联结词的 `intro` 和 `elim` 运算，以及关系的性质：

```lean
import Mathlib.Logic.Basic

#check And.intro
#check And.elim
#check Or.intro_left
#check Or.intro_right
#check Or.elim

#check Eq.refl
#check Eq.symm
#check Eq.trans
```

然而请注意，对于公理化的逻辑和算术运算，我们并不这样做。

```lean
import Mathlib.Algebra.Group.Basic

#check and_assoc
#check mul_comm
#check mul_assoc
#check @mul_left_cancel  -- multiplication is left cancelative
```

不过在大多数情况下，我们依赖描述性名称。定理的名称
往往直接描述其结论：

```lean
import Mathlib.Algebra.Ring.Basic
open Nat
#check succ_ne_zero
#check mul_zero
#check mul_one
#check @sub_add_eq_add_sub
#check @le_iff_lt_or_eq
```

如果描述的一个前缀就足以传达含义，
名称可以变得更短：

```lean
import Mathlib.Algebra.Ring.Basic

#check @neg_neg
#check Nat.pred_succ
```

当一个运算以中缀形式书写时，定理名也随之而行。例如，
我们写 `neg_mul_neg` 而非 `mul_neg_neg`，
以描述模式 `-a * -b`。

有时，为消除定理名称的歧义或更好地传达
其意图，有必要描述某些
假设。词 "of" 用于分隔这些假设：

```lean
import Mathlib.Algebra.Order.Monoid.Lemmas

open Nat

#check lt_of_succ_le
#check lt_of_not_ge
#check lt_of_le_of_ne
#check add_lt_add_of_lt_of_le
```

这些假设按它们出现的顺序列出，_而非_ 逆序。
例如，定理 `A → B → C` 将被命名为
`C_of_A_of_B`。

有时缩写或替代描述更便于使用。例如，我们使用 `pos`、`neg`、`nonpos`、`nonneg` 而非
`zero_lt`、`lt_zero`、`le_zero` 和 `zero_le`。

```lean
import Mathlib.Algebra.Order.Monoid.Lemmas
import Mathlib.Algebra.Order.Ring.Lemmas

open Nat

#check mul_pos
#check mul_nonpos_of_nonneg_of_nonpos
#check add_lt_of_lt_of_nonpos
#check add_lt_of_nonpos_of_lt
```

这些约定并不完美。它们无法区分仅在结合性上不同的
复合表达式，也无法区分某个模式中重复出现的部分。对此，我们只能尽力而为。例如，`a + b - b = a`
既可命名为 `add_sub_self`，也可命名为 `add_sub_cancel`。

有时词 "left" 或 "right" 有助于描述一个定理的
不同变体。

```lean
import Mathlib.Algebra.Order.Monoid.Lemmas
import Mathlib.Algebra.Order.Ring.Lemmas

open Nat

#check add_le_add_left
#check add_le_add_right
#check le_of_mul_le_mul_left
#check le_of_mul_le_mul_right
```

当在某个引理名中引用一个不在同一命名空间下的、带命名空间的定义时，
应去掉该定义的命名空间。如果
去掉命名空间后定义名仍无歧义，则可直接
使用。否则，将命名空间以
`lowerCamelCase` 形式重新加回。这是为了确保引理名中
由 `_` 分隔的字符串对应于某个定义名或联结词。
```lean
import Mathlib.Data.Int.Cast.Basic
import Mathlib.Data.Nat.Cast.Basic
import Mathlib.Topology.Constructions

#check Prod.fst
#check continuous_fst

#check Nat.cast
#check map_natCast
#check Int.cast_natCast
```

## 结构性引理的命名

我们正力图为某些结构性引理标准化特定的命名模式。

### 外延性

形如 `(∀ x, f x = g x) → f = g` 的引理应命名为 `.ext`，
并标注 `@[ext]` 属性。
这类引理常常可以通过在某个结构上标注
`@[ext]` 属性来自动生成。
（不过，自动生成的引理总是以结构投影来表述，
而往往存在一个更好的陈述，
例如使用强制转换的陈述，此时应手动书写并标注 `@[ext]`。）

形如 `f = g ↔ ∀ x, f x = g x` 的引理应命名为 `.ext_iff`。

### 单射性

在可能的情况下，单射性引理应以
`Function.Injective f` 作为结论来表述，并使用完整单词 `injective`，通常形如 `f_injective`。
形式 `injective_f` 在 mathlib 中仍频繁出现。

除此之外，通常还应提供一个双向蕴含的变体，
例如形如 `f x = f y ↔ x = y`，它可由 `Function.Injective.eq_iff` 得到。
此类引理应命名为 `f_inj`
（不过若它们位于合适的命名空间中，`.inj` 也很好）。
双向单射性引理常常是适合标注 `@[simp]` 的候选。
mathlib 中仍有许多名为 `inj` 的单向蕴含，
在遇到它们时予以更新和替换是合理的。

不过请注意，归纳类型的构造子有
自动生成的单向蕴含，命名为 `.inj`，
并且无意更改这一点。
当这样一个自动生成的引理已经存在，
而又需要一个双向引理时，可将其命名为 `.inj_iff`。

使用 "left" 或 "right" 的单射性引理应指向那个“发生变化”的
参数。例如，陈述为
`a - b = a - c ↔ b = c` 的引理可命名为 `sub_right_inj`。

### 归纳与递归原理

归纳/递归原理是为某个类型 `T` 的所有元素构造数据或证明的方式，
其途径是提供在更受约束的特定情形下构造此数据或证明的方法。
这些原理应被表述为接受一个 `motive` 参数，
它声明了我们要对所有 `T` 证明什么性质或构造什么数据。
当 motive 消去到 `Prop` 时，它是一个归纳原理，名称中应包含
`induction`。另一方面，当 motive 消去到 `Sort u` 或 `Type u` 时，
它是一个递归原理，名称中应改为包含 `rec`。

此外，当且仅当在参数顺序中值先于构造出现时，名称中才应包含 `on`。

下表概括了这些命名约定：

| motive 消去到： | `Prop`           | `Sort u` 或 `Type u` |
|-------------------------|------------------|----------------------|
| 值在先             | `T.induction_on` | `T.recOn`            |
| 构造在先     | `T.induction`    | `T.rec`              |

必要时（例如为消歧义）可对这些名称做变体。

### 作为后缀的谓词

大多数谓词应作为前缀添加。例如 `IsClosed (Icc a b)` 应命名为 `isClosed_Icc`，而非 `Icc_isClosed`。

某些广泛使用的谓词不遵循这一规则。它们是那些与某个已按命名约定加上后缀的原子相类似的谓词。以下是一个非穷尽的列表：
* 我们用 `_inj` 表示 `f a = f b ↔ a = b`，因此也用 `_injective` 表示 `Injective f`、`_surjective` 表示 `Surjective f`、`_bijective` 表示 `Bijective f`……
* 我们用 `_mono` 表示 `a ≤ b → f a ≤ f b`、`_anti` 表示 `a ≤ b → f b ≤ f a`，因此也用 `_monotone` 表示 `Monotone f`、`_antitone` 表示 `Antitone f`、`_strictMono` 表示 `StrictMono f`、`_strictAnti` 表示 `StrictAnti f` 等等……

作为后缀的谓词之前可以加上 `_left` 或 `_right`，以表明
一个二元运算是左单调或右单调的。
例如，`mul_left_monotone : Monotone (· * a)` 证明的是乘法的左单调性，
而非左乘的单调性。

### 取值为 Prop 的类

mathlib 有许多取值为 `Prop` 的类以及其他定义。例如“设 $R$ 为一个
拓扑环”写作 `variable (R : Type*) [Ring R] [TopologicalSpace R] [IsTopologicalRing R]`，
而“设 $G$ 为一个群，$H$ 为一个正规子群”写作
`variable (G : Type*) [Group G] (H : Subgroup G) [Normal H]`。这里 `IsTopologicalRing R`
与 `Normal H` 并非额外的数据，而是对我们已有数据所施加的额外假设。

对于这些取值为 `Prop` 的类，mathlib 目前力图遵循以下命名约定。如果该类是一个名词，则其名称应以 `Is` 开头。然而如果它是一个形容词，则其名称无需以 `Is` 开头。例如，对于“正规子群”类型类，`IsNormal` 是可接受的，但 `Normal` 也可以；在非正式语言中我们会说“假设子群
`H` 是正规的”。然而对于“拓扑环”类型类，`IsTopologicalRing` 更
受青睐，因为我们在非正式语言中不会说“假设环 `R` 是
拓扑的”。

### 函数的未展开形式与展开形式

两个函数 `f` 与 `g` 的乘法可以等价地记作
`f * g` 或 `fun x ↦ f x * g x`。这两个表达式在定义上相等，但在语法上不相等（且它们在索引树中不共享同一键），这意味着诸如 `rw`、`fun_prop` 或 `apply?`
之类的工具不会将一种形式的定理用于另一种形式的表达式。因此，
有时同时提供使用这两种形式的陈述变体是方便的。如果需要
区分它们，涉及第一种未展开形式的陈述仅用 `mul` 来书写，
而使用第二种展开形式的陈述则应改用 `fun_mul`。如果由于某个引理只以展开形式给出而无需
消歧义，则前缀 `fun_` 不是必需的。

例如，两个连续函数的乘法是连续的这一事实为
```lean
theorem Continuous.fun_mul (hf : Continuous f) (hg : Continuous g) : Continuous fun x ↦ f x * g x
```
以及
```lean
theorem Continuous.mul (hf : Continuous f) (hg : Continuous g) : Continuous (f * g)
```
这两个定理都值得标注 `fun_prop` 属性。

加法、减法、取负、幂以及函数的复合也是如此。
