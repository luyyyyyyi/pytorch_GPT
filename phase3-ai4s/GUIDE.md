# 阶段三：AI for Science（切入科研方向）

> 周期：约 4-6 周 · 目标：跑通一个真实的 AI4S 工作流，产出可作为"敲门砖"的实验报告。
> 产出：一个机器学习势函数 / 材料属性预测实验 + 实验报告，用于联系科研导师。

## 选哪个项目

| 路线 | 项目 | 适合 | 链接 |
|------|------|------|------|
| 主线（硬核）| `deepmodeling/deepmd-kit` (DeePMD-kit) | 想做分子动力学/计算化学，能用上 C/C++，拿过 Gordon Bell 奖 | https://github.com/deepmodeling/deepmd-kit |
| 备选（平缓）| `deepchem/deepchem` | 先用现成数据集 + 图神经网络预测材料/分子属性入门 | https://github.com/deepchem/deepchem |

建议：**先用 DeepChem 花 1 周快速尝鲜**（门槛低、教程多），确认对这个方向有兴趣后，再投入 DeePMD-kit 做更扎实的成果。

## 前置准备

```bash
bash scripts/clone_repos.sh phase3     # 克隆 deepmd-kit（备选 deepchem 在脚本里注释着）
# 这阶段依赖较重，建议单独建 conda 环境（Python 3.10/3.11）
```

## 路线 A（备选 / 入门）：DeepChem 材料属性预测（约 1 周）
1. 安装：`pip install deepchem` （需要 torch 或 tensorflow 后端）。
2. 跟官方 tutorial `Introduction_To_Material_Science.ipynb`：
   - 用 MoleculeNet 内置数据集，`CGCNNModel` 预测材料的形成能。
3. 里程碑：跑通一个"加载数据→特征化→训练 GNN→评估"的完整 ML 流程，画出预测 vs 真实散点图。

## 路线 B（主线 / 科研向）：DeePMD-kit 深度势能 + 分子动力学（约 3-5 周）

跟官方 Quick Start（端到端 4 步）：
1. **准备数据**：用 `dpdata` 把 DFT 计算结果（VASP/QE/CP2K 等）转成 DeePMD 格式。官方有现成示例数据，先用它跑通。
2. **训练**：写 `input.json`（描述符 + 网络结构 + 训练参数），`dp train input.json`。
3. **冻结 + 测试**：`dp freeze` 导出模型，`dp test` 评估能量/力的误差。
4. **接分子动力学**：把训练好的势函数接到 LAMMPS，跑一段 MD 模拟。

里程碑：得到一个深度势能模型，能量/力的预测误差进入合理范围，并能驱动一段 MD。

> 你的 C/C++ 优势在这里也用得上：DeePMD-kit 有 C++ 核与 LAMMPS 插件，深入可以读它的算子实现/接口。

## 验收标准
- [ ] 至少跑通一条完整工作流（DeepChem 属性预测 或 DeePMD 势函数训练）。
- [ ] 有量化的评估结果（误差/精度）+ 图表。
- [ ] 写出实验报告（见 [portfolio/技术报告模板.md](../portfolio/技术报告模板.md)）。
- [ ]（加分）读懂一篇相关论文，能说清这个方法解决什么科学问题。

## 怎么把它变成科研机会
- 锁定学校里做"计算材料 / 计算化学 / AI4S"的实验室，看他们论文用什么工具。
- 用本阶段的实验报告 + GitHub 复现，按 [联系导师邮件模板](../portfolio/联系导师邮件模板.md) 主动联系。
- 表达："我已经能独立跑通 XX 工具链并做了 YY 实验，希望参与课题组工作"。

## 常见坑
- 依赖较重，强烈建议用独立 conda 环境，别和阶段一/二混。
- DFT 数据可能难拿，先用官方示例数据跑通流程，再考虑自己产数据。
- 看不懂物理背景不要紧，先把"数据→模型→评估"的 ML 闭环跑通，物理边做边补。
