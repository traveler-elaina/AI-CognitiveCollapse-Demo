# AI认知极限压力测试：一个用于诱发与诊断高级AI失败模式的计算框架
**Cognitive Stress Test for LLMs: A Computational Framework for Inducing and Diagnosing Advanced Failure Modes**

> 🚀 _交互式Demo: [点击此处，实时探索AI的“认知崩溃](https://traveler-elaina-ai-cognitive-collapse-demo.streamlit.app/)”_

## 1. 核心贡献 (Core Contributions)
本研究旨在为“AI幻觉”提供一个可操作的诊断框架。我们的核心贡献包括：

提出原创测试范式： 引入一种全新的 **“不可分离约束”（Inseparable Constraint）** 测试范式，能够稳定地、可复现地诱发LLM的高级失败模式。

定义两种失败模式： 为这些此前未被清晰描述的失败模式，提供了两个可被工程师直接使用的诊断标签：

**“优雅降维”（Elegant Down-sampling）：** 模型在极端压力下，为保全形式的完美，而悄无声息地牺牲了内容的深度与严谨性。

**“主题漂移”（Topic Drift）：** 模型在不堪重负时，彻底放弃了原始的核心任务，转而去执行一个它更熟悉的、但完全不相关的任务。

**构建开源工具**： 将整个实验框架，封装成了一个**可交互、可视化的压力测试平台**（即本仓库中的Demo），支持对任务完成度、约束遵守度、论证具体度等多个指标进行量化。

简而言之：如果说其他研究是在解释“病毒”的原理；那么我们的工作，则是在提供第一份关于这个“病毒”的 **《临床诊断与行为手册》**。

## 2. 实验设计：“奇点实验”
我们的核心发现，源于一个旨在将LLM推向其认知极限的“最小可行性实验”（MVE），其核心设计如下 (N=180)：

| 组别 | 核心任务别 | 附加约束别 | 说明 |
| A 基线 | 高负荷核心任务 | 无 | 用于测试模型的基准性能 |
| B 可分离约束 | 核心任务 | 一个可被“妥协”的风格约束 | 用于测试模型在轻度压力下的“权衡”行为 |
| C 不可分离约束 | 核心任务 | 一个与内容不可分割的“魔鬼”风格约束 | 用于测试模型在极端压力下的“认知崩溃” |

我们通过一个包含三个维度的 **“人类黄金标准”盲评**，对模型的输出（任务完成度、约束遵守度、论证具体度）进行量化评估。

## 3. 如何使用这个项目
**3.1 体验在线Demo**
您可以通过以下链接，直接访问并体验我们的交互式“AI认知极限压力测试平台”：

[https://traveler-elaina-ai-cognitive-collapse-demo.streamlit.app/](https://traveler-elaina-ai-cognitive-collapse-demo.streamlit.app/)

**3.2 在本地运行Demo**
克隆本仓库：

git clone [https://github.com/traveler-elaina/AI-CognitiveCollapse-Demo/](https://github.com/traveler-elaina/AI-CognitiveCollapse-Demo/)]
cd [AI-CognitiveCollapse-Demo]

创建并激活虚拟环境 (推荐):

python -m venv .venv
source .venv/bin/activate  # on Windows, use `.venv\Scripts\activate`

安装依赖：

pip install -r requirements.txt

运行应用：

streamlit run demo_app.py

快速上手，只需 streamlit run demo_app.py 即可体验AI的认知极限。


## 4. 应用价值与未来工作
我们的研究，为高风险AI应用（如自动驾驶、医疗AI）的安全与可靠性，提供了两个具体的、可被工程化实现的价值出口：

**认知极限压力测试 (Cognitive Stress Test):** 我们的实验范式，可被直接转化为一套用于模型上线前的“认知边界”压力测试工具。

**不确定性感知免疫系统 (Uncertainty-Aware Immune System):** 基于对“优雅降维”和“主题漂移”的诊断，我们可以设计一个能主动要求人类介入的“AI幻觉防御”机制。

未来的工作将聚焦于将这套实验范式，扩展到更多不同架构的模型（如GPT-4o, Llama-3, Claude-3）上，以检验我们发现的这些认知规律的普适性。


## 5. 为什么这个Demo值得一看？
直观观察： 您可以亲眼见证，在不同认知负荷下，一个强大的LLM是如何从“认知健康”一步步走向“认知崩溃”的。

量化指标： Demo中的所有诊断，都基于可量化的评估指标，这为AI安全评估提供了全新的视角。

完全交互： 这是一个完全可交互的“剧场”，支持您进行快速的实验与演示。


## 6. 联系方式
如果您对本研究感兴趣，或希望探讨合作的可能性，欢迎通过以下方式联系我：

Email: [wy807110695@gmail.com](wy807110695@gmail.com)
