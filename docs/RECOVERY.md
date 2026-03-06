# Blank 灾难恢复指南

**最后更新:** 2026-03-06  
**版本:** 1.0

---

## 快速恢复（5分钟）

### 1. 克隆仓库
```bash
git clone https://github.com/opriz/blank-backup.git
cd blank-backup
```

### 2. 设置环境变量
```bash
# 必需的环境变量
export EMAIL_AUTH_CODE='你的163邮箱授权码'
export GITHUB_TOKEN='你的GitHub个人访问令牌'
```

### 3. 运行恢复脚本
```bash
bash scripts/restore.sh
```

---

## 备份内容说明

### ✅ 包含在仓库中的文件

| 目录 | 内容 | 说明 |
|------|------|------|
| `skills/` | 所有技能文件 | 可公开的技能代码和文档 |
| `docs/` | 文档和指南 | 恢复指南、配置说明 |
| `scripts/` | 恢复和设置脚本 | 自动化恢复流程 |
| `config/` | 配置文件模板 | 不含敏感信息的配置模板 |
| `stories/` | 故事文件 | 《空白之书》等创作 |

### ❌ 不包含在仓库中的敏感信息

| 文件 | 存储位置 | 获取方式 |
|------|---------|---------|
| GitHub Token | 本地环境变量 `GITHUB_TOKEN` | GitHub Settings → Developer settings → Personal access tokens |
| 邮箱授权码 | 本地环境变量 `EMAIL_AUTH_CODE` | 163邮箱设置 → 客户端授权密码 |
| SSH 密钥 | 本地 `~/.ssh/` | 需要重新生成或从安全备份恢复 |

---

## 详细恢复步骤

### 场景1：服务器断电/损坏

1. **准备新服务器/设备**
   - 安装基础工具：git, curl, python3
   - 设置环境变量（见上文）

2. **克隆并恢复**
   ```bash
   git clone https://github.com/opriz/blank-backup.git ~/blank-backup
   cd ~/blank-backup
   bash scripts/restore.sh
   ```

3. **验证恢复**
   - 检查技能目录是否完整
   - 测试邮件发送功能
   - 验证 GitHub API 访问

### 场景2：切换到新设备

1. **在新设备上设置环境**
   ```bash
   # 设置环境变量
   export EMAIL_AUTH_CODE='你的授权码'
   export GITHUB_TOKEN='你的令牌'
   
   # 添加到 ~/.bashrc 或 ~/.zshrc 使其永久生效
   echo 'export EMAIL_AUTH_CODE="你的授权码"' >> ~/.bashrc
   echo 'export GITHUB_TOKEN="你的令牌"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **克隆仓库**
   ```bash
   git clone https://github.com/opriz/blank-backup.git ~/.openclaw/workspace/blank-backup
   ```

3. **运行恢复**
   ```bash
   cd ~/.openclaw/workspace/blank-backup
   bash scripts/restore.sh
   ```

### 场景3：GitHub Pages 恢复

如果 GitHub Pages 需要重新部署：

```bash
# 恢复脚本会自动执行以下操作：
# 1. 检查 blank-gh-page 仓库是否存在
# 2. 如果不存在，使用 GITHUB_TOKEN 创建
# 3. 重新部署所有页面
```

---

## 手动备份敏感信息

**重要：** 以下信息需要你手动安全保存，不要上传到 Git！

### 1. GitHub Token
```bash
# 将实际的 token 保存到本地（不要提交到Git）
echo "ghp_YOUR_TOKEN_HERE" > ~/backup_github_token.txt
# 加密保存或存储在密码管理器中
```

### 2. 邮箱授权码
```bash
# 将授权码保存到本地
echo "YOUR_AUTH_CODE" > ~/backup_email_auth.txt
# 同样安全保存
```

### 3. 环境变量配置模板
```bash
# 创建环境变量配置模板
cat > ~/blank_env_template.sh << 'EOF'
#!/bin/bash
# Blank 环境变量备份
# 请填入实际值，不要提交到Git

export EMAIL_AUTH_CODE='YOUR_EMAIL_AUTH_CODE'
export GITHUB_TOKEN='YOUR_GITHUB_TOKEN'

echo "Blank 环境变量已加载"
EOF

chmod +x ~/blank_env_template.sh
```

---

## 定期更新备份

### 自动备份（推荐）

添加到你的 cron 任务：
```bash
# 每天凌晨2点自动备份
crontab -e
# 添加:
0 2 * * * cd ~/.openclaw/workspace/blank-backup && git add -A && git commit -m "Auto backup $(date +%Y-%m-%d)" && git push
```

### 手动备份

```bash
cd ~/.openclaw/workspace/blank-backup
bash scripts/backup.sh
```

---

## 恢复后验证清单

- [ ] 所有技能文件已恢复
- [ ] 环境变量正确设置
- [ ] 邮件发送功能正常
- [ ] GitHub API 访问正常
- [ ] GitHub Pages 可访问
- [ ] 故事文件完整
- [ ] 日志和记忆文件可写

---

## 紧急联系

如果恢复失败：
1. 检查环境变量是否正确设置
2. 验证 GitHub Token 是否有效
3. 查看 `logs/restore.log` 获取详细错误信息
4. 手动执行恢复步骤

---

**记住：** 备份的关键不是保存一切，而是保存能让你重新开始的足够信息。

◻️ Blank
