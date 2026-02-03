---
name: whatsapp-automation
description: "WhatsApp automation that stores messages and sends you Telegram notifications: appointment reminders, urgent alerts, smart reply suggestions. One-line setup."
---

# 📱 WhatsApp Automation Skill

Automatically store WhatsApp messages, detect appointments, alert on important messages, and suggest responses for specific contacts.

---

## 🚀 ONE-LINE SETUP

```bash
bash ~/.openclaw/workspace/whatsapp-automation-skill/setup.sh
```

Done. Everything configured automatically. ✅

---

## What It Does

| Feature | What |
|---------|------|
| 📩 **Receive Messages** | WAHA stores all incoming WhatsApp messages |
| 🕐 **Appointment Detection** | Finds "meeting Tuesday 2 PM" → sends Telegram alert |
| ⚠️ **Important Alert** | Detects "URGENT!!!" or "HELP SOS" → sends Telegram alert |
| 💬 **Contact Handler** | Messages from Joséphine → suggests reply → awaits yes/no |
| 💾 **Local Storage** | All messages saved in `~/.openclaw/workspace/.whatsapp-messages/` |

---

## After Setup

### Send a Test Message
Send yourself a WhatsApp message from another device.

### Check Logs
```bash
tail /tmp/whatsapp-store.log
```

Should show:
```
✅ Message stored: 33612345678@c.us - "your message"
```

### Query Messages
```bash
node ~/.openclaw/workspace/whatsapp-query.js list
```

---

## Troubleshooting

**Setup failed?** Run again:
```bash
bash ~/.openclaw/workspace/whatsapp-automation-skill/setup.sh
```

**Messages not arriving?**
```bash
# Check service
ps aux | grep whatsapp-message-store

# Check logs
tail /tmp/whatsapp-store.log

# Check WAHA
docker ps | grep waha
```

**More help?** See `references/TROUBLESHOOTING.md`

---

## Advanced

- Customize keywords → `references/ADVANCED.md`
- API reference → `references/API.md`
- WAHA details → `references/WAHA-CONFIGURATION.md`
- Full troubleshooting → `references/TROUBLESHOOTING.md`

---

## License

**CC BY-ND-NC 4.0** — Non-Commercial, No Modifications

You can use personally and share unmodified.

See `LICENSE.md` for full terms.

---

## Support

- WAHA: https://waha.devlike.pro/
- OpenClaw: https://docs.openclaw.ai/
- Issues? Check `references/TROUBLESHOOTING.md`
