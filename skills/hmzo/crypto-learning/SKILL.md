---
name: crypto-learning
description: 加密货币自学系统。每天早上9点自动推送学习内容，每次调用时通过browser搜索最新知识点的具体内容并整合呈现。包含完整学习大纲（小白向、投资向、进阶投资三个阶段），支持进度跟踪和跳过功能。
---

# Crypto Learning - 加密货币自学系统

## 概述

这个 skill 帮助 hmzo 系统学习加密货币知识，包含完整的学习大纲和进度跟踪。

## 学习大纲位置

学习大纲存储在 `content.json` 中，包含三个阶段：
- **小白向**（30天）：基础概念、区块链、钱包、交易所、安全
- **投资向**（60天）：技术分析、基本面、DeFi、风险管理、市场周期
- **进阶投资**（90天）：期权合约、链上数据、宏观经济、税务合规、投资心理学

## 工作流程

当 skill 被调用时，执行以下步骤：

### 1. 读取当前进度

读取 `progress.json` 文件，获取：
- 当前学习阶段（current_stage）
- 当前主题索引（current_topic_index）
- 当前子主题索引（current_subtopic_index）
- 已完成的子主题列表（completed_subtopics）

### 2. 获取今日学习内容

根据进度信息，从 `content.json` 中获取对应的学习内容：
- 阶段名称
- 主题名称
- 子主题标题
- 子主题基础内容（content.json 中的简要说明）

### 3. 使用 browser 搜索最新内容

**关键步骤**：使用 `browser` 工具搜索该知识点的最新、详细内容。

搜索策略：
- 使用 Brave Search 搜索相关的中文和英文资料
- 搜索关键词组合：子主题标题 + "加密货币" + "教程"
- 优先搜索权威来源：币安学院、CoinMarketCap、Investopedia等

示例搜索查询：
```
"什么是加密货币" + "加密货币教程" + "新手入门"
```

### 4. 整合内容并呈现

将以下内容整合后呈现给用户：

**学习卡片格式：**
```
📚 第 X 天学习内容
━━━━━━━━━━━━━━━━━━━━━━
阶段：小白向
主题：什么是加密货币
今日重点：加密货币的定义

📖 基础知识
[从 content.json 读取的基础内容]

🌐 最新资料
[从 browser 搜索到的详细内容，整合多个来源]

💡 学习建议
[根据知识点给出学习建议]

━━━━━━━━━━━━━━━━━━━━━━
明天继续学习：[下一个子主题]
```

### 5. 更新进度

学习完成后，更新 `progress.json`：
- 增加已完成的子主题
- 更新当前索引（移动到下一个子主题）
- 更新最后推送日期
- 增加完成天数

## 用户命令

### 开始学习计划
启动每日推送，从当前进度继续。

### 查看进度
显示当前学习进度：
- 已完成天数
- 当前阶段和主题
- 已完成的知识点列表

### 跳过今天
跳过今天的学习，不更新进度。

### 重置计划
重新开始学习计划，清空所有进度。

### 手动学习某个主题
用户可以指定学习某个特定主题，不更新自动进度。

## 技术细节

### 文件结构

```
crypto-learning/
├── SKILL.md              # 本文件
├── content.json          # 学习大纲（所有知识点）
├── progress.json         # 学习进度跟踪
└── schedule.sh           # 定时推送脚本（可选）
```

### 进度文件格式

```json
{
  "user_id": "hmzo",
  "started_at": "2026-02-11T19:36:38.919015",
  "current_stage": "beginner",
  "current_topic_index": 0,
  "current_subtopic_index": 1,
  "completed_subtopics": ["b1-1"],
  "skipped_dates": [],
  "last_push_date": "2026-02-11",
  "total_days_completed": 1,
  "enabled": true
}
```

### Cron 定时任务

使用 OpenClaw 的 cron 功能设置每天早上 9 点推送：

```bash
cron add --job '{
  "name": "crypto-learning-daily",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Singapore"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "继续加密货币学习"
  },
  "sessionTarget": "main",
  "enabled": true
}'
```

## 注意事项

1. **搜索质量**：使用多个搜索关键词组合，确保获得全面、准确的信息
2. **内容整合**：不要简单复制搜索结果，要理解并重新组织内容
3. **进度管理**：确保每次调用后正确更新进度文件
4. **错误处理**：如果搜索失败，使用 content.json 中的基础内容作为后备
5. **用户友好**：内容要简洁易懂，适合初学者，避免过于技术化
