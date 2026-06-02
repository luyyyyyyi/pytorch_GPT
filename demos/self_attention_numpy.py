"""
纯 numpy 实现的单头自注意力 (self-attention)。

作用：
  1) 不依赖 PyTorch 即可运行，用来验证 .venv 环境是否就绪（阶段一的自检 demo）。
  2) 用最少的代码讲清楚 Transformer 的核心：Q/K/V、缩放点积、softmax、加权求和。
     等你在 LLMs-from-scratch 里看到 PyTorch 版的 attention 时，会发现就是这几行。

运行：
  python demos/self_attention_numpy.py
"""

import numpy as np


def softmax(x, axis=-1):
    # 减去最大值是为了数值稳定，避免 exp 溢出
    x = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=axis, keepdims=True)


def self_attention(x, w_q, w_k, w_v, causal=True):
    """x: (seq_len, d_model)。返回每个位置融合上下文后的新表示。"""
    q = x @ w_q  # (seq_len, d_k)
    k = x @ w_k  # (seq_len, d_k)
    v = x @ w_v  # (seq_len, d_v)

    d_k = q.shape[-1]
    scores = q @ k.T / np.sqrt(d_k)  # 缩放点积，(seq_len, seq_len)

    if causal:
        # 因果掩码：第 i 个 token 只能看到 <= i 的 token（GPT 训练的关键）
        seq_len = scores.shape[0]
        mask = np.triu(np.ones((seq_len, seq_len)), k=1).astype(bool)
        scores = np.where(mask, -np.inf, scores)

    weights = softmax(scores, axis=-1)  # 注意力权重，每行和为 1
    out = weights @ v                   # 用权重对 V 加权求和
    return out, weights


def main():
    rng = np.random.default_rng(42)
    seq_len, d_model, d_head = 4, 8, 8

    # 假装这是 4 个 token 经过 embedding 后的向量
    x = rng.standard_normal((seq_len, d_model))
    w_q = rng.standard_normal((d_model, d_head)) * 0.1
    w_k = rng.standard_normal((d_model, d_head)) * 0.1
    w_v = rng.standard_normal((d_model, d_head)) * 0.1

    out, weights = self_attention(x, w_q, w_k, w_v, causal=True)

    print("环境自检通过 ✓  numpy 版本:", np.__version__)
    print("\n输入 x 形状:", x.shape)
    print("输出 形状:", out.shape, "(应与输入序列长度一致)")
    print("\n因果注意力权重 (下三角，每行和为 1):")
    np.set_printoptions(precision=3, suppress=True)
    print(weights)
    row_sums = weights.sum(axis=1)
    assert np.allclose(row_sums, 1.0), "softmax 每行应和为 1"
    assert np.allclose(weights[0, 1:], 0.0), "第 0 个 token 不应看到未来的 token"
    print("\n断言通过：每行权重和为 1，且因果掩码生效。")
    print("下一步：去 phase1-llm/GUIDE.md 开始用 PyTorch 复现完整的 GPT。")


if __name__ == "__main__":
    main()
