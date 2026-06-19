# 认识社区

Lean 社区相当多元。我们有许多来自数学领域的用户，一些来自计算机科学领域，还有少数来自其他领域（如物理学）。
大多数用户是学生或学者，但也有一些在业界工作的数据科学家和软件工程师。

由社区成员组成的若干[团队](teams.html)承担着各自指定的职责。

下方的地图可以帮助你找到地理位置上离你较近的社区成员。

<div id="userMap"></div>

如果你想把自己加入到上方的地图中，
可以在你的 Zulip 个人资料中设置 `latitude` 和 `longitude` 字段；
你可以通过右键点击地图来获取你的坐标。
地图将在 24 小时内更新，即网站下一次构建时。
我们建议标注你工作或学习的主要建筑物的坐标，而不是你居住的地方。

## Lean Zulip 聊天

我们社区的主要聚集地是一个
[Zulip 聊天实例](https://leanprover.zulipchat.com)。
你无需注册即可浏览最受欢迎的“频道”上的公开讨论。

我们欢迎你注册 Zulip 聊天，
这将让你参与到讨论中来。
我们强烈建议你使用真实姓名作为显示名称。
我们也欢迎你先在
[*new members* 频道](https://leanprover.zulipchat.com/#narrow/stream/113489-new-members)
中简短地介绍一下自己。

我们欢迎各个水平层次的用户提出问题。
在 new members 频道提出你的第一个问题，可以确保回答不会预设你对 Lean 已经很了解。不过你也欢迎使用更专业的频道。
请开启新的讨论主题，而不要使用无关的已有主题。
如果你需要编程方面的帮助，可能会被要求提供一个“最小可运行示例”
（[MWE](mwe.html)）。
此外也要警惕 [XY 问题](https://mywiki.wooledge.org/XyProblem)：尽量给出足够的上下文。

要内联地发布一段代码，请用单个反引号将其括起来：`` `my code here` ``。
如果你的代码本身包含反引号，则用比它所含数量更多的反引号将其括起来：
``` `` my`code`contains`backticks `` ```。

较长的代码片段应当置于两行各含三个反引号的行之间，例如：
````md
```
def n : myNat := 5
#check n
```
````

你可以使用 LaTeX，用 `$$` 括起内联 LaTeX，并用
````md
```math
my LaTeX code here
```
````

来表示独立显示的数学公式。

## GitHub

继 Zulip 之后的另一个聚集地是 GitHub，它托管着所有的
[社区代码仓库](https://github.com/leanprover-community)。
特别是，
[mathlib 拉取请求](https://github.com/leanprover-community/mathlib4/pulls)
页面正是查看我们正在进行的工作的合适之处。
你也可以在我们的[博客](/blog/)上阅读近期的工作进展。

贡献的方式有很多种：开发新的数学理论、为现有理论补充并撰写文档、开发配套的软件工具，以及评审他人提出的贡献。
如果你想为我们的项目做出贡献，可以阅读我们的
[贡献指南](contribute/index.html)。

## 社区准则

通过在 [Lean Zulip 聊天](https://leanprover.zulipchat.com/)
或 [leanprover-community GitHub 组织](https://github.com/leanprover-community/)内的任何代码仓库中互动，
即表示你同意遵守[社区准则](community_guidelines.html)。