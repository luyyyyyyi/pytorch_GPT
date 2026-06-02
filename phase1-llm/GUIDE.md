# 阶段一：大模型 / LLM 入门（同时把 PyTorch 学会）

> 周期：约 3-4 周 · 目标：从零手写并训练一个 GPT 小模型，把 PyTorch 真正用起来。
> 产出：一个能训练 + 推理的 GPT、一份复现笔记、一个自己的 fork。

## 为什么是这几个项目

| 项目 | 角色 | 链接 |
|------|------|------|
| `rasbt/LLMs-from-scratch` | 主线教材，专为"会 Python 不会 PyTorch"的人写，附录 A 教 PyTorch | https://github.com/rasbt/LLMs-from-scratch |
| `karpathy/build-nanogpt` | 配套视频，逐行复现 GPT-2，git 历史一步步可回放 | https://github.com/karpathy/build-nanogpt |
| `karpathy/minbpe` | 学透分词器 BPE（LLM 的"第一步"） | https://github.com/karpathy/minbpe |

## 前置准备

```bash
# 在项目根目录
bash scripts/setup_env.sh              # 建 venv + 装 torch（注意 Python 版本，见 README）
bash scripts/clone_repos.sh phase1     # 克隆三个仓库到 external/
source .venv/bin/activate
```

如果本机没 GPU：阶段一的小模型 **CPU 也能跑**（慢一点）。需要更大算力时再用云 GPU（Colab 免费档 / AutoDL / Lambda）。

## 周计划

### 第 1 周：PyTorch 基础 + 注意力机制
1. 先跑本仓库自检，确认你理解了注意力在算什么：
   ```bash
   python demos/self_attention_stdlib.py   # 纯手写版，看清每一步
   python demos/self_attention_numpy.py    # numpy 版对照（需先装 numpy）
   ```
2. 读 `LLMs-from-scratch` 的 **附录 A（PyTorch 入门）** + **第 2 章（文本数据与分词）**，把 notebook 跑一遍：
   ```bash
   cd external/LLMs-from-scratch && jupyter lab
   ```
3. 笔记：用 [notes/复现笔记模板.md](notes/复现笔记模板.md) 记录张量、自动求导、Dataset/DataLoader 三个概念。

### 第 2 周：手写注意力与 GPT 结构
- 跟 `LLMs-from-scratch` 第 3 章（注意力）、第 4 章（GPT 模型结构）逐节实现。
- 自己默写一遍多头注意力（不看代码），对照 demo 检查。
- 里程碑：能解释 Q/K/V、因果掩码、残差连接、LayerNorm 各自的作用。

### 第 3 周：预训练 + 文本生成
- 第 5 章：在小语料上预训练，画出 loss 曲线（matplotlib），让模型能生成像样的文本。
- 然后切到 `build-nanogpt`，跟视频用 `git log` 一步步看它如何从空文件搭到 GPT-2：
  ```bash
  cd external/build-nanogpt
  git log --oneline        # 每个 commit 对应视频一个步骤
  python train_gpt2.py     # 按 README 配置后训练（小规模先 CPU/单卡试跑）
  ```
- 里程碑：复现出能输出连贯英文的小 GPT；保存一张 loss 曲线截图。

### 第 4 周：分词器 + 收尾
- 跟 `minbpe` 的 `exercise.md` 一步步实现 BPE 分词器，训练自己的 tokenizer。
- 第 6-7 章：微调（分类 / 指令跟随）选一个跑通。
- 整理复现笔记，把 fork 的 README 写好（见 [portfolio/技术报告模板.md](../portfolio/技术报告模板.md)）。

## 验收标准（达到即算这阶段"有产出"）
- [ ] 能从零写出多头自注意力并解释每一步。
- [ ] 训练出一个能生成连贯文本的 GPT 小模型，保存 loss 曲线。
- [ ] 用 minbpe 训练出自己的分词器。
- [ ] fork 仓库 + 复现笔记发到自己 GitHub。

## 常见坑
- **Python 版本**：torch 没装上多半是 Python 太新（3.14），换 3.12。
- **显存不足**：调小 `batch_size` / `block_size` / 模型层数；先用最小配置跑通再放大。
- **loss 不降**：检查学习率、是否忘了 `optimizer.zero_grad()`、数据是否 shuffle。
- **别一次性读完代码再动手**：跑通 → 改一个超参 → 看变化 → 再理解。
