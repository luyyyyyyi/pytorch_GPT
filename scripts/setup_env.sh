#!/usr/bin/env bash
# 一键搭建 Python 环境并跑自检 demo。
# 用法: bash scripts/setup_env.sh
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> 寻找合适的 Python 解释器 (优先 3.12 >= 3.11 >= 3.10)"
PYBIN=""
for v in python3.12 python3.11 python3.10 python3.13 python3; do
  if command -v "$v" >/dev/null 2>&1; then
    PYBIN="$(command -v "$v")"
    echo "    使用: $PYBIN ($($PYBIN --version 2>&1))"
    break
  fi
done

if [ -z "$PYBIN" ]; then
  echo "!! 未找到 python，请先安装 Python 3.10-3.12"
  exit 1
fi

PYVER="$($PYBIN -c 'import sys; print("%d.%d"%sys.version_info[:2])')"
# 默认都尝试安装 torch；装失败也不影响其它步骤。
TORCH_OK=1

echo "==> 创建虚拟环境 .venv"
"$PYBIN" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip >/dev/null

# 国内直连 PyPI 常出现 IncompleteRead 中断，默认用清华镜像（可用 PIP_MIRROR 覆盖/置空）
PIP_MIRROR="${PIP_MIRROR-https://pypi.tuna.tsinghua.edu.cn/simple}"
MIRROR_ARGS=()
[ -n "$PIP_MIRROR" ] && MIRROR_ARGS=(-i "$PIP_MIRROR")

# pip_retry: 网络不稳定时多试几次（IncompleteRead 等中断常见）
pip_retry() {
  for i in 1 2 3 4 5; do
    if pip install "${MIRROR_ARGS[@]}" --retries 5 --timeout 180 "$@"; then return 0; fi
    echo "    第 $i 次失败，3 秒后重试..."; sleep 3
  done
  return 1
}

echo "==> 安装基础依赖 (numpy)"
pip_retry "numpy>=1.26" || echo "!! numpy 安装失败（多为网络问题）。纯标准库自检 demo 不受影响。"

echo "==> 安装 PyTorch 及阶段一依赖 (Python $PYVER)"
if pip_retry torch tiktoken matplotlib tqdm jupyterlab; then
  echo "    PyTorch 等依赖安装成功"
else
  echo "!! 安装失败 (多为网络中断或该 Python 版本暂无 torch wheel)。"
  echo "   可稍后手动重试: pip install torch tiktoken matplotlib tqdm jupyterlab"
  echo "   若反复失败, 建议用 pyenv/conda 装 Python 3.12 后重跑本脚本。"
fi

echo "==> 运行自检 demo (纯标准库自注意力，无需任何依赖)"
python demos/self_attention_stdlib.py

if python -c "import numpy" 2>/dev/null; then
  echo "==> numpy 可用，额外运行 numpy 版自注意力"
  python demos/self_attention_numpy.py
fi

echo ""
echo "==> 完成。激活环境: source .venv/bin/activate"
