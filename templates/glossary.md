# Lean 术语表

本文档收集了在 Lean 社区中可能遇到的术语的简短解释。

尽管下文中的许多条目都有精确的技术定义，但我们更倾向于解释它们在日常交流中的用法，并附上额外的参考链接以供进一步了解。

下文中的少数内部链接对应的是尚未添加的条目，因此在它们完成之前，这些链接还不会指向任何条目定义。
若想请求向本术语表添加新的条目，欢迎[提交一个 issue](https://github.com/leanprover-community/leanprover-community.github.io/issues/new?title=Add%20a%20glossary%20entry%20for%20)。

本页中的条目可以通过锚点链接来引用（例如 `https://leanprover-community.github.io/glossary.html#widget`）。
对于某些条目，在条目标题之前还提供了更易于输入的额外锚点——例如 [`#heavy-rfl`](#heavy-rfl) 会指向 “heavy `rfl` / heavy `refl`” 条目。
新术语条目的作者如果条目标题较长、含有反引号或者难以输入，应当考虑添加这些额外的锚点。

### attribute（属性）

可以应用于某个 Lean [声明](#declaration)的一个或多个标签或标记，它可能影响该声明本身的行为，或者影响与之交互的其他 Lean 对象的行为。
属性既可以在 [core Lean](#core-lean) 中定义，也可以在 [Mathlib](#Mathlib) 中定义，或在任何 Lean 代码中定义。

应用一个属性的方式是：在声明命令前加上 `@[name-of-attribute]` 前缀，或者事后使用 `attribute` 命令，如 `attribute [name-of-attribute] name-of-declaration`。

例如，`@[simp]` 属性会将一个声明（通常是 `lemma`、`theorem` 或 `def`）标记为一个 [simp 引理](#simp-lemma)。

##### 另见

* [*The Lean Reference Manual* 第 5.4 节](https://lean-lang.org/doc/reference/latest/Attributes/#attributes)，其中列出了在 [core lean](#core-lean) 中定义的属性

### beta reduction（β 归约）

[依值类型论](#dependent-type-theory)（以及 Lean 对它的实现）中的一种特定的化简操作，它可以作为判定两个[项](#term)是否[定义相等](#defeq)过程的一部分来执行。

更确切地说，它是将诸如 `(λ x, t) a` 这样的表达式化简为 `t[a/x]` 的过程，其中 `t` 中出现的变量 `x` 已被替换为 `a`。

##### 另见

* [Theorem Proving in Lean 第 2.3 节](https://lean-lang.org/theorem_proving_in_lean4/Dependent-Type-Theory/#function-abstraction-and-evaluation)

### big operators（大型运算符）

这指的是使用 `∑` 和 `∏` 字符表示的求和与求积记号，例如 [Finset.sum](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/BigOperators/Group/Finset/Defs.html#Finset.sum) 和 [Finset.prod](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/BigOperators/Group/Finset/Defs.html#Finset.prod)。

### binder（绑定子）

诸如 `(a : α)`、`[a : α]` 或 `{a : α}` 这样的表达式（其中 `a` 为任意标识符，`α` 为类型），它们作为各种 Lean 语法元素——[声明](#declaration)、`fun`、量词及其他——的一部分，表示将在该语法元素或声明的主体中被绑定的标识符。

每种绑定子在标识符是被隐式绑定（无需调用方传入）、显式绑定，还是通过[类型类推断](#typeclass-inference)绑定方面都有不同的含义。

在某些场合，特别是在 `def` 中，允许定义不带外围括号的“简单”绑定子，例如对某个标识符 `a` 使用绑定子 `a`（不带显式类型）。

### bundled vs unbundled（捆绑式与非捆绑式）

给定一个具有性质 `P` 的数学对象 `O`，捆绑 `P` 指的是创建一个 Lean [结构](#structure)，在其字段中除了结构性地定义 `O` 所需的字段外，还包含一个 `P` 的证明作为其字段之一。

相反，非捆绑式结构只包含 `O` 的定义，并单独创建一个可应用于 `O` 的项的 `is_P` 命题。

举一个具体的例子，一个[群同态](https://en.wikipedia.org/wiki/Group_homomorphism)可以看作群之间的映射 `φ: G → H`，连同一个证明 `h : φ(a * b) = φ(a) * φ(b)`。
一个捆绑式群同态会同时将 `φ` 和 `h` 作为字段，而一个非捆绑式群同态则只包含 `φ`，并配有一个单独的用于证明 `h` 的 `IsGroupHomomorphism` [声明](#declaration)。

在选择捆绑或非捆绑时，存在性能、风格或实现方面的考量，此外还有介于两者之间的灰色地带，即部分捆绑结构的某些部分而将其余部分保持非捆绑。
[Mathlib](#Mathlib) 中的[类型类](#class)主要是半捆绑式的，通常只将[载体](#carrier)类型本身非捆绑。
Mathlib 中的态射则更常采用完全捆绑式，不过两种方法的痕迹都有所存在，并在下面的资源中有所讨论。

##### 另见

* [The Lean Mathematical Library](https://arxiv.org/pdf/1910.09336.pdf)（PDF）的第 4.1.1 节（Bundled Type Classes）和第 4.1.2 节（Bundled Morphisms），这是一篇由 Mathlib 社区撰写的论文，描述了 [Mathlib](#Mathlib) 的许多架构与设计选择。

### cache（缓存）

通常指的是由 [Mathlib](#Mathlib) 的[持续集成](#continuous-integration)在每次拉取请求被合并或获得新提交时构建的一组共享的、预先构建好的 [`olean` 文件](#olean-file)。

它的目的是减轻每个 [Mathlib](#Mathlib) 用户在本地构建（或重新构建）相同 Lean 文件的需要，因为这样做可能花费大量时间（在一台普通计算机上要数小时）。

缓存是在上述持续集成中构建的，通常 Mathlib 用户使用 `lake exe cache get` 来获取其构建好的文件。

### `calc` mode（`calc` 模式）

一种[模式](#mode)，它由对表达式进行的一系列连续变换组成，这些变换涉及诸如 `=`、`<` 等传递关系，或其他被标记了 `trans` [属性](#attribute)的关系。
它通过 `calc` 关键字进入。

##### 另见

* [*Theorem Proving in Lean* 第 4.3 节](https://lean-lang.org/theorem_proving_in_lean4/Quantifiers-and-Equality/#calculational-proofs)
* [`calc` 模式社区文档](https://leanprover-community.github.io/extras/calc.html)

### carrier（载体）

对于一个将类型 `T` 与某种以附加字段表示的额外数学结构[捆绑](#bundled-vs-unbundled)在一起的 Lean [结构](#structure)（例如 [`Group`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/Group/Defs.html#Group)），载体即底层元素的类型 `T`。

对于一个将集合 `S` 与某种以附加字段表示的额外性质[捆绑](#bundled-vs-unbundled)在一起的 Lean [结构](#structure)（例如 [`Subgroup`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/Group/Subgroup/Defs.html#Subgroup)），载体即底层集合 `S`。

### class（类型类）

更完整地说，是一个 *typeclass*（或 *type class*，类型类）。

一个 Lean [结构](#structure)，其[实例](#instance)可以通过[类型类推断](#typeclass-inference)来检索。

它不同于面向对象语言中 *class* 的用法——这个词在函数式编程语言中的用法源自 [Haskell 的类型类](https://en.wikipedia.org/wiki/Type_class)。

### `conv` mode（`conv` 模式）

[策略模式](#tactic-mode)的一个子模式，它便于在假设或[目标](#goal)内部进行导航，以便重写或化简它们的目标部分。
它从策略模式经由 `conv` 关键字进入。

##### 另见

* [`conv` 模式社区文档](https://leanprover-community.github.io/extras/conv.html)

### core Lean（核心 Lean）

与 [Mathlib](#Mathlib) 或其他社区编写的 Lean 代码相区别，core Lean（或“核心库”）指的是随 Lean 自身发行版一同提供的那部分 Lean。

从历史上看，Mathlib 项目本身曾是 core Lean 的一部分，后来为了便于加快开发速度，被拆分为一个单独维护的项目。

即使在拆分之后，一些基础的[声明](#declarations)仍然是 core Lean 的一部分。

core Lean 当前的各部分内容可以在 [Lean 4 仓库](https://github.com/leanprover/lean4/tree/master/src)中找到。

### declaration（声明）

Lean 环境中的单个 Lean 运行时对象。

或者，含糊地说，指可以定义或声明此类对象的若干 Lean 命令中的任意一个。

此类命令的例子包括 `def`、`lemma`、`theorem`、`constant` 或 `example` 命令等。

更多细节可在 [Lean 文档](https://lean-lang.org/lean4/doc/declarations.html#basic-declarations)中找到。

### defeq（定义相等）

*定义相等（Definitional equality）*。两个[项](#term) `a b : α` 是定义相等的，如果内核能够自动证明 `rfl : a = b`。
这比[命题相等](#propeq)更强，但不如[句法相等](#syntactical-equality)那么强。

##### 另见

[Equality, specifications and implementations](https://xenaproject.wordpress.com/2020/07/03/equality-specifications-and-implementations/)，来自 Xena Project

### dependent type theory（依值类型论）

一种[类型论](#type-theory)，在其中还可以拥有依赖于参数的类型，例如“某个日历月份中的天数”这一类型，其具体取值依赖于具体的月份，因为不同的月份天数不同。
更多例子可在下面的资源中找到。
Lean 对依值类型论的实现基于所谓的*构造演算（Calculus of Constructions）*，使其既可用于复杂的数学推理，也可用于软件验证。

##### 另见

* [*Theorem Proving in Lean* 第 2 节](https://lean-lang.org/theorem_proving_in_lean4/Dependent-Type-Theory/)，其中讨论了 Lean 特定版本的依值类型论

* [构造演算，来自 Wikipedia](https://en.wikipedia.org/wiki/Calculus_of_constructions)，对构造演算的进一步概述

* [Dependent Type Theory，来自 nLab](https://ncatlab.org/nlab/show/dependent+type+theory)，对依值类型论的一般性论述

* [Mike Shulman 的 *In Praise of Dependent Types*](https://golem.ph.utexas.edu/category/2010/03/in_praise_of_dependent_types.html)

* [Andrej Bauer 对“What makes dependent type theory more suitable than set theory for proof assistants?”的回答](https://mathoverflow.net/a/376973)

### diamond（菱形）

在类型类[实例](#instance)图中，存在某个[类型类](#class)的多个相互冲突的[项](#term)。
菱形很可能在[类型类推断](#typeclass-inference)过程中引发问题，因为推断试图构造该类型类的单一项，因而可能无法做到。
在不加限定时，“菱形”最常指这种不良情形，即菱形中非[定义相等](#defeq)的项可能导致错误，导致无法通过 `refl` 证明的[目标](#goal)，甚至可能导致根本无法证明相等的目标。
在 [Mathlib](#Mathlib) 中，由于其众多的[层级](#hierarchy)，菱形大量存在。
修复或缓解菱形通常涉及重构出问题类型类的字段或实例优先级。
跨库边界的菱形——例如类型类图的一部分位于 Mathlib 中，另一部分位于某个依赖 Mathlib 并添加新实例或类型类的库中——可能特别难以在不进行修改的情况下修复或避免。

##### 另见

* [Mathlib 关于 `AddMonoid` 和 `Monoid` 的设计注记](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/Group/Defs.html#Design-note-on-AddMonoid-and-Monoid)，一个规避菱形的具体例子

* [Forgetful Inheritance](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/Group/Defs.html#Mathlib.LibraryNote.%C2%ABforgetful%20inheritance%C2%BB)，同样来自 Mathlib 文档，讨论了在类型上的“更丰富”与较贫乏结构这一情形下避免菱形的一般模式

<a name="dot-notation"></a>

### dot notation / generalized field notation / generalized projections（点号记法 / 广义字段记法 / 广义投影）

允许诸如 `((foo a b c).bar x.y).baz` 这样记号的语法糖。

Lean 为语法 `foo.bar` 提供了两种解释：它可以表示 `foo` 命名空间中的声明 `bar`，也可以是广义字段记法。我们在此对后者展开说明。

假设 `foo` 的类型为 `C x1 ... xn`，其中 `C` 是某个常量，`x1 ... xn` 是任意的，并假设上下文中存在一个名为 `C.bar` 的声明，它接受一个类型为 `C x1 ... xn` 的参数。那么 `foo.bar` 就是 `C.bar foo` 的语法糖。对于形如 `foo.bar _ ... _` 的、带有（隐式或显式）参数的调用，Lean 足够智能，能够展开为 `C.bar _ ... foo _ ... _`，从而使一切都能通过类型检查。在前面这些例子中，`foo` 也可以是更复杂的表达式，例如 `(foo bar baz).quux` 中的函数应用。

### environment linter（环境检查器）

*环境检查器*是一种通过分析导入声明与本地声明所构成的整个环境，来寻找 Lean 声明中无意错误的[检查器](#lint)。
此外还有[句法检查器](#syntax-linter)（对单个声明运行）和[风格检查器](#style-linter)（对字面源文本运行）。
要对当前文件运行环境检查器，请使用 `#lint` 命令。
偶尔会引入新的检查器以检测更多类别的错误。
Mathlib 的[持续集成](#continuous-integration)确保任何此类新代码都能通过既定的检查器。

可以通过使用 `nolint` [属性](#attribute)对某一段特定代码禁用环境检查。
一些早于 CI 句法检查器的检查器失败被记录在一个自动生成的 [nolint 文件](https://github.com/leanprover-community/mathlib4/blob/master/scripts/nolints.json)中；随着这些错误被修复，该文件的长度应当随时间趋于零。

### `equiv`（等价）

与数学上的相等不同，[`equiv`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Logic/Equiv/Defs.html) 允许定义类型之间的等价或同余。
需要注意的一点是，`equiv` [携带数据，而不仅仅是一个证明](#bundled-vs-unbundled)。

### goal（目标）

在 Lean 中交互式地证明定理的语境下，指每个证明正在进行中的目标陈述。

或者更广泛地，从类型论的角度看，指需要为之给出一个[项](#term)的单个类型。
对于命题而言，给出一个[项](#term)等价地归结为前述的证明这一概念。

### golfing（代码高尔夫）

试图或努力使某一段可工作的代码尽可能简短；在 Lean 的语境下，常常是对证明的长度进行高尔夫优化。
经过高尔夫优化的证明常常使用[项模式](#term-mode)，并且总体上将简洁性置于可读性之上。
这种混淆常被有意或有利地用来向读者表明某个证明是机械性的或平凡的。

<a name="heavy-rfl"></a>

### heavy `rfl` / heavy `refl`（重型 `rfl` / 重型 `refl`）

一种由 Lean 求值时运行缓慢的 `rfl`（或 `refl`）用法。
当 `rfl` 被要求一次性执行许多步定义性归约时，就会出现重型 `rfl`，其结果是一个很小的证明项，但需要 Lean 进行大量计算才能确保其通过类型检查。

[这个 Zulip 讨论](https://leanprover.zulipchat.com/#narrow/stream/113488-general/topic/refl.20taking.2020.20seconds)给出了一个特别慢的例子。

### hierarchy（层级）

数学某个相关领域内一系列约束逐渐增强的[类型类](#class)的集合。
在 [Mathlib](#Mathlib) 中，我们有*代数层级*（`semiring`、`ring`、`field`……）、*序层级*（`preorder`、`partial_order`、`linear_order`……）、*拓扑层级*（`t1_space`、`t2_space`、`normal_space`……）、*范畴层级*（`preadditive`、`abelian`、`monoidal`……），还有*标量层级*（`mul_action`、`distrib_mul_action`、`module`……）、*范数层级*，以及前述层级的交集，如*序-代数层级*、*拓扑-代数层级*等等。

### HoTT（同伦类型论）

*同伦类型论（Homotopy Type Theory）*，一种[类型论](#type-theory)，其特点是包含了一条额外的*单价公理（univalence axiom）*，它使得这样一个概念变得精确：被认为等价的某类型的两个不同实现，在数学意义上也是相等的。

在 Lean 2 中，Lean [内核](#kernel)可以被实例化为标准模式和 HoTT 模式。
标准库与[同伦类型论库](https://github.com/leanprover/lean2/blob/8072fdf9a0b31abb9d43ab894d7a858639e20ed7/hott/hott.md)是并行开发的。这两种实例化彼此并不兼容，因为（标准模式中的）单例消去与 HoTT 的单价公理是不相容的。
Lean 3 的[内核](#kernel)放弃了对 HoTT 模式的支持。因此，从 Lean 3 起，Lean 不再随附 HoTT 库。

举一个说明性的具体例子，自然数类型有许多[定义](https://en.wikipedia.org/wiki/Natural_number#Formal_definitions)，它们都可以看作是在构造等价的数学对象。
core Lean 拥有一个[皮亚诺式的实现](https://leanprover-community.github.io/mathlib_docs/init/core.html#nat)，而 [Mathlib](#Mathlib) 还拥有一个[基于二进制表示的实现](https://leanprover-community.github.io/mathlib_docs/data/num/basic.html#pos_num)，并证明了它与前者等价。
鉴于 Lean *不*具有单价公理，这两个类型是等价的，但它们作为类型并不能被证明*相等*。
而一种基于 HoTT 的语言（或库）则会进一步将这些类型称为相等的。

<a name="intervals"></a>

### `Icc`, `Ico`, `Ioc`, `Ioo`, `Ici`, `Ioi`, `Iic`, `Iio`

在 [Mathlib](#Mathlib) 中用于指代 8 种数学区间之一的简写记号。
共有 `8` 种区间类型，取决于该区间在每一端是*闭的（closed）*、*开的（open）*还是延伸至*无穷（infinity）*。
这些名称被设计得很紧凑，方法是将每个区间记为 `I` + 它在左端的端点情况 + 它在右端的端点情况。
`Iii`（按命名约定将指代两端皆无穷的区间）并未使用。

##### 另见

* [`Mathlib.Order.Interval.Set.UnorderedInterval`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/Interval/Set/UnorderedInterval.html)，它在这些区间之上构建了无序区间（其端点可以按任意顺序给定）。

### infoview（信息视图）

在交互式编辑 Lean 文件的语境下，指一个显示增量[目标](#goal)状态、诊断信息、错误以及 Lean [小部件](#widget)输出的窗口或界面。

### instance（实例）

两个密切相关概念之一：

* 由 `def`、`lemma` 或其他[声明](#declaration)所接受的、用方括号（`[]`）括起来的[类型类](#class)参数，使其在使用该声明时由[类型类推断](#typeclass-inference)系统解析。
* 用同名的 `instance` 命令创建的[声明](#declaration)，或等价地用 `instance` [属性](#attributes)标记的声明，二者都会将该声明注册到类型类推断系统中，以供上述用途使用。
举一个具体的例子，[Mathlib](#Mathlib) 为 `ℝ` 定义了一个 `linear_order` 实例，使得实数可以用 `<` 进行比较。

### Lean 3

Lean 的一个已弃用版本，已被 Lean 4 取代。Mathlib 在 2022—2023 年间完全从 Lean 3 移植到了 Lean 4。

### kernel（内核）

在 Lean 的实现（以及[更广泛地](https://en.wikipedia.org/wiki/Proof_assistant#System_comparison)的证明助手）的语境下，内核是验证每个证明正确性的核心组件。

相比于 Lean 的[策略](#tactic)实现代码的规模[1^]，更不用说相比于 [Mathlib](#Mathlib)，Lean 的内核实现相对较小，从而使我们能够更有信心地确信证明没有错误，而无需依赖庞大或复杂的高层构造。

[1^]: 这种相对的小巧性，以及由此带来的可独立验证性，被称为证明助手实现的 *de Bruijn 判据*

##### 另见

* [Lean 的内核实现](https://github.com/leanprover/lean4/tree/master/src/kernel)

* [The challenge of computer mathematics，作者 Henk Barendregt 与 Freek Wiedijk (2005)](https://royalsocietypublishing.org/doi/full/10.1098/rsta.2005.1650)

* [证明助手的组成部分，来自 Andrej Bauer 对“What makes dependent type theory more suitable than set theory for proof assistants?”的回答](https://mathoverflow.net/a/376973)

### Lean Together

面向 Lean 用户社区、其 [Mathlib](#Mathlib) 库用户以及更广泛的定理证明器社区的[年度会议](https://leanprover-community.github.io/lt2026/)。

往届活动的演讲或报告已[分享在社区 YouTube 频道](https://www.youtube.com/channel/UCWe5B7Ikr0AI9727doEUxPg)上。

### lint（检查）

*检查器（linter）*是一种用于查找代码中难以发现的错误的小程序。
在提交拉取请求时，Mathlib 会在每次 [CI 运行](#continuous-integration)中接受检查。

我们有多种机制来检查代码的不同方面：
风格与格式、单个声明的句法，以及声明在环境中相互组合的方式。
对于这几种情形中的每一种，检查器的使用和定义方式都大不相同。

* [风格检查器](#style-linter)由 `lake exe lint-style` 运行，它们在 Mathlib 中定义并在 Mathlib 中的某个特定文件中声明，以文件的 `String` 内容作为输入，并通过在 `scripts/nolints-style.txt` 中添加例外来将其静默。
* [句法检查器](#syntax-linter)自动运行，它们在 core Lean 中定义并用 `add_linter` 命令声明，以声明的 `Lean.Syntax` 作为输入，并通过 `set_option` 命令将其静默。
* [环境检查器](#environment-linter)由 `#lint` 或 `lake exe lintAll` 运行，它们在 Batteries 中定义并用 `@[env_linter]` 属性声明，以文件的 `Environment` 作为输入，并通过 `@[nolint]` 属性将其静默。

### Mathlib

一个面向 Lean 4 的[大型、由社区维护的数学集合](https://github.com/leanprover-community/mathlib4)。

### mode（模式）

在编写 Lean 代码的语境下，指一组相关的语法元素或关键字，它们使某种特定风格的形式化推理或[证明项](#proof-term)的构造变得高效。
Lean，尤其是限定于 [Mathlib](#Mathlib) 范围内的 Lean，拥有少数几种这样的模式——[策略模式](#tactic-mode)、[项模式](#term-mode)、[calc 模式](#calc-mode)和 [conv 模式](#conv-mode)。
某种特定的模式可能使针对特定类型[目标](#goal)的推进变得更容易。
然而，在构造一个[证明项](#proof-term)的过程中，一个证明往往会混合使用各种模式。

### module（模块）

包含 Lean 源代码的单个文件。

不要将其与数学中的 `module`（模）混淆，即向量空间的推广。

### module docstring（模块文档字符串）

[模块](#module)级别的注释，概述文件中可以找到的内容。
我们要求每个文件都有一个，但[一些旧文件](https://github.com/leanprover-community/mathlib4/blob/master/scripts/style-exceptions.txt)仍然没有。

### MWE（最小可工作示例）

*最小可工作示例（Minimal Working Example）*，一种通过将一段 Lean 代码精简到其本质部分、同时仍可被他人运行，从而更容易就该代码获得帮助的方式。

更多信息可在 [MWE 页面](mwe.html)上找到。

### non-terminal `simp`（非终结性 `simp`）

`simp` 策略的一次调用，它既不是在某个特定[子目标](#goal)上调用的最后一个策略，也不使用 `simp only` 来显式限制它所考虑的 [simp 引理](#simp-lemma)。
应避免使用非终结性 `simp`，因为它们难以维护，原因在于随着 Mathlib 随时间推移添加或修改 `simp` 引理集，它们的行为或运行时会发生变化。

##### 另见

`simp` 文档的[“非终结性 `simp`”一节](https://leanprover-community.github.io/extras/simp.html#non-terminal-simps)

### olean file（olean 文件）

Lean 在构建一个 Lean [模块](#module)时所产生的一种缓存的、已编译的二进制文件。
`olean` 文件与构建它们的特定 Lean 版本绑定，其名称与对应的模块相匹配（因此一个名为 `Foo.lean` 的文件将在 `.lake` 文件夹中有一个对应的 `Foo.olean` 文件）。
构建一个 `olean` 文件可以手动完成（例如通过 `lake build`），但对于像 [Mathlib](#Mathlib) 这样的协作项目，它们是通过 [CI](#continuous-integration) 构建为一个共享的 [olean 缓存](#cache)，然后每个 Mathlib 用户只需检索即可。

### orange bar of hell（地狱橙条）

在 VSCode（或其他编辑器）中交互式编辑 Lean 通常相当流畅。

然而，*地狱橙条*指的是偶尔出现的、Lean 文件旁侧边栏中的橙色条不消失或不更新的情形。
通常这些条指示文件中 Lean 仍在求值的部分，但如果这些条一直存在，则表明进度没有推进。
修复这些条通常可以通过关闭任何不活动的编辑器标签页，然后打开 VSCode 命令面板（`ctrl-shift-p` 或 `cmd-shift-p`）并运行 `Lean: Restart` 来完成。
出现这种情况的另一个常见原因是，由于[缓存的](#cache) [olean 文件](#olean-file)集不匹配，Lean 不得不（重新）编译所有导入的 [Mathlib](#Mathlib) 文件。
在这种情况下，通过 `lake exe cache get` 确保正确下载 Mathlib 缓存应当能解决该问题。

### propeq（命题相等）

*命题相等（Propositional equality）*。两个[项](#term) `a b : α` 是命题相等的，如果我们能够证明 `a = b`。
这比[定义相等](#defeq)和[句法相等](#syntactical-equality)都更弱。

##### 另见

[Equality, specifications and implementations](https://xenaproject.wordpress.com/2020/07/03/equality-specifications-and-implementations/)，来自 Xena Project

### `simp` lemma（`simp` 引理）

一个被标记了某个[属性](#attribute)的引理，该属性使其可被 `simp` 策略使用。

好的 `simp` 引理会引导 `simp` 策略将复杂的表达式归约为更简单的表达式，常常达到 `simp` 策略本身就能闭合许多目标的程度。

##### 另见

* [Mathlib 的 `simp` 文档](https://leanprover-community.github.io/extras/simp.html#simp-lemmas)。
* [*Theorem Proving in Lean* 第 5.7 节](https://lean-lang.org/theorem_proving_in_lean4/Tactics/#using-the-simplifier)。

### `simp`-normal form（`simp` 范式）

[Mathlib](#Mathlib) 中的一种约定，用于将具有多种等价形式的命题表达为单一的约定形式。

例子和更多细节可在 [`simp` 页面](simp.html#simp-normal-form)上找到。

### syntax linter（句法检查器）

*句法检查器*是一种试图查找 Lean 声明中无意错误的[检查器](#lint)。
此外还有[环境检查器](#environment-linter)（对整个环境运行）和[风格检查器](#style-linter)（对字面源文本运行）。
偶尔会引入新的检查器以检测更多类别的错误。
Mathlib 的[持续集成](#continuous-integration)确保任何此类新代码都能通过既定的检查器。
可以通过使用 `set_option` 命令对某一段特定代码禁用句法检查。

### style linter（风格检查器）

*风格检查器*是一种试图确保 [Mathlib](#Mathlib) 内代码外观或风格统一、而不影响其工作行为的[检查器](#lint)。
此外还有[环境检查器](#environment-linter)（对整个环境运行）和[句法检查器](#syntax-linter)（对单个声明运行）。
具体而言，Mathlib 包含一些[简短的 Lean 程序](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/Linter/TextBased.html)，例如检查行末是否不以空白结尾，等等。
还有一些用 Python 实现的风格检查器，它们正被用 Lean 编写的检查器所取代。
Mathlib 的[持续集成](#continuous-integration)确保新代码都能通过既定的检查器。
允许的风格检查例外被存储在仓库内的一个[风格例外文件](https://github.com/leanprover-community/mathlib4/blob/master/scripts/style-exceptions.txt)中。

### syntactical equality（句法相等）

两个[项](#term) `a b : α` 是句法相等的，如果它们字面上是同一个表达式。
这比[定义相等](#defeq)和[句法相等](#syntactical-equality)都更强。

##### 另见

[Equality, specifications and implementations](https://xenaproject.wordpress.com/2020/07/03/equality-specifications-and-implementations/)，来自 Xena Project

### tactic mode（策略模式）

一种 Lean [模式](#mode)，其特点是依赖于一系列[策略](#tactic)，这些策略常常便于产生与基于纸笔的推理颇为相似的证明，尽管往往要使用复杂的策略来自动化证明中繁琐的部分。
有多种[进入策略模式](https://lean-lang.org/theorem_proving_in_lean/tactics.html#entering-tactic-mode)的方式。
可以从[项模式](#term-mode)使用 `by` 关键字进入它。
其他模式也可以穿插在其中，常常是为了协同产生一个易于理解、高效、简短或可读的整体证明。
最终，一个策略模式块的结果是一个[项](#term)，它是通过其中的策略组装而成的。

##### 另见

* [*Theorem Proving in Lean* 第 5 节](https://lean-lang.org/theorem_proving_in_lean4/Tactics/#Theorem-Proving-in-Lean-4--Tactics)，其中讨论了策略，以及进出策略模式

* [`show_term` 策略](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference/#show_term)，它可以揭示组装而成的[项](#term)

* [Mathlib 策略文档](https://leanprover-community.github.io/mathlib-manual/html-multi/Tactics/)，其中有一份全面的策略列表

### term（项）

*项*是 Lean [类型论](#type-theory)中表示某个（数学）对象的基本组成部分。

*项*这个词也可以用来与*类型*形成对照：如果我们写 `x : X`，那么 `x` 是项，而 `X` 是它的类型。
在像 Lean 这样的[依值类型论](#dependent-type-theory)中，类型本身也由项来表示。

*证明项*是表示一个数学证明的一种方式。
我们也称这样的证明是用[项模式](#term-mode)（与[策略模式](#tactic-mode)相对）写成的。

##### 另见

* [*Lean Language Reference* 第 4 节](https://lean-lang.org/doc/reference/latest/The-Type-System/#--tech-term-Terms)

### term mode（项模式）

一种 Lean [模式](#mode)，它通过使用函数式子表达式来组装单个[项](#term)。
与[策略模式](#tactic-mode)相比，项模式的证明往往长度较短，尽管对人类来说可能更难阅读。
有多种进入项模式的方式。
一个[声明](#declaration)的主体以项模式开始，或者在[策略模式](#tactic-mode)中常常使用 `exact` [策略](#tactic)进入它。
高效的项模式证明常常有助于[代码高尔夫](#golfing)。

诸如 `have`、`suffices` 和 `show` 这样的命令可以用来编写结构化的项模式证明，它们比裸的证明项更易于阅读。

### TPIL

“[Theorem Proving in Lean](https://lean-lang.org/theorem_proving_in_lean4/)”，一本由 Jeremy Avigad、Leonardo de Moura、Soonho Kong 和 Sebastian Ullrich 编写、并有 Lean 社区贡献的免费在线教科书，“旨在教你在 Lean 中开发和验证证明”。
该书从对 Lean 所使用的[类型论](https://lean-lang.org/theorem_proving_in_lean4/Dependent-Type-Theory/#dependent-type-theory)的简单介绍开始，进而阐释诸如[策略](https://lean-lang.org/theorem_proving_in_lean4/Tactics/#Theorem-Proving-in-Lean-4--Tactics)、[归纳类型](https://lean-lang.org/theorem_proving_in_lean4/Inductive-Types/#inductive-types)和[类型类](https://lean-lang.org/theorem_proving_in_lean4/Type-Classes/#type-classes)等主题。

### type theory（类型论）

一种带有两类基本对象——[项](#term)和类型——的形式系统。
它也可以指对这类语言的研究领域，因为某种特定的类型论可能包含的各种附加性质或特征之间存在着细微差别。

Lean 的[依值](#dependent-type-theory)类型论是其数学基础系统的根基，与集合论形成对照。
在集合论的基础上，所有对象在形式意义上都是由单一种类的原始对象——集合——构建出来的。人们推理所构造的集合是否是其他集合的成员。
这种成员关系的概念可以对任意两个形式集合提出，这可能使一些陈述在形式上有意义，即便它们对人类而言在数学上毫无意义——例如询问数 2 是否是数 37 的成员（数按[集合论方式](https://en.wikipedia.org/wiki/Set-theoretic_definition_of_natural_numbers)定义）。
相比之下，在类型论中，每个项都有一个相关联的类型，陈述或命题本身也是如此。
例如，人们有自然数类型（在 [Mathlib](#Mathlib) 中为 `ℕ`），或命题类型（`Prop`），或 `2 + 2 = 4` 的*证明*的类型，或从 `ℕ` 到 `Prop` 的函数的类型（`ℕ → Prop`），并且可以构造这些类型的项——分别可能是项 `2`、`2 + 2 = 37`、`rfl` 和 `λ n, true`。
然而并非每个项*都是*一个类型，因此与前述集合论的困难不同，如果询问 37 是否具有*类型* 2 是没有意义的，那么人们就无法构造出这样的陈述。

### unicode abbreviation（Unicode 缩写）

在编辑 Lean 文件的语境下，缩写是一种使用描述性快捷方式来输入标准键盘布局上通常没有的符号的方法。

例如，不等号 “≠” 可以用序列 `\neq` 输入。

完整的缩写列表（及其替换内容）可在 [`vscode-lean4` 仓库](https://github.com/leanprover/vscode-lean4/blob/master/lean4-unicode-input/src/abbreviations.json)中找到。

### whnf（弱头范式）

如果一个 Lean 表达式满足下面所链接资源中提到的若干归约判据，则称它处于*弱头范式（weak head normal form）*，常缩写为 `whnf`。
非正式地说，处于 whnf 的表达式其最外层部分已被求值，尽管内部的子表达式可能尚未被求值。

它也可以指一个将表达式归约为此形式的命令。

##### 另见

* [What is weak head normal form? - Stack Overflow](https://stackoverflow.com/questions/6872898/what-is-weak-head-normal-form)
* [Weak head normal form - The Haskell wiki](https://wiki.haskell.org/Weak_head_normal_form)

### widget（小部件）

一个可扩展的框架，用于通过 Lean 代码定义交互式的、组件化的图形元素，这些元素在交互式定理证明期间渲染于[信息视图](#infoview)中。

小部件也可以指由上述框架渲染的单个图形元素。

小部件提供了一种机制，用于显示在交互式定理证明过程中会更新的额外上下文或信息。

##### 另见

* [Lean Together 2021: Widgets, interactive output in VSCode](https://www.youtube.com/watch?v=8NUBQEZYuis)，一场由 Edward Ayers 在 [Lean Together 2021](#lean-together) 上所作的报告，展示了小部件所支持的一些功能
* [core Lean 中的小部件源代码](https://leanprover-community.github.io/mathlib4_docs/Lean/Widget/Types.html)
