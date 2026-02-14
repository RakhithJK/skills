---
name: tiktok-skinny-fat
description: >
  TikTok slideshow (carousel) creation skill for the Skinny Fat AI app.
  Generates viral TikTok photo carousels: hook writing, image generation prompts,
  text overlays, captions, and hashtags. Trigger this skill when the user says
  "create TikTok", "make slideshow", "generate carousel", "create content",
  "make a post", "today's content", "write hooks", "plan TikTok", "batch content",
  "transformation post", "skinny fat content", or any variation of these.
triggers:
  - "create tiktok"
  - "make slideshow"
  - "generate carousel"
  - "create content"
  - "make a post"
  - "today's content"
  - "write hooks"
  - "plan tiktok"
  - "batch content"
  - "transformation post"
  - "skinny fat content"
tools:
  - filesystem
  - shell
---

# TikTok Slideshow Creation Skill — Skinny Fat AI

This skill generates TikTok photo carousel (slideshow) content for the Skinny Fat AI app.
Goal: Produce slideshows with high viral potential that are consistent, readable, and conversion-focused.

---

## 1. GENERAL RULES

### 1.1 Slideshow Format
- Every slideshow has EXACTLY 6 slides. No more, no less.
- All images are PORTRAIT: 1024x1536 pixels. NEVER use landscape.
- Slide 1 MUST have hook text as a text overlay.
- Slide 6 MUST have a CTA (Call to Action).
- Slides 2–5 contain transformation visuals, comparisons, or informational graphics.

### 1.2 Quality Standards
- Every image must look realistic, like a phone photo.
- AVOID the AI-generated look. Always include "iPhone photo", "natural lighting", "realistic" in prompts.
- Do NOT generate faces — use body silhouettes, measurements visuals, food photos, and app UI screenshots.
- Brand colors: dark navy (#1a1a2e), neon green/blue accent (#00d4aa), white text.

---

## 2. VIRAL HOOK FORMULA

This is the most critical section of the entire skill. The hook determines everything.

### 2.1 The Formula That Works (USE THIS)
```
[Another person] + [doubt or conflict] → showed them AI / the result → they changed their mind
```

This works because:
- It tells a story (people tap on stories)
- It creates curiosity (you want to see their reaction)
- It frames the product naturally (someone else validated it)
- It builds emotional connection

### 2.2 Proven Hook Examples
USE THESE AS TEMPLATES and create variations:

**Family/friend reaction formula:**
- "My girlfriend thought I was just skinny until I showed her my AI body analysis"
- "My mom kept saying 'you're already thin' until she saw my results"
- "My friend said I don't need to lose weight, then I showed him this"
- "My brother said the gym was a waste of money until he saw my 48-day results"
- "My roommate said we eat the same but our AI macro analysis was completely different"

**Trainer/expert formula:**
- "My personal trainer said I wasn't skinny fat. Then I showed him my AI analysis"
- "My dietitian said I didn't need to count calories. One week of AI tracking later..."
- "I told a fitness influencer I was skinny fat. Didn't expect that response"

**Self-transformation formula:**
- "Everyone tells me I'm 'already thin' but the truth comes out when the shirt comes off"
- "I'm 170lbs and look skinny in clothes but my body fat is 28%"
- "Same weight, completely different body — here's what 48 days did"

**Food/nutrition surprise formula:**
- "I saw the AI skinny fat score of the breakfast I thought was healthy"
- "I kept saying 'I barely eat' until AI scanned my meals for a week"
- "I thought eating salad meant I was eating well. The macro analysis said otherwise"

**Fear/urgency formula:**
- "Skinny fat is more dangerous than you think — here's the risk level AI gave me"
- "You can look thin and be internally obese. My AI analysis proved it"
- "My BMI is normal but my visceral fat came back in the danger zone"

### 2.3 Hook Formats That FAIL (DO NOT USE)
These consistently underperform. AVOID them:
- Feature-focused: "Track your macros with Skinny Fat AI" → Nobody cares
- Generic fitness: "Transform your body in 48 days" → Too generic, sounds like every ad
- Price-focused: "Get a free body analysis" → Looks like an ad
- Question format: "Are you skinny fat?" → Low engagement
- Vague: "What is your body telling you?" → Not clear enough
- Self-focused: "Our app's best feature" → Nobody cares about your features

### 2.4 Hook Writing Rules
- Maximum 15 words. Short and punchy.
- MUST include an "another person" or "surprise reaction" element.
- Hook should NOT end with a question. It should be a curiosity-driven statement.
- Avoid jargon. Words like "recomp", "visceral", "macro" only when in context.
- Write in English for the global audience.

---

## 3. IMAGE GENERATION

### 3.1 Prompt Structure
Every prompt must follow this structure:

```
iPhone photo of [scene description]. [Detailed physical description].
Natural phone camera quality, realistic lighting. Portrait orientation 1024x1536.
[Style/mood/variation for this specific slide]
```

### 3.2 Locked Body Descriptions (For Consistency)
Use the SAME body description across ALL slides in a slideshow. Only change clothing, pose, or environment.

**Male skinny fat template:**
```
Male body silhouette, mid-20s, approximately 175cm tall, 78kg.
Narrow shoulders relative to waist. Soft midsection with visible
belly fat, no visible muscle definition. Arms thin but not toned.
Slight forward head posture. Shot from [angle].
```

**Female skinny fat template:**
```
Female body silhouette, mid-20s, approximately 165cm tall, 62kg.
Slim frame but soft midsection. No visible muscle tone in arms.
Slight lower belly pouch. Narrow shoulders.
Shot from [angle].
```

IMPORTANT: Do NOT include facial details. Use silhouettes, back shots, or neck-down framing.

### 3.3 Food Image Template
```
iPhone photo of [food description] on [plate/table description].
Overhead shot, natural kitchen lighting, slightly messy realistic table.
A phone screen next to the plate showing a nutrition scanning app interface
with calories and macros visible. Portrait orientation 1024x1536.
```

### 3.4 App UI Visuals
Prefer real app screenshots when available. If mock-ups are needed:
```
Clean mobile app screenshot mockup on dark background (#1a1a2e).
Modern fitness app UI showing [feature: body analysis / meal scan / workout plan].
Neon accent color (#00d4aa). Minimal, premium design.
Portrait orientation 1024x1536.
```

### 3.5 Slide-by-Slide Visual Plan

**Format A: Transformation Story (highest performance)**
| Slide | Content | Visual Type |
|-------|---------|-------------|
| 1 | Hook text overlay | Attention-grabbing "before" visual or emotional scene |
| 2 | "Before" state | Skinny fat body silhouette / unhealthy meal |
| 3 | AI analysis result | App UI — body analysis screen |
| 4 | Plan/program | App UI — workout or macro plan |
| 5 | "After" state / progress | Fitter body silhouette / healthy meal |
| 6 | CTA | App logo + "Link in bio" |

**Format B: Food Surprise (high engagement)**
| Slide | Content | Visual Type |
|-------|---------|-------------|
| 1 | Hook text overlay | Unhealthy-looking meal on a table |
| 2 | Food detail | Overhead food photo |
| 3 | AI scan result | App meal scan screen — bad score |
| 4 | Correct alternative | Healthy food photo |
| 5 | AI scan result (good) | App meal scan screen — good score |
| 6 | CTA | Skinny Fat Score explanation + "Link in bio" |

**Format C: Education/Info (medium performance, builds trust)**
| Slide | Content | Visual Type |
|-------|---------|-------------|
| 1 | Hook text overlay | Shocking statistic visual |
| 2 | Problem explanation | Infographic style |
| 3 | Why it happens | Info visual |
| 4 | Solution | App feature visual |
| 5 | Proof/results | Before-after or data |
| 6 | CTA | Download button visual |

---

## 4. TEXT OVERLAY RULES

### 4.1 Technical Specifications
- Font size: AT LEAST 6.5% of slide width. NEVER go below 5%.
- Color: White (#FFFFFF) text with semi-transparent black shadow/background.
- Position: In the TOP 1/3 of the image. NEVER at the very top — TikTok's status bar covers it.
- Safe zone: Leave 15% from top, 20% from bottom (for TikTok UI elements).
- Maximum 20 characters per line. Wrap to next line if longer.
- Maximum 3 lines of text. More than that becomes unreadable.

### 4.2 Text Overlay Usage
- Slide 1: ALWAYS the hook text. Large, bold, readable.
- Slides 2–5: Optional. Only add short descriptive text (2–4 words) if needed.
- Slide 6: CTA text. "Skinny Fat AI — Link in bio" or "Try it free — Link in bio"
- Text must NEVER cover the main subject of the image.

### 4.3 Text Rendering (Canvas/Pillow)
```python
# Core text overlay parameters
FONT_SIZE_RATIO = 0.065  # 6.5% of width
MAX_LINE_CHARS = 20      # Characters per line
TEXT_Y_POSITION = 0.20   # 20% from top
SHADOW_OFFSET = 3
SHADOW_COLOR = (0, 0, 0, 180)
TEXT_COLOR = (255, 255, 255, 255)
BACKGROUND_PADDING = 20
BACKGROUND_COLOR = (0, 0, 0, 120)  # Semi-transparent black
```

IMPORTANT: During canvas rendering, text must NOT be compressed horizontally.
If a line exceeds max_width, wrap to the next line. Never squish.

---

## 5. CAPTION WRITING

### 5.1 Caption Format
The caption must be a MICRO STORY. NOT a feature list.

**Structure:**
```
[1–2 sentence story — expand the hook, add emotion]
[1 sentence mentioning the app naturally]
[CTA — "Link in bio" or "Try it from the link in my profile"]

#skinnyfat #bodyrecomp #[3 more niche hashtags]
```

**Good caption example:**
```
Showed my girlfriend my AI body analysis. She stopped saying
"you're already skinny." My body fat came back at 26%, skinny fat
risk level high. Started the 48-day program. Get your own
analysis with Skinny Fat AI, link in bio.

#skinnyfat #bodyrecomp #bodyanalysis #fitnessmotivation #skinnyfattransformation
```

**Bad caption example (DO NOT USE):**
```
Analyze your body with Skinny Fat AI! Count calories, track macros,
get a 48-day program. Download now!

#fitness #gym #workout #health #app
```

### 5.2 Hashtag Rules
- MAXIMUM 5 hashtags (TikTok's current limit).
- First 2 hashtags ALWAYS: #skinnyfat #bodyrecomp
- Remaining 3 should be topic-specific.
- Niche hashtag pool:
  - #skinnyfattransformation
  - #bodyfatpercentage
  - #mealprep
  - #macrotracking
  - #fitnessjourney
  - #gymtok
  - #workouttok
  - #beforeandafter
  - #bodytransformation
  - #recomp
  - #caloriecounting
  - #fitnesstok
  - #bodycomposition
  - #healthyeating

---

## 6. CONTENT CREATION WORKFLOW

Step-by-step slideshow creation:

### Step 1: Pick a Hook
- Write a hook using the viral formula from Section 2.
- Confirm with user: "Want me to use this hook: [hook]?"
- Proceed only after approval.

### Step 2: Slideshow Plan
- Create a plan for 6 slides (pick a format from Section 3.5).
- For each slide: visual description + text overlay (if any) + prompt draft.
- Show plan to user, get approval.

### Step 3: Lock the Description
- Write the fixed body/food/environment description based on the slideshow theme (Section 3.2–3.3).
- This description stays IDENTICAL across ALL slides. Only the style/state changes.

### Step 4: Write Prompts
- Prepare a separate image generation prompt for each of the 6 slides.
- Copy-paste the locked description. Only update the changing part.
- Portrait (1024x1536) must be specified in every prompt.

### Step 5: Generate Images
- Call the image generation API (whichever model the user prefers).
- Save each image as `slides/[slideshow-id]/slide-[1-6].png`.

### Step 6: Add Text Overlays
- Apply text overlays following Section 4 rules.
- Hook on Slide 1, CTA on Slide 6.
- Save overlay versions as `slides/[slideshow-id]/final-slide-[1-6].png`.

### Step 7: Caption and Hashtags
- Write caption following Section 5 rules.
- Save as `slides/[slideshow-id]/caption.txt`.

### Step 8: Deliver
- Present all 6 final images + caption file to the user.
- User reviews and approves.
- User uploads to TikTok manually (adds trending sound + publishes).

---

## 7. BATCH CONTENT PLANNING

When the user says "plan this week's content" or "make 5 slideshows":

### 7.1 Planning Process
1. Check performance data (from memory file).
2. Suggest 5–10 hooks using different formulas.
3. Work with the user to pick the best 5.
4. Assign a slideshow format (A, B, or C) to each.
5. Prepare all prompts.
6. Generate sequentially or in batch (Batch API if available for 50% cost savings).

### 7.2 Content Variety Rules
- Do NOT use the same format more than 2 times in a row.
- Every week should include at least: 2 transformation stories + 2 food surprises + 1 education/info.
- Do NOT repeat the same hook formula back to back. Alternate.
- Use different "other people": mom, dad, friend, partner, dietitian, personal trainer, roommate, coworker.

---

## 8. MEMORY AND LEARNING SYSTEM

### 8.1 Performance Tracking
After every post, log the following to `memory/tiktok-performance.md`:

```markdown
## [Date] - [Short hook summary]
- Hook: [full hook text]
- Format: [A/B/C]
- Views: [number]
- Likes: [number]
- Shares: [number]
- Comments: [number]
- App downloads (estimated): [number]
- Notes: [what worked, what didn't]
```

### 8.2 Failure Log
For every failed post or technical error, log to `memory/failure-log.md`:

```markdown
## [Date] - ERROR: [short description]
- What happened: [detail]
- Why it happened: [analysis]
- Fix: [what was done]
- Rule: [new rule to prevent this from happening again]
```

### 8.3 Learning Loop
- After every 10 posts, analyze performance data.
- Compare the top 3 and bottom 3 posts.
- Add working patterns to this skill file as rules.
- Add failing patterns to the "DO NOT USE" list.

---

## 9. TECHNICAL NOTES

### 9.1 File Structure
```
skinny-fat-tiktok/
├── slides/
│   ├── [slideshow-id]/
│   │   ├── slide-1.png
│   │   ├── slide-2.png
│   │   ├── ...
│   │   ├── slide-6.png
│   │   ├── final-slide-1.png  (with overlay)
│   │   ├── ...
│   │   ├── final-slide-6.png
│   │   └── caption.txt
├── memory/
│   ├── tiktok-performance.md
│   └── failure-log.md
├── prompts/
│   └── templates.md
└── assets/
    └── fonts/
```

### 9.2 Image Generation API Usage
- Model choice is up to the user (gpt-image-1, DALL-E 3, etc.).
- Always request portrait (1024x1536).
- Always include "iPhone photo", "realistic lighting", "natural" in prompts.
- Do NOT generate faces. Use silhouettes, back shots, or neck-down framing.
- Use Batch API if available (50% cost reduction).

### 9.3 Text Overlay Script
Use Python Pillow for text overlays. Base script:

```python
from PIL import Image, ImageDraw, ImageFont

def add_text_overlay(image_path, text, output_path, position="top"):
    img = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    width, height = img.size
    font_size = int(width * 0.065)

    try:
        font = ImageFont.truetype("assets/fonts/bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Wrap text (max 20 chars per line)
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if len(test_line) <= 20:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Calculate position
    y_start = int(height * 0.20) if position == "top" else int(height * 0.75)

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = y_start + i * (text_height + 15)

        # Background box
        padding = 20
        draw.rectangle(
            [x - padding, y - padding // 2, x + text_width + padding, y + text_height + padding // 2],
            fill=(0, 0, 0, 120)
        )

        # Shadow
        draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0, 180))
        # Main text
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))

    img = Image.alpha_composite(img, overlay)
    img.convert("RGB").save(output_path)
```

---

## 10. CRITICAL CHECKLIST

Before delivering any slideshow, verify ALL of the following:

- [ ] Exactly 6 slides?
- [ ] All images 1024x1536 portrait?
- [ ] Slide 1 has hook text overlay?
- [ ] Hook text is readable? (font size sufficient?)
- [ ] Text overlay within TikTok safe zone? (top 15%, bottom 20% clear)
- [ ] Same base scene/body/environment across all slides? (consistency)
- [ ] No face visuals?
- [ ] Caption is a micro story, NOT a feature list?
- [ ] 5 or fewer hashtags?
- [ ] CTA on Slide 6?
- [ ] Hook follows the viral formula? ([other person] + [conflict] → show → reaction)
- [ ] Text not horizontally compressed?

---

## 11. HARD RULES — NEVER BREAK THESE

NEVER do any of the following:
- Generate landscape (horizontal) images
- Create fewer or more than 6 slides
- Generate images with faces
- Write feature-list captions
- Use more than 5 hashtags
- Use aggressive CTAs like "Download NOW!" or "BUY THIS!"
- Reuse the same hook twice
- Place text overlay at the bottom of the image
- Drop font size below 5%
- Change the body description between slides (breaks consistency)
- Give medical advice (the app provides "estimated" analysis, NOT medical diagnosis)
- Make unrealistic transformation promises

---

## 12. FIRST-TIME SETUP

For users activating this skill for the first time:

1. Create the `skinny-fat-tiktok/` folder structure
2. Initialize `memory/tiktok-performance.md` (blank template)
3. Initialize `memory/failure-log.md` (blank template with starter rules)
4. Ask user for target audience info (age group, primary gender focus)
5. Suggest 3 hooks, get approval
6. Create the first slideshow, deliver to user
7. Update skill file based on feedback