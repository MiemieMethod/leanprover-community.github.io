<div class="alert alert-info">
<p>
我们目前正在更新 Lean 社区网站，以介绍如何使用 Lean 4 进行工作，
但你今天在这里看到的大部分信息仍然是关于 Lean 3 的。
</p>
<p>
<b><em>警告：Lean 3 与 Lean 4 互不兼容。</em></b> 本页面中的所有示例在 Lean 4 中都无法运行。
  关于编写 Lean 4 策略的参考资料，例如可参见
  <a href="https://leanprover-community.github.io/lean4-metaprogramming-book/">Metaprogramming in Lean 4</a>
  以及 <a href="https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Custom-Tactics/#custom-tactics">The Lean Language Reference</a>。
</p>
<p>
非常欢迎提交更新本页面以适配 Lean 4 的拉取请求。
本页面底部有相关链接。
</p>
<p>
在这一过渡时期，请访问 <a href="https://leanprover.zulipchat.com">leanprover zulip</a>，
寻求你所需要的任何帮助！
</p>
<p>
Lean 3 的网站已被<a href="https://leanprover-community.github.io/lean3/">归档</a>。
如果你需要链接到 Lean 3 特有的资源，请链接到那里。
</p>
</div>

# 教程：在 Lean 3 中编写策略

***本页面是关于 Lean 3 的：**请在继续之前阅读上方的提示横幅。*

这是一篇帮助你开始在 Lean 中编写自己的策略的入门教程。
它面向的读者群体不一定有在函数式编程语言中
使用单子（monad）的经验（例如大多数数学家）。

学习编写策略时其他有用的资源包括：
* Rob Lewis 在 Lean for the Curious Mathematician 2020 上关于 Lean 元编程的
  [视频教程](https://www.youtube.com/playlist?list=PLlF-CfQhukNnq2kDCw2P_vI5AfXN7egP2)
* [Hitchhiker's Guide to Logical Verification](https://github.com/blanchette/logical_verification_2021/raw/main/hitchhikers_guide.pdf) 的第 7 章
* 关于 Lean 元编程的原始论文
  [A Metaprogramming Framework for Formal Verification](https://lean-lang.org/papers/tactic.pdf)

## 单子学（Monadology）

策略是作用于证明状态的程序。但 Lean 是一门
函数式编程语言。这意味着你所能做的一切就是
定义并求值函数。每个函数接受具有
预定义类型的输入，并给出具有预定义类型的输出。这似乎
妨碍了拥有全局状态（例如当前的假设和目标），
也妨碍了输出类型依赖于输入值（例如一个
策略可以成功或失败），或输出消息。这些问题
通过三层技巧来解决（以下简短的描述
有望在后文中变得更加清晰）：
* 使用复杂的类型，将证明状态和策略运行
  状态携带传递
* 使用巧妙的记号，隐藏掉大部分复杂的类型
  管理与组合
* 使用交互式策略块，由 `by` 引入或由
  `begin`/`end` 界定

前两点统称为单子式编程（monadic programming，
当然有更精确的定义，但我们会尽量忽略它）。

一个能够检视证明状态、修改它，并
可能返回某个类型为 `α` 的值（或失败）的函数，其类型称为 `tactic α`。特别地，
`tactic unit` 只关乎操作证明状态，而不
尝试返回任何东西（从技术上讲它会返回某个类型为
`unit` 的值，`unit` 是恰好只有一个项的类型，记作 `()`）。
这样的函数要么被其他
策略调用——这些通常位于 `tactic` 命名空间中——要么被
用户在策略块内交互式地调用——这些必须位于
`tactic.interactive` 命名空间中（对于非常简单的
策略这并非完全必要，但一般而言忽略此规则会发生奇怪的事情）。一个
有时很方便的捷径是：可以使用
`` run_cmd add_interactive [`my_tac1,`my_tac2, `my_tac3] `` 将名为
`my_tac1`、`my_tac2`、`my_tac3` 的定义复制到 `tactic.interactive` 命名空间中。
这些函数将用于生成 Lean 证明，但我们既不会对这些函数本身证明
任何东西，常量 `my_tac1`、
`my_tac2` 等也不会出现在它们所生成的证明
中。通过在它们前面加上关键字 `meta`，我们告诉 Lean
它们仅用于“求值目的”，这会禁用
非 `meta` 声明必须通过的某些检查。
有了这些知识，就足以编写第一个策略了。

```lean
meta def my_first_tactic : tactic unit := tactic.trace "Hello, World."

example : true :=
begin
  my_first_tactic,
  trivial
end
```

在该示例中，`my_first_tactic` 以绿色下划线标出（在 VS Code 中），
将光标移到那一行上会在 Lean
消息缓冲区中显示我们的消息。

接下来我们需要学习如何串联多个动作。归根结底，这
完全是关于组合函数的，但单子记号将其隐藏，
并模拟命令式编程。我们需要使用 `and_then`
组合子。第一种方式是使用中缀记号 `>>`，如下：

```lean
meta def my_second_tactic : tactic unit :=
tactic.trace "Hello," >> tactic.trace "World."
```
现在这会分两段打印我们的消息。或者，可以使用
`do` 语法，它还有其他好处。它引入了一个
以逗号分隔的指令列表，按顺序依次执行。
```lean
meta def my_second_tactic' : tactic unit :=
do
  tactic.trace "Hello,",
  tactic.trace "World."
```

除了显示消息之外，策略接下来能做的事情是失败，
并可能附带一些说明。
```lean
meta def my_failing_tactic  : tactic unit := tactic.failed

meta def my_failing_tactic' : tactic unit :=
tactic.fail "This tactic failed, we apologize for the inconvenience."
```

在串联指令时，第一次失败会中断整个过程。
然而 `orelse` 组合子（以中缀 `<|>` 表示）允许在
其左侧失败时尝试其右侧。下面的策略将
成功地传达它的消息。
```lean
meta def my_orelse_tactic : tactic unit :=
my_failing_tactic <|> my_first_tactic
```

接下来要做的组合操作是使用某个函数，它在
读取或改变证明状态之后，实际尝试返回
某个值。例如内置的 `tactic.target`（尝试）返回
当前目标。这个目标的类型是 `expr`（关于该类型后文会详述）。
因此 `tactic.target` 的类型是 `tactic expr`。假设我们想追踪
当前目标。一个朴素的尝试是：
```lean
meta def broken_trace_goal : tactic unit :=
tactic.trace tactic.target    -- WRONG!
```
这不可能正确，因为 `tactic.target` 可能失败（可能
不再有目标），而 `tactic.trace` 不能把这种失败作为
输入。我们需要绑定（bind）组合子，其中缀记号为 `>>=`，它在
成功时把左侧的输出传给右侧，否则失败。
```lean
meta def trace_goal : tactic unit :=
 tactic.target >>= tactic.trace
```
或者，特别是当 `tactic.target` 的输出可能被多次
使用时，可以在 `do` 块中使用 `←` 进行赋值（与重写
语法中的箭头相同）。当然，如果赋值右侧失败，这种对命令式
变量赋值的模拟也会失败（就像上面那些失败的策略一样）。
```lean
meta def trace_goal' : tactic unit :=
do
 goal ← tactic.target,
 tactic.trace goal
```
请注意，这种赋值只是尝试从某个类型为 `tactic α` 的东西中
提取类型为 `α` 的数据。它不能用于存储
普通的东西。下面这段代码无法工作。
```lean
meta def broken_assignment : tactic unit :=
do
 message ← "Hello, World.",  -- WRONG!
 tactic.trace message
```
不过，可以在 `do` 块中使用 `let`，如下：
```lean
meta def let_example : tactic unit :=
do
 let message := "Hello, World.",
 tactic.trace message
```
接下来，我们想编写返回某个值的策略，正如 `tactic.target`
所做的那样。唯一额外的要素是 `return` 函数。
下面的函数在没有更多目标时尝试返回 `tt`，否则返回 `ff`。
接下来的那个可以交互式使用，并追踪其结果
（注意，交互式地使用第一个函数不会产生任何可见效果，
因为交互式使用会忽略返回值）。
```lean
meta def is_done : tactic bool :=
(tactic.target >> return ff) <|> return tt

meta def trace_is_done : tactic unit :=
is_done >>= tactic.trace
```
关于单子赋值，我们还需要了解的最后一件事是模式匹配
赋值。下面的策略尝试将表达式 `l` 和 `r` 定义为
当前目标的左侧和右侧。它还使用了
`to_string` 函数，该函数与 `trace` 结合使用对于
调试策略非常方便，并且适用于任何作为 `has_to_string` 实例的类型。
```lean
meta def trace_goal_is_eq : tactic unit :=
do t ← tactic.target,
   match t with
   | `(%%l = %%r) := tactic.trace $ "Goal is equality between " ++ (to_string l) ++ " and " ++ (to_string r)
   | _ := tactic.trace "Goal is not an equality"
   end
```
Lean 还为带有单个模式和一个通配符的模式匹配提供了专门的语法，
其中只有在模式匹配成功时执行才会继续到 `do` 块的下一行，否则
执行 `|` 之后的表达式：
```lean
meta def trace_goal_is_eq : tactic unit :=
do `(%%l = %%r) ← tactic.target | tactic.trace "Goal is not an equality",
   tactic.trace $ "Goal is equality between " ++ (to_string l) ++ " and " ++ (to_string r)
```

如果省略 `|`，那么当模式不匹配时该策略会失败。
我们可以使用前面提到的 `orelse` 组合子来捕获这种失败，但请注意，
这样做会比前面捕获更多类型的失败：
```lean
meta def trace_goal_is_eq : tactic unit :=
(do  `(%%l = %%r) ← tactic.target,
     tactic.trace $ "Goal is equality between " ++ (to_string l) ++ " and " ++ (to_string r),
     some_other_tactic)
   <|> tactic.trace "Goal is not an equality, or `some_other_tactic` failed"
```
上面代码中的圆括号看起来不太美观。可以改用
花括号，它允许界定一个 `do` 块，如下：
```lean
meta def trace_goal_is_eq : tactic unit :=
do { `(%%l = %%r) ← tactic.target,
     tactic.trace $ "Goal is equality between " ++ (to_string l) ++ " and " ++ (to_string r) }
   <|> tactic.trace "Goal is not an equality"
```

## 第一个实际可用的策略

我们已经学习了足够的单子学，可以理解我们的第一个有用的策略了：
`assumption` 策略，它在局部上下文中搜索一个
能够关闭当前目标的假设。它还使用了另外几个内置
策略，它们都在核心库的
[init/meta/tactic.lean](https://github.com/leanprover-community/lean/blob/master/library/init/meta/tactic.lean) 中声明并有简要文档说明，但实际上是用 C++ 实现的。
首先 `infer_type : expr → tactic expr`
尝试确定一个表达式的类型（由于它返回一个
`tactic expr`，它必须如上所述与 `>>=` 或 `←` 串联起来）。
其次是 `tactic.unify`，它在忽略几个可选参数的情况下，接受
两个表达式，当且仅当它们在定义上相等时成功。
assumption 策略的第一部分是一个辅助函数，它在一个
表达式列表中搜索与某个表达式 `e` 共享类型的
表达式，并返回第一个匹配项（如果没有匹配项则失败）。
```lean
meta def find_matching_type (e : expr) : list expr → tactic expr
| []         := tactic.failed
| (H :: Hs)  := do t ← tactic.infer_type H,
                   (tactic.unify e t >> return H) <|> find_matching_type Hs
```
请利用前一节的内容，确保你真正理解上面代码中的控制流。
其基本模式是经典的列表递归查找。注意表达式 `e`
位于冒号左侧，因此它会原封不动地传递给递归调用
`find_matching_type Hs`。名称 `H` 取自 `hypothesis`（假设），
而 `Hs` 遵循 Haskell 的命名约定，表示多个假设。对于
非空列表所发生的事情，其命令式类比可以
写成如下命令式伪代码
```text
if unify(e, infer_type(H)) then return H else find_matching_type(e, HS)
```
现在我们可以把这个函数用于我们的交互式策略。我们首先需要
使用 `local_context` 来获取局部上下文，它返回一个
表达式列表，我们可以将其传给 `find_matching_type`。如果那个
函数成功，它的输出会被传给内置策略
`tactic.exact`。这里我们需要使用完全限定名，因为可能会与
`exact` 的交互式版本混淆（后者接受
不同的参数，因此它并不是非交互式版本的精确副本）。这是一个
很好的机会来指出：本教程开头为清晰起见到处都使用了
完全限定名，但当然
实际工作流程中应该打开 `tactic` 命名空间。
```lean
meta def my_assumption : tactic unit :=
do { ctx ← tactic.local_context,
     t   ← tactic.target,
     find_matching_type t ctx >>= tactic.exact }
<|> tactic.fail "my_assumption tactic failed"
```
附加问题：如果我们去掉花括号会怎样？它是否仍然能
通过类型检查？如果能，得到的策略是否相同？


##  单子式循环

命令式编程的一个关键工具是循环，因此单子必须
模拟这一点。我们已经从通常的 Lean 中知道 `list.map` 和
`list.foldr`/`list.foldl` 允许对列表元素进行循环。但我们需要
能与单子世界良好交互的版本（消费并
返回类型为 `tactic stuff` 的项）。这些版本以
“m”（表示 monad）作为前缀，例如 `list.mmap`、`list.mfoldr` 等。于是我们的策略是：
```lean
meta def list_types : tactic unit :=
do
  l ← tactic.local_context,
  l.mmap (λ h, tactic.infer_type h >>= tactic.trace),
  return ()
```
最后一行有点傻：它之所以存在，是因为我们从
上一行得到的东西类型是 `list unit`，所以它不能是 do 块的
最后一部分。因此我们加上 `return ()`，其中 `()` 是
类型 `unit` 唯一的项。也可以使用策略 `skip` 来达到
同样的目的。这种特殊情况如此常见，以至于我们实际上有一个
`list.mmap` 的变体 `list.mmap'`，它丢弃
应用于列表元素的函数的结果，并在遍历完
列表后返回 `()`。

## 操作局部上下文

我们接下来的目标是能够在局部上下文中使用和创建假设。
我们将编写一个策略，通过把两个已知的
等式相加来产生一个新的假设（如果这个操作没有意义则惨败）。
起初这两个等式的名称会被愚蠢地硬编码在我们的
策略中。所以我们想要一个策略来执行下面证明中的第一行。
```lean
example (a b j k : ℤ) (h₁ : a = b) (h₂ : j = k) :
  a + j = b + k :=
begin
  have := congr (congr_arg has_add.add h₁) h₂,
  exact this
end
```

我们需要的第一个新概念是名称（name）。为了支持
命名空间管理，Lean 中的名称实际上被定义为一个归纳
类型，在核心库 [meta/name.lean](https://github.com/leanprover-community/lean/blob/master/library/init/meta/name.lean) 中。直接操作它的构造子并不
方便，所以我们改用反引号记号（这是策略编写中众多
反引号用法中的第一个）。实际上我们在
最开始讨论 `add_interactive` 命令时就已经这样做过了。通过名称访问
局部上下文中的某一项是通过 `tactic.get_local` 完成的。我们需要的下一个
新部件是 `tactic.interactive.«have»`，它将创建我们新的
上下文项。它那古怪的名称是为了绕开 `have` 是关键字、
因而不是合法名称这一事实。它接受两个可选参数，我们现在
先忽略它们，以及一个预表达式（pre-expression），它是我们新项的
证明。这样的预表达式使用双反引号加圆括号记号来
构造：``` ``(...) ```。``(...) ```. Inside such a construction, previously assigned expressions can be inserted
使用反引用前缀 `%%` 来访问。这种语法与
我们上面看到的模式匹配语法非常相近（但不同）。

``` ``(...) ```. Inside such a construction, previously assigned expressions
are accessed using the anti-quotation prefix `%%`. This syntax is very close
to the pattern matching syntax we saw above (but different).

```
关于上述策略的最后一点说明：名称 `` `h₁ `` 和 `` `h₂ `` 是在
该策略执行时解析的。为了在解析该策略时触发名称解析，
应使用双反引号，如 ``` ``h₁ ```。当然在
上面的上下文中，这会触发一个错误，因为在策略解析时
没有任何名为 `h₁` 的东西。但它在其他情况下可能有用。

## 策略参数的解析

### 解析标识符

显然，如果假设名称是硬编码的，前面的策略就没什么用。所以我们将它替换为：
```
A last remark about the above tactic: the names `` `h₁ `` and `` `h₂ `` are resolved
when the tactic is executed. In order to trigger name resolution when
the tactic is parsed, one should use double-backtick, as in ``` ``h₁ ```. Of course
in the above context, that would trigger an error since nothing named `h₁` is
in sight at tactic parsing time. But it can be useful in other cases.

## Tactic arguments parsing

### Parsing identifiers

Obviously the previous tactic is useless if the assumption names are hardwired. So we replace it by:
```
参数 `h1` 和 `h2` 告诉 Lean 去解析标识符。这里
发生了相当多的把戏。Lean 解析器看到冒号左侧的 `parse`，
所以它知道必须做一些参数解析，但随后得到的类型
不过是一个名称，如下所示。
```
The arguments `h1` and `h2` tell lean to parse identifiers. There is quite a
bit of trickery going one here. The Lean parser sees `parse` left of colon,
so it knows it must do some argument parsing, but then the resulting type is
nothing but a name, as demonstrated below.
```

### 解析可选参数并使用记号（token）

对该策略的下一项改进提供了一个机会来给新的
局部假设命名（它当前命名为 `this`）。这样的名称
传统上由记号 `with` 引入，后跟所需的标识符。
这个“后跟”是用 `seq_right` 组合子表达的（这里又
潜伏着一个单子），其记号为 `*>`。解析一个记号是由
`lean.parser.tk` 后跟一个字符串引入的，该字符串必须取自一个
预先确定的列表（这个列表的初始值可以在
Lean 源代码中找到，位于 [frontends/lean/token_table.cpp](https://github.com/leanprover-community/lean/blob/master/src/frontends/lean/token_table.cpp)，
当字面量被用于 `notation`、`infix` 或 `precedence` 时会向此列表添加元素）。
然后整个组合被包裹进 `optional` 以使其成为可选的。我们在
下面得到的项 `h` 于是具有类型 `option name`，可以作为
`«have»` 的第一个参数传入，`«have»` 会在提供时使用它，
否则使用名称 `this`。
```

### Parsing optional arguments and using tokens

The next improvement to this tactic offers the opportunity to name the new
local assumption (which is currently named `this`). Such names are
traditionally introduced by the token `with`, followed by the desired identifier.
The "followed by" is expressed by the `seq_right` combinator (there is again
a monad lurking here), with notation `*>`. Parsing a token is introduced by
`lean.parser.tk` followed by a string which must be taken from a
predetermined list (the initial value of this list can be found in
Lean source code, in [frontends/lean/token_table.cpp](https://github.com/leanprover-community/lean/blob/master/src/frontends/lean/token_table.cpp),
elements are added to this list when literals are used in `notation`, `infix`, or `precedence`).
And then the combination is wrapped into `optional` to make it optional. The term `h` we
get below has then type `option name` and can be passed as the first argument
of `«have»`, which will use it if provided, and otherwise use the name `this`.
```

### 解析位置（location）和表达式

我们的下一个策略将一个等式从左侧乘以一个给定的表达式
（如果这个操作没有意义则失败）。我们想把下面的证明机械化。
```

### Parsing locations and expressions

Our next tactic multiplies from the left an equality by a given expression
(or fails if this operation wouldn't make sense). We want to mechanize the following proof.
```

这里主要的新技能在于使用传统记号 `at` 来指明
我们想要作用的位置，以及向策略传递一个表达式。
位置在核心库 [meta/interactive_base.lean](https://github.com/leanprover-community/lean/blob/master/library/init/meta/interactive_base.lean) 中被定义为
一个具有两个构造子的归纳类型：`wildcard` 表示所有
位置，以及 `loc.ns`，它接受一个 `list (option name)`，其中 `option name` 中的
`none` 表示当前目标，而 `some n` 表示局部上下文中
名为 `n` 的东西。在我们的情形中，我们将对
解析出的位置进行模式匹配，并拒绝除了从局部上下文中指定单个名称之外的
一切。第二个新部件是如何解析用户提供的
表达式。相关的解析器是 `interactive.types.texpr`，其结果通过
`tactic.i_to_expr` 转换为实际的表达式。这也是
我们第一次认真使用模式匹配赋值的机会，
以及使用 `«have»` 的第二个可选参数（即期望类型）的机会
（否则我们会得到带有显式 lambda 的、未应用的乘法，试试看！）。
```

The main new skills here consist in indicating at what location we want to
act, using the traditional token `at`, and passing an expression to the
tactic. Locations are defined in the core library [meta/interactive_base.lean](https://github.com/leanprover-community/lean/blob/master/library/init/meta/interactive_base.lean) as
an inductive type having two constructors: `wildcard` which indicates all
locations, and `loc.ns` which takes a `list (option name)`, where `none` in
the `option name` means the current goal, whereas `some n` means the thing
named `n` in the local context. In our case we will pattern-match on the
parsed location and reject everything except specifying a single name from
the local context. The second new piece is how to parse a user-provided
expression. The relevant parser is `interactive.types.texpr`, whose result is
converted to an actual expression using `tactic.i_to_expr`. This is also the
opportunity for our first serious use of pattern matching assignment, and
for using the second optional argument of `«have»` which is the expected type
(otherwise we would get unapplied multiplication, with an explicit lambda, try it!).
```

作为最后一项改进，让我们做一个该策略的版本，它通过追加 `.mul`
来给相乘后的等式命名，并在策略名称后跟 `!` 时
可选地删除原始等式。这是使用
`when` 的机会，它是 `ite` 的单子版本（else 分支什么也不做）。
关于这一想法的其他变体，参见核心库中的 [control/combinators.lean](https://github.com/leanprover-community/lean/blob/master/library/init/control/combinators.lean)。
```

As a last refinement, let us make a version of this tactic which names the
multiplied equality by appending `.mul`, and optionally removes the original
one if the tactic name is followed by `!`. This is the opportunity to use
`when` which is the monadic version of `ite` (with else branch doing nothing).
See [control/combinators.lean](https://github.com/leanprover-community/lean/blob/master/library/init/control/combinators.lean) in core library for other variations on this idea.
```

## 现在该读些什么？

这就是本教程的结尾了（不过下面还有两份速查表）。
如果你想了解更多，可以阅读核心库或 mathlib 中
策略的定义，看看你能理解多少，并在 Zulip 上提出具体的
问题。如需更多理论，特别是对单子的正确解释，你可以阅读
[Programming in Lean](https://lean-lang.org/programming_in_lean/)，但其中实际编写策略的部分并不是最新的。策略框架的官方文档是
论文 [A Metaprogramming Framework for Formal Verification](https://lean-lang.org/papers/tactic.pdf)。

## Mario 的反引号速查表

本节是 Mario 在 Zulip 上发的消息的直接汇编。

* `` `my.name `` 是引用一个名称的方式。它本质上是一种字符串引用形式；除了
  把点解析成带命名空间的名称之外，不做任何检查。

* ``` ``some ``` 在解析时进行名称解析，所以这个例子展开为 `` `option.some ``，
  如果给定的名称不存在则会报错。
* `` `(my expr) `` 在解析时构造一个表达式，在（该策略的）当前
  命名空间中尽可能地进行解析。
* ``` ``(my pexpr) ``` 在解析时构造一个预表达式，在（该策略的）当前
  命名空间中进行解析。
* ```` ```(my pexpr) ```` 构造一个 `pexpr`，但将解析推迟到（该策略的）运行时，
  这意味着任何引用都会在用户的 `begin` `end` 块的命名空间中解析，
  而不是在策略本身的命名空间中解析。
* `%%`：这称为反引用（anti-quotation），在所有 expr 和 pexpr 引用
  表达式 `` `(expr) ``、``` ``(pexpr) ```、```` ```(pexpr) ```` 以及 `` `[tacs] `` 中都受支持。
  在这些引用构造中任何期望表达式的地方，你都可以改用 `%%e`，
  其中 `e` 在策略的外层上下文中具有类型 `expr`，它会被拼接
  进所构造的 `expr`/`pexpr` 等之中。例如，如果 `a b : expr`，那么 `` `(%%a + %%b) `` 的
  类型是 `expr`。
* 如果 Lean 能推断出一个实例 `reflected t`，则 `reflect` 函数会把一个项 `t : T` 变成
  一个反射 `t` 的 `expr`。例如，这可以用于在引用内部
  使用 `%%(reflect n)` 来引用策略定义中的局部变量。举个例子，我们可以写
    ```lean
    meta def assert_ge_zero (n : ℕ) : tactic unit :=
    do v ← to_expr ``(nat.zero_le %%(reflect n)),
       t ← infer_type v,
       assertv `h t v,
       skip
    ```
    如果你在这里直接写 `n`，就会得到 “unexpected local in quotation expression”
    错误。
* `` `[tac...] `` 与 `begin tac... end` 完全相同，意思是它使用交互模式解析器
  解析 `tac...`，但与其求值该策略以产生一个项，不如说它只是
  把策略列表包裹成一个类型为 `tactic unit` 的单一策略。这对于编写
  “宏”或轻量级的策略编写很有用。


同样值得一提的是 `expr` 模式匹配，它的语法与
`` `(%%a + %%b) `` 相同。这些可以用在 match 的模式位置，或用在 do 记号中
`←` 的左侧，它们会解构一个表达式并
绑定被反引用的变量。
例如，如果 `e` 是一个表达式，那么 `` do `(%%a = %%b) ← return e, ... `` 会检查
`e` 是否是一个等式，并把左侧和右侧绑定到 `a` 和 `b`（类型为 `expr`），如果它不是
等式，该策略就会失败。

（值得注意的是，这种模式匹配是在语法层面工作的。有时
使用合一（unification）会更灵活。）

## Mario 的单子符号速查表

下面列表中的所有函数和记号都适用于比 `tactic` 更一般的单子，因此
它们以通用形式列出，但就本教程而言，
`m` 始终是 `tactic`（或 `lean.parser`）。尽管
一切都可以用本教程中介绍的符号完成，但更
深奥的符号可以压缩代码，理解它们对于
阅读现有的策略很有用。

* `return`：在单子中产生一个值（类型：`A → m A`）
* `ma >>= f`：从 `ma : m A` 中取出类型为 `A` 的值并把它传给 `f : A → m B`。替代
  语法：`do a ← ma, f a`
* `f <$> ma`：把函数 `f : A → B` 应用于 `ma : m A` 中的值，得到一个 `m B`。等同于
  `do a ← ma, return (f a)`
* `ma >> mb`：等同于 `do a ← ma, mb`；这里 `ma` 的返回值被忽略，然后调用 `mb`。
  替代语法：`do ma, mb`
* `mf <*> ma`：等同于 `do f ← mf, f <$> ma`，或 `do f ← mf, a ← ma, return (f a)`
* `ma <* mb`：等同于 `do a ← ma, mb, return a`
* `ma *> mb`：等同于 `do ma, mb`，或 `ma >> mb`。为什么同一件事有两种记号？历史
  原因。
* `pure`：等同于 `return`。同样是历史原因。
* `failure`：失败值（具体的单子通常有更有用的形式，例如策略的 `fail` 和
  `failed`）。
* `ma <|> ma'` 从失败中恢复：运行 `ma`，如果它失败则运行 `ma'`。
* `a $> mb`：等同于 `do mb, return a`
* `ma <$ b`：等同于 `do ma, return b`
