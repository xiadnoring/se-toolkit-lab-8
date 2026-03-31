# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question 1: "What is the agentic loop?"**

Response:
```
The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks. It typically consists of these core stages:

1. Perceive
   The agent gathers information about its environment or current state. This includes:
   - Reading user input
   - Observing tool outputs
   - Checking memory/context
   - Monitoring external data sources

2. Reason/Plan
   The agent processes the information and decides what to do:
   - Analyze the current situation
   - Break down complex goals into steps
   - Select appropriate tools or actions
   - Consider constraints and preferences

3. Act
   The agent executes its decision:
   - Call tools (search, file operations, API calls, etc.)
   - Send messages
   - Modify state or environment
   - Request clarification if needed

4. Reflect/Learn
   The agent evaluates the outcome:
   - Did the action succeed?
   - What new information was gained?
   - Should the plan be adjusted?
   - Update memory with important facts

Then Repeat →

This loop continues until the goal is achieved or the agent determines it cannot proceed.

In my case (nanobot), the loop looks like:
1. Perceive: Read your message and context (time, workspace, memory)
2. Reason: Determine what tools or actions are needed
3. Act: Execute tool calls (read files, search web, run commands, etc.)
4. Reflect: Process results, update memory if needed, respond to you

This architecture enables agents to handle complex, multi-step tasks autonomously rather than just responding to single-turn queries.
```

**Question 2: "What labs are available in our LMS?"**

Response (without MCP - agent inspects local files):
```
Based on my exploration of the workspace, here are the available labs in this LMS (Learning Management System) project:

Lab 8 — The Agent is the Interface

This is the current lab you're working on. It focuses on building an AI agent (nanobot) as a natural-language interface to the LMS.

Required Tasks:
1. Task 1 — Set Up the Agent (install nanobot, configure Qwen API, add MCP tools, write skill prompt)
2. Task 2 — Deploy and Connect a Web Client (Dockerize nanobot, add WebSocket channel + Flutter chat UI)
3. Task 3 — Give the Agent New Eyes (explore observability data, write log/trace MCP tools)
4. Task 4 — Diagnose a Failure and Make the Agent Proactive (investigate a failure, schedule health checks, fix a planted bug)

Optional Tasks:
1. Task 1 — Add a Telegram Bot Client (same agent, different interface)

The LMS system itself includes:
- Backend: FastAPI application with endpoints for items, interactions, and learners
- Database: PostgreSQL with seeded data
- Frontend: React dashboard and Flutter web chat UI
- Observability: OpenTelemetry Collector, VictoriaLogs, and VictoriaTraces
```

Note: Without MCP, the agent inspects local repo files but cannot query live LMS backend data.

## Task 1B — Agent with LMS tools

**Question 1: "What labs are available?"**

Response (with MCP - real backend data):
```
Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08
```

**Question 2: "Which lab has the lowest pass rate?"**

Response (agent chains multiple MCP tool calls):
```
Based on the completion rates for all labs:

| Lab    | Completion Rate | Passed | Total |
|--------|-----------------|--------|-------|
| Lab 01 | 100.0%          | 258    | 258   |
| Lab 02 | 89.1%           | 131    | 147   |
| Lab 03 | 89.1%           | 156    | 175   |
| Lab 04 | 97.2%           | 239    | 246   |
| Lab 05 | 98.8%           | 247    | 250   |
| Lab 06 | 98.4%           | 242    | 246   |
| Lab 07 | 99.6%           | 238    | 239   |
| Lab 08 | 0.0%            | 0      | 0     |

Lab 02 and Lab 03 are tied for the lowest pass rate among labs with submissions, both at 89.1%.

Note: Lab 08 shows 0.0% completion rate, but this is because it has no submissions yet (0 total), so it's not a meaningful comparison.
```

## Task 1C — Skill prompt

**Question: "Show me the scores" (without specifying a lab)**

Response (with LMS skill prompt - agent asks for lab selection):
```
Which lab would you like to see scores for? Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Please let me know which lab you're interested in, or I can show you scores for all of them.
```

The skill prompt teaches the agent to:
- Call `lms_labs` first when no lab is specified
- Present available labs with clear labels
- Ask the user to choose before proceeding

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
