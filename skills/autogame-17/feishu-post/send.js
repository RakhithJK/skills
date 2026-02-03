const { fetchWithAuth } = require('../common/feishu-client.js');
const fs = require('fs');
const path = require('path');

// --- Upstream Logic Injection (Simplified) ---
// Ported from upstream src/send.ts (m1heng/clawdbot-feishu)
// Adapted for our lightweight architecture

async function sendPost(options) {
    let contentText = options.text || '';
    if (options.textFile) {
        try { contentText = fs.readFileSync(options.textFile, 'utf8'); } catch(e) {}
    }

    if (!contentText && !options.content) {
        throw new Error('No content provided');
    }

    // Determine ID Type
    let receiveIdType = 'open_id';
    if (options.target.startsWith('oc_')) receiveIdType = 'chat_id';
    else if (options.target.startsWith('ou_')) receiveIdType = 'open_id';
    else if (options.target.includes('@')) receiveIdType = 'email';

    // Build Payload (RichText)
    // Upstream Logic: Wrap markdown in Post Object
    const postContent = {
        zh_cn: {
            title: options.title || '',
            content: [
                [{ tag: 'text', text: contentText }] // Simple Text Block for now
            ]
        }
    };

    // TODO: Add proper Markdown parsing logic from our old script if needed
    // or adopt upstream's "runtime.channel.text.convertMarkdownTables" logic eventually.
    
    const messageBody = {
        receive_id: options.target,
        msg_type: 'post',
        content: JSON.stringify(postContent)
    };

    // Support Reply (New Feature from Upstream)
    let url = `https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=${receiveIdType}`;
    if (options.replyTo) {
        url = `https://open.feishu.cn/open-apis/im/v1/messages/${options.replyTo}/reply`;
        delete messageBody.receive_id; // Reply doesn't need receive_id
    }

    console.log(`Sending Post to ${options.target}...`);
    
    try {
        const res = await fetchWithAuth(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(messageBody)
        });
        const data = await res.json();
        
        if (data.code !== 0) throw new Error(`API Error ${data.code}: ${data.msg}`);
        
        console.log(`Success: Message sent (ID: ${data.data.message_id})`);
        return data.data;
    } catch (e) {
        console.error(`Send Failed: ${e.message}`);
        // Fallback Logic from old script can be re-added here if critical
        throw e;
    }
}

// CLI Wrapper
if (require.main === module) {
    const { program } = require('commander');
    program
        .requiredOption('-t, --target <id>', 'Target ID')
        .option('-x, --text <text>', 'Text content')
        .option('-f, --text-file <path>', 'File content')
        .option('--title <text>', 'Title')
        .option('--reply-to <id>', 'Message ID to reply to')
        .parse(process.argv);
    
    sendPost(program.opts()).catch(() => process.exit(1));
}

module.exports = { sendPost };
