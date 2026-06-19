# Lean 中的数学：范畴论

`Category` 类型类定义于 [`Mathlib.CategoryTheory.Category.Basic`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Category/Basic.html)。
它依赖于对象的类型，因此例如当我们讨论一个其对象为类型（位于宇宙 `u` 中）的范畴时，可能会写作 `Category (Type u)`。

函子（它是一个结构，而非类型类）连同恒等函子与函子复合，定义于 [`Mathlib.CategoryTheory.Functor.Basic`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Functor/Basic.html)。

自然变换及其复合定义于 [`Mathlib.CategoryTheory.NatTrans`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/NatTrans.html)。

固定范畴 `C` 与 `D` 之间的函子与自然变换所构成的范畴定义于 [`Mathlib.CategoryTheory.Functor.Category`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Functor/Category.html)。

范畴、函子与自然变换的笛卡尔积出现于 [`Mathlib.CategoryTheory.Products.Basic`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Products/Basic.html)。

类型的范畴以及 hom 配对函子定义于 [`Mathlib.CategoryTheory.Types`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Types.html)。

## 记号

### 范畴

我们使用 `⟶`（`\hom`）箭头来表示态射集，如 `X ⟶ Y`。
这使得实际所涉及的范畴保持隐式；它由 `X` 与 `Y` 的类型通过类型类推断得出。

我们使用 `𝟙`（`\b1`）来表示恒等态射，如 `𝟙 X`。

我们使用 `≫`（`\gg`）来表示态射的复合，如 `f ≫ g`，其含义为“先 `f` 后 `g`”。
你也许更倾向于按照通常的约定来书写复合，即使用 `⊚`（`\oo` 或 `\circledcirc`），如 `f ⊚ g` 表示“先 `g` 后 `f`”。为此，你需要通过如下方式在局部添加该记号：

```lean
local notation f ` ⊚ `:80 g:80 := category.comp g f
```

### 同构

我们使用 `≅` 来表示同构。

### 函子

我们使用 `⥤`（`\func`）来表示函子，如 `C ⥤ D` 表示从 `C` 到 `D` 的函子的类型。

我们使用 `F.obj X` 来表示函子在对象上的作用。
我们使用 `F.map f` 来表示函子在态射上的作用。

函子复合可写作 `F ⋙ G`。

### 自然变换

我们使用 `τ.app X` 来表示自然变换的各个分量。

除此之外，我们大多沿用任意范畴中态射的记号：

我们使用 `F ⟶ G`（`\hom` 或 `-->`）来表示函子 `F` 与 `G` 之间自然变换的类型。
我们使用 `F ≅ G`（`\iso`）来表示自然同构的类型。

对于自然变换的纵向复合，我们直接使用 `≫`。对于横向复合，则使用 `hcomp`。
