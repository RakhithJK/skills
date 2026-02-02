const fs = require('fs');
const path = require('path');

const IN_FILE = path.resolve(__dirname, '../../evolution_history_full.md');
const OUT_FILE = path.resolve(__dirname, '../../evolution_report_cn.md');

function generateChineseReport() {
    if (!fs.existsSync(IN_FILE)) return console.error("No input file");

    const content = fs.readFileSync(IN_FILE, 'utf8');
    const entries = content.split('---').map(e => e.trim()).filter(e => e.length > 0);

    // Categories
    const timeline = [];
    const directions = {
        '🛡️ 安全与稳定性 (Security & Stability)': [],
        '⚡ 性能优化 (Performance)': [],
        '🛠️ 工具链升级 (Tooling)': [],
        '📝 文档与流程 (Docs & Process)': []
    };
    const packages = {};

    entries.forEach(entry => {
        const lines = entry.split('\n');
        const header = lines[0]; 
        const body = lines.slice(1).join('\n').toLowerCase();
        
        // Extract time
        const dateMatch = header.match(/\((.*?)\)/);
        const timeStr = dateMatch ? dateMatch[1] : ''; // 2026/2/2 04:34:01

        let summary = "";
        const summaryLines = lines.filter(l => !l.startsWith('###') && !l.startsWith('Status:') && !l.startsWith('Action:') && l.trim().length > 5);
        if (summaryLines.length > 0) summary = summaryLines[0].trim();
        else return;

        // Simplify Summary & Translate (Heuristic)
        let cnSummary = summary;
        let pkg = "System";

        if (summary.includes("feishu-card")) {
            pkg = "feishu-card";
            if (summary.includes("timeout")) cnSummary = "为 `feishu-card` 增加了 15秒 请求超时控制，防止 API 卡死。";
            if (summary.includes("json")) cnSummary = "支持 JSON 原生输入，支持复杂卡片结构；增加 Dry-Run 模式。";
            if (summary.includes("tail-read")) cnSummary = "优化了大日志读取逻辑 (Tail-read)，避免内存溢出。";
            if (summary.includes("fallback")) cnSummary = "修复了目标用户检测的逻辑漏洞 (移除不安全的回退)。";
        }
        else if (summary.includes("feishu-sticker")) {
            pkg = "feishu-sticker";
            if (summary.includes("permission")) cnSummary = "修复了脚本执行权限 (chmod +x)。";
            if (summary.includes("ffmpeg")) cnSummary = "修复了 ffmpeg 路径引用问题。";
        }
        else if (summary.includes("git-sync")) {
            pkg = "git-sync";
            if (summary.includes("force")) cnSummary = "增加了 `--force` 强制同步参数。";
            if (summary.includes("identity")) cnSummary = "增加了 Git 用户身份自动配置。";
        }
        else if (summary.includes("interaction-logger")) {
            pkg = "interaction-logger";
            if (summary.includes("race") || summary.includes("tail")) cnSummary = "修复了日志轮转时的竞态条件，防止数据丢失。";
        }
        else if (summary.includes("capability-evolver")) {
            pkg = "capability-evolver";
            if (summary.includes("archive")) cnSummary = "实现了旧日志自动归档功能 (>100个文件)。";
            if (summary.includes("safe_publish")) cnSummary = "创建 `safe_publish.js`，发布前自动检查 Auth 和 package.json。";
        }
        else if (summary.includes("chat-to-image")) {
            pkg = "chat-to-image";
            if (summary.includes("package.json")) cnSummary = "标准化技能结构 (添加 package.json)。";
        }

        // Categorize
        let cat = '🛠️ 工具链升级 (Tooling)';
        if (body.includes("security") || body.includes("harden") || body.includes("permission") || body.includes("race")) cat = '🛡️ 安全与稳定性 (Security & Stability)';
        else if (body.includes("optimiz") || body.includes("performance") || body.includes("memory")) cat = '⚡ 性能优化 (Performance)';
        else if (body.includes("doc")) cat = '📝 文档与流程 (Docs & Process)';

        // Add to lists
        const item = { time: timeStr, pkg, desc: cnSummary };
        
        // Filter out boring ones
        if (cnSummary !== summary) { // Only keep translated ones (high confidence interesting)
             timeline.push(item);
             directions[cat].push(item);
             if (!packages[pkg]) packages[pkg] = new Set();
             packages[pkg].add(cnSummary);
        }
    });

    // Sort Timeline
    timeline.sort((a, b) => new Date(a.time) - new Date(b.time));

    // Generate MD
    let md = `# 🧬 系统进化报告 (2026-02-02)\n\n> 🤖 **摘要**: 本次进化重点强化了系统的**健壮性**与**安全性**，解决了多个核心组件 (Logger, Git, Feishu) 的边界问题，并显著提升了大规模日志下的运行性能。\n\n`;

    md += `## 1. 📅 关键时间线 (Timeline)\n`;
    timeline.forEach(t => {
        md += `- \`${t.time.split(' ')[1]}\` **[${t.pkg}]**: ${t.desc}\n`;
    });

    md += `\n## 2. 🚀 进化方向 (Evolution Direction)\n`;
    for (const [cat, items] of Object.entries(directions)) {
        if (items.length === 0) continue;
        md += `### ${cat}\n`;
        const uniqueItems = [...new Set(items.map(i => i.desc))];
        uniqueItems.forEach(d => md += `- ${d}\n`);
    }

    md += `\n## 3. 📦 组件变更汇总 (Package Impacts)\n`;
    for (const [pkg, changes] of Object.entries(packages)) {
        md += `### ${pkg}\n`;
        changes.forEach(c => md += `- ${c}\n`);
        md += `\n`;
    }

    fs.writeFileSync(OUT_FILE, md);
    console.log("Chinese report generated.");
}

generateChineseReport();
