# 如何加速一个 Mathlib 文件

我们将说明如何让一个运行缓慢的 Mathlib 文件变得更快。这些笔记基于
Mathlib PR
[#12412](https://github.com/leanprover-community/mathlib4/pull/12412)
中进行的实验。

1. 第一步是找出代码中哪些部分较慢。为此，
   在 `import` 语句之后添加一行 `set_option profiler true`。
   这将在 infoview 中产生形如 `<blah> took <number>ms`（甚至 `<number>s`）
   的行，记录那些耗时至少 `100ms` 的步骤（这一以毫秒为单位的下界
   可通过 `set_option profiler.threshold <num>` 进行调整）。
2. 对于每一行这样的输出，尝试按照下面的说明加速相应的步骤。
3. 上一步可以在降低 `profiler.threshold` 设置后重复进行，
   以便发现并加速那些不太慢、但也不太快的部分。然而，
   这最终会带来递减的收益。
4. 再次移除 profiler 选项，然后提交 PR！

## 处理特定的缓慢步骤

这里我们说明如何尝试加速代码中导致 profiler 在 infoview 中
产生消息的各个部分。

### `typeclass inference of <name> took <a long time>`

1. 在引发该消息的声明之前紧接着添加 `set_option trace.Meta.synthInstance true in`。
2. 查看 infoview 中生成的实例综合（instance synthesis）追踪，找出
   `<name>` 中较慢的那个（些）实例。
3. 在该声明之前使用 `#synth <name> <args>`（如有需要，可临时向上下文中
   添加 `variable`），以获得一个提供该实例的合适的项。
4. 在该声明之前（或在当前 section/namespace 的开头附近）添加一行
   `@[local instance] lemma/def <some name> <possibly some args> : <name> <args> := <term>`。
   如果该实例需要证明内部的某些局部上下文，则改为在证明中合适的位置添加
   `have/let <some name> <possibly some args> : <name> <args> := <term>`。
5. 移除该声明之前的 `set_option` 行。

有可能 `<term>` 又会触发一次缓慢的实例搜索，因此这一过程
可能需要重复进行。

**取舍：** 在文件中到处散布局部实例并不美观，而且在某种程度上
有违类型类系统的初衷。

当然，一个更好的解决方案是找出*究竟是什么*导致了所发现情形中
类型类搜索变慢，然后为之找到修复方法。这很可能会使
Mathlib 中许多其他文件同样受益。

### `simp took <a long time>`

将相关的 `simp/simpa` 调用替换为 `simp?/simpa?`，并点击 `Try this:`
建议，以将其替换为 `simp/simpa only` 调用。在某些情况下，
还可以在一定程度上精简引理列表。

**取舍：** 证明可能会增长好几行密集的内容，并且现在会按名称提及许多引理，
其中每一个都可能在将来被重命名，从而破坏你的证明。

### `elaboration took <a long time>`

查找引发该消息的声明中的 `_`，弄清它们是由什么填充的，
并将它们替换为相应的显式参数。

**取舍：** 如果显式参数很长，这会使陈述变得更长，
并且可能更难阅读。

### `compilation of <name> took <a long time>`

尝试在定义之前添加 `noncomputable`。

**取舍：** 定义将不再是内核可归约的（kernel-reducible），但在大多数情况下
这应该不成问题。

### `tactic execution of <tactic> took <a long time>`

尝试将缓慢的策略替换为对更简单策略的调用。

* 例如，一个缓慢的 `nontriviality ... using ...` 可以替换为
  ```lean
  rcases subsingleton_or_nontrivial ... with H | H
  · -- get `Subsingleton` case out of the way
    ...
  -- now we have `Nontrivial ...`
  ```

* 一个缓慢的 `convert` 可以这样避免：先完成在它之后所做的那些重写，
  然后再使用 `refine` 或 `exact`。

**取舍：** 证明可能会变得稍长一些，也更繁琐一些。
