# Changelog

All notable changes to the Grok Imagine Video skill will be documented in this file.

## [1.0.1] - 2026-02-11

### Fixed
- `edit_video()` in `grok_video_api.py` referenced undefined variable `prompt` instead of the `edit_prompt` parameter, causing a `NameError` when editing videos
- `SKILL.md` documented `download_video()` with a raw URL string argument instead of the expected response dict

## [1.0.0] - 2026-02-11

### Added
- Initial release of Grok Imagine Video skill
- Text-to-video generation via xAI Grok Imagine API
- Image-to-video animation with configurable motion strength
- Video editing via natural language instructions
- Async job polling with progress callbacks
- Video download utility
- Full API reference documentation
