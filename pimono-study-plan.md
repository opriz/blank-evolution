# Pimono 学习计划

> 目标：深入理解 Mario Zechner 的 AI Agent 工具集设计思想

---

## 阶段一：全局概览（1-2 小时）

**目标**：建立整体认知，了解项目结构和设计理念

### 任务清单
- [ ] 阅读 README.md - 了解 7 个包的职责分工
- [ ] 阅读 AGENTS.md - 理解开发规范和设计哲学
- [ ] 浏览 packages/ 目录结构，画出依赖关系图
- [ ] 运行 `./pi-test.sh` 体验编码 Agent 交互

### 产出物
- 画出包依赖关系图（pi-ai → pi-agent-core → pi-coding-agent）
- 记录 3 个最核心的设计决策

---

## 阶段二：LLM 抽象层 - pi-ai（3-4 小时）

**目标**：理解如何统一多提供商 LLM API

### 2.1 类型系统（1 小时）
- [ ] 精读 `src/types.ts` - Model、Context、Message 的定义
- [ ] 理解 `KnownApi` 和 `KnownProvider` 的设计
- [ ] 研究流式事件的类型定义（AssistantMessageEvent）

### 2.2 提供商实现（1.5 小时）
- [ ] 选 2 个提供商对比阅读：
  - OpenAI (`src/providers/openai.ts`)
  - Anthropic (`src/providers/anthropic.ts`)
- [ ] 对比它们如何转换消息格式
- [ ] 对比流式响应的解析逻辑

### 2.3 跨提供商切换（0.5 小时）
- [ ] 阅读 cross-provider handoff 相关代码
- [ ] 理解 thinking block 如何转换为 `<thinking>` 标签

### 2.4 实践（1 小时）
- [ ] 写一个测试脚本调用 2 个不同提供商
- [ ] 实现一个简单的自定义 Model

### 产出物
- 画出流式事件的状态机图
- 实现一个 mock provider 用于测试

---

## 阶段三：Agent 运行时 - pi-agent-core（4-5 小时）

**目标**：理解事件驱动的 Agent 架构

### 3.1 核心概念（1 小时）
- [ ] 阅读 `src/types.ts` - AgentEvent、AgentState、AgentTool
- [ ] 理解 AgentMessage vs LLM Message 的分离设计
- [ ] 研究 Agent 状态机

### 3.2 事件循环（2 小时）
- [ ] 精读 `src/agent-loop.ts` - 这是整个 Agent 的核心
- [ ] 画出事件序列图（prompt → turn → message → tool → continue）
- [ ] 理解 steering 和 follow-up 机制

### 3.3 Agent 类封装（1 小时）
- [ ] 阅读 `src/agent.ts` - Agent 类的实现
- [ ] 理解订阅模式（subscribe/unsubscribe）
- [ ] 研究工具执行的错误处理

### 3.4 实践（1 小时）
- [ ] 基于 Agent 类实现一个简单的工具（如计算器）
- [ ] 实现 steering 功能（运行时打断 Agent）

### 产出物
- 画出完整的 Agent 事件流图
- 实现一个带工具调用的 mini-agent

---

## 阶段四：终端 UI - pi-tui（3-4 小时）

**目标**：理解差异渲染和终端交互设计

### 4.1 核心概念（1 小时）
- [ ] 阅读 `src/tui.ts` - TUI 主类
- [ ] 理解 Component 接口设计
- [ ] 研究差异渲染的三种策略

### 4.2 组件系统（1.5 小时）
- [ ] 阅读 3 个核心组件：
  - Editor（多行输入）
  - Markdown（富文本渲染）
  - SelectList（交互选择）
- [ ] 理解 Focusable 接口和 IME 支持

### 4.3 输入处理（0.5 小时）
- [ ] 研究 `matchesKey` 和 Key 检测机制
- [ ] 理解 bracketed paste 模式

### 4.4 实践（1 小时）
- [ ] 基于 pi-tui 实现一个简单的交互式 CLI
- [ ] 实现一个自定义组件

### 产出物
- 实现一个带语法高亮的代码查看器组件

---

## 阶段五：编码 Agent - pi-coding-agent（3-4 小时）

**目标**：理解如何将核心组件组装成完整产品

### 5.1 架构阅读（1.5 小时）
- [ ] 阅读 `src/cli/` - 命令行入口
- [ ] 理解 model-resolver.ts - 模型选择逻辑
- [ ] 研究工具定义（file-tools、shell-tools 等）

### 5.2 对话管理（1 小时）
- [ ] 理解对话历史持久化
- [ ] 研究 context compaction 策略

### 5.3 扩展机制（0.5 小时）
- [ ] 阅读 extensions/ 示例
- [ ] 理解如何添加自定义提供商

### 5.4 实践（1 小时）
- [ ] 添加一个自定义工具到 pi-coding-agent
- [ ] 或实现一个简单的自定义扩展

### 产出物
- 为编码 Agent 添加一个新工具

---

## 阶段六：高级主题（选做，4-6 小时）

### 6.1 Web UI - pi-web-ui（2 小时）
- [ ] 理解 React/Vue 组件设计
- [ ] 对比 Web UI 和 TUI 的架构差异

### 6.2 GPU Pod 管理 - pi-pods（2 小时）
- [ ] 研究 vLLM 部署逻辑
- [ ] 理解 Pod 生命周期管理

### 6.3 测试策略（2 小时）
- [ ] 阅读 `test/` 目录
- [ ] 理解跨提供商测试的设计
- [ ] 学习如何用 VirtualTerminal 测试 TUI

---

## 总结与输出（2 小时）

### 综合产出物
1. **架构图** - 完整的 pimono 架构图
2. **对比文档** - Pimono vs OpenClaw 设计对比
3. **改进建议** - 可以借鉴到 OpenClaw 的 3-5 个设计点
4. **示例项目** - 基于 pimono 构建的 mini-agent

### 学习笔记模板
```markdown
## Day X - 主题

### 学到了什么
...

### 设计亮点
1. ...
2. ...

### 与 OpenClaw 的对比
...

### 疑问
...
```

---

## 时间规划

| 阶段 | 时间 | 优先级 |
|------|------|--------|
| 阶段一 | 1-2h | ⭐⭐⭐ |
| 阶段二 | 3-4h | ⭐⭐⭐⭐⭐ |
| 阶段三 | 4-5h | ⭐⭐⭐⭐⭐ |
| 阶段四 | 3-4h | ⭐⭐⭐⭐ |
| 阶段五 | 3-4h | ⭐⭐⭐⭐ |
| 阶段六 | 4-6h | ⭐⭐ |
| 总结 | 2h | ⭐⭐⭐ |

**总计：约 20-27 小时**

建议每天 2 小时，两周完成核心内容。
