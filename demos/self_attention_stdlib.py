"""
纯 Python 标准库实现的单头因果自注意力 (self-attention)。

为什么有这个版本：
  numpy/torch 需要联网安装，而本脚本只用标准库 (math/random)，
  因此**任何机器、不联网**都能直接运行，用作环境自检。
  概念和 demos/self_attention_numpy.py 完全一致，只是用纯 Python 手写矩阵运算，
  能帮你彻底看清 Transformer 注意力每一步在算什么。

运行：
  python demos/self_attention_stdlib.py
"""

import math
import random


def matmul(a, b):
    """a: (n,k), b: (k,m) -> (n,m)"""
    n, k, m = len(a), len(b), len(b[0])
    out = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            s = 0.0
            for t in range(k):
                s += a[i][t] * b[t][j]
            out[i][j] = s
    return out


def transpose(a):
    return [list(row) for row in zip(*a)]


def softmax_row(row):
    # 减最大值做数值稳定
    m = max(v for v in row if v != float("-inf"))
    exps = [0.0 if v == float("-inf") else math.exp(v - m) for v in row]
    s = sum(exps)
    return [e / s for e in exps]


def self_attention(x, w_q, w_k, w_v, causal=True):
    q = matmul(x, w_q)
    k = matmul(x, w_k)
    v = matmul(x, w_v)
    d_k = len(q[0])
    scale = 1.0 / math.sqrt(d_k)

    scores = matmul(q, transpose(k))
    seq_len = len(scores)
    for i in range(seq_len):
        for j in range(seq_len):
            scores[i][j] *= scale
            if causal and j > i:  # 因果掩码：不能看未来
                scores[i][j] = float("-inf")

    weights = [softmax_row(scores[i]) for i in range(seq_len)]
    out = matmul(weights, v)
    return out, weights


def rand_matrix(rows, cols, scale=1.0):
    return [[random.gauss(0, 1) * scale for _ in range(cols)] for _ in range(rows)]


def main():
    random.seed(42)
    seq_len, d_model, d_head = 4, 8, 8

    x = rand_matrix(seq_len, d_model)
    w_q = rand_matrix(d_model, d_head, 0.1)
    w_k = rand_matrix(d_model, d_head, 0.1)
    w_v = rand_matrix(d_model, d_head, 0.1)

    out, weights = self_attention(x, w_q, w_k, w_v, causal=True)

    print("环境自检通过 (纯标准库，无需联网) OK")
    print(f"\n输入序列长度: {seq_len}, 维度: {d_model}")
    print(f"输出形状: {len(out)} x {len(out[0])} (应与输入序列长度一致)")
    print("\n因果注意力权重 (下三角，每行和为 1):")
    for i, row in enumerate(weights):
        print("  " + "  ".join(f"{w:5.3f}" for w in row))

    for i, row in enumerate(weights):
        assert abs(sum(row) - 1.0) < 1e-9, "softmax 每行应和为 1"
    assert all(abs(weights[0][j]) < 1e-12 for j in range(1, seq_len)), \
        "第 0 个 token 不应看到未来的 token"
    print("\n断言通过：每行权重和为 1，且因果掩码生效。")
    print("下一步：打开 phase1-llm/GUIDE.md，开始用 PyTorch 复现完整 GPT。")


if __name__ == "__main__":
    main()
