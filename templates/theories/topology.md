# Lean 中的数学：拓扑空间、一致空间与度量空间

`TopologicalSpace` 类型类定义于 mathlib 中的 `Mathlib.Topology.Defs.Basic`。`topology` 中有大量代码，涵盖了拓扑空间、连续函数、拓扑群与拓扑环以及无穷求和的基础内容。本文档仅关注 `Mathlib.Topology` 文件夹中的内容。

### 基本类型类

`TopologicalSpace` 类型类是一个归纳类型，它以显然的方式定义为类型 `α` 上的一个结构：其中有一个 `IsOpen` 谓词，用以判断 `U : Set α` 何时为开集，随后是拓扑的诸公理（细致的说明：关于空集为开集的公理被省略了，因为它可由开集之并为开集这一事实应用于空并得出！）。

注意，将任意开集之并为开集这一公理形式化有两种方式：可以要求给定一族开集，其并为开集；也可以要求给定从某指标集 `I` 到开集集合的函数，该函数取值之并为开集。Mathlib 采用了前者，因此该公理为

```lean
isOpen_sUnion : ∀ (s : Set (set α)), (∀ t ∈ s, IsOpen t) → IsOpen (⋃₀ s)
```

而指标集版本则作为一条引理：

```lean
lemma isOpen_biUnion {f : ι → Set α} {s : Set ι} (h : ∀ i ∈ s, IsOpen (f i)) : IsOpen (⋃ i ∈ s, f i)
```

注意 mathlib 中通行的命名约定：`sUnion` 是对一族集合取并，而 `biUnion` 是对一个指标集上的函数像取并。大写的 U 用以表示任意大小的并，与 `union` 相区别，后者表示两个集合之并：

```lean
lemma IsOpen.union (h₁ : is_open s₁) (h₂ : is_open s₂) : is_open (s₁ ∪ s₂)
```

文档中定义了谓词 `IsClosed`，以及函数 `interior`、`closure` 和 `frontier`（闭包减去内部，在数学中有时称为边界），并证明了它们的基本性质。例如

```lean
import Mathlib.Topology.Basic


open TopologicalSpace
variable {X : Type} [TopologicalSpace X] {U V C D Y Z : Set X}

example : IsClosed C → IsClosed D → IsClosed (C ∪ D) := IsClosed.union

example : IsOpen Cᶜ ↔ IsClosed C := isOpen_compl_iff

example : IsOpen U → IsClosed C → IsOpen (U \ C) := IsOpen.sdiff

example : interior Y = Y ↔ IsOpen Y := interior_eq_iff_isOpen

example : Y ⊆ Z → interior Y ⊆ interior Z := interior_mono

example : IsOpen Y ↔ ∀ x ∈ Y, ∃ U ⊆ Y, IsOpen U ∧ x ∈ U := isOpen_iff_forall_mem_open

example : closure Y = Y ↔ IsClosed Y := closure_eq_iff_isClosed

example : closure Y = (interior Yᶜ)ᶜ := closure_eq_compl_interior_compl
```

### 滤子

在 mathlib 中，不同于数学教科书中典型的处理方式，滤子被广泛用作拓扑空间理论中的工具。让我们简要回顾一下数学中滤子的概念。集合 `X` 上的滤子是 `X` 的子集所构成的一个非空族 `F`，满足以下两条公理：

1) 若 `U ∈ F` 且 `U ⊆ V`，则 `V ∈ F`；以及
2) 若 `U, V ∈ F`，则存在 `W ∈ F` 使得 `W ⊆ U ∩ V`。

非正式地说，可以将 `F` 看作 `X` 的"大"子集的集合。例如，若 `X` 是一个集合，`F` 是 `X` 的满足 `X \ Y` 有限的所有子集 `Y` 的集合，则 `F` 是一个滤子。它称为 `X` 上的_有限余滤子_（cofinite filter）。

注意，若滤子 `F` 包含空集，则由第一条公理它包含 `X` 的所有子集。这个滤子有时称为"底"（bottom，稍后我们会看到原因）。某些文献要求滤子中不允许含有空集——Lean 并无此限制。不含空集的滤子有时称为"真滤子"（proper filter）。

若 `X` 是拓扑空间，且 `x ∈ X`，则 `x` 的_邻域滤子_ `𝓝 x` 是 `X` 的满足 `x` 属于 `Y` 内部的所有子集 `Y` 的集合。容易验证这是一个滤子（技术性说明：要看出这确实是 mathlib 中 `𝓝 x` 的定义，了解以下一点会有帮助：一个类型上的所有滤子构成一个完备格，其偏序为 `F ≤ G` 当且仅当 `G ⊆ F`，因此那个涉及下确界的定义实际上是一个并；此外，我这里给出的定义并非 mathlib 中字面上的定义，但 `lemma mem_nhds_iff` 表明它们的定义与此处的定义一致。还需注意，这正是为什么含集合最多的滤子被称为底！）。

我们为何对这些滤子感兴趣？这是因为，给定从 `ℕ` 到拓扑空间 `X` 的映射 `f`，可以验证所得序列 `f 0`、`f 1`、`f 2`…… 趋于 `x ∈ X`，当且仅当滤子 `𝓝 x` 中任一元素的原像属于 `ℕ` 上的有限余滤子——这不过是以另一种方式表述：给定任意包含 `x` 的开集 `U`，存在 `N` 使得对所有 `n ≥ N` 有 `f n ∈ U`。因此滤子提供了一种思考极限的方式。

作为例子，下面用 Lean 表述了三个极限。该例使用了滤子 `atTop` 和 `atBot`，它们在配有序结构的类型中表示"趋于 `∞`"和"趋于 `-∞`"。

```lean
open Filter Topology

-- The limit of `2 * x` as `x` tends to `3` is `6`
example : Tendsto (fun x : ℝ ↦ 2 * x) (𝓝 3) (𝓝 6) := sorry
-- The limit of `1 / x` as `x` tends to `∞` is `0`
example : Tendsto (fun x : ℝ ↦ 1 / x) atTop (𝓝 0) := sorry
-- The limit of `x ^ 2` as `x` tends to `-∞` is `∞`
example : Tendsto (fun x : ℝ ↦ x ^ 2) atBot atTop := sorry
```

附属于集合 `X` 的子集 `Y` 的_主滤子_ `Filter.principal Y` 是 `X` 的所有包含 `Y` 的子集所构成的族。因此不难说服自己，以下结果应当成立：

```lean
variable (X : Type) [TopologicalSpace X] (Y : Set X)

example : interior Y = {x | 𝓝 x ≤ Filter.principal Y} := interior_eq_nhds

example : IsOpen Y ↔ ∀ y ∈ Y, Y ∈ (𝓝 y).sets := isOpen_iff_eventually
```

### 用滤子刻画紧性

作为以滤子为核心的处理方式的一个后果，mathlib 中某些定义对于不习惯这一方式的数学家而言会显得相当奇怪。我们已经见过用滤子给出的关于序列趋于极限的定义。紧性的定义也以滤子论的术语写出：

```lean
/-- A set `s` is compact if for every nontrivial filter `f` that contains `s`,
    there exists `a ∈ s` such that every set of `f` meets every neighborhood of `a`. -/
def IsCompact (s : Set X) :=
  ∀ ⦃f⦄ [NeBot f], f ≤ 𝓟 s → ∃ x ∈ s, ClusterPt x f
```

翻译过来，这是说：拓扑空间 `X` 的子集 `Y` 是紧的，如果对 `X` 上的每个真滤子 `F`，若 `Y` 是 `F` 的元素，则存在 `Y` 中的元素 `y`，使得同时包含 `F` 与 `y` 的邻域滤子的最小滤子也不是 `X` 的所有子集所构成的滤子。这应当被看作 Bolzano-Weierstrass 定理（即在 `ℝ^n` 的紧子空间中任一序列都有收敛子列）的恰当的一般类比。

人们或许会问，为何选择这一紧性定义，而非关于开覆盖有有限子覆盖的标准定义。其原因在某种意义上是计算机科学的而非数学的——问题不应在于最终选择何种定义（事实上，开发者尽可以选择他们喜欢的任意定义，只要它在逻辑上与通常的定义等价即可，且他们可能基于运行时间等非数学因素而有所考量），问题应在于如何证明所内置的定义与你在实践中想用的定义等价。所幸我们有

```lean
example : IsCompact Y ↔ ∀ {ι : Type} (U : ι → Set X),
      (∀ i, IsOpen (U i)) → (Y ⊆ ⋃ i, U i) → ∃ t : Finset ι, Y ⊆ ⋃ i ∈ t, U i :=
    isCompact_iff_finite_subcover
```

因此 Lean 中的定义与标准定义等价。

### Hausdorff 空间

在 Lean 中，他们选用术语 `T2Space` 来表示 Hausdorff（也许是因为它更短！）。

```lean
class T2Space (X : Type u) [TopologicalSpace X] : Prop where
  /-- Every two points in a Hausdorff space admit disjoint open neighbourhoods. -/
  t2 : Pairwise fun x y => ∃ u v : Set X, IsOpen u ∧ IsOpen v ∧ x ∈ u ∧ y ∈ v ∧ Disjoint u v
```

当然，Hausdorff 性正是确保极限唯一所需的条件，但由于极限是用滤子定义的，这一陈述最终读起来如下：

```lean
lemma tendsto_nhds_unique [T2Space X] {f : β → X} {l : Filter β} {x y : X}
  [l.NeBot] (hx : Tendsto f l (𝓝 x)) (hb : Tendsto f l (𝓝 y)) : x = y
```

注意，这一陈述实际上比经典陈述"在 Hausdorff 空间中若一序列趋于两个极限则这两个极限相同"更为一般，因为它适用于任意集合上的任意非平凡滤子，而不仅限于自然数上的有限余滤子。

### 拓扑的基。

若 `X` 是一个_集合_，`S` 是 `X` 的子集所构成的一个族，则可以考虑由 `S`"生成"的拓扑，它（如在此类情形中常见的那样）可以用两种方式定义：其一是 `X` 上所有包含 `S` 的拓扑之交（这里我们将拓扑等同于其底层的开集族），其二则更具构造性，即用拓扑空间的诸公理由 `S`"生成"的集合。不出所料，Lean 中采用的正是后一种定义，因为开集自然构成一个归纳类型；这些开集称为 `generate_open S`，而该拓扑为 `generate_from S`。

mathlib 中关于拓扑基的定义包含一条公理，即该拓扑按上述意义由该基生成，这可能使得终端用户难以直接证明某给定集合满足该定义。不过我们再次有一条定理，将问题归约为验证拓扑基通常的两条公理：

```lean
example (B : Set (Set X)) (h_open : ∀ V ∈ B, IsOpen V)
  (h_nhds : ∀ (x : X) (U : Set X), x ∈ U → IsOpen U → ∃ V ∈ B, x ∈ V ∧ V ⊆ U) :
IsTopologicalBasis B :=
isTopologicalBasis_of_isOpen_of_nhds h_open h_nhds
```

### 其他内容

还有其他涉及滤子的内容，有可分空间、第一可数空间和第二可数空间、积空间、子空间拓扑与商拓扑（以及更一般的拓扑的拉回与推前），还有诸如 t1 与 t3 空间之类的内容。

## 文件组织

以下"核心"模块构成一条线性的导入链。涉及这几个文件中所定义概念的定理，应当在此顺序中最后那个相关文件里找到。

* `Mathlib.Topology.Basic`
  拓扑空间。开子集与闭子集、内部、闭包与边界（frontier）。邻域滤子。滤子的极限。局部有限族。连续性与某点处的连续性。
* `Mathlib.Topology.Order.Basic`
  固定集合上的拓扑所构成的完备格结构。诱导拓扑与共诱导拓扑。
* `maps`
  开映射与闭映射。"诱导"（inducing）映射。嵌入、开嵌入与闭嵌入。商映射。
* `Mathlib.Topology.Constructions`
  由旧拓扑空间构造新拓扑空间：积、和、子空间与商。
* `Mathlib.Topology.Separation`
  分离公理 T₀ 至 T₄，分别也称为 Kolmogorov、Tychonoff 或 Fréchet、Hausdorff、正则与正规空间。

其余的一些目录与文件，排列不分先后：

* `Mathlib.Topology.Algebra`
  配有相容的代数结构或序结构的拓扑空间。
* `Mathlib.Topology.Category`
  拓扑空间、一致空间等所构成的范畴。
* `Mathlib.Topology.Instances`
  具体的拓扑空间，如实数与复数。
* `Mathlib.Topology.MetricSpace`
  度量空间理论；但其中某些人们可能预期会出现于此的概念，实际上被推广到了一致空间。
* `Mathlib.Topology.Sheaves`
  拓扑空间上的预层。
* `Mathlib.Topology.UniformSpace`
  一致空间理论，包括完备性、一致连续性与全有界集等概念。
* `Mathlib.Topology.Bases`
  滤子与拓扑空间的基。可分空间、第一可数空间与第二可数空间。
* `Mathlib.Topology.CompactOpen`
  两个拓扑空间之间连续映射所构成空间上的紧开拓扑。
* `Mathlib.Topology.ContinuousOn`
  相对于某子集的邻域。某子集上的连续性，以及某子集内某点处的连续性。
* `Mathlib.Topology.DenseEmbedding`
  嵌入及其他具有稠密像的函数。
* `Mathlib.Topology.Homeomorph`
  拓扑空间之间的同胚。
* `Mathlib.Topology.List`
  列表与向量上的拓扑。
* `Mathlib.Topology.Sequences`
  序列闭包与序列空间。序列连续函数。
* `Mathlib.Topology.StoneCech`
  拓扑空间的 Stone-Čech 紧化。