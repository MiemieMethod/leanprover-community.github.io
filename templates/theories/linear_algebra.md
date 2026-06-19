# Lean 中的数学：线性代数

### 半模、模与向量空间

#### [`Mathlib.Algebra.Module.Defs`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/Module/Defs.html)

此文件定义了类型类 `Module R M`，它在类型 `M` 上给出了一个 `R`-模结构。
一个加法交换幺半群 `M` 是（半）环 `R` 上的模，如果存在一个标量乘法 `•`（`SMul`），它满足关于 `+`（在 `M` 和 `R` 中）以及 `*`（在 `R` 中）所期望的分配律公理。
要定义一个 `Module R M` 实例，你首先需要 `Semiring R` 和 `AddCommMonoid M` 的实例。
通过拆分这些依赖关系，我们避免了实例循环与菱形问题。

在一般的数学用法中，半环上的模也称为半模，域上的模也称为向量空间。
我们没有单独的 `Semimodule` 或 `VectorSpace` 类型类，因为通过改变 `R`（和 `M`）上的类型类实例可以更容易地表达这些要求。
在本文档中，我们将用“模”作为“半模、模或向量空间”的通称，用“环”作为“（交换）半环、环或域”的通称。

设 `m` 为任意类型，例如 `Fin n`，那么典型的例子有：
`m → ℕ` 是一个 `ℕ`-半模，`m → ℤ` 是一个 `ℤ`-模，`m → ℚ` 是一个 `ℚ`-向量空间
（在类型论之外，它们分别被称为 `ℕ^m`、`ℤ^m` 和 `ℚ^m`）。
一个环是其自身上的模，其中 `•` 定义为 `*`（这一等式由 `simp` 引理 [`smul_eq_mul`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/Group/Action/Defs.html#smul_eq_mul) 给出）。
每个加法幺半群都有一个由 `n • x = x + x + ... + x`（`n` 次）给出的标准 `ℕ`-模结构，每个加法群都有一个类似定义的标准 `ℤ`-模结构；这些也适用于（半）环。

文件 [`Mathlib.LinearAlgebra.LinearIndependent`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/LinearIndependent.html) 定义了模中带索引族的线性无关性。
要表达一个集合 `s : Set M` 是线性无关的，我们将其视为以自身为索引的族，写作 `LinearIndependent R ((↑)  : s → M)`。

文件 [`Mathlib.LinearAlgebra.Basis`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Basis.html) 定义了模的基。

文件 [`Mathlib.LinearAlgebra.Dimension.Basic`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Dimension/Basic.html) 将模的 `rank`（秩）定义为一个基数。
我们也用 `rank` 表示向量空间的维数，因为其维数总是等于其秩。
线性映射的 `rank` 定义为其像的维数。
此文件中的大多数定义是不可计算的。

文件 [`Mathlib.LinearAlgebra.Dimension.Finrank`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Dimension/Finrank.html) 将模的 `finrank` 定义为一个自然数。
按照约定，如果秩是无穷的，则 `finrank` 等于 0。

### 矩阵

#### [`Mathlib.Data.Matrix.Basic`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/Matrix/Basic.html)

类型 `Matrix m n α` 包含由类型 `α` 的元素构成的 `m` 行 `n` 列的矩形数组。
它是类型 `m → n → α` 的别名。矩阵类型可以由任意类型索引。
例如，一个图的邻接矩阵可以由该图中的节点索引。
如果你想用自然数 `m n : ℕ` 来指定矩阵的维数，可以使用 `Fin m` 和 `Fin n` 作为索引类型。

通过给出从索引到元素的映射来构造矩阵：`(fun (i : m) (j : n) ↦ (_ : α)) : Matrix m n α`。
然而，不建议使用形如 `fun i j ↦ _` 甚至 `(fun i j ↦ _ : Matrix m n α)` 的项来构造矩阵，
因为 Lean 不会将它们识别为具有正确的类型。相反，应当使用 `Matrix.of`。
对于由自然数索引的矩阵，你还可以使用 [`Mathlib.Data.Matrix.Notation`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/Matrix/Notation.html) 中定义的记号：`![![a, b, c], ![b, c, d]] : Matrix (Fin 2) (Fin 3) α`。
要获取矩阵 `M : Matrix m n α` 中第 `i : m` 行、第 `j : n` 列的元素，
你可以将 `M` 应用于这些索引：`M i j : α`。
关于矩阵元素的引理通常以 `_apply` 结尾：`Matrix.add_apply M N i j : (M + N) i j = M i j + N i j`。

矩阵乘法与转置具有由命令 `open scoped Matrix` 提供的记号。
矩阵的乘法照常用 `*` 表示。中缀运算符 `⬝ᵥ` 表示 `Matrix.dotProduct`，
后缀运算符 `ᵀ` 表示 `Matrix.transpose`。

在处理矩阵时，*向量*指的是对于任意 `Fintype` `m` 的一个函数 `m → α`。
它们具有在 [`algebra.module.pi`](https://leanprover-community.github.io/mathlib_docs/algebra/module/pi.html) 中定义的模（或向量空间）结构，
由逐点加法和乘法构成。
行向量与列向量的区别仅由函数的选取来体现。
例如，`Matrix.mulVec M v`（记作 `M *ᵥ v`）将一个矩阵与一个列向量 `v : m → α` 相乘，而 `Matrix.Vecmul v M`
（记作 `v ᵥ* M`）将一个行向量 `v : m → α` 与一个矩阵相乘。
如果你大量使用 `mulVec` 和 `Vecmul`，那么你可能需要考虑改用线性映射（见下文）。

置换矩阵定义在 [`Mathlib.LinearAlgebra.Matrix.Permutation`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/Permutation.html) 中。

矩阵的行列式定义在 [`Mathlib.LinearAlgebra.Matrix.Determinant.Basic`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/Determinant/Basic.html) 中。

伴随矩阵以及非奇异矩阵的逆定义在 [`Mathlib.LinearAlgebra.Matrix.Adjugate`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/Adjugate.html) 和 [`Mathlib.LinearAlgebra.Matrix.NonsingularInverse`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/NonsingularInverse.html) 中。

类型 `Matrix.SpecialLinearGroup m R` 是行列式为 `1` 的 `m` 阶矩阵构成的群，
定义在 [`Mathlib.LinearAlgebra.Matrix.SpecialLinearGroup`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/SpecialLinearGroup.html) 中。

### 线性映射与等价

#### [`Mathlib.Algebra.Module.LinearMap.Defs`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/Module/LinearMap/Defs.html)

类型 `M →[R]ₗ M₂`（即 `LinearMap R M M₂`）表示从 `R`-模 `M` 到 `R`-模 `M₂` 的 `R`-线性映射。
它们由其在 `M` 的元素上的作用来定义。
类型 `M ≃[R]ₗ M₂`（即 `LinearEquiv R M M₂`）是从 `M` 到 `M₂` 的可逆 `R`-线性映射的类型。

矩阵与线性映射之间的等价在 [`Matrix.toLin`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/ToLin.html#Matrix.toLin) 中被形式化。
[`Matrix.toLin'`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/ToLin.html#Matrix.toLin') 表明 `Matrix.mulVec` 是 `Matrix m n R` 与 `(n → R) →[R]ₗ (m → R)` 之间的一个线性等价。
此外，[`LinearMap.toMatrix`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/ToLin.html#LinearMap.toMatrix) 接受 `M₁` 的一组基 `ι` 和 `M₂` 的一组基 `κ`，
并给出 `M₁` 与 `M₂` 之间的 `R`-线性映射和 `Matrix ι κ R` 之间的等价。
如果你的映射有一组明确的基，那么这一等价允许你进行诸如求行列式之类的计算。

矩阵与线性映射之间的区别在于：矩阵本质上是一个元素数组
（这恰好允许诸如 `Matrix.mulVec` 之类的运算），
而线性映射本质上是对向量的一种作用
（如果我们有一组有限基，这恰好可以由一个矩阵来表示）。
如果你想进行计算，矩阵是更好的选择。
如果你想进行不涉及计算的证明，线性映射是更好的选择。

类型 [`Matrix.GeneralLinearGroup R M`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/GeneralLinearGroup/Defs.html#Matrix.GeneralLinearGroup) 是从 `M` 到其自身的可逆 `R`-线性映射构成的群。
`LinearMap.GeneralLinearGroup.generalLinearEquiv R M` 是 `GeneralLinearGroup` 与 `M ≃[R]ₗ M` 之间的等价。
`Matrix.SpecialLinearGroup.toGL` 是从特殊线性群（矩阵的）到一般线性群（线性映射的）的嵌入。

对偶空间由线性映射 `M →[R]ₗ R` 构成，定义在 [`Mathlib.LinearAlgebra.Dual`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Dual.html) 中。

### 双线性型、半双线性型与二次型

#### [`Mathlib.LinearAlgebra.BilinearMap`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/BilinearMap.html)

对于一个 `R`-模 `M`，类型 `LinearMap.BilinForm R M` 是对两个参数都线性的映射 `M → M → R` 的类型。
`LinearMap.BilinForm R M` 与对两个参数都线性的映射 `M →ₗ[R] M →ₗ[R] R` 之间的等价称为 `bilin_linear_map_equiv`。
一个矩阵 `M` 对应于一个双线性型，它将向量 `v` 和 `w` 映为 `row v ⬝ M ⬝ col w`。
`BilinForm R (n → R)` 与 `Matrix n n R` 之间的等价称为 [`BilinForm.toMatrix`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/BilinearForm.html#BilinForm.toMatrix)。

#### [`Mathlib.LinearAlgebra.SesquilinearForm`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/SesquilinearForm.html)

对于一个 `R`-模 `M` 和 `I : R →+* R`，类型 `M →ₗ M →ₛₗ[I] R` 是对第一个参数线性、
而对第二个参数为 `I`-[半线性](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/Module/LinearMap/Defs.html#LinearMap)的映射 `M → M → R` 的类型。
`f` 关于环同态 `I` 的半线性意味着以下等式成立：`f x (a • y) = I a * f x y`。

#### [`Mathlib.LinearAlgebra.QuadraticForm.Basic`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/QuadraticForm/Basic.html)

对于一个 `R`-模 `M`，类型 `QuadraticForm R M` 是满足 `f (a • x) = a * a * f x` 且 `fun x y ↦ f (x + y) - f x - f y` 是双线性映射的映射 `f : M → R` 的类型。

至多相差一个因子 `2`，二次型与双线性型的理论是等价的。
[`LinearMap.BilinMap.toQuadraticMap f`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/QuadraticForm/Basic.html#LinearMap.BilinMap.toQuadraticMap) 是由 `fun x ↦ f x x` 给出的二次型。
[`QuadraticMap.associatedHom f`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/QuadraticForm/Basic.html#QuadraticMap.associatedHom) 是由 `fun x y ↦ ⅟2 * (f (x + y) - f x - f y)` 给出的双线性型（如果 `2` 有乘法逆元）。
[`QuadraticMap.toMatrix'`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/QuadraticForm/Basic.html#QuadraticMap.toMatrix') 和 [`Matrix.toQuadraticMap'`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/QuadraticForm/Basic.html#Matrix.toQuadraticMap') 是二次型与矩阵之间的映射。