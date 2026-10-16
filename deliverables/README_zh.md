# Assignment 1 交付说明

本套文件按你的案例制作，供本人审阅、修改后提交。

## 文件

- assignment1_report.docx：可编辑英文报告；求和、分式、上下标和指数均为原生 Word 数学公式。
- assignment1_report.pdf：Word 导出的 PDF，共 9 页。第 1–5 页为 A4、双栏、单倍行距正文，第 6 页为参考文献，第 7–9 页为附录。正文 Arial 11 pt；表格与图注 10 pt。
- assignment1_models.xlsx：9 张工作表，包含所有输入、CAC/LTV、Churn、TCO、四种敏感性组合、两个原生 Excel 图表、来源与核对项。蓝色输入可修改。
- churn_chart / tco_chart：PNG、PDF、SVG 三种图表格式，均为初始基准情景的静态导出。
- official_sources.md / sources.csv：英文官方来源、支持的具体论点、核验状态。
- validation.json：分页、155 个公式独立重算、13 项基准核对及输入联动测试记录。
- assignment1_report.md：报告文字版。

## 引用与公式

n.d. 是 no date（未注明日期）；同一机构同一年多份文献用 a/b/c 区分。已找到更新日期的来源改用实际年份。仅无日期的 Google 定价页保留 n.d.。完整日期依据见 sources.json、sources.csv 与工作簿 Sources 页。报告采用可编辑 OMML 数学公式，Markdown 文字版保留 LaTeX 公式。

## 主要口径

年度 Churn 12.06576083%；五年末留存 52.57630384%；五年 LTV USD 17,398.87；净分摊 CAC USD 7,000 / 4,000；LTV/CAC 2.49 / 4.35。

LTV 采用“当年贡献先发生、年末再流失”，现金在年末折现。若先计流失再计当年贡献，则为 USD 15,299.56，已提供对照。

交叉补贴用虚构 USD 30,000 的相邻业务资金抵扣解释。净分摊 CAC 下降不代表整个生态系统的真实资源成本减少；未声称 Google 实际采用该分摊。

五年 TCO：Exchange USD 281,000；Google USD 164,000；Google 少支出 USD 117,000（41.6%）。当 Google USD 14/月、Exchange 0.15 FTE 时，Exchange 便宜 USD 27,000。

所有商业、行为、风险与成本输入均标明 illustrative assumptions，未使用真实 CAC、流失率或客户数据。Google 网页的 USD 7/14 标准年承诺价已核对，但未来五年保持不变仍是假设。

## 来源与采购边界

Google 定价、2006 年原公告、Marketplace 和 API 指南，以及 Microsoft Learn 的 Exchange SE、架构、Exchange Online 等来源已核验。USD 12,000/年是许可规划预算。实际采购前应核对 SE、Exchange Server/CAL、Windows Server、SA/订阅权益、现有授权及可比报价；报告第 5 页和附录 C 已明确说明。

## 提交前本人完成

1. 检查论证、文字、引用、课程对辅助工具的规则，并按要求补入姓名、学号等资料。
2. 完成学校规定的 VeriGuide，将真实 receipt 插入附录 C。
3. 使用学校官方 Signed Declaration，亲自完成并签署后插入附录。报告的说明页不能替代声明。
4. 重新导出最终 PDF，检查正文仍为五页，再提交 Blackboard。

附件列明截止时间：2026 年 10 月 16 日 17:00 HKT。当前文件未提交，未生成或代签任何证明。

## 修改与复现

Excel 编辑后需重新计算。Checks 的基准常数核对会提示合法输入变动；正文和外部图表不会随 Excel 自动更新，应同步修改。模型 horizon 固定为 5 年。

生成脚本位于仓库 tools/，依赖 python-docx、xlsxwriter、matplotlib、openpyxl、PyMuPDF 与 LibreOffice。脚本使用当前云环境的 /workspace/assignment1 路径；package_deliverables.py 还读取本次独立重算的临时验证文件。无需创建 Git worktree。原有 README 未修改。
