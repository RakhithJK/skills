const fs = require('fs');
const path = require('path');
const https = require('https');
require('dotenv').config({ path: path.resolve(__dirname, '../../.env') });

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const HISTORY_FILE_HEAD = 'temp_history_head.md';
const HISTORY_FILE_TAIL = 'temp_history_tail.md';

async function summarize() {
    let content = '';
    try {
        content += fs.readFileSync(HISTORY_FILE_HEAD, 'utf8');
        content += "\n...[Middle Skipped]...\n";
        content += fs.readFileSync(HISTORY_FILE_TAIL, 'utf8');
    } catch(e) { return "No content"; }

    const prompt = `
    Role: Senior Technical Analyst
    Task: Summarize the "Evolution History" log of an AI Agent (Mad Dog Evolver).
    Language: Chinese (中文)
    Format: Markdown
    
    Source Log (Snippet):
    ${content.substring(0, 30000)} 
    
    Requirements:
    1. **Key Milestones**: What major capabilities were added? (e.g., Feishu Card, Git Sync, ClawHub).
    2. **Stats**: Estimated number of cycles (Look at the Cycle # IDs).
    3. **Strategy Shifts**: Did it change from "Stability" to "Mutation"? 
    4. **Conclusion**: Current state of the system.
    `;

    try {
        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
        });
        const data = await res.json();
        return data.candidates?.[0]?.content?.parts?.[0]?.text || "Summary failed.";
    } catch (e) {
        return `Error: ${e.message}`;
    }
}

(async () => {
    console.log("Summarizing...");
    const summary = await summarize();
    
    // Write to memory
    fs.writeFileSync('memory/evolution_summary.md', summary);
    console.log("Done.");
})();
