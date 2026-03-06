# Blank 备份仓库

这是 Blank (◻️) 的灾难恢复仓库。

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/opriz/blank-backup.git
cd blank-backup

# 2. 设置环境变量
export EMAIL_AUTH_CODE='你的授权码'
export GITHUB_TOKEN='你的GitHub令牌'

# 3. 运行恢复
bash scripts/restore.sh
```

## 详细指南

查看 [docs/RECOVERY.md](docs/RECOVERY.md) 获取完整的恢复指南。

## 包含内容

- ✅ 所有技能文件（邮件自动化、故事创作、系统监控）
- ✅ 《空白之书》故事全集
- ✅ 恢复脚本和文档
- ✅ 配置模板

## 安全说明

❌ **不包含**在仓库中的内容：
- GitHub Token（需要设置环境变量）
- 邮箱授权码（需要设置环境变量）
- SSH 私钥（需要重新配置）

请确保这些敏感信息安全保存在本地或密码管理器中。

---

◻️ Blank
Last updated: 2026-03-06
