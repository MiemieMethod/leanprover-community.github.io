# Lean 的 Github 生态系统

关于向 Lean、Batteries 和 Mathlib 提交拉取请求时所涉及的分支、标签与 CI 工作流的说明文档。

* [你需要了解的事项](#things-you-need-to-know) 对所有人都适用
* [标签与分支](#tags-and-branches) 仅面向"专家"，即那些在 Lean 中制造或修复破坏性变更的人，
  或希望理解 Mathlib CI 内部工作原理的人。

## 你需要了解的事项

* 如果你向 `leanprover/lean4` 提交一个可能涉及破坏性变更的拉取请求，
  请将你的 PR 变基（rebase）到 `nightly-with-mathlib` 分支上。这将启用与 Mathlib 的联合 CI。

* 如果你向 `leanprover-community/mathlib4` 提交拉取请求，
  请从一个 fork 中提交。Mathlib 的 `.olean` 缓存现在可以与来自 fork 的 PR 一同工作。

## 标签与分支

### `leanprover/lean4`

* 开发在 `master` 分支上进行。
* 稳定版本和候选发布版本带有标签，例如 `v4.2.0` 或 `v4.3.0-rc1`。
  * 若要在某个项目中使用这些版本之一，你的 `lean-toolchain` 文件应包含例如 `leanprover/lean4:v4.2.0`。
* 稳定版本在每个月末发布，并且与最后一个候选发布版本完全相同。
* 下一个版本的第一个候选发布版本会在稳定版本发布后立即发布。
* 每个版本都有一个 `releases/v4.X.0` 功能分支，它可能包含
  * 用于发布说明的额外提交
  * 从 `master` 精选（cherry pick）而来、通过候选发布版本发布的关键修复提交。
* 我们会定期从 `master` 制作每夜构建版本（nightly release），它在 `leanprover/lean4-nightly`
  仓库上带有诸如 `nightly-2023-11-01` 这样的标签。
  * 若要在项目中使用某个每夜构建版本，你的 `lean-toolchain` 文件应包含例如 `leanprover/lean4:nightly-2023-11-01`。（注意它不应是 `leanprover/lean4-nightly:nightly-2023-11-01`，因为 `elan` 在此处施加了一些神奇的智慧。）
  * 每夜构建版本可以通过手动触发发布工作流来*修订*。修订后的每夜构建版本
    在 `leanprover/lean4-nightly` 上带有形如 `nightly-YYYY-MM-DD-revK` 的标签（K 从 1 开始）。
    若要在项目中使用某个修订后的每夜构建版本，你的 `lean-toolchain` 文件应包含例如
    `leanprover/lean4:nightly-2023-11-01-rev1`。
    修订后的每夜构建版本在基础每夜构建版本之后排序：base < rev1 < rev2 < 次日的每夜构建版本。
    Mathlib 的每夜构建测试基础设施会自动处理修订后的每夜构建版本。
* 在 `leanprover/lean4` 上有一个 `nightly` 分支，它跟随用于构建某个每夜构建版本的最新提交。
* 每个 PR 在成功构建后都会自动获得一个工具链。该 PR 随后会带有标签 `toolchain-available`。
  若要在项目中使用 PR #NNNN，你的 `lean-toolchain` 文件应包含
  `leanprover/lean4-pr-releases:pr-release-NNNN`。
* 对于任何可能影响 Batteries 或 Mathlib 的 PR，你应将你的 PR 建立在 `nightly-with-mathlib` 分支的 HEAD 之上。
  在这种情况下，会创建一个 `lean-pr-testing-NNNN` Mathlib 分支（下文详述），并且来自该分支的结果会
  通过 PR 讨论区中的评论进行报告。

### `leanprover-community/batteries`（即 'Batteries'）

* 开发在 `main` 上进行。
* Batteries 在其 `lean-toolchain` 中使用最新的稳定版本或候选发布版本。
  * 由于我们在发布 `v4.X.0` 之后立即发布 `v4.X+1.0-rc1`，
    Batteries 仅在极短的时间内处于稳定版本上。
* `main` 上使用新工具链的第一个提交会被打上该工具链版本号的标签（例如 `v4.2.0`）。
* 有一个 `stable` 分支跟随 `v4.X.Y` 标签。
* Batteries 有一个 `bump/v4.X.0` 分支，用于 Lean 即将到来的稳定版本，
  * 它包含已获得维护者批准的、针对破坏性变更的适配
  * 并且将使用 `leanprover-lean4:nightly-YYYY-MM-DD` 工具链。
* Batteries 有一个 `nightly-testing` 分支，它
  * 使用最近的每夜构建版本（这会自动更新）
  * 自动将 `main` 的所有提交合并进来
  * 可以手动将 `bump/v4.X.0` 的任何变更合并进来
  * 可以包含任何其他提交，包括未经审查的提交，只要这些提交是使 `nightly-testing`
    分支能够在最近的每夜构建版本上正常工作所必需的。
* `nightly-testing` 分支上的 CI 失败会由一个机器人报告到 zulip 的 [`nightly-testing-batteries` 频道](https://leanprover.zulipchat.com/#narrow/channel/595626-nightly-testing-batteries/topic/Batteries.20status.20updates/with/592700605)。
* `nightly-testing` 分支上的 CI 成功会导致创建一个与该提交相匹配的标签
  `nightly-testing-YYYY-MM-DD`，如果该标签尚不存在的话。
  * 因此，如果 `nightly-testing-YYYY-MM-DD` 存在，我们就知道在它上面：
    * `lean-toolchain` 是 `leanprover/lean4:nightly-YYYY-MM-DD`，并且
    * CI 成功。
* 当需要修改 Batteries 以适配 Lean 中的破坏性变更时，
  你需要创建一个分支，并随后从该分支开启一个 PR。
  （注意，下面的步骤在 Mathlib 处会自动发生，
  但对于 Batteries 则需要手动完成。）
  * 如果该变更是在 `leanprover/lean4#NNNN` 中做出的，
    那么 Batteries 的适配分支应当命名为 `lean-pr-testing-NNNN`。
  * Batteries 的适配分支应基于标签 `nightly-testing-YYYY-MM-DD`，
    其中 `YYYY-MM-DD` 是你的 Lean PR 所基于的每夜构建版本的日期。
  * 如果 `nightly-testing-YYYY-MM-DD` 标签尚不存在，你需要等待
    （并可能推进到后续的某个每夜构建版本）。
    如有需要，请联系 `@kim-em` 寻求帮助。
  * 理想情况下，你会将 `lean-pr-testing-NNNN` 分支推送到 Batteries 的主仓库；
    如有需要，我们可以提供写入权限。
  * 此分支上的 `lean-toolchain` 必须包含 `leanprover/lean4-pr-releases:pr-release-NNNN`。
  * 你可以从 `lean-pr-testing-NNNN` 分支开启一个 PR，无论是在完成所需的适配之前还是之后。
  * 开启 PR 时，记得将基础分支设置为 `nightly-testing`。
  * 请为该 PR 打上 `v4.X.0` 和 'depends on core changes' 标签。
    （如果你没有写入权限，可请求他人代为完成。）
  * 一旦 Lean PR 被合并并在某个每夜构建版本中发布，Batteries 的适配 PR
    * 应将其 `lean-toolchain` 更新为 `leanprover/lean4:nightly-YYYY-MM-DD`
    * 其变更可以根据需要手动合并到 `nightly-testing` 中，以保持 `nightly-testing`
      正常工作（不要更改基础分支并合并该 PR，我们仍然需要它）。
  * 一旦 Batteries 的适配 PR 获得批准，
    维护者会将其合并到 `bump/v4.X.0`（而非 `nightly-testing-YYYY-MM-DD`）。
* 始终允许将 `bump/v4.X.0` 合并到 `nightly-testing` 中，但反之则不行。
  （对 `bump/v4.X.0` 的变更已经过审查，但对 `nightly-testing` 的变更可能尚未审查。）
* 当需要将 Batteries 更新到 Lean 的新版本时，
  *希望*所需做的只是创建一个新的 PR，
  其内容为将 `bump/v4.X.0` 压缩合并（squash merge）到 `main`。

### `leanprover-community/mathlib4`（即 'Mathlib'）

* 上面关于 Batteries 所说的一切都适用于 Mathlib，但有以下例外：
  * 开发在 `master` 上进行。
  * `nightly-testing` 状态更新会发布在 `#nightly-testing-mathlib` 的[此话题](https://leanprover.zulipchat.com/#narrow/channel/595625-nightly-testing-mathlib/topic/Mathlib.20status.20updates/with/592729346)中。
  * 向 Mathlib 提交的 PR 应从 fork 中发起。Mathlib 的 `.olean` 缓存现在可以与来自 fork 的 PR 一同工作。
* `lean-pr-testing-NNNN`、`nightly-testing`、`nightly-testing-*` 标签以及 `bump/v4*` 分支
  全都位于 `leanprover-community/mathlib4-nightly-testing`，它是 mathlib4 的一个 fork。
  如果你需要经常对这些分支进行写入访问，你可以在 Zulip 上的
  [`nightly-testing-mathlib` 频道](https://leanprover.zulipchat.com/#narrow/channel/595625-nightly-testing-mathlib)
  中请求被添加到 `nightly-testing` GitHub 团队。
* 注意，Mathlib 的 `nightly-testing` 分支可以根据需要使用 Batteries 的 `nightly-testing` 分支。
* 类似地，Mathlib 的 `bump/v4.X.0` 分支可以根据需要使用 Batteries 的 `bump/v4.X.0` 分支。
* 对于任何通过 CI 且基于某个每夜构建版本的 Lean PR，都会自动创建 `lean-pr-testing-NNNN` 分支。
  （与 Batteries 不同，那里必须手动创建。）
* `lean-pr-testing-NNNN` 分支上的 Mathlib 适配 PR 可能需要更改 Batteries 的依赖，
  以使用 Batteries 的 `lean-pr-testing-NNNN` 分支，如果 Batteries 也遭遇了破坏的话。

### Mathlib 的 nightly 与 bump 分支

每个月都有一个新的 Lean 版本发布，
而 Mathlib 力求尽快迁移到新的 Lean 版本。
为了使这一过程尽可能顺畅，我们遵循以下流程：

* `nightly-testing` 分支位于 `leanprover-community/mathlib4-nightly-testing`，并使用 Lean 的每夜构建工具链版本。
  换言之，该分支上的 `lean-toolchain` 文件包含诸如 `leanprover/lean4:nightly-2024-09-26` 之类的内容。
  - 该分支不保证能够无错误地构建。
  - 对该分支的变更不会经过 Mathlib 维护者团队的审查。
  - 该分支不受保护：`nightly-testing` GitHub 团队的成员可以向其推送修复。
  - 该分支的目的是使 Mathlib 适配 Lean 每夜构建工具链版本中的变更。
  - 通常，向 Lean 核心提交的 PR `#NNNN` 会伴随着 Mathlib 在 `lean-pr-testing-NNNN` 分支中的适配。
    一旦 Lean 核心 PR 进入某个每夜构建工具链，Mathlib 的 `lean-pr-testing-NNNN` 分支就可以合并到 `nightly-testing` 中。
    通常需要解决 `lean-toolchain`、`lakefile.lean` 和/或 `lake-manifest.json` 中的合并冲突。
  - 如果 CI 在该分支上失败，它会在 Zulip 上的 ["nightly-testing-mathlib > Mathlib status updates"](https://leanprover.zulipchat.com/#narrow/channel/595625-nightly-testing-mathlib/topic/Mathlib.20status.20updates) 中发布一条消息，指明该失败。
  - 如果 CI 在该分支上通过，则会在同一话题中发布一条消息，指明成功，并给出创建 PR 以审查这些适配的说明。（见下文。）
* `leanprover-community/mathlib4-nightly-testing` 中的 `nightly-testing-green` 分支跟踪 `nightly-testing` 最后一个成功构建的提交。
  用于 `nightly-testing` 构建的工具会从该分支获取。
* `bump/v4.X.Y` 分支同样位于 `leanprover-community/mathlib4-nightly-testing`，并使用 Lean 的每夜构建工具链版本。
  - 该分支应始终能够无错误地构建。
  - 对该分支的变更会经过 Mathlib 维护者团队的审查。
  - 该分支受保护：只有 Mathlib 维护者和某些机器人才能向其推送。
  - 该分支的目的是准备一个 Mathlib `master` 分支的并行版本，使其能在 Lean 的即将到来的版本上构建。
    一旦该版本发布，`bump/v4.X.Y` 分支就会合并到 `master`。
    这次合并本质上是原子性的，因为其差异已经通过所有的每日适配 PR 得到审查。（见下文。）
* 当 `nightly-testing` 通过 CI 时，一个机器人会向 Zulip 发布消息，说明如何创建一个"适配 PR"，以将 `nightly-testing` 上的变更合并到 `bump/v4.X.Y`。
  - 这个 PR 可以按照 Zulip 消息中的指示，使用 `scripts/create-adaptation-pr.sh` 来准备。
  - 这个 PR 应由 Mathlib 维护者团队审查。
* 在 Lean 发布周期（即一个月）的过程中，`bump/v4.X.Y` 会累积针对未来 Lean 版本的适配。
  - 但 `master` 也会累积数千行的变更。
  - 因此应当定期将 `master` 合并到 `bump/v4.X.Y` 中。
  - 在撰写本文时，这一步骤已被整合进 `scripts/create-adaptation-pr.sh` 流程中。
  - 偶尔会发生合并冲突。这些冲突应当由 Mathlib 维护者团队审查，尽管目前并未做到这一点。

### Lean 与 Mathlib 之间的联合 CI

* 对于每一个向 Lean 提交的 PR，我们都会尝试针对所产生的工具链运行 Mathlib CI。
* 为使其正常工作，你需要将你的 PR 变基到 `nightly-with-mathlib` 分支上。
  `nightly-with-mathlib` 分支指向最新的、能通过 Mathlib CI 的每夜 Lean 构建版本，
  并且 Mathlib（可能还有 Batteries）上存在对应的 `nightly-testing-YYYY-MM-DD` 标签。
* 机器人会从 `nightly-testing-YYYY-MM-DD` 标签在 `leanprover-community/mathlib4-nightly-testing` 上
  创建一个 `lean-pr-testing-NNNN` 分支，如果它已存在则向其推送一个空提交。
* 来自该 Mathlib 分支的后续 CI 结果会以评论的形式报告回 Lean PR。
* 如果你的 PR 不是从一个能成功构建 Mathlib 的每夜构建版本分叉而来，机器人会在你的
  PR 上发表评论。
  每当你向 PR 推送时，它都会重新尝试。
* 如果 `nightly-with-mathlib` 对你的用途而言过于陈旧，你可以基于 `nightly`，那么一旦该每夜构建版本本身通过 Mathlib CI 并且你向 PR 推送，Mathlib CI
  就会开始运行。
* 也有可能那个每夜构建版本永远不会通过 Mathlib CI。在这种情况下，你可能不得不
  等待 `nightly-with-mathlib` 更新，然后变基到它上面。


<img src="img/tags_and_branches.png" alt="Mathlib/Batteries 分支概览" width="80%"/>
