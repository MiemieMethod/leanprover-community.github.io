# Lean 中的数学：集合与类集合对象

### 列表（Lists）

#### `Mathlib.Data.List.Basic`

`List α` 是由类型 `α` 的元素构成的列表的类型。列表是有限且有序的，并且可以包含重复元素。列表只能包含同一类型的元素。列表通过 cons 函数构造，该函数将一个 `α` 类型的元素追加到列表的顶端。关于列表的更多讨论见 TPIL 第 7.5 章。

`[1, 1, 2, 4] ≠ [1, 2, 1, 4]`

`[1, 2, 1, 4] ≠ [1, 2, 4]`

### 多重集（Multisets）

#### `Mathlib.Data.Multiset.Basic`

`Multiset α` 是由类型 `α` 的元素构成的多重集的类型。多重集是有限的，可以包含重复元素，但不是有序的。它们被定义为列表对 `Perm` 等价关系的商。多重集只能包含同一类型的元素。

`{1, 1, 2, 4} = {1, 2, 1, 4}`

`{1, 1, 2, 4} ≠ {1, 2, 4}`

### Finset（有限集）

#### `Mathlib.Data.Finset.Basic`

`Finset α` 是由类型 α 的互不相同的元素构成的无序列表的类型。一个 finset 由一个多重集以及该多重集不含重复元素的证明构造而成。finset 是有限的。finset 只能包含同一类型的元素。

`{1, 1, 2, 4} = {1, 2, 1, 4}`

`{1, 1, 2, 4} = {1, 2, 4}`

### 集合与子类型

#### `Mathlib.Data.Set.Basic`

`Set α`。集合被定义为一个谓词，即一个函数 `α → Prop`。所使用的记号如 `{n : ℕ | 4 ≤ n}` 表示大于或等于 4 的自然数构成的集合。集合可以是无限的，并且只能包含同一类型的元素。

子类型与集合类似，也是由一个谓词所定义。所使用的记号如 `{n : ℕ // 4 ≤ n}` 表示大于或等于 4 的自然数构成的类型。然而，子类型是一个类型而非集合，并且上述子类型的元素并不具有类型 `ℕ`，而是具有类型 `{n : ℕ // 4 ≤ n}`。这意味着加法在该类型上没有定义，自然数与该类型之间的相等关系也没有定义。不过，可以将该子类型的元素强制转换回自然数，正如自然数可以强制转换为整数那样，转换之后加法与相等便如常运作（关于强制转换的更多内容见 TPIL 第 6.7 章）。要构造 α 的某个子类型的元素，你需要一个 α 的元素以及它满足该谓词的证明，例如下例中的 `4` 与 `le_refl 4`。

```lean
def x : {n : ℕ // 4 ≤ n} := ⟨4, le_refl 4⟩
example : (x : ℕ) + 6 = 10 := rfl
```

在期望出现类型的地方都可以使用集合，此时集合会被强制转换为对应的子类型。

```lean
def S : Set ℕ := {n : ℕ | 4 ≤ n}
example : ∀ n : S, 4 ≤ (n : ℕ) := fun ⟨n, hn⟩ ↦ hn
```

当你需要在子类型上定义函数，或需要使用子类型的基数时，使用子类型而非集合是有益的。

### 有限类型

#### `Mathlib.Data.Fintype.Basic`

`Fintype α` 表示类型 α 是有限的。它由一个包含某类型全部元素的 finset 构造而成。

```lean
class Fintype (α : Type*) where
  /-- The `Finset` containing all elements of a `Fintype` -/
  elems : Finset α
  /-- A proof that `elems` contains every element of the type -/
  complete : ∀ x : α, x ∈ elems
```

`Fintype α` 不是一个命题，因为它包含数据，但它是一个子单例（subsingleton），意即任意两个 `Fintype α` 类型的元素都相等。

`Finset.univ` 是在给定 `Fintype α` 实例的情况下，包含某类型全部元素的 finset。

### 有限集合

#### `Mathlib.Data.Set.Finite`

有限集合的定义（不同于 finset）是其对应的类型与某个 `n : ℕ` 的 `Fin n` 之间存在双射。
这意味着当该集合被强制转换为子类型时，类型 `Fintype s` 是非空的。
利用 `Classical.choose`，你可以从 `Finite s` 的证明中产生一个 `Fintype s` 类型的对象。有一个函数 `Set.Finite.toFinset`，它从一个有限集合产生一个 finset。

### 基数

有三个函数 `Finset.card`、`Fintype.card` 和 `Multiset.card`，分别表示 finset、有限类型与多重集的大小。对于集合的有限基数，可以在给定该集合有限的证明的前提下使用 `Fintype.card`。

```lean
example : ∀ n : ℕ, Fintype.card (Fin n) = n := Fintype.card_fin
example : ∀ n : ℕ, Finset.card (Finset.range n) = n := Finset.card_range
```

这里，`Fin n` 是小于 n 的自然数的类型，而 `Finset.range n` 是小于 `n` 的自然数构成的 finset。

`Mathlib.SetTheory.Cardinal.Basic` 包含关于无限基数的理论。
