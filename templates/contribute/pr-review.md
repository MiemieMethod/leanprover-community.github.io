# 拉取请求审查指南

本指南详细介绍了如何为 mathlib 进行 PR 审查。你也许会
疑惑本指南是否适用于你，答案是“适用！”

虽然只有 mathlib 维护者（maintainer）才有权限*合并*拉取请求，
但每个人都欢迎、甚至被鼓励去*审查*拉取请求。（注意：实际上
还有另一类人，即 mathlib *审查者*（reviewer），他们已经证明自己能够提供
有价值的 PR 审查；来自这些用户、带有 `maintainer merge` 的赞成审查会被维护者
更快地合并）。

一段有帮助的审查历史是入选 mathlib
审查者或 mathlib 维护者团队的关键标准。

本指南首先给出进行审查的总体[准则](#guidelines-for-review)，
对审查者应当考虑哪些方面给出一个高层次的[概览](#what-to-consider-when-reviewing)，
然后聚焦于若干实际的[示例](#examples)。

虽然本指南篇幅相当长，但并不要求你在开始审查之前
通晓所有内容。部分审查本身就是有帮助的，你可以随着
对 Lean 和 mathlib 理解的加深，零散地逐步了解
各种考量因素。

## 审查准则

### 尊重与鼓励

与 mathlib 社区中的所有互动一样，请务必遵守
[行为准则](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)。
简而言之，要保持尊重。然而，在审查时也请务必
保持*鼓励*的态度。大多数贡献者只提交过
寥寥几个拉取请求，这甚至可能是他们的第一个！因此
避免诸如“这个结果没用，我们已经有它的一个
版本了”这样的评论是很重要的。相反，你可以更温和地说，比如，“感谢
你证明了这个结果，但我想我们已经有一个具有同样效果的引理了，它是
`my_generic_lemma`。请尝试改用它。”尽量发现
他们工作中的优点，即便在指出可改进之处时也是如此。

### 谦逊

我们当中没有人，包括 mathlib 维护者，是完美的，或对最佳实践
拥有垄断权。因此，审查者应当始终为他人
提出更好的方案留出余地。此外，认识到
*你也可能是错的*并接受这种可能性，是很重要的。当然，完美是
良好的敌人，所以没有必要为了
更好的方案或新想法而无限期地等待。

## 审查时应考虑什么

审查本质上是审视代码并向自己提问。
那些基础性的问题，大致按从易到难的顺序排列，依次是：
风格、文档、位置、改进以及库的整合。

注意，新审查者完全有能力对前两个
或前三个问题发表评论，而回答库整合方面的问题
通常需要数月之久才能培养出对 mathlib 的熟悉度，并对
审查过程有所贡献。

以下是你作为审查者可以向自己提出的一些具体问题。
这只是一个提纲；在后续章节中，我们将通过示例
更详细地探讨每一个问题。

- [它是否遵循风格规范？](#style)
    + [代码格式](style.html)
    + [命名约定](naming.html)
    + [PR 标题和描述](commit.html)是否提供了恰当的信息？
- [是否有有用的文档？](#documentation)
    + 这些定义是否有足够翔实的文档字符串（docstring）？
    + 是否有指向相关声明的交叉引用？
    + 复杂的证明是否在其中穿插了注释来给出一个梗概？
    + 重要的定理是否有文档字符串？
    + 当代码只应以特定方式使用时，是否对用户有警示？
    + 它是否在形式化文献中的某些内容？
- [位置，位置，位置](#location)
    + 这些声明是否位于恰当的文件中？
      在这里 [`#find_home`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Util/Imports.html#«command#find_home_») 会很有用。
    + 这些结果是否已经存在了？可能以更一般的形式、以不同的名字存在？
      `apply?` 或 `exact?` 策略有时能帮助回答这个问题。
    + 是否引入了新的 `import`，如果是，它们是否为本文件引入了过多的内容？
    + 是否应当将某些结果放到一个新文件中，以尽量减少导入需求？
    + 是否应当将一个文件拆分成多个部分，因为它变得过长（例如，超过 1000 行），
      或涉及过多不同的主题？
- [是否有明显可以做出的改进？](#improvements)
    + 能否将某些部分拆分为辅助引理或定义（尤其是对于较长的证明）？
    + 能否使用不同的／更好的策略来提升可读性（例如，使用 `gcongr`
      而非 `mul_le_mul_of_nonneg_left`）？
      注意：只要*不牺牲可读性*，代码精简（code golfing）是可以的，不过精简
      平凡的结果通常也无妨。
    + 不同的证明结构是否能极大地简化论证？
    + 所引入的定义是否是形式化该概念的最佳方式（非常困难！）？
- [它是否推进或改进了库？](#library-integration)
    + 它是否提供了合理的 API？
    + 它是否足够一般，以支持已知的未来需求？
    + 它是否契合 mathlib 的设计和集体愿景？
- 更具体的考量
    + 声明是否使用 `α β : Type*` 而非 `α β : Type _` 来指代任意的宇宙层级？
      （注意：这是一个性能问题，因为使用 `Type _` 会引入需要求解的合一问题。）
    + 引理在应当标注 `@[simp]`、`@[ext]` 等属性的地方是否做了标注？或者在不应当标注的地方是否避免了标注？
    + 新定义是否附带了关于它们的引理（也许仅仅是那些由 `@[simps]` 生成的引理）？
    + 任何新声明的实例是否会造成菱形（diamond）？是非定义相等（non-defeq）还是非命题相等（non-propeq）的？

## 示例

本指南的其余部分专门探讨审查过程中既有的虚构示例，也有真实
案例。我们试图为上述每一个问题提供示例。真实
案例中涉及的相关方已被征询过将其纳入本风格指南的许可。

并非每个问题都有对应的示例，但我们试图至少为
每种情形提供一段关于应当考虑什么的讨论。

### 风格

#### 代码格式

```lean
-- do NOT write code in this style!
theorem mul_assoc_assoc {α : Type*} [Semigroup α] (a b c d : α)
: a*b*c*d=a*(b*(c*d)) :=
by
rw [mul_assoc,
    mul_assoc]
```

上面的代码违反了若干格式准则：二元运算
周围没有空格，行首以 `:` 开头而不是
在上一行结尾处结束，`by` 应当移到上一行
而不是单独占一行（无论如何，CI 中的风格 linter 应当能捕获这一点），
而且 `rw` 策略被不必要地拆分到了多行。

在这种情形下，该 PR 的作者由于违反了如此多的
风格准则，很可能是一位新贡献者，并且不熟悉、
或不记得风格指南。一条恰当的审查评论
大致可以是这样的：

````markdown
In case you're unaware, please familiarize yourself with the mathlib
[style guide](https://leanprover-community.github.io/contribute/style.html).
You need spaces around `*`, `:` at the end of the line and the `rw` to 
be on the same line.
```suggestion
theorem mul_assoc_assoc {α : Type*} [Semigroup α] (a b c d : α) :
    a * b * c * d = a * (b * (c * d)) := by
  rw [mul_assoc, mul_assoc]
```
````

#### 命名约定

```lean
theorem inv_is_unit_times_self_eq_1 {M : Type*} [Monoid M] {a : M} (h : IsUnit a) :
    ↑(IsUnit.unit h)⁻¹ * a = 1 := sorry
```

上面的引理直接取自库，你能猜到它实际的名字吗？
它是 `IsUnit.inv_val_mul`。一条建议新名字的恰当审查
大致可以是这样的：

````markdown
In order to accord with the 
[naming conventions](https://leanprover-community.github.io/contribute/naming.html)
for mathlib, I suggest renaming this to: `IsUnit.inv_val_mul`. Note that:

- we use `mul` instead of `times`, and `one` instead of `1`
- the lemma is sufficiently clear without the reference to `1`
- If we are referencing an `IsUnit` hypothesis, we would use `isUnit`, not `is_unit`
- However, since we have an `IsUnit` hypothesis, putting it in the `IsUnit.` 
  namespace allows for use with dot notation.
- we should reference the coercion that appears here, which is `Subtype.val`, hence
  the `val` in the suggested name.
````

这为 PR 作者提供了一个指向命名约定的链接，以防他们
尚未看过它，同时也指出了具体的问题，这样他们就
不必再通读整份指南。如果他们只在命名约定上犯了一个
错误，这种做法也很可能是有帮助的。

注意：并非所有声明都恰好只有一个合适的名字，可能会有几个，
每个都有各自的优点和缺点。

#### PR 标题和描述是否提供了恰当的信息？

考虑以下 PR 标题和描述：

```markdown
Title: feat(Analysis/SpecificLimits)
Description: Where should we put these lemmas?
```

这有两个问题：标题没有提供任何关于改动的
信息，而描述包含的是一个讨论性问题，而不是关于改动的
信息。一条合理的审查评论大致可以是这样的：

```markdown
Please update the PR title and description to be more informative about what 
you have added or changed as these will be permanently included in the git
history when this is merged. Questions or topics for discussion are allowed
in the PR description, but should be placed after the `---`, as then they
will be treated as comments and not included in the git history.
```

当然，你可以提供建议，甚至自己更新 PR 标题和
描述，但你或许会想要指出这一点，尤其是当
PR 作者是一位相对较新的贡献者时。

### 文档

#### 这些定义是否有足够翔实的文档字符串？

`docBlame` linter 应当确保用户为他们所有的
定义添加文档字符串。然而，文档字符串*存在*并不必然
意味着它是*有用*且*准确*的。审查者应当尽力确保
所提供的文档字符串以易于理解的方式准确描述了该 `def`。

#### 重要的定理是否有文档字符串？

下面的示例参考了
[#5580](https://github.com/leanprover-community/mathlib4/pull/5580/files) 中的审查。
在那个 PR 中，添加了以下定理：

```lean
protected theorem _root_.WithSeminorms.equicontinuous_TFAE {κ : Type*}
    {q : SeminormFamily 𝕜₂ F ι'} [UniformSpace E] [UniformAddGroup E] [u : UniformSpace F]
    [hu : UniformAddGroup F] (hq : WithSeminorms q) [ContinuousSMul 𝕜 E]
    (f : κ → E →ₛₗ[σ₁₂] F) : TFAE
    [ EquicontinuousAt ((↑) ∘ f) 0,
      Equicontinuous ((↑) ∘ f),
      UniformEquicontinuous ((↑) ∘ f),
      ∀ i, ∃ p : Seminorm 𝕜 E, Continuous p ∧ ∀ k, (q i).comp (f k) ≤ p,
      ∀ i, BddAbove (range fun k ↦ (q i).comp (f k)) ∧ Continuous (⨆ k, (q i).comp (f k)) ] :=
  sorry
```

这个定理是有用的，但也有点长，需要花时间（对人类而言）去解析。
因此，它或许应当有一个文档字符串，这导致了
[以下评论](https://github.com/leanprover-community/mathlib4/pull/5580/files#r1286511394)

```markdown
Can you please add a docstring explaining the statement of the theorem, as well as a cross reference to
`NormedSpace.equicontinuous_TFAE`?
```

随后 PR 作者用以下翔实的文档字符串更新了该定理，在这里我们能够
看到巨大的附加价值：

```lean
/-- Let `E` and `F` be two topological vector spaces over a `NontriviallyNormedField`, and assume
that the topology of `F` is generated by some family of seminorms `q`. For a family `f` of linear
maps from `E` to `F`, the following are equivalent:
* `f` is equicontinuous at `0`.
* `f` is equicontinuous.
* `f` is uniformly equicontinuous.
* For each `q i`, the family of seminorms `k ↦ (q i) ∘ (f k)` is bounded by some continuous
  seminorm `p` on `E`.
* For each `q i`, the seminorm `⊔ k, (q i) ∘ (f k)` is well-defined and continuous.
In particular, if you can determine all continuous seminorms on `E`, that gives you a complete
characterization of equicontinuity for linear maps from `E` to `F`. For example `E` and `F` are
both normed spaces, you get `NormedSpace.equicontinuous_TFAE`. -/
```

#### 是否有指向相关声明的交叉引用？

参见上一个示例，其中请求为一个相关声明添加交叉引用。

#### 复杂的证明是否在其中穿插了注释来给出一个梗概？

在这个示例中，我们仅展示一个现成的例子，说明穿插的注释如何能够
显著增加 Lean 中证明的价值。这直接复制自
[GromovHausdorff.instSecondCountableTopologyGHSpace](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Topology/MetricSpace/GromovHausdorff.html#GromovHausdorff.instSecondCountableTopologyGHSpace) 的源码。

每当一个复杂的证明没有像这样被注释时，请鼓励 PR
作者这样做。你可以向他们指出这段代码。

```
/-- The Gromov-Hausdorff space is second countable. -/
instance : SecondCountableTopology GHSpace := by
  refine secondCountable_of_countable_discretization fun δ δpos => ?_
  let ε := 2 / 5 * δ
  have εpos : 0 < ε := mul_pos (by simp) δpos
  have (p : GHSpace) : ∃ s : Set p.Rep, s.Finite ∧ univ ⊆ ⋃ x ∈ s, ball x ε := by
    simpa only [subset_univ, true_and] using
      finite_cover_balls_of_compact (X := p.Rep) isCompact_univ εpos
  -- for each `p`, `s p` is a finite `ε`-dense subset of `p` (or rather the metric space
  -- `p.Rep` representing `p`)
  choose s hs using this
  -- cardinality of the nice finite subset `s p` of `p.Rep`, called `N p`
  let N := fun p : GHSpace => Nat.card (s p)
  -- equiv from `s p`, a nice finite subset of `p.Rep`, to `Fin (N p)`, called `E p`
  let E := fun p : GHSpace => (hs p).1.equivFin
  -- A function `F` associating to `p : GHSpace` the data of all distances between points
  -- in the `ε`-dense set `s p`.
  let F : GHSpace → Σ n : ℕ, Fin n → Fin n → ℤ := fun p =>
    ⟨N p, fun a b => ⌊ε⁻¹ * dist ((E p).symm a) ((E p).symm b)⌋⟩
  refine ⟨Σ n, Fin n → Fin n → ℤ, inferInstance, F, fun p q hpq => ?_⟩
  /- As the target space of F is countable, it suffices to show that two points
  `p` and `q` with `F p = F q` are at distance `≤ δ`.
  For this, we construct a map `Φ` from `s p ⊆ p.Rep` (representing `p`)
  to `q.Rep` (representing `q`) which is almost an isometry on `s p`, and
  with image `s q`. For this, we compose the identification of `s p` with `Fin (N p)`
  and the inverse of the identification of `s q` with `Fin (N q)`. Together with
  the fact that `N p = N q`, this constructs `Ψ` between `s p` and `s q`, and then
  composing with the canonical inclusion we get `Φ`. -/
  have Npq : N p = N q := (Sigma.mk.inj_iff.1 hpq).1
  let Ψ : s p → s q := fun x => (E q).symm (Fin.cast Npq ((E p) x))
  let Φ : s p → q.Rep := fun x => Ψ x
  -- Use the almost isometry `Φ` to show that `p.Rep` and `q.Rep`
  -- are within controlled Gromov-Hausdorff distance.
  have main : ghDist p.Rep q.Rep ≤ ε + ε / 2 + ε := by
    refine ghDist_le_of_approx_subsets Φ ?_ ?_ ?_
    · show ∀ x : p.Rep, ∃ y ∈ s p, dist x y ≤ ε
      -- by construction, `s p` is `ε`-dense
      intro x
      have : x ∈ ⋃ y ∈ s p, ball y ε := (hs p).2 (mem_univ _)
      obtain ⟨y, ys, hy⟩ := mem_iUnion₂.1 this
      exact ⟨y, ys, hy.le⟩
    · show ∀ x : q.Rep, ∃ z : s p, dist x (Φ z) ≤ ε
      -- by construction, `s q` is `ε`-dense, and it is the range of `Φ`
      intro x
      have : x ∈ ⋃ y ∈ s q, ball y ε := (hs q).2 (mem_univ _)
      obtain ⟨y, ys, hy⟩ := mem_iUnion₂.1 this
      let i : ℕ := E q ⟨y, ys⟩
      let hi := ((E q) ⟨y, ys⟩).is_lt
      have ihi_eq : (⟨i, hi⟩ : Fin (N q)) = (E q) ⟨y, ys⟩ := by rw [Fin.ext_iff, Fin.val_mk]
      have hiq : i < N q := hi
      have hip : i < N p := by rwa [Npq.symm] at hiq
      let z := (E p).symm ⟨i, hip⟩
      use z
      have C1 : (E p) z = ⟨i, hip⟩ := (E p).apply_symm_apply ⟨i, hip⟩
      have C2 : Fin.cast Npq ⟨i, hip⟩ = ⟨i, hi⟩ := rfl
      have C3 : (E q).symm ⟨i, hi⟩ = ⟨y, ys⟩ := by
        rw [ihi_eq]; exact (E q).symm_apply_apply ⟨y, ys⟩
      have : Φ z = y := by simp only [Φ, Ψ]; rw [C1, C2, C3]
      rw [this]
      exact hy.le
    · show ∀ x y : s p, |dist x y - dist (Φ x) (Φ y)| ≤ ε
      /- the distance between `x` and `y` is encoded in `F p`, and the distance between
      `Φ x` and `Φ y` (two points of `s q`) is encoded in `F q`, all this up to `ε`.
      As `F p = F q`, the distances are almost equal. -/
      intro x y
      -- introduce `i`, that codes both `x` and `Φ x` in `Fin (N p) = Fin (N q)`
      let i : ℕ := E p x
      have hip : i < N p := ((E p) x).2
      have hiq : i < N q := by rwa [Npq] at hip
      have i' : i = (E q) (Ψ x) := by simp only [i, Ψ, Equiv.apply_symm_apply, Fin.coe_cast]
      -- introduce `j`, that codes both `y` and `Φ y` in `Fin (N p) = Fin (N q)`
      let j : ℕ := E p y
      have hjp : j < N p := ((E p) y).2
      have hjq : j < N q := by rwa [Npq] at hjp
      have j' : j = ((E q) (Ψ y)).1 := by
        simp only [j, Ψ, Equiv.apply_symm_apply, Fin.coe_cast]
      -- Express `dist x y` in terms of `F p`
      have : (F p).2 ((E p) x) ((E p) y) = ⌊ε⁻¹ * dist x y⌋ := by
        simp only [F, (E p).symm_apply_apply]
      have Ap : (F p).2 ⟨i, hip⟩ ⟨j, hjp⟩ = ⌊ε⁻¹ * dist x y⌋ := by rw [← this]
      -- Express `dist (Φ x) (Φ y)` in terms of `F q`
      have : (F q).2 ((E q) (Ψ x)) ((E q) (Ψ y)) = ⌊ε⁻¹ * dist (Ψ x) (Ψ y)⌋ := by
        simp only [F, (E q).symm_apply_apply]
      have Aq : (F q).2 ⟨i, hiq⟩ ⟨j, hjq⟩ = ⌊ε⁻¹ * dist (Ψ x) (Ψ y)⌋ := by
        simp [← this, *]
      -- use the equality between `F p` and `F q` to deduce that the distances have equal
      -- integer parts
      have : (F p).2 ⟨i, hip⟩ ⟨j, hjp⟩ = (F q).2 ⟨i, hiq⟩ ⟨j, hjq⟩ := by
        have hpq' : (F p).snd ≍ (F q).snd := (Sigma.mk.inj_iff.1 hpq).2
        rw [Fin.heq_fun₂_iff Npq Npq] at hpq'
        rw [← hpq']
      rw [Ap, Aq] at this
      -- deduce that the distances coincide up to `ε`, by a straightforward computation
      -- that should be automated
      have I :=
        calc
          ε⁻¹ * |dist x y - dist (Ψ x) (Ψ y)| = |ε⁻¹ * (dist x y - dist (Ψ x) (Ψ y))| := by
            rw [abs_mul, abs_of_nonneg (inv_pos.2 εpos).le]
          _ = |ε⁻¹ * dist x y - ε⁻¹ * dist (Ψ x) (Ψ y)| := by congr; ring
          _ ≤ 1 := le_of_lt (abs_sub_lt_one_of_floor_eq_floor this)
      calc
        |dist x y - dist (Ψ x) (Ψ y)|
        _ = ε * (ε⁻¹ * |dist x y - dist (Ψ x) (Ψ y)|) := by grind
        _ ≤ ε * 1 := by gcongr
        _ = ε := mul_one _
  calc
    dist p q = ghDist p.Rep q.Rep := dist_ghDist p q
    _ ≤ ε + ε / 2 + ε := main
    _ = δ := by ring
```

#### 当代码只应以特定方式使用时，是否对用户有警示？

某些声明只打算在特定文件内使用，也许是因为它们是辅助性的。
另一些声明可以在任何地方使用，但应当谨慎使用，且只在首选方法
不可用、或使用它的弊端无关紧要时才使用。

##### 在特定文件中使用

前者的一个例子是：
[PiLp.iSup_edist_ne_top_aux](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/NormedSpace/PiLp.html#PiLp.iSup_edist_ne_top_aux)，
它包含以下文档字符串。

```lean
/-- An auxiliary lemma used twice in the proof of `PiLp.pseudoMetricAux` below. Not intended for use outside this file. -/
```

这个引理通过它的名字（包含 `aux`）和它的文档字符串向读者表明它并不打算用于
通用目的。其原因在于，紧接其前的那个声明，
[PiLp.pseudoEmetricAux](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/NormedSpace/PiLp.html#PiLp.pseudoEmetricAux)，
是一个仅被临时激活以构建恰当的伪扩展度量结构的实例。
它的文档字符串也阐明了这一点：

```lean
/-- Endowing the space `PiLp p β` with the `L^p` pseudoemetric structure. This definition is not
satisfactory, as it does not register the fact that the topology and the uniform structure coincide
with the product one. Therefore, we do not register it as an instance. Using this as a temporary
pseudoemetric space instance, we will show that the uniform structure is equal (but not defeq) to
the product one, and then register an instance in which we replace the uniform structure by the
product one using this pseudoemetric space and `PseudoEMetricSpace.replaceUniformity`. -/
```

##### 使用条件

后者的一个例子是：
[completeLatticeOfSup](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/CompleteLattice.html#completeLatticeOfSup)，
它包含以下文档字符串。

````lean
/-- Create a `CompleteLattice` from a `PartialOrder` and `SupSet`
that returns the least upper bound of a set. Usually this constructor provides
poor definitional equalities.  If other fields are known explicitly, they should be
provided; for example, if `inf` is known explicitly, construct the `CompleteLattice`
instance as
```
instance : CompleteLattice my_T :=
  { inf := better_inf,
    le_inf := ...,
    inf_le_right := ...,
    inf_le_left := ...
    -- don't care to fix sup, sInf, bot, top
    ..completeLatticeOfSup my_T _ }
```
-/
````

在这种情形下，构造了一个 `CompleteLattice`，但承载数据的 `sup`、`sInf`、
`bot` 和 `top` 字段是用 `sSup` 来定义的，因此当需要访问其定义时，
将不便于对它们进行证明。所以这条
文档字符串充当了对用户的一个重要警示：此构造器
应当谨慎使用，并且如果这些承载数据的字段是已知的，
就应当明确地提供它们。
    
#### 它是否在形式化文献中的某些内容？

mathlib 中有些对象仅仅是为了服务于形式化而存在的（例如 `AddMonoidWithOne`），
但大多数被形式化的想法直接来自数学
文献。在这种情况下，尤其是当贡献者在模仿一篇已发表的
纸面证明时，应当鼓励他们在 `references.bib` 文件中添加一个条目，
并在模块文档和／或相关定理的文档字符串中引用它。

此外，让 mathlib 中的数学与文献相关联，是对
所添加内容的相关性的一项额外的合理性检查，并且但愿
日后会有人关心它并使用它。将数学纳入 mathlib
会带来维护所添加内容的负担，如果某些内容永远不会被用到，
就没有理由承担这一负担。

### 位置

#### 这些声明是否位于恰当的文件中？

考虑来自 [#5742](github.com/leanprover-community/mathlib4/pull/5742) 的以下示例，
其中 PR 作者正在为 `Unitization` 配置一个范数结构。作者
正在创建一个新文件 `Analysis.NormedSpace.Unitization`，并在某处声明了
该实例：

```lean
instance Unitization.instNontrivial {𝕜 A} [Nontrivial 𝕜] [Nonempty A] :
    Nontrivial (Unitization 𝕜 A) :=
  nontrivial_prod_left
```

注意，这个实例与范数毫无关系，因此它很可能应当属于一个
更早的文件。审查者可以使用 `#find_home Unitization.instNontrivial` 来确定
放置此声明的自然位置是 `Algebra.Algebra.Unitization`。一位有帮助的
审查者可以这样评论：

```markdown
It seems like this instance doesn't have anything to do with the norm structure on the 
`Unitization`. Perhaps you could place this instance in `Algebra.Algebra.Unitization` instead.
```

#### 这些结果是否已经存在了？可能以更一般的形式、以不同的名字存在？

mathlib 到现在已是一个相当庞大的库，任何人，尤其是新
用户，都难以熟悉它所有不同的角落以及究竟哪些结果是
可用的。这一点因我们追求一般性、摒弃
代码重复这一事实而加剧；这导致了新用户经常提出的问题：“mathlib 真的
缺少向量空间和群同态吗？”，以及它的答案：“不，它们分别是 `Module`
和 `MonoidHom`。”

因此，新贡献者（甚至是经验丰富的贡献者！）为一个
已经存在的结果创建 PR 的情况并不罕见，有时是逐字逐句地相同，有时则是
以更大的一般性出现。

`apply?` 和 `exact?` 策略有时能帮助回答这个问题。如果你怀疑某个
结果已经存在，只需将它复制到一个带有 `import Mathlib` 的新文件中并尝试 `exact?`。

#### 是否引入了新的 `import`？它们是否导入了过多的内容？

维护 mathlib 导入层级的组织结构是一项重要的任务，
但如果不仔细审查，它很容易失控。一般来说，问题
以下面这种方式出现。

一位贡献者想：“我想添加 `my_theorem`，它完全是关于 `Z` 的，所以我会
把它添加到 `X.Y.Z`。”在尝试把这个定理添加到那里时，贡献者意识到：“哦，
我没有访问 `helper_lemma` 的权限，我需要 `import A.B.C`。”在审查期间，
审查者专注于其他事情，于是这个 PR 连同这一导入改动一起被合并了。
这就是某个时刻 `Analysis.NormedSpace.Star.Basic` 导入了
`Analysis.NormedSpace.OperatorNorm` 的来龙去脉！这发生在
[#16964](https://github.com/leanprover-community/mathlib/pull/16964) 中，
随后不得不在 [#18194](https://github.com/leanprover-community/mathlib/pull/18194) 中加以修复。

再举一个例子，在 [#6239](https://github.com/leanprover-community/mathlib4/pull/6239) 中，
贡献者向 `LinearAlgebra.Matrix.DotProduct` 添加了导入
`Data.IsROrC.Basic`。对于一位新贡献者来说，这很可能
是一件难以察觉的事情，因为它有时需要对库的
组织方式有相当程度的熟悉。

当然，审查者应当尽力捕获最为离谱的例子
（例如，把 `Analysis` 文件导入到 `Algebra` 文件中通常相当可疑），
但提出这个问题总归是有道理的。它往往可能意味着这些结果应当
属于别处，意味着该文件应当沿一条自然边界拆分，或者意味着新结果应当
放到一个新文件中。

#### 是否应当将一个文件拆分成多个部分？

拆分一个文件本质上有三个理由：

1. 它实在太长，以致用起来不舒服。
   这里一个不错的经验法则是它超过了 1000 行。
2. 该文件被分成多个只是松散相关的部分。
3. 为了避免因引入与既有结果密切相关的新结果而导致的导入蔓延。

假设有一些结果，约 500 行的量，被添加到一个本就已经包含 700 行的
既有文件中，并进一步假设这些新材料与该文件中某些既有材料
密切相关。审查者应当留意一条自然边界，可以沿着它把该文件拆分成连贯的
部分。

### 改进

#### 拆分为辅助引理或定义（尤其是对于较长的证明）？

冗长的独立证明常常是一个迹象，表明手边附近就潜藏着一次值得进行的
重构。新贡献者往往不知道库中既有的
引理，或者可能不知道如何把他们的定理拆分成更
易于管理的小块。在这些情形下，审查者有几种选择，包括：
撸起袖子，以 GitHub 上的 `suggestion`（建议）形式亲自把结果重构成多个
引理；寻找一个潜在的
重构方向并提及它，比如“你或许可以考虑把第 xx 行的
论证拆分成它自己的引理，这将简化证明”；或者
干脆问，“这个证明似乎相当冗长且笨重，你是否考虑过
它可以如何被拆分成更易于管理的部分？”；或者甚至，“如果你利用定理 X，这个
证明似乎可能会更容易。”

#### 用不同的策略来提升可读性

一个使用更好的策略或精简代码能够*提升*可读性的好例子
可以在 [#6140](https://github.com/leanprover-community/mathlib4/pull/6140/files/d2506ba26543b630722124dbf030339f43f6590a#r1287284988) 的这条建议中找到。
在这个例子中，证明里原始的子策略序列是：

```lean
  have h₀ : log b = log (- -b) := by simp
  rw [h₀, log_neg_eq_log]
  have hb' : 0 < -b := by linarith
  have h₁ : log (-b) < 0 := by rw [log_neg_iff hb']; linarith
  refine tendsto_exp_atBot.comp ?_
  rw [tendsto_const_mul_atBot_of_neg h₁]
  show atTop ≤ atTop
  rfl
```

而建议是将其精简为：

```lean
  refine tendsto_exp_atBot.comp <| (tendsto_const_mul_atBot_of_neg ?_).mpr tendsto_id
  rw [←log_neg_eq_log, log_neg_iff (by linarith)]
  linarith
```

从精简后的版本中，我们可以轻易看出，这本质上只是把一些
关于 `Filter.Tendsto` 的库引理复合起来，外加为其中一个定理提供
一个假设，而该假设是用一些基本的重写和对 `linarith` 的调用来证明的。

一个使用更好的策略能够提升可读性的例子可以在
[#4702](https://github.com/leanprover-community/mathlib4/pull/4702/files) 的整个 diff 中找到，
它使用新的 `gcongr` 策略精简了整个库中的引理。我们将
突出一个特别漂亮的例子以供参考。原始代码是：

```lean
  _ ≤ ε / 2 * ‖∑ i in range n, g i‖ + ε / 2 * ∑ i in range n, g i := by
    rw [← mul_sum]
    exact add_le_add hn (mul_le_mul_of_nonneg_left le_rfl (half_pos εpos).le)
```

它被用 `gcongr` 改进为：

```lean
  _ ≤ ε / 2 * ‖∑ i in range n, g i‖ + ε / 2 * ∑ i in range n, g i := by rw [← mul_sum]; gcongr
```

或者，来自同一个 PR 的这个例子，它使用 `positivity` 从：

```lean
  · have ha' := mul_le_mul_of_nonneg_left ha (inv_pos.2 hab).le
    rwa [MulZeroClass.mul_zero, ← div_eq_inv_mul] at ha'
  · have hb' := mul_le_mul_of_nonneg_left hb (inv_pos.2 hab).le
    rwa [MulZeroClass.mul_zero, ← div_eq_inv_mul] at hb'
```

变为：

```lean
  · positivity
  · positivity
```

#### 不同的证明结构是否能极大地简化论证？

一个极好的例子出现在
[#5602](https://github.com/leanprover-community/mathlib4/pull/5602/files/ea99653c047046bae3a109ee980314eec0bb9e81#r1282044795) 的审查中。
在这个例子中，PR 作者证明了：

```lean
variable {R S A : Type*} [CommSemiring R] [Semiring A] [Algebra R A] [SetLike S A]
  [hSA : NonUnitalSubsemiringClass S A] [hSRA : SMulMemClass S R A] (s : S)

-- `NonUnitalSubalgebra.unitization s : Unitization R s →ₐ[R] Algebra.adjoin R (s : Set A)`
theorem NonUnitalSubalgebra.unitization_surjective :
    Function.Surjective (NonUnitalSubalgebra.unitization s) := by
  apply Algebra.adjoin_induction'
  · refine' fun x hx => ⟨(0, ⟨x, hx⟩), Subtype.ext _⟩
    simp only [NonUnitalSubalgebra.unitization_apply_coe, Subtype.coe_mk]
    change (algebraMap R { x // x ∈ Algebra.adjoin R (s : Set A) } 0 : A) + x = x
    rw [map_zero, Subsemiring.coe_zero, zero_add]
  · exact fun r => ⟨algebraMap R (Unitization R s) r, AlgHom.commutes _ r⟩
  · rintro _ _ ⟨x, rfl⟩ ⟨y, rfl⟩
    exact ⟨x + y, map_add _ _ _⟩
  · rintro _ _ ⟨x, rfl⟩ ⟨y, rfl⟩
    exact ⟨x * y, map_mul _ _ _⟩
```

审查者评论道：

```markdown
I see why it's not immediate (you'd have to get back to the full codomain),
but is there really no good way of using `Algebra.adjoin_le` here?
```

这带来了大为改进的三行证明：

```lean
theorem NonUnitalSubalgebra.unitization_surjective :
    Function.Surjective (NonUnitalSubalgebra.unitization s) := by
  have : Algebra.adjoin R s ≤ ((Algebra.adjoin R (s : Set A)).val.comp (unitization s)).range :=
    Algebra.adjoin_le fun a ha ↦ ⟨(⟨a, ha⟩ : s), by simp⟩
  fun x ↦ match this x.property with | ⟨y, hy⟩ => ⟨y, Subtype.ext hy⟩
```

在这个例子中，诉诸引理 `Algebra.adjoin_le` 相比于使用
`Algebra.adjoin_induction'`，是一次巨大的简化。

#### 所引入的定义是否是形式化该概念的最佳方式（非常困难！）？

这在一般意义上极难描述，但也许能给出的最简单的
经验法则是：定义越是避免使用
依值类型，就越好。

举例来说，考虑 [Vector](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/Vector.html#Vector) 的定义。
许多依值类型论的入门讲解将 `Vector`
定义为一个归纳类型，并把它作为依值
类型的典型例子。虽然依值类型是不可避免的，但 mathlib 的定义
转而选择了 `List` 的一个简单子类型，而对 `ℕ` 的
依赖只出现在 `List.length` 的相等命题中。这具有
这样的优点：我们可以通过强制转换到 `List` 轻松地
跳出依值类型的世界，然后生活就轻松多了。事实上，`Vector`
上的大多数运算恰恰就是 `List` 上对应的运算结合
一个关于长度的相等证明。

### 库的整合

这里的许多问题都有点含糊，并且通常需要对 mathlib 的
结构有大量的熟悉，或者至少在形式化方面有显著的先前
经验。如果你发现自己在审查时难以处理这些问题，不必
气馁。

#### 它是否提供了合理的 API？

- 属性是否被恰当地添加（例如 `@[simp]`、`@[ext]`、`@[gcongr]`、`@[aesop]` 等）？
- 是否提供了重写引理，以避免总是需要在定义层面上穿过相等关系？
- 一个新类型是否在常见用例中提供了便利的构造器？

#### 它是否足够一般，以支持已知的未来需求？

这需要知道一些未来的需求可能是什么！活跃于 Zulip
有助于让审查者意识到这些需求。然而，人们可以为这个问题使用一个替代物，
即“文献中是否存在这个结果的某个更一般的版本，且它调用了 mathlib 中
预先存在的概念？”如果有，那么或许现有的 PR 应当被一般化。

#### 它是否契合 mathlib 的设计和集体愿景？

同样地，这是一个含糊的问题，需要知道其设计和集体愿景是什么！
然而，举一些实际的例子：

- 如果一位用户正在添加一种新的态射（不在范畴论库中），那么他们很可能
  应当定义一个捆绑式（bundled）的态射类型，并且大概还要使用 `FunLike` API
  定义一个相关联的态射类。
- 类似地，如果一位贡献者正在添加一个新的子对象，那么他们大概应当使用捆绑式
  子对象，并利用 `SetLike` API。作为参考，请见 [Mathematics in Lean 中
  的相关章节](https://leanprover-community.github.io/mathematics_in_lean/C08_Hierarchies.html#sub-objects)。
- 遵循任何既有的 library note（库说明）的建议。
