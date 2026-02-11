# Grok Imagine Video Skill

Generate, animate, and edit videos using xAI's Grok Imagine API.

## Installation

1. Get your API key from https://console.x.ai/
2. Add to environment:
   ```bash
   export XAI_API_KEY="your-key-here"
   ```
3. Copy `grok-imagine-video.skill` to your OpenClaw skills directory:
   ```bash
   mkdir -p ~/.openclaw/skills
   cp grok-imagine-video.skill ~/.openclaw/skills/
   cd ~/.openclaw/skills/
   unzip grok-imagine-video.skill
   ```
4. Restart OpenClaw gateway if running:
   ```bash
   openclaw gateway restart
   ```

## Configuration

**API Key:**
- Get your own key from https://console.x.ai/
- Never share your API key
- Set via environment variable: `export XAI_API_KEY="your-key"`

**Environment Options:**
```bash
# Railway/VPS deployment
railway variables set XAI_API_KEY="your-key"

# Local development
echo 'export XAI_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc

# Workspace-specific
echo 'XAI_API_KEY="your-key"' >> .env
```

## Usage

Say to your OpenClaw bot in chat (Discord, Telegram, WhatsApp):

**Text-to-video:**
- "Generate a video of a sunset over the ocean"
- "Make a 10-second video of a cat playing with yarn"

**Image-to-video:**
- "Animate this image - make the clouds move"
- "Bring this photo to life with gentle motion"

**Video editing:**
- "Edit this video - add a warm sunset filter"
- "Modify this clip to slow motion by 50%"

## Troubleshooting

**API key not found:**
```
Error: XAI_API_KEY environment variable not set
```
Run: `export XAI_API_KEY="your-key-from-console.x.ai"`

**Rate limit exceeded:**
Wait 1-2 minutes and try again.

**Request timeout:**
Try reducing duration or complexity:
```bash
# Try shorter video
"Generate a 5-second video of [simpler prompt]"
```

## Requirements

- OpenClaw framework installed
- Python 3.8+
- xAI API key from https://console.x.ai/

## Support

For issues or questions, check:
- xAI Docs: https://docs.x.ai/developers/model-capabilities/video/generation
- OpenClaw Docs: https://docs.openclaw.ai

---

**Note:** This skill uses YOUR API key, not the developer's. Each user must configure their own credentials.
