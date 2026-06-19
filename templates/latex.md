# LaTeX 示例

本测试页面汇集了若干在 Markdown 中使用 LaTeX 的示例。此页面仅用于开发用途。

对照：<https://math.meta.stackexchange.com/revisions/9386/164>

## 来自 doc-gen issue 的示例

来自 [doc-gen#10](https://github.com/leanprover-community/doc-gen/issues/10)，如果我在 TeX 中写入 $f[*a,*b](cd)$ 会怎样？$g_{x_0}(y)$ ？

来自 [doc-gen#62](https://github.com/leanprover-community/doc-gen/issues/62)：

- 可能表示 $R[X_i : i \in \sigma]$。
- 示例：$x \in \sigma$，另外单独写 `y`
- 示例：$x \in \sigma$，另外单独写 `s`
- 示例：$x \in \sigma$，另外单独写 `sigm`
- 示例：$x \in \sigma$，另外单独写 `simg`
- 示例：单独写 `s`，以及 $x \in \sigma$

来自 [dynamics.circle.rotation_number.translation_number](https://github.com/leanprover-community/mathlib/blob/c35672bbe581370c345d0862c078fbbbe1258fb3/src/dynamics/circle/rotation_number/translation_number.lean#L641) 的示例：

对任意 `x : ℝ`，序列 $\frac{f^n(x)-x}{n}$ 趋向于 `f` 的平移数。
特别地，这一极限不依赖于 `x`。

## [mathlib#3776](https://github.com/leanprover-community/mathlib/pull/3776)

[PR 之前](https://github.com/leanprover-community/mathlib/blob/d61bd4ae29222280e1b6dec421c840fb83c30438/src/algebra/classical_lie_algebras.lean#L45)（有一处多余的 `cc`），行距过大：

$$
  J = \left[\begin{align}{cc}
              0_l & 1_l\\\\
              1_l & 0_l
            \end{align}\right]
$$

[PR 之后](https://github.com/leanprover-community/mathlib/blob/0166d0baa856ca4c3d516025105cfe8f912f48dc/src/algebra/classical_lie_algebras.lean#L46)，行距过大：

$$
  J = \left[\begin{array}{cc}
              0_l & 1_l\\\\
              1_l & 0_l
            \end{array}\right]
$$

实际已修复：

$$
  J = \left[\begin{array}{cc}
              0_l & 1_l\\
              1_l & 0_l
            \end{array}\right]
$$


## [mathlib#6175](https://github.com/leanprover-community/mathlib/pull/6175)

[PR 之前](https://github.com/leanprover-community/mathlib/blob/c70feebd43e143d81a695f7d7e5b21e5892286e8/src/analysis/analytic/basic.lean#L626)（渲染正确）：

如果一个函数在圆盘 `D(x, R)` 内解析，那么它在该圆盘所包含的任意圆盘内也解析。事实上，可以写出
$$
f (x + y + z) = \sum_{n} p_n (y + z)^n = \sum_{n, k} \binom{n}{k} p_n y^{n-k} z^k
= \sum_{k} \Bigl(\sum_{n} \binom{n}{k} p_n y^{n-k}\Bigr) z^k.
$$
于是相应的幂级数的第 `k` 个系数等于
$\sum_{n} \binom{n}{k} p_n y^{n-k}$。在 `pₙ` 为多重线性映射的一般情形中，这需要被恰当地解释：不再使用二项式系数，而应对 `fin n` 中所有可能的、基数为 `k` 的子集 `s` 求和，并将 `z` 赋给 `s` 中的指标，将
`y` 赋给 `s` 之外的指标。
本段落中我们实现这一点。新的幂级数记作 `p.change_origin y`。然后我们验证它的收敛性，以及它的和与原来的和一致这一事实。这一讨论的结论是：一个函数解析的点集是开集。


[PR 之后](https://github.com/leanprover-community/mathlib/blob/676836509e16e6b6d3baf1354594658257f687bd/src/analysis/analytic/basic.lean#L626)（在 `sum` 前加了两个反斜杠作为变通；应当渲染失败）：

如果一个函数在圆盘 `D(x, R)` 内解析，那么它在该圆盘所包含的任意圆盘内也解析。事实上，可以写出
$$
f (x + y + z) = \\sum_{n} p_n (y + z)^n = \\sum_{n, k} \binom{n}{k} p_n y^{n-k} z^k
= \\sum_{k} \Bigl(\\sum_{n} \binom{n}{k} p_n y^{n-k}\Bigr) z^k.
$$
于是相应的幂级数的第 `k` 个系数等于
$\\sum_{n} \binom{n}{k} p_n y^{n-k}$。在 `pₙ` 为多重线性映射的一般情形中，这需要被恰当地解释：不再使用二项式系数，而应对 `fin n` 中所有可能的、基数为 `k` 的子集 `s` 求和，并将 `z` 赋给 `s` 中的指标，将
`y` 赋给 `s` 之外的指标。

## 行距测试

（每个示例上方给出 math.stackexchange.com 的结果）

---

渲染正常 ✅：
$\alpha
\alpha$

---

不应渲染 ❌：
$\alpha

\alpha$

---

不应渲染 ❌：
$$\alpha

\alpha$$

---

不应渲染 ❌：
$$

\alpha
\alpha

$$

---

渲染正常 ✅：
$$ \alpha\alpha
$$

---

渲染正常 ✅：
$$
\alpha\alpha
[hi](345)
b
$$

---

不应渲染 ❌：
$$ \alpha\alpha [hi](https://github.com) \beta

$$

---

渲染正常 ✅：
\begin{align}
\begin{matrix}
a & b & c
\end{matrix}
\end{align}

---

只有内层的 matrix 环境应被渲染：
\begin{align}

[hi](https://github.com)
\begin{matrix}
a & b & c
\end{matrix}
\end{align}

---

不应渲染 ❌：
\begin{align}

\begin{matrix}

a & b & c
\end{matrix}
\end{align}

---

渲染正常 ✅：

hi there \begin{align} 3 \\ 3 \end{align}

---

不应渲染 ❌：
\begin{align}
\end{blah}

---

不应渲染 ❌：
\begin{align}
[link](https://github.com) { {\alpha}
\end{align}

## 嵌套环境

来自 <http://web.archive.org/web/20120617014306/http://www.st.fmph.uniba.sk/~kiselak1/pdfka/tex/latexMath_align.pdf>

\begin{align}T(n) & \leq 2(c\lfloor n/2 \rfloor \lg( \lfloor n/2 \rfloor )) + n \\T(n) & \leq 2(cn/2) \lg(n/2) + n \\T(n) & = cn (\lg n - 1) + n \\T(n) & \leq cn \lg n\end{align}

\begin{align}
T(n) & \leq 2(c\lfloor n/2 \rfloor \lg( \lfloor n/2 \rfloor )) + n \\
T(n) & \leq 2(cn/2) \lg(n/2) + n \\
T(n) & = cn (\lg n - 1) + n \\
T(n) & \leq cn \lg n
\end{align}

\begin{gather}
\begin{aligned}T(n) & \leq 2(c\lfloor n/2 \rfloor \lg( \lfloor n/2 \rfloor )) + n \\T(n) & \leq 2(cn/2) \lg(n/2) + n \\T(n) & = cn (\lg n - 1) + n \\T(n) & \leq cn \lg n\end{aligned}\end{gather}

\begin{gather}
\begin{aligned}
T(n) & \leq 2(c\lfloor n/2 \rfloor \lg( \lfloor n/2 \rfloor )) + n \\
T(n) & \leq 2(cn/2) \lg(n/2) + n \\
T(n) & = cn (\lg n - 1) + n \\
T(n) & \leq cn \lg n
\end{aligned}
\end{gather}

\begin{align}\begin{aligned}T(n) & \leq 2(c\lfloor n/2 \rfloor \lg( \lfloor n/2 \rfloor )) + n \\T(n) & \leq 2(cn/2) \lg(n/2) + n \\T(n) & = cn (\lg n - 1) + n \\T(n) & \leq cn \lg n\end{aligned}\end{align}


## MathJax 基础教程与快速参考

来自 <https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference>

（德语版：[MathJax: LaTeX Basic Tutorial und Referenz](https://www.mathelounge.de/509545/mathjax-latex-basic-tutorial-und-referenz-deutsch)）

1. 要查看任意提问或回答中（包括本文）某个公式是如何写成的，在该表达式上右键单击并选择 “Show Math As > TeX Commands”。（这样做时，`$` 不会显示出来。请确保你自己添加上它们。参见下一条。还有[其他方式](https://math.meta.stackexchange.com/q/659)可以查看公式或整篇帖子的代码。）

2. **对于行内公式，将公式包在 `$...$` 中。对于独立显示的公式，使用 `$$...$$`。**
二者的渲染方式不同。例如，键入
`$\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}$`
会显示 $\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}$（这是行内模式），或键入
`$$\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}$$`
会显示
$$\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}$$
（这是显示模式）。

3. 对于**希腊字母**，使用 `\alpha`、`\beta`、…、`\omega`：$\alpha, \beta, … \omega$。对于大写形式，使用 `\Gamma`、`\Delta`、…、`\Omega`：$\Gamma, \Delta, …, \Omega$。某些希腊字母有变体形式：
`\epsilon \varepsilon` $\epsilon$、$\varepsilon$，`\phi \varphi` $\phi$、$\varphi$，等等。

4. 对于**上标和下标**，使用 `^` 和 `_`。例如，`x_i^2`：$x_i^2$，`\log_2 x`：$\log_2 x$。

5. **分组**。上标、下标以及其他运算只作用于紧接其后的“分组”。所谓“分组”，要么是单个符号，要么是用花括号 `{`…`}` 括起来的任意公式。如果你写 `10^10`，你会得到一个意外的结果：$10^10$。但 `10^{10}` 会得到你大概想要的结果：$10^{10}$。用花括号来界定上标或下标所作用的公式：`x^5^6` 是错误的；`{x^y}^z` 是 ${x^y}^z$，而 `x^{y^z}` 是 $x^{y^z}$。注意 `x_i^2` $x_i^2$ 与 `x_{i^2}` $x_{i^2}$ 之间的区别。

6. **括号** 普通符号 `()[]` 生成圆括号和方括号 $(2+3)[4+4]$。使用 `\{` 和 `\}` 来生成花括号 $\{\}$。

    这些括号**不会**随中间的公式自动缩放，因此如果你写 `(\frac{\sqrt x}{y^3})`，括号会显得太小：$(\frac{\sqrt x}{y^3})$。使用 `\left(`…`\right)` 会使括号大小自动适配其所包含的公式：`\left(\frac{\sqrt x}{y^3}\right)` 是 $\left(\frac{\sqrt x}{y^3}\right)$。

   `\left` 和 `\right` 适用于以下各类括号：`(` 和 `)` $(x)$、`[` 和 `]` $[x]$、`\{` 和 `\}` $\{ x \}$、`|` $|x|$、`\vert` $\vert x \vert$、`\Vert` $\Vert x \Vert$、`\langle` 和 `\rangle` $\langle x \rangle$、`\lceil` 和 `\rceil` $\lceil x \rceil$，以及 `\lfloor` 和 `\rfloor` $\lfloor x \rfloor$。`\middle` 可用于添加额外的分隔符。还有不可见的括号，用 `.` 表示：`\left.\frac12\right\rbrace` 是 $\left.\frac12\right\rbrace$。

    若需要手动调整大小：
`\Biggl(\biggl(\Bigl(\bigl((x)\bigr)\Bigr)\biggr)\Biggr)` 给出
$\Biggl(\biggl(\Bigl(\bigl((x)\bigr)\Bigr)\biggr)\Biggr)$。

7. **求和与积分** `\sum` 和 `\int`；下标是下限，上标是上限，例如 `\sum_1^n` $\sum_1^n$。如果上下限不止一个符号，别忘了用 `{`…`}`。例如，`\sum_{i=0}^\infty i^2` 是 $\sum_{i=0}^\infty i^2$。类似地，`\prod` $\prod$、`\int` $\int$、`\bigcup` $\bigcup$、`\bigcap` $\bigcap$、`\iint` $\iint$、`\iiint` $\iiint$、`\idotsint` $\idotsint$。

8. **分数** 有[三种生成方式](https://math.meta.stackexchange.com/q/12978/3111)。`\frac ab` 作用于紧接其后的两个分组，生成 $\frac ab$；对于较复杂的分子和分母，使用 `{`…`}`：`\frac{a+1}{b+1}` 是 $\frac{a+1}{b+1}$。如果分子和分母都很复杂，你可能更倾向于使用 `\over`，它会拆分它所在的分组：`{a+1\over b+1}` 是 ${a+1\over b+1}$。
使用 `\cfrac{a}{b}` 命令对于连分数很有用 $\cfrac{a}{b}$，更多细节[见此子文章](https://math.meta.stackexchange.com/a/5058/3111)。

9. **字体**

  * 使用 `\mathbb` 或 `\Bbb` 表示“黑板粗体”：$\mathbb{CHNQRZ}$。
  * 使用 `\mathbf` 表示粗体：$\mathbf{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$  $\mathbf{abcdefghijklmnopqrstuvwxyz}$。
    * 对于基于表达式的字符，改用 `\boldsymbol`：$\boldsymbol{\alpha}$
  * 使用 `\mathit` 表示斜体：$\mathit{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$ $\mathit{abcdefghijklmnopqrstuvwxyz}$。
  * 使用 `\pmb` 表示粗斜体：$\pmb{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$ $\pmb{abcdefghijklmnopqrstuvwxyz}$。
  * 使用 `\mathtt` 表示“打字机”字体：$\mathtt{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$ $\mathtt{abcdefghijklmnopqrstuvwxyz}$。
  * 使用 `\mathrm` 表示罗马字体：$\mathrm{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$  $\mathrm{abcdefghijklmnopqrstuvwxyz}$。
  * 使用 `\mathsf` 表示无衬线字体：$\mathsf{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$  $\mathsf{abcdefghijklmnopqrstuvwxyz}$。
  * 使用 `\mathcal` 表示“花体”字母：$\mathcal{ ABCDEFGHIJKLMNOPQRSTUVWXYZ}$
  * 使用 `\mathscr` 表示手写体字母：$\mathscr{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$
  * 使用 `\mathfrak` 表示“Fraktur”（旧式德文风格）字母：$\mathfrak{ABCDEFGHIJKLMNOPQRSTUVWXYZ} \mathfrak{abcdefghijklmnopqrstuvwxyz}$。

10. **根号 / 方根** 使用 `sqrt`，它会自适应其参数的大小：`\sqrt{x^3}` $\sqrt{x^3}$；`\sqrt[3]{\frac xy}` $\sqrt[3]{\frac xy}$。对于复杂的表达式，可以考虑改用 `{...}^{1/2}`。

11. 某些**特殊函数**，如 “lim”、“sin”、“max”、“ln” 等，通常以罗马字体而非斜体字体排版。使用 `\lim`、`\sin` 等来生成它们：`\sin x` $\sin x$，而不是 `sin x` $sin x$。使用下标将记号附加到 `\lim`：`\lim_{x\to 0}` $$\lim_{x\to 0}$$ 非标准的函数名可以用 `\operatorname{foo}(x)` $\operatorname{foo}(x)$ 来设置。

12. 还有数量极其庞大的**特殊符号与记号**，多到无法在此一一列出；参见[这份较短的列表](http://pic.plover.com/MISC/symbols.pdf)，或[这份详尽的列表](https://www.ctan.org/tex-archive/info/symbols/comprehensive/symbols-a4.pdf)。其中最常见的包括：
  * `\lt \gt \le \leq \leqq \leqslant \ge \geq \geqq \geqslant \neq` $\lt$、$\gt$、$\le$、$\leq$、$\leqq$、$\leqslant$、$\ge$、$\geq$、$\geqq$、$\geqslant$、$\neq$。你可以用 `\not` 在几乎任何符号上加一条斜杠：`\not\lt` $\not\lt$，但它常常看起来不太好。
  * `\times \div \pm \mp` $\times$、$\div$、$\pm$、$\mp$。`\cdot` 是居中的点：$x\cdot y$
  * `\cup \cap \setminus \subset \subseteq \subsetneq \supset \in \notin \emptyset \varnothing` $\cup$、$\cap$、$\setminus$、$\subset$、$\subseteq$、$\subsetneq$、$\supset$、$\in$、$\notin$、$\emptyset$、$\varnothing$
  * `{n+1 \choose 2k}` 或 `\binom{n+1}{2k}` ${n+1 \choose 2k}$
  * `\to \rightarrow \leftarrow \Rightarrow \Leftarrow \mapsto` $\to$、$\rightarrow$、$\leftarrow$、$\Rightarrow$、$\Leftarrow$、$\mapsto$
  * `\land \lor \lnot \forall \exists \top \bot \vdash \vDash` $\land$、$\lor$、$\lnot$、$\forall$、$\exists$、$\top$、$\bot$、$\vdash$、$\vDash$
  * `\star \ast \oplus \circ \bullet` $\star$、$\ast$、$\oplus$、$\circ$、$\bullet$
  * `\approx \sim \simeq \cong \equiv \prec \lhd \therefore` $\approx$、$\sim $、$\simeq$、$\cong$、$\equiv$、$\prec$、$\lhd$、$\therefore$
  * `\infty \aleph_0` $\infty\, \aleph_0$ `\nabla \partial` $\nabla$、$\partial$ `\Im \Re` $\Im$、$\Re$
  * 对于模同余，按如下方式使用 `\pmod`：`a\equiv b\pmod n` $a\equiv b\pmod n$。
  * 对于二元取模运算符，按如下方式使用 `\bmod`：`a\bmod 17` $a\bmod 17$。
  * 避免使用 `\mod`，因为它会产生额外的空白：将上面的结果与 `a\mod 17` $a\mod 17$ 对比。
  * `\ldots` 是 $a_1, a_2, \ldots ,a_n$ 中的点 `\cdots` 是 $a_1+a_2+\cdots+a_n$ 中的点
  * 手写体小写 l 是 `\ell` $\ell$。

  [Detexify](http://detexify.kirelabs.org/classify.html) 让你在网页上画出一个符号，然后列出看起来与之相似的 $\TeX$ 符号。这些不保证在 MathJax 中可用，但是一个很好的起点。要检查某个命令是否受支持，请注意 MathJax.org 维护着一份[当前受支持的 $\LaTeX$ 命令列表](http://docs.mathjax.org/en/latest/tex.html#supported-latex-commands)，你也可以查阅 Dr. Carol JVF Burns 的 [$\TeX$ Commands Available in MathJax](http://www.onemathematicalcat.org/MathJaxDocumentation/TeXSyntax.htm) 页面。

13. **空白** MathJax 通常会依据一套复杂的规则自行决定公式中的间距。在公式中放入额外的字面空格不会改变 MathJax 所插入的间距量：`a␣b` 和 `a␣␣␣␣b` 都是 $a    b$。要增加更多空白，使用 `\,` 表示窄空白 $a\,b$；`\;` 表示更宽的空白 $a\;b$。`\quad` 和 `\qquad` 是大空白：$a\quad b$、$a\qquad b$。

  要排版纯文本，使用 `\text{…}`：$\{x\in s\mid x\text{ is extra large}\}$。你可以在 `\text{…}` 内嵌套 `$…$`，例如用于插入空格。

14. **重音符号与变音符号** 对单个符号使用 `\hat` $\hat x$，对较大的公式使用 `\widehat` $\widehat{xy}$。如果你把它弄得太宽，就会显得很滑稽。类似地，还有 `\bar` $\bar x$ 和 `\overline` $\overline{xyz}$，以及 `\vec` $\vec x$、`\overrightarrow` $\overrightarrow{xy}$ 和 `\overleftrightarrow` $\overleftrightarrow{xy}$。对于点，如 $\frac d{dx}x\dot x =  \dot x^2 +  x\ddot x$，使用 `\dot` 和 `\ddot`。

15. MathJax 解析时所用的特殊字符可以用 `\` 字符转义：`\$` $\$$、`\{` $\{$、`\_` $\_$ 等。如果你想要 `\` 本身，应使用 `\backslash`（符号）或 `\setminus`（[二元运算](https://tex.stackexchange.com/a/511332)）来表示 $\backslash$，因为 `\\` 是用于换行的。

（教程到此结束。）

-------------

重要的是，本注记应保持合理的篇幅，不要过度膨胀。要收录更多主题，请撰写简短的附录并将其作为回答发布，而不要将它们插入本帖。

目录
---
按标题字母顺序排列的 MathJax 主题链接列表：

 - [Absolute values and norms](https://math.meta.stackexchange.com/a/15078/161490) • [Additional symbolic decorations](https://math.meta.stackexchange.com/a/13081/161490) • [Aligning Equations][3]
 - [Alternative Ways of Writing in LaTeX](https://math.meta.stackexchange.com/a/27910/161490) • [Annotations of reasoning](https://math.meta.stackexchange.com/a/21258/161490) • [Arbitrary operators](https://math.meta.stackexchange.com/a/15077/161490)
 - [Arrays](https://math.meta.stackexchange.com/a/5044/161490) • [Big braces](https://math.meta.stackexchange.com/a/11423/161490) • [Colors](https://math.meta.stackexchange.com/a/10116/161490)
 - [Commutative diagrams](https://math.meta.stackexchange.com/a/16888/161490) • [Continued fractions](https://math.meta.stackexchange.com/a/5058/161490) • [Crossing things out](https://math.meta.stackexchange.com/a/13183/161490)
 - [Definitions by cases (piecewise functions)](https://math.meta.stackexchange.com/a/5025/161490) • [Degree symbol](https://math.meta.stackexchange.com/a/19678/161490) • [Display style](https://math.meta.stackexchange.com/a/25054/161490)
 - [Equation numbering](https://math.meta.stackexchange.com/a/27793/161490) • [Fussy spacing issues](https://math.meta.stackexchange.com/a/5057/161490) • [Highlighting expressions](https://math.meta.stackexchange.com/a/22395/161490)
 - [Left and right arrows](https://math.meta.stackexchange.com/a/13310/161490) • [Limits](https://math.meta.stackexchange.com/a/12850/161490) • [Linear programming](https://math.meta.stackexchange.com/a/27756/161490)
 - [Long division](https://math.meta.stackexchange.com/a/21096/161490) • [Math Programming][2] • [Matrices][1]
 - [Markov Chains](https://math.meta.stackexchange.com/a/31141/161490) • [Mixing code and MathJax formatting on lines](https://math.meta.stackexchange.com/a/25251/161490) • [The \newcommand function](https://math.meta.stackexchange.com/a/11638/161490)
 - [Numbering Equations][4] • [Overlaying Symbols](https://math.meta.stackexchange.com/a/32210/736802) • [Packs of cards](https://math.meta.stackexchange.com/a/22516/161490)
 - [Symbols](https://math.meta.stackexchange.com/a/11284/161490)
• [System of equations](https://math.meta.stackexchange.com/a/6267/161490) • [Tables](https://math.meta.stackexchange.com/a/29979/161490)
 - [Tags and references](https://math.meta.stackexchange.com/a/11491/161490) • [Tensor indices](https://math.meta.stackexchange.com/a/30661/161490) • [Units](https://math.meta.stackexchange.com/a/27212/161490)
 - [Vertical spacing](https://math.meta.stackexchange.com/a/25048/161490)

  [1]: https://math.meta.stackexchange.com/a/5023/676335
  [2]: https://math.meta.stackexchange.com/a/27756/676335
  [3]: https://math.meta.stackexchange.com/a/5024/676335
  [4]: https://math.meta.stackexchange.com/a/11491/676335
  [5]: https://math.meta.stackexchange.com/a/29979/676335

## 对齐的方程

<https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference/5024#5024>

人们常常希望排列一系列方程，使其等号对齐。要实现这一点，使用 `\begin{align}…\end{align}`。每一行都应以 `\\` 结尾，并在需要对齐之处（通常是紧接等号之前）放置一个 & 符号。

例如，

\begin{align}
\sqrt{37} & = \sqrt{\frac{73^2-1}{12^2}} \\
 & = \sqrt{\frac{73^2}{12^2}\cdot\frac{73^2-1}{73^2}} \\
 & = \sqrt{\frac{73^2}{12^2}}\sqrt{\frac{73^2-1}{73^2}} \\
 & = \frac{73}{12}\sqrt{1 - \frac{1}{73^2}} \\
 & \approx \frac{73}{12}\left(1 - \frac{1}{2\cdot73^2}\right)
\end{align}

是由以下代码生成的


    \begin{align}
\sqrt{37} & = \sqrt{\frac{73^2-1}{12^2}} \\
 & = \sqrt{\frac{73^2}{12^2}\cdot\frac{73^2-1}{73^2}} \\
 & = \sqrt{\frac{73^2}{12^2}}\sqrt{\frac{73^2-1}{73^2}} \\
 & = \frac{73}{12}\sqrt{1 - \frac{1}{73^2}} \\
 & \approx \frac{73}{12}\left(1 - \frac{1}{2\cdot73^2}\right)
\end{align}

这里通常用于界定显示公式的 `$$` 标记可以省略。


## 分情形定义（分段函数）

<https://math.meta.stackexchange.com/a/5025>

使用 `\begin{cases}…\end{cases}`。每种情形以 `\\` 结尾，并在应当对齐的部分之前使用 `&`。

例如，你会得到这个：

$$f(n) =
\begin{cases}
n/2,  & \text{if $n$ is even} \\
3n+1, & \text{if $n$ is odd}
\end{cases}$$

写法如下：

      f(n) =
    \begin{cases}
n/2,  & \text{if $n$ is even} \\
3n+1, & \text{if $n$ is odd}
\end{cases}

花括号可以移到右侧：
$$
\left.
\begin{array}{ll}
\text{if $n$ is even:}&n/2\\
\text{if $n$ is odd:}&3n+1
\end{array}
\right\}
=f(n)
$$
写法如下：

    \left.
    \begin{array}{ll}
\text{if $n$ is even:}&n/2\\
\text{if $n$ is odd:}&3n+1
\end{array}
    \right\}
    =f(n)

要在各情形之间获得更大的垂直间距，我们可以用 `\\[2ex]` 代替 `\\`。例如，你会得到这个：

$$f(n) =
\begin{cases}
\frac{n}{2},  & \text{if $n$ is even} \\[2ex]
3n+1, & \text{if $n$ is odd}
\end{cases}$$

写法如下：

    f(n) =
    \begin{cases}
\frac{n}{2},  & \text{if $n$ is even} \\[2ex]
3n+1, & \text{if $n$ is odd}
\end{cases}

（一个 ‘ex’ 是等于字母 `x` 高度的长度；这里的 `2ex` 意味着该空白应为两个 ex 高。）

## 矩阵

<https://math.meta.stackexchange.com/a/5023/>

1. 使用 `$$\begin{matrix}…\end{matrix}$$`。在 `\begin` 和 `\end` 之间放入矩阵元素。每一行矩阵以 `\\` 结尾，并用 `&` 分隔矩阵元素。例如，

        $$
        \begin{matrix}
        1 & x & x^2 \\
        1 & y & y^2 \\
        1 & z & z^2 \\
        \end{matrix}
$$

    生成：

$$
        \begin{matrix}
        1 & x & x^2 \\
        1 & y & y^2 \\
        1 & z & z^2 \\
        \end{matrix}
$$

  MathJax 会调整各行各列的大小，使一切都能容纳。

2. 要添加括号，可以像教程第 6 节那样使用 `\left…\right`，或者将 `matrix` 替换为 `pmatrix` $\begin{pmatrix}1&2\\3&4\\ \end{pmatrix}$、`bmatrix` $\begin{bmatrix}1&2\\3&4\\ \end{bmatrix}$、`Bmatrix` $\begin{Bmatrix}1&2\\3&4\\ \end{Bmatrix}$、`vmatrix` $\begin{vmatrix}1&2\\3&4\\ \end{vmatrix}$、`Vmatrix` $\begin{Vmatrix}1&2\\3&4\\ \end{Vmatrix}$。

3. 当你想省略某些条目时，使用 `\cdots` $\cdots$ `\ddots` $\ddots$ `vdots` $\vdots$：

     $$\begin{pmatrix}
     1 & a_1 & a_1^2 & \cdots & a_1^n \\
     1 & a_2 & a_2^2 & \cdots & a_2^n \\
     \vdots  & \vdots& \vdots & \ddots & \vdots \\
     1 & a_m & a_m^2 & \cdots & a_m^n
     \end{pmatrix}$$


4. 对于水平“增广”矩阵，在一个格式适当的表格周围加上圆括号或方括号；详见下文的[数组](http://meta.math.stackexchange.com/a/5044/)。这里是一个例子：

  $$ \left[\begin{array}{cc|c}
  1&2&3\\
  4&5&6
  \end{array}\right] $$

  由以下代码生成：

        $$ \left[
    \begin{array}{cc|c}
      1&2&3\\
      4&5&6
    \end{array}
\right] $$

  这里 `cc|c` 是关键部分；它表示有三个居中的列，并在第二列和第三列之间有一条竖线。

5. 对于垂直“增广”矩阵，使用 `\hline`。例如

$$
\begin{pmatrix}
a & b \\
c & d\\
\hline
1 & 0\\
0 & 1
\end{pmatrix}
$$
由以下代码生成

    $$
      \begin{pmatrix}
        a & b\\
        c & d\\
      \hline
        1 & 0\\
        0 & 1
      \end{pmatrix}
    $$


6. 对于小型行内矩阵，使用 `\bigl(\begin{smallmatrix} ... \end{smallmatrix}\bigr)`，例如 $\bigl( \begin{smallmatrix} a & b \\ c & d \end{smallmatrix} \bigr)$ 由以下代码生成：

         $\bigl( \begin{smallmatrix} a & b \\ c & d \end{smallmatrix} \bigr)$

## 来自 `tactic_writing.md`

* `return`：在 monad 中产生一个值（类型：`A → m A`）
* `ma >>= f`：从 `ma : m A` 中取出类型为 `A` 的值并将其传给 `f : A → m B`。等价
  写法：`do a ← ma, f a`
* `f <$> ma`：将函数 `f : A → B` 作用于 `ma : m A` 中的值，得到一个 `m B`。等同于
  `do a ← ma, return (f a)`
* `ma >> mb`：等同于 `do a ← ma, mb`；这里 `ma` 的返回值被忽略，然后调用 `mb`。等价写法：`do ma, mb`
* `mf <*> ma`：等同于 `do f ← mf, f <$> ma`，或 `do f ← mf, a ← ma, return (f a)`
* `ma <* mb`：等同于 `do a ← ma, mb, return a`
* `ma *> mb`：等同于 `do ma, mb`，或 `ma >> mb`。为何同一件事有两种记法？历史
  原因。
* `pure`：等同于 `return`。同样是历史原因。
* `failure`：失败值（具体的 monad 通常有更有用的形式，如策略的 `fail` 和
  `failed`）。
* `ma <|> ma'` 从失败中恢复：运行 `ma`，若失败则运行 `ma'`。
* `a $> mb`：等同于 `do mb, return a`
* `ma <$ b`：等同于 `do ma, return b`
