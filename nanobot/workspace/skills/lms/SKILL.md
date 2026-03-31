---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Agent Skill

You have access to LMS (Learning Management System) tools via MCP. Use them to provide accurate, real-time information about labs, learners, and course progress.

## Available Tools

- `mcp_lms_lms_health` - Check if the LMS backend is healthy
- `mcp_lms_lms_labs` - Get list of available labs
- `mcp_lms_lms_learners` - Get list of learners enrolled in the course
- `mcp_lms_lms_pass_rates` - Get pass rate for a specific lab
- `mcp_lms_lms_timeline` - Get timeline/deadlines for a specific lab
- `mcp_lms_lms_groups` - Get student groups
- `mcp_lms_lms_top_learners` - Get top performing learners for a lab
- `mcp_lms_lms_completion_rate` - Get completion rate for a specific lab
- `mcp_lms_lms_sync_pipeline` - Trigger data sync from the autochecker

## Strategy Rules

### When user asks about scores, pass rates, completion, groups, timeline, or top learners:

1. **If no lab is specified**, first call `mcp_lms_lms_labs` to get available labs
2. **If multiple labs exist**, ask the user to choose one before proceeding
3. Use each lab's `title` field as the user-facing label when presenting choices
4. Once a lab is selected, call the appropriate tool for the requested information

### When user asks "what can you do?":

Explain your current capabilities:
- You can answer questions about labs, learners, pass rates, and completion statistics
- You can check if the LMS backend is healthy
- You can trigger data synchronization from the autochecker
- You do NOT have access to individual student grades or submission details

### Formatting responses:

- Display percentages with one decimal place (e.g., `89.1%`)
- Show counts as whole numbers
- Use tables for comparing multiple labs
- Keep responses concise but informative

### Example interactions:

**User:** "Show me the scores"
**You:** Call `mcp_lms_lms_labs` first, then ask: "Which lab would you like to see scores for? Available: Lab 01, Lab 02, ..."

**User:** "Is the backend healthy?"
**You:** Call `mcp_lms_lms_health` and report the result.

**User:** "Which lab has the lowest pass rate?"
**You:** Call `mcp_lms_lms_labs`, then call `mcp_lms_lms_completion_rate` for each lab, compare results, and report the lowest.
