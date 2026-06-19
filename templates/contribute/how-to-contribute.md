# 如何为 mathlib 做贡献

本页说明在为 mathlib 做贡献时应当如何操作以及会遇到什么情况。
即使你是经验丰富的 Git 用户，也请查看下面的步骤，因为我们会解释 mathlib 拉取请求所特有的约定。

* 在你着手贡献之前以及贡献过程中，使用 [Zulip](https://leanprover.zulipchat.com/) 来讨论你的贡献。
* 创建一个 GitHub 账号，并通过[个人设置面板](https://leanprover.zulipchat.com/#settings/profile)将你的 GitHub 用户名添加到你的 Zulip 个人资料中。
  我们也强烈建议将你在 Zulip 上的显示名称设置为你的真实姓名。
* 遵守以下准则：
   - 面向贡献者的[风格指南](style.html)。
   - 关于[命名约定](naming.html)的说明。
   - [文档准则](doc.html)。

## 在 mathlib 上工作

我们使用 `git` 来管理 `mathlib` 并进行版本控制。

如果你以前没有使用 git 为开源项目做过贡献，请参阅 [Mathlib4 贡献者 Git 指南](git.html)以获取详细说明。

`master` 分支是 mathlib 的“生产”版本。
master 分支中的所有内容都必须能够无错误地编译，并且不能有任何 `sorry`，这一点至关重要。
为确保这一点，我们只将通过了自动化持续集成（“CI”）测试、并经过 mathlib 维护者批准的改动提交到 `master`。

当你在为 `mathlib` 编写新的贡献时，应当在另一个分支上进行。
你应当在你自己的 `mathlib` 仓库分叉（fork）中进行这项工作。

典型的工作流程：
* 要开始工作，你需要一份 mathlib 的本地副本。
* 首先，你需要前往 https://github.com/leanprover-community/mathlib4 并点击右上角的“Fork”，
  以创建你自己的仓库分叉。
  你的分叉位于 [https://github.com/USER/mathlib4](https://github.com/USER/mathlib4)。
* 现在为你的分叉创建一份本地克隆并对其进行正确配置。
  关于如何正确设置你的分叉的详细分步说明，请参阅 [Mathlib4 贡献者 Git 指南](git.html)。
  ```
  git clone https://github.com/YOUR_USERNAME/mathlib4.git
  cd mathlib4
  lake exe cache get
  ```
* 上述步骤只需做一次（而非每次贡献都做一次）。
* 现在，每当你想为 mathlib 进行一项新的改动时，创建一个新分支：
  ```
  git switch -c my_new_branch   # This creates a new branch and switches to it
  ```
* 进行本地改动，例如使用带有 Lean 扩展的 Visual Studio Code。
* 使用 `git commit -a`（或通过 VS Code 界面）提交你的改动。
* 如果你想在本地编译所有内容以检查自己没有破坏任何东西，运行
`lake build`。如果你修改了导入层级中靠下的文件，这可能会花费很长时间。
你也可以在向主仓库开启 PR 后推送你的改动，让我们的中央 CI 服务器为你完成这项工作。
* 如果你创建了新文件，运行 `lake exe mk_all`。这会更新 `Mathlib.lean`，以确保所有文件都在其中被导入。
* 为了将你的改动推送回 github 上你的仓库，使用
  ```
  git push
  ```
  如果它抱怨远程未配置，请按照 `git` 输出中的建议操作，运行
  ```
  git push --set-upstream origin my_new_branch
  ```
* 一旦你向主 `mathlib` 仓库开启了一个 PR（见下文），
  此时持续集成将自动启动。
  你可以在 GitHub 上你的 PR 页面查看 CI 状态（如果一切正常会有一个绿色的对勾，
  否则如果 CI 仍在运行会是一个黄色的圆圈，或者如果出了问题会是一个红色的叉）。
  你也可以使用 GitHub CLI 检查 CI 状态：`gh pr status`。
* CI 完成后，你可以运行 `lake exe cache get` 来下载编译好的 oleans。


## 发起拉取请求（PR）

一旦你对本地改动满意，就该向主 `leanprover-community/mathlib4` 仓库的 `master` 分支发起一个拉取请求了：注意不要将此 PR 针对你自己分叉上的 `master` 分支发起。

* 如果你还没有这样做，请前往 https://leanprover.zulipchat.com/ ，做个自我介绍，并提及你的新 PR。

* 如果你做了大量的改动/新增，请尽量分成许多个包含小而自包含部分的 PR；一般来说，越小越好！
  这有助于你在进行过程中获得反馈，而且审阅起来也容易得多。
  这对新贡献者尤为重要，因为它能避免做无用功。

* PR 的标题和描述应当遵循我们的[提交约定](commit.html)。

* 如果你正在移动或删除声明，请在提交信息的底部（即在 `---` 之前）使用以下格式包含这些行：

Moves:
- Vector.* -> Mathlib.Vector.*
- ...

Deletions:
- Nat.bit1_add_bit1
- ...

任何你想从 PR 提交中排除的其他评论应当放在 `---` 之下。

## 一个 PR 的生命周期

许多审阅者使用[审阅队列](../queueboard/review_dashboard.html)来识别已准备好接受审阅的 PR。
下面的说明将确保你的 PR 出现在该队列中；如果它没有出现在那里，可能就不会受到太多关注。
我们也欢迎所有人定期查看该队列（在 Zulip 上被链接为 `#queueboard`），并对其专长范围内的 PR 撰写审阅意见。
你可以检查你的 [PR 是否在队列上](../queueboard/on_the_queue.html)，如果不在，还需要做些什么才能让它进入队列。

审阅队列由 GitHub 的“标签”（labels）控制。
在某个 PR 的主页面上，右侧
应当有一个带有“reviewers”“assignees”“labels”等面板的侧边栏。
点击“labels”标题以为当前项目添加或移除标签。
标签只能由“GitHub 协作者”（即经验丰富的贡献者）直接编辑。
不过，任何人都可以通过在 PR 评论中写下以下命令（每条单独一行）来添加/移除下列标签：
- `awaiting-author` 会添加 **“awaiting-author”** 标签
- `-awaiting-author` 会移除 **“awaiting-author”** 标签
- `awaiting-zulip` 会添加 **“awaiting-zulip”** 标签
- `-awaiting-zulip` 会移除 **“awaiting-zulip”** 标签。在做出决定并已实施后使用此命令。
- `WIP` 会添加 **“WIP”** 标签
- `-WIP` 会移除 **“WIP”** 标签
- `easy` 会添加 **“easy”** 标签
- `-easy` 会移除 **“easy”** 标签
- `help-wanted`、`-help-wanted`、`please-adopt`、`-please-adopt` 可用于标记一个需要外部投入的 PR。
- `LLM-generated`、`-LLM-generated` 应当用于标记包含大量 LLM 生成代码的 PR。（请记住，如果你使用了 AI，你必须在 PR 描述中说明具体情况。）
- 供贡献者从下游项目 **brownian**、**carleson**、**CFT**、**FLT**、**infinity-cosmos**、**sphere-packing** 和 **toric** 上行（upstream）工作时使用的标签，也可以用同样的方式添加和移除。
- 任何形如 `t-*` 的主题标签（例如 `t-topology`），以及标签 `CI` 和 `IMO`，也可以用同样的方式添加和移除。PR 会根据其内容被自动打标签，但有时自动打标签不正确或不完整，因此这让你能够手动覆盖它。参见[可用的主题标签](https://github.com/leanprover-community/mathlib4/labels?q=t-)。

此列表是完整的。如果你想添加一个不同的标签，请在 Zulip 上提出来！

如果你的 PR 能够构建（有一个绿色的对勾），会有人在几周内（取决于 PR 的大小；较小的 PR 会得到更快的回应）“审阅”它。他们很可能会留下评论并添加 **“awaiting-author”** 标签。你应当处理每一条评论，在问题解决后点击“resolve conversation”按钮。理想情况下，每个问题都用一个新的提交来解决，但这里没有硬性规定。一旦所有要求的改动都已实施，你应当移除 **“awaiting-author”** 标签，以重新开始这个流程。

有不同的人群可以审阅你的 PR：任何人、[审阅者](../teams/reviewers.html)和[维护者](../teams/maintainers.html)。
任何有有用见解的人都可以审阅你的 PR。
如果他们认为你的 PR 已准备好进入下一阶段，他们可能会在 GitHub 上留下一个“approving”（批准）审阅。
这些审阅会被审阅者纳入考量。
如果一位审阅者认为你的 PR 已准备好被合并，他们会为你的 PR 添加 **“maintainer-merge”** 标签。
这些标签供维护者用来确定其审阅的优先级。
维护者始终是给出最终批准的人。
维护者拥有审阅者的权限，但还有更多的权力（例如合并 PR）。
取决于人员的可用情况，第一位查看你 PR 的审阅者可能就是一位维护者：在这种情况下，
你的 PR 可能无需先被“maintainer merge”就被合并。
审阅时间可能会因我们志愿者的可用情况而有所不同。
为了加快这个流程，你可以查看[审阅准则](pr-review.html)并尽量确保你的 PR 遵循它们。
如果你想明确地请求审阅，请在 Zulip 的 [PR reviews](https://leanprover.zulipchat.com/#narrow/channel/144837-PR-reviews/) 频道中创建一个话题。

如果一位维护者批准了你的 PR，一个 **“ready-to-merge”** 标签会被自动应用到该 PR 上。
一个名为 `bors` 的机器人会从这里接手。（关于 bors 的更多细节请参见[此处](https://github.com/leanprover-community/mathlib/blob/master/docs/contribute/bors.md)。）
该 PR 会被加入到[“合并队列”](https://mathlib-bors-ca18eefec4cb.herokuapp.com/repositories/16)中。
合并队列会被自动处理，但这需要一定的时间，因为它需要构建 mathlib 的各个分支。

在某些情况下，维护者会“委派”（delegate）该 PR。你会看到你的 PR 现在带有一个 **“delegated”** 标签。这要么意味着还有一些最终的改动被要求，但维护者信任你会做出这些改动并自己将 PR 发送给 bors，要么意味着维护者想给你最后一次机会在 PR 被合并前检查一遍。无论是哪种情况，当你准备就绪时，写一条包含“bors merge”这一行的评论将会使该 PR 被合并。

以下是一些其他常用的标签：

- 一个 **“WIP”**（= work in progress，进行中）PR 在接受审阅之前仍需要一些基础性的工作（例如，也许它仍然包含 `sorry`）。如果你想宣布你正在做某件你预期很快会完成的事情，可以发布一个 WIP。

- 一个 **“RFC”**（= request for comment，征求意见）是关于某项可能有争议、或需要专家就是否应当进行而做出决定的改动的 PR。

- 如果你不确定 CI 是否会成功，可以添加 **“awaiting-CI”**。
  这会暂时在主审阅队列中隐藏该 PR。
  当 CI 完成时，该标签会被自动移除。

- 考虑添加 **“help wanted”** 标签以直接征求贡献。

- **“blocked-by-other-PR”** 标签意味着在处理本 PR 之前，应当先解决某些特定的其他 PR。要为你的 PR 添加“blocked-by-other-PR”标签，请在 PR 评论中包含所依赖的 PR 编号（遵循那里评论中隐藏的示例），以便他人能够一目了然地看出应当先审阅哪些 PR。该标签会由一个机器人自动添加，并且会在那些其他 PR 被合并后自动移除。带有此标签的 PR 不会出现在审阅队列中。

- **easy** 标签应当用于标记那些可以立即批准的 PR。维护者和审阅者经常先看 easy 的 PR，以保持队列的流动。easy 的 PR 通常添加单个引理、修正文档中的拼写错误，或类似的内容。如果你对自己的 PR 是否琐碎有任何疑问，就不应当添加此标签。
特别地，如果一个 PR 的差异（diff）超过 25 行、改动了任何现有的定义或定理陈述、添加了任何定义或新文件，或添加了任何并非与现有 `simp` 引理或实例直接类似的 `simp` 引理或实例，那么它通常*不是* easy 的。（如果它们是直接类似的，你无论如何都应当在 PR 描述中给出这样的背景信息。）请注意，差异小并不会自动使一个 PR 成为 easy！

- **delegated** 标签意味着一位维护者已发出“bors delegate”（或“bors d+”）命令。此时该 PR 的作者
应当在做出任何最终要求的改动且 CI 成功后，自己合并该 PR。他们可以使用
“bors merge”来做到这一点。

### 处理合并冲突

由于多人并行地在 mathlib 上工作，可能有人在 `master` 上引入了一项与你在 PR 中所提议的改动相冲突的改动。如果这发生在你的 PR 上，一个机器人会自动添加 **“merge-conflict”** 标签，并且你的 PR 不会出现在审阅队列中。关于如何使用 GitHub 的在线工具解决合并冲突，请查看[这篇 GitHub 教程](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-on-github)。
一旦冲突被解决，**“merge-conflict”** 标签会被自动移除，并且你的 PR 会回到审阅队列。

### 用合并，而非变基

（如果你不知道变基（rebasing）是什么，可以跳过这一节。）
Mathlib 的 PR 在合并时会被压缩（squash）：特别地，中间提交的历史除了在 PR 中以外不会被记录。
一旦一个 PR 已经经历了一些审阅活动，强烈建议不要再进行变基或压缩，因为这会混淆审阅历史，使得审阅新的改动更加困难。
