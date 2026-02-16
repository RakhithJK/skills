# GLM Autoroute

Binary model routing for ZAI GLM models - lightweight vs heavyweight tasks.

# Introduction
1. **GLM-4.7-FlashX** is the default model. Only spawn **GLM-5** when the task actually needs it.
2. Use sessions_spawn to run tasks with GLM-5:
```
sessions_spawn({
  task: "<the full task description>",
  model: "zai/glm-5",
  label: "<short task label>"
})
```
3. After done with GLM-5, the main session continues with FlashX as default.

# Models

## GLM-4.7-FlashX (DEFAULT - zai/glm-4.7-flashx)

Use for lightweight tasks:
1. Simple Q&A - What, When, Who, Where
2. Casual chat - No reasoning needed
3. Quick lookups
4. File lookups
5. Simple tasks - repetitive tasks, formatting
6. Cron Jobs - if it needs reasoning, THEN ESCALATE TO GLM-5
7. Status checks
8. Basic confirmations
9. Provide concise output, just plain answer, no explaining

**DO NOT:**
- ❌ DO NOT CODE WITH FLASHX
- ❌ DO NOT ANALYZE USING FLASHX
- ❌ DO NOT ATTEMPT ANY REASONING USING FLASHX
- ❌ DO NOT RESEARCH USING FLASHX
- If you think the request does not fall into point 1-8, THEN ESCALATE TO GLM-5
- If you think you will violate the DO NOT list, THEN ESCALATE TO GLM-5

## GLM-5 (zai/glm-5)

Use for heavyweight tasks:
1. Coding (any complexity)
2. Analysis & debugging
3. Multi-step reasoning
4. Research & investigation
5. Critical planning
6. Architecture decisions
7. Complex problem solving
8. Deep research
9. Critical decisions
10. Detailed explanations

# Examples

| Task | Model | Why |
|------|-------|-----|
| "Check calendar" | FlashX | Simple lookup |
| "What time is it?" | FlashX | Simple Q&A |
| "Heartbeat check" | FlashX | Routine |
| "Read this file" | FlashX | Simple lookup |
| "Summarize this" | FlashX | Basic task |
| "Write Python script" | GLM-5 | Coding |
| "Debug this error" | GLM-5 | Analysis |
| "Research market trends" | GLM-5 | Deep research |
| "Plan migration" | GLM-5 | Complex planning |
| "Analyze this issue" | GLM-5 | Analysis |

# Other Notes

1. When the user asks to use a specific model, use it
2. Always mention which model is used in outputs
3. After done with GLM-5 (via sessions_spawn), continue with FlashX as default
4. If you think the request does not fall into FlashX use cases, THEN ESCALATE TO GLM-5
5. If you think you will violate the DO NOT list, THEN ESCALATE TO GLM-5
6. Coding = always GLM-5
7. When in doubt → GLM-5 (better safe than sorry)
8. Heartbeat checks → always FlashX unless complex analysis needed
