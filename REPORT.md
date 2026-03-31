# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

🐈 nanobot
The agentic loop is the fundamental cycle that AI agents follow to accomplish tasks autonomously.Perceive                                                                                                                                                               
 2 Reason                                                                                                                                                             
 3 Act                                                                                                                                                               
 4 Observe          
 5 Repeat                                            
This loop enables agents to:                                                               

 • Break complex tasks into smaller steps                                                   
 • Adapt based on feedback and errors                                                       
 • Use tools dynamically as needed                                                         
 • Work toward goals with minimal human intervention                                                    
 ID  Title                                                   
 ─────────
 1   Lab 01       
 2   Lab 02 
 3   Lab 03 
 4   Lab 04         
 5   Lab 05       
 6   Lab 06                  
 7   Lab 07     
 8   lab-08                                                  

There are 8 labs total. Would you like more details about any specific lab, such as pass rates, completion rates, or submission timelines? 

## Task 1B — Agent with LMS tools

Here are the available labs in the LMS:                                                                                                                                                                                                                               
 ID  Title                                                   
 ─────────────────────────────────────────────────────────── 
 1   Lab 01 – Products, Architecture & Roles                 
 2   Lab 02 — Run, Fix, and Deploy a Backend Service         
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy 
 4   Lab 04 — Testing, Front-end, and AI Agents              
 5   Lab 05 — Data Pipeline and Analytics Dashboard          
 6   Lab 06 — Build Your Own Agent                           
 7   Lab 07 — Build a Client with an AI Coding Agent         
 8   lab-08                                                

There are 8 labs total. Would you like more details about any specific lab, such as pass rates, completion rates, or submission timelines?   

System Components               
1. Core Application Stack                                                                                                                                                                             
 Component        Technology                                                                                             
 ───────────────────────────────
 Caddy            Go                 
 FastAPI Backend  Python, SQLModel, Uvicorn                   
 PostgreSQL       PostgreSQL                                 
 pgAdmin          pgAdmin 4    
2. AI Agent Layer                                                                                                             
 Component     Technology                                                                              
 ───────────────────────────
 Nanobot       Python, nanobot-ai 
 Telegram Bot  Python, aiogram   
3. Observability Stack (for monitoring)                                                                                                                                                                                                                            

 • OpenTelemetry Collector — Collects telemetry data                                                                                                                                                                                                               
 • VictoriaLogs — Log storage and querying                                                                                                                                                                                                                         
 • VictoriaTraces — Distributed trace storage                                                                                                                                                                        
Data Model (OBER-based)                                 

This architecture enables the AI agent to act as a natural-language interface to the LMS/

## Task 1C — Skill prompt

🐈 nanobot
Here are the scores (pass rates) for all labs.                                                                                        

The agent asking which lab or listing options?


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
