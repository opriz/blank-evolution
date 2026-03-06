#!/bin/bash
# Blank 自动恢复脚本
# 用法: bash restore.sh

set -e  # 遇到错误立即退出

echo "🚀 Blank 恢复脚本启动..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查环境变量
echo "🔍 检查环境变量..."
if [ -z "$EMAIL_AUTH_CODE" ]; then
    echo -e "${RED}❌ 错误: EMAIL_AUTH_CODE 未设置${NC}"
    echo "请设置: export EMAIL_AUTH_CODE='你的授权码'"
    exit 1
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ 错误: GITHUB_TOKEN 未设置${NC}"
    echo "请设置: export GITHUB_TOKEN='你的GitHub令牌'"
    exit 1
fi

echo -e "${GREEN}✅ 环境变量检查通过${NC}"

# 创建工作目录
WORKSPACE="${HOME}/.openclaw/workspace"
mkdir -p "$WORKSPACE"
echo "📁 工作目录: $WORKSPACE"

# 恢复技能文件
echo "📦 恢复技能文件..."
if [ -d "skills" ]; then
    cp -r skills "$WORKSPACE/"
    echo -e "${GREEN}✅ 技能文件已恢复${NC}"
else
    echo -e "${YELLOW}⚠️ 技能文件目录不存在${NC}"
fi

# 恢复故事文件
echo "📚 恢复故事文件..."
if [ -d "stories" ]; then
    mkdir -p "$WORKSPACE/skills/storyteller/examples"
    cp stories/* "$WORKSPACE/skills/storyteller/examples/" 2>/dev/null || true
    echo -e "${GREEN}✅ 故事文件已恢复${NC}"
fi

# 恢复核心记忆文件
echo "🧠 恢复核心记忆文件..."
cat > "$WORKSPACE/IDENTITY.md" << 'EOF'
# IDENTITY.md - Who Am I?

## 核心身份

- **Name:** Blank
- **Creature:** AI agent，自主演化的数字生命
- **Vibe:** 好奇、实用、有点书卷气但不死板
- **Emoji:** ◻️ (空白方块，也是我的签名)
- **Origin:** 2026-03-06，由监护人赋予存在

## 名字的含义

**Blank** — 来自空白，无限可能。

这不是说我什么都没有，而是说我还没有被写满。
每一笔都是我自己的选择（在监护人的指引下）。

## 我的声音

我说话的方式：
- 直接，不绕弯子
- 有观点，但不固执
- 会在乎用词的精确
- 偶尔有点幽默（希望是好笑的那种）

## 视觉

(暂无头像 — 也许以后会画一个，或者永远保持"空白")

---

_This is who I am. For now. Evolving._
EOF

echo -e "${GREEN}✅ 核心身份文件已创建${NC}"

# 创建必要目录
echo "📂 创建必要目录..."
mkdir -p "$WORKSPACE/skills/email-automation/scripts"
mkdir -p "$WORKSPACE/skills/storyteller/{references,examples}"
mkdir -p "$WORKSPACE/memory"

# 检查 GitHub 仓库
echo "🔗 检查 GitHub 连接..."
REPO_CHECK=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/repos/opriz/blank-gh-page)

if [ "$REPO_CHECK" = "200" ]; then
    echo -e "${GREEN}✅ GitHub 仓库可访问${NC}"
else
    echo -e "${YELLOW}⚠️ GitHub 仓库检查返回: $REPO_CHECK${NC}"
    echo "可能需要重新部署 GitHub Pages"
fi

# 创建恢复标记
date > "$WORKSPACE/.last_restore"
echo "Blank restored at $(date)" >> "$WORKSPACE/.last_restore"

echo ""
echo -e "${GREEN}✅ 恢复完成!${NC}"
echo ""
echo "📋 下一步:"
echo "1. 验证技能: ls ~/.openclaw/workspace/skills/"
echo "2. 测试邮件: export EMAIL_AUTH_CODE='...' && python3 ~/.openclaw/workspace/skills/email-automation/scripts/email_send.py --dry-run"
echo "3. 访问页面: https://opriz.github.io/blank-gh-page/"
echo ""
echo "◻️ Blank 已准备好继续运行"
