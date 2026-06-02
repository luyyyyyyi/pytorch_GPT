# 阶段二：边缘计算 / 端侧推理（重点 · 你的差异化护城河）

> 周期：约 4-6 周 · 主线项目：[`ggml-org/llama.cpp`](https://github.com/ggml-org/llama.cpp)
> 为什么是重点：这是纯 C/C++ 的工业级推理引擎，正好吃你的 C/C++ 老本，而 90% 学 AI 的同学碰不了。
> 产出：端侧量化部署 demo + 不同量化等级的性能/精度 benchmark +（争取）一个开源 PR。

## 这阶段你会学到什么（写进简历的关键词）
- 模型量化（GGUF Q4/Q5/Q8）、KV cache、内存映射（mmap）
- CPU/GPU/Apple Metal 后端、SIMD 向量化
- 端侧推理的吞吐/延迟/内存权衡与 benchmark 方法

## 前置准备

```bash
bash scripts/clone_repos.sh phase2     # 克隆 llama.cpp 到 external/llama.cpp
```

Mac（Apple Silicon）已自带 Metal 加速，编译最简单：
```bash
cd external/llama.cpp
cmake -B build
cmake --build build --config Release -j
```

## 递进路径（从"会用"到"能改"）

### 第 1 阶段：跑通端侧推理（1 周）
1. 下载一个小的量化模型（GGUF 格式），推荐先用 1B-3B 级别：
   - 去 Hugging Face 搜 `Qwen2.5-1.5B-Instruct GGUF` 或 `TinyLlama GGUF`，选 `Q4_K_M`。
   - 或用 llama.cpp 自带的 `-hf` 直接拉：
     ```bash
     ./build/bin/llama-cli -hf Qwen/Qwen2.5-1.5B-Instruct-GGUF -p "你好，介绍一下你自己"
     ```
2. 起一个本地服务，用浏览器/curl 调：
   ```bash
   ./build/bin/llama-server -m model.gguf --port 8080
   ```
3. 里程碑：在自己电脑上完全离线跑起一个 LLM，记录首 token 延迟和 tokens/s。

### 第 2 阶段：自己量化模型（1 周）
1. 拿一个 FP16 的 HF 模型，用仓库脚本转 GGUF 再量化：
   ```bash
   python convert_hf_to_gguf.py /path/to/hf-model --outfile model-f16.gguf
   ./build/bin/llama-quantize model-f16.gguf model-q4_k_m.gguf Q4_K_M
   ```
2. 分别量化成 Q8_0 / Q5_K_M / Q4_K_M / Q2_K，准备做对比。
3. 里程碑：理解不同量化等级如何换取"体积 vs 速度 vs 精度"。

### 第 3 阶段：读懂核心代码（1-2 周）
- 重点读：`ggml`（张量/算子）、量化 kernel（`ggml-quants.c`）、`llama.cpp` 主推理循环、KV cache。
- 方法：从 `llama-cli` 的 main 入手，用断点/打印跟踪一次完整前向。
- 里程碑：能画出"输入 prompt → 推理 → 输出 token"的数据流图，能解释 mmap 和 KV cache 省了什么。

### 第 4 阶段：benchmark + 开源贡献（1-2 周）
1. 用 `phase2-edge/benchmark/run_benchmark.sh` 跑各量化等级的对比，填进 `benchmark/REPORT_模板.md`。
2. 用 `llama-bench` 工具做标准化测速：
   ```bash
   ./build/bin/llama-bench -m model-q4_k_m.gguf
   ```
3. 找一个力所能及的贡献：修文档错别字、补一个平台的编译说明、加一个小测试、回答 issue。
   - 里程碑：一个 benchmark 报告 +（理想情况）一个 merged PR。

## 验收标准
- [ ] 本地离线跑通至少一个端侧 LLM（CLI + server）。
- [ ] 自己量化出 ≥3 个等级的 GGUF 模型。
- [ ] 产出一份 benchmark 报告（体积/速度/内存/简单质量对比）。
- [ ] 能讲清量化、KV cache、mmap 的原理。
- [ ] （加分）向 llama.cpp 提交一个被合并的小 PR。

## 常见坑
- 编译报错先看 README 的 Build 章节，Mac 用 cmake + Metal 最省心。
- 模型跑不动：换更小的量化等级或更小的模型（先 1B 跑通）。
- benchmark 要控制变量：同一台机器、同一段 prompt、同样的线程数。
