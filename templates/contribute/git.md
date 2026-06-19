# 面向 Mathlib4 贡献者的 Git 指南

本指南面向初次接触 git 但希望为 mathlib4 库做出贡献的数学工作者。
贡献通过拉取请求来完成。我们将一步步介绍必要的工作流程。
请注意，网络上还有许多其他指南介绍如何通过拉取请求为开源项目做出贡献。

本指南分为三个主要部分：

1. [**一次性设置**](#part-1-one-time-setup)（在你首次开始贡献时执行一次）
2. [**日常工作流程**](#part-2-daily-workflow)（处理贡献时的常用操作）
3. [**补充信息**](#additional-information)

## 前置条件

在开始之前，请确保你已具备：

- 计算机上已安装 Git
- [一个 GitHub 账户](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github)
- （可选但推荐）已安装 [GitHub CLI 工具（`gh`）](https://cli.github.com/)

---

# 第一部分：一次性设置

以下步骤只需在你首次开始为 mathlib4 做贡献时执行一次。

## 使用 GitHub CLI 直接跳到步骤 4

以下命令会为你完成步骤 1 到 3：
它将 mathlib4 仓库 fork 到你的 GitHub 账户，
将仓库克隆到你当前的目录中，
并按推荐方式设置远程仓库。

```bash
gh repo fork leanprover-community/mathlib4 --default-branch-only --clone
```

## 步骤 1：在 GitHub 上 Fork 仓库

首先，你需要创建自己的 mathlib4 仓库副本（fork）：

1. 前往 https://github.com/leanprover-community/mathlib4
2. 点击右上角的 "Fork" 按钮
3. 选择你的 GitHub 账户作为目标。建议保持勾选 "copy the master branch only"。
4. 等待 GitHub 创建你的 fork

**此步骤你只需执行一次。**
你可以将你的 fork 复用于许多不同的分支和拉取请求。

## 步骤 2：获取仓库的本地副本

你在上一步创建的 fork 是 mathlib4 的一个"远程"副本，它位于 GitHub 的服务器上。
现在你需要在自己的计算机上设置 mathlib4 的本地副本（也称为"克隆"）。

根据你是否已经拥有 mathlib4 的克隆，你有两种选择：

### 选项 A：如果你尚未克隆 mathlib4

#### 方法 1：使用 GitHub CLI（推荐）

在下面的 shell 命令中，将 `YOUR_USERNAME` 替换为你的 GitHub 用户名：

```bash
gh repo clone YOUR_USERNAME/mathlib4
cd mathlib4
```

#### 方法 2：手动克隆

在下面的 shell 命令中，将 `YOUR_USERNAME` 替换为你的 GitHub 用户名，以便将你的 fork（而非原始仓库）克隆到当前工作目录下一个名为 `mathlib4` 的目录中，然后进入该目录：

```bash
git clone https://github.com/YOUR_USERNAME/mathlib4.git
cd mathlib4
```

这会自动将你的 fork 设置为 `origin` 远程仓库，这正是我们想要的。

### 选项 B：如果你已经克隆了 mathlib4

如果你已经从原始仓库克隆了一份（例如你通过 Lean 4 VS Code 扩展创建了一份），你可以复用它。只需进入你现有的 mathlib4 目录：

```bash
cd path/to/your/existing/mathlib4
```

#### 配置 GitHub CLI（如已安装）

如果你已安装 GitHub CLI，请将默认仓库设置为上游 mathlib4：

```bash
gh repo set-default leanprover-community/mathlib4
```

这可确保诸如 `gh pr checkout` 之类的 GitHub CLI 命令作用于主 mathlib4 仓库，而非你的 fork。

## 步骤 3：正确设置远程仓库

远程仓库的设置取决于你在上面选择了哪个选项：

### 如果你使用 GitHub CLI 克隆了你的 fork（选项 A，方法 1）

`gh` 已经为你处理好了这一步。

### 如果你未使用 GitHub CLI 克隆你的 fork（选项 A，方法 2）

你需要将原始仓库添加为 `upstream`：

```bash
git remote add upstream https://github.com/leanprover-community/mathlib4.git
```

### 如果你使用了已有的克隆（选项 B）

你需要重命名现有的远程仓库并添加你的 fork。
将 `YOUR_USERNAME` 替换为你的 GitHub 用户名：

```bash
git remote rename origin upstream
git remote add origin https://github.com/YOUR_USERNAME/mathlib4.git
```

### 验证你的远程仓库

无论你选择了哪个选项，都要验证你的远程仓库设置是否正确：

```bash
git remote -v
```

你应当看到：

```
origin    https://github.com/YOUR_USERNAME/mathlib4.git (fetch)
origin    https://github.com/YOUR_USERNAME/mathlib4.git (push)
upstream  https://github.com/leanprover-community/mathlib4.git (fetch)
upstream  https://github.com/leanprover-community/mathlib4.git (push)
```

## 步骤 4：配置 Master 分支

首先，从上游获取分支：

```bash
git fetch upstream
```

然后确保你的 `master` 分支跟踪 `upstream/master`：

```bash
git branch --set-upstream-to=upstream/master master
```

## 步骤 5：为你的工作流程配置 Git

### 设置默认推送行为

将 git 配置为默认将新分支推送到 `origin`：

```bash
git config push.default current
git config push.autoSetupRemote true
```

### 防止意外提交到 Master（可选但推荐）

为避免意外地直接提交到 `master`，你可以设置一个 pre-commit 钩子。
首先，创建钩子文件：

```bash
mkdir -p .git/hooks
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
branch="$(git rev-parse --abbrev-ref HEAD)"
if [ "$branch" = "master" ]; then
  echo "You can't commit directly to master branch"
  exit 1
fi
EOF
```

然后使其可执行：

```bash
chmod +x .git/hooks/pre-commit
```

---

# 第二部分：日常工作流程

以下是你在处理贡献时会经常用到的操作。

## 创建并在新分支上工作

### 保持你的 Master 分支为最新

**在创建新分支之前执行此操作**，以确保你基于最新的更改进行工作：

```bash
git switch master
git pull
```

### 创建新分支

然后创建并切换到一个新分支：

```bash
git switch -c my-feature-branch
```

当你首次推送该分支时，它会自动跟踪 `origin/my-feature-branch`。

### 基于另一个 PR 进行工作

如果你打算让你的工作依赖于另一个 PR：

1. 检出相关的 PR 分支：如果这是你自己的 PR，运行 `git switch <pr-branch-name>`；如果你打算在他人的 PR 之上进行工作，请按照下面 [`与他人的 PR 协作`](#working-with-others-prs) 一节中的说明操作。
2. 运行 `git pull` 以确保你与该拉取请求保持同步。
3. 运行 `git switch -c my-feature-branch` 以在当前分支之上创建一个新分支。


## 推送你的分支并开启 PR

### 推送你的分支

在完成你的更改和提交之后：

```bash
git push
```

### 开启拉取请求

1. 前往你在 GitHub 上的 fork：`https://github.com/YOUR_USERNAME/mathlib4`
2. 你应当看到一个横幅，建议为你最近的推送开启一个 PR
3. 点击 "Compare & pull request"
4. 填写 PR 标题和描述
5. 点击 "Create pull request"

或者，如果你没有看到该横幅，你也可以前往 https://github.com/leanprover-community/mathlib4/compare，然后点击 `compare across forks`。
你需要在 "head repository" 下拉菜单中选择你的 fork，并在 "compare" 下拉菜单中选择你想要合并的分支。

## 与他人的 PR 协作

请注意，即使只是用 VS Code 打开来自某个不可信来源分支的 Lean 代码，也可能在你的计算机上执行代码！
请查阅[补充信息一节中的安全警告](#-security-warning)。

### 方法 1：使用 GitHub CLI（推荐）

这比手动方法简单得多。要检出 PR #1234：

```bash
gh pr checkout 1234
```

这会自动处理远程设置和分支检出。

要切回你自己的分支：

```bash
git switch my-feature-branch
```

### 方法 2：手动检出

要手动检出他人的 PR，首先将他们的 fork 添加为远程仓库（将 `USERNAME` 替换为他们的 GitHub 用户名）：

```bash
git remote add contributor-name https://github.com/USERNAME/mathlib4.git
```

然后获取他们的分支：

```bash
git fetch contributor-name
```

最后，检出他们的分支：

```bash
git checkout contributor-name/their-branch-name
```

（可以用 `git remote remove <contributor-name>` 移除远程仓库。）

要切回你自己的分支：

```bash
git switch my-feature-branch
```

## 授予协作者访问权限

如果你想允许他人直接推送到你的 PR 分支：

1. 前往你的 fork：`https://github.com/YOUR_USERNAME/mathlib4`
2. 点击 "Settings" 标签页
4. 点击 "Collaborators"（你可能需要重新认证）
5. 输入他们的 GitHub 用户名
6. 选择 "Write" 权限级别
7. 发送邀请

一旦他们接受，他们就可以在按照 [《基于另一个 PR 进行工作》](#basing-work-on-another-pr) 中的某种方法操作后，使用 `git push` 直接推送到你的 PR 分支。

---

# 补充信息

## ⚠️ 安全警告

**重要**：当你授予某人对你 fork 的协作者访问权限，或者当你检出并运行他人的代码时，你可能在自己的计算机上运行了未经审查的代码。请只与你信任的人协作，因为他们有可能植入在构建过程中运行的恶意代码。

## 获取帮助

如果你遇到问题或对 git 工作流程有疑问，请在 [Lean Zulip 聊天](https://leanprover.zulipchat.com) 的 `#new users` 频道中提问。社区非常乐于助人，欢迎大家提问！

## 快速参考

下面是你将会用到的最常见命令的汇总。

更新 master：

```bash
git switch master
git pull
```

在当前分支之上创建一个新分支：

```bash
git switch -c new-branch-name
```

推送你的分支并设置跟踪：

```bash
git push origin new-branch-name
```

如果你已按照[上面指南设置了默认推送选项](#set-default-push-behavior)，那么以下命令即可：
```bash
git push
```

检出他人的 PR：

```bash
gh pr checkout PR_NUMBER
```

检查远程仓库配置：

```bash
git remote -v
```

检查你当前所在的分支：

```bash
git branch
```

切换到另一个分支进行工作：

```bash
git switch your-branch-name
```

## 常见故障排查

**问题**："Your branch is behind 'upstream/master'"
**解决方法**：
```bash
git switch master
git pull
```

**问题**："fatal: The current branch has no upstream branch"
**解决方法**：
```bash
git push --set-upstream origin branch-name
```

**问题**：意外地提交到了你的 master 分支副本
**解决方法**：将这些提交移到一个新分支：
```bash
git branch new-branch-name
git switch master
git reset --hard upstream/master
git switch new-branch-name
```

## 其他资源

* [git 术语表](https://git-scm.com/docs/gitglossary)
* [日常 git 命令](https://git-scm.com/docs/giteveryday)
* [git 用户手册](https://git-scm.com/docs/user-manual)