#!/usr/bin/env bash
# 对不同量化等级的 GGUF 模型跑 llama-bench，输出对比表。
# 用法: bash run_benchmark.sh <llama.cpp构建目录> <模型目录>
# 例:   bash run_benchmark.sh ../../external/llama.cpp/build ./models
set -e

BUILD_DIR="${1:-../../external/llama.cpp/build}"
MODEL_DIR="${2:-./models}"
BENCH="$BUILD_DIR/bin/llama-bench"

if [ ! -x "$BENCH" ]; then
  echo "找不到 llama-bench: $BENCH"
  echo "请先编译 llama.cpp，并把量化好的 *.gguf 放进 $MODEL_DIR/"
  exit 1
fi

echo "# llama.cpp 量化等级 benchmark"
echo "机器: $(uname -msr)"
echo "时间: $(date)"
echo ""

shopt -s nullglob
models=("$MODEL_DIR"/*.gguf)
if [ ${#models[@]} -eq 0 ]; then
  echo "在 $MODEL_DIR 没找到 .gguf 模型。"
  exit 1
fi

for m in "${models[@]}"; do
  size=$(du -h "$m" | cut -f1)
  echo "## $(basename "$m")  (体积: $size)"
  "$BENCH" -m "$m"
  echo ""
done

echo "把上面的 tokens/s、体积填进 REPORT_模板.md"
