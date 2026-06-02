#!/usr/bin/env bash
# 克隆三阶段需要的开源仓库到 external/（已在 .gitignore 中忽略）。
# 用法: bash scripts/clone_repos.sh [phase1|phase2|phase3|all]
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p external
cd external

TARGET="${1:-all}"

clone() {
  local url="$1" dir="$2"
  if [ -d "$dir" ]; then
    echo "    已存在: external/$dir (跳过)"
  else
    echo "==> clone $url"
    git clone --depth 1 "$url" "$dir"
  fi
}

if [ "$TARGET" = "phase1" ] || [ "$TARGET" = "all" ]; then
  echo "## 阶段一：LLM / PyTorch 入门"
  clone https://github.com/rasbt/LLMs-from-scratch.git LLMs-from-scratch
  clone https://github.com/karpathy/build-nanogpt.git  build-nanogpt
  clone https://github.com/karpathy/minbpe.git         minbpe
fi

if [ "$TARGET" = "phase2" ] || [ "$TARGET" = "all" ]; then
  echo "## 阶段二：边缘计算 / 推理引擎"
  clone https://github.com/ggml-org/llama.cpp.git llama.cpp
fi

if [ "$TARGET" = "phase3" ] || [ "$TARGET" = "all" ]; then
  echo "## 阶段三：AI for Science"
  clone https://github.com/deepmodeling/deepmd-kit.git deepmd-kit
  # 轻量备选：
  # clone https://github.com/deepchem/deepchem.git deepchem
fi

echo ""
echo "==> 完成。仓库位于 external/，可按各阶段 GUIDE.md 操作。"
