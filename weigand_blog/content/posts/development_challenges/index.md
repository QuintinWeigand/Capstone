---
Title: Challenges and Solutions During Development
Date: 2025-12-14
draft: "false"
---

---
# Table of Contents
1. [Overview](#overview)
2. [Technical Challenges](#technical_challenges)
3. [Architecture Challenges](#architecture_challenges)
4. [Integration Challenges](#integration_challenges)
5. [Performance Challenges](#performance_challenges)
6. [Development Workflow Challenges](#development_workflow_challenges)
7. [Conclusion](#conclusion)

---
## Overview

Developing a distributed AI system with multiple components presented various challenges throughout the capstone project. This post documents the key obstacles encountered and the solutions implemented to overcome them, providing insights into the development process and problem-solving approaches.

---
## Technical Challenges

### Challenge 1: MongoDB Integration in Go

**Problem:**
The MongoDB integration boilerplate in Go was significantly more complex than in Python. While Python allows for simple database declaration and immediate use, Go requires more verbose setup with connection management, context handling, and explicit error checking throughout the codebase.

**Solution:**
Implemented a dedicated MongoDB wrapper (`mongo_wrapper.go`) to centralize connection management and provide a cleaner interface for database operations.

**Lessons Learned:**
Go's explicit error handling and type safety, while more verbose, provides better reliability and catch potential issues at compile time rather than runtime.

### Challenge 2: LLM Response Format Inconsistency

**Problem:**
The LLM frequently returned responses in formats or with markdown that weren't requested, causing JSON parsing failures and tool call errors. This was particularly problematic when the model wrapped valid JSON in markdown code blocks or added explanatory text.

**Solution:**
Extensive system prompt engineering to enforce strict response formatting. Added regex-based cleaning to strip unwanted markdown and implemented robust JSON parsing with fallback mechanisms. The migration to Llama 3.1 8B also significantly improved response consistency.

**Lessons Learned:**
Smaller models like Gemma 2B struggle with consistent output formatting, and prompt engineering alone isn't always sufficient - model capability plays a crucial role in reliability.

### Challenge 3: Audio Format Compatibility

**Problem:**
The audio format recorded by the browser (WebM with Opus codec) wasn't immediately compatible with the server-side processing expectations, requiring format conversion or adjustment of the processing pipeline.

**Solution:**
Quick fix by adjusting the server-side audio handling to properly process WebM format and ensuring Whisper model could handle the input format correctly.

**Lessons Learned:**
Browser audio recording formats need to be considered early in development, and compatibility between client-side recording and server-side processing is crucial for smooth voice functionality.

### Challenge 4: Whisper Model Loading Strategy

**Problem:**
The current lazy loading approach for the Whisper model works well for single-user development, but could become a bottleneck with multiple users sending voice prompts simultaneously, as each request might trigger model loading.

**Solution:**
Implemented lazy loading with a global model instance to ensure only one model load per application lifecycle. This works for current usage but would need reconsideration for multi-user scenarios.

**Lessons Learned:**
Model loading strategies need to scale with expected user load. Lazy loading is good for development but pre-loading or model pooling might be necessary for production environments with concurrent users.

---
## Architecture Challenges

### Challenge 1: Technology Stack Selection

**Problem:**
Choosing appropriate technologies for different components while balancing development speed, learning opportunities, and project requirements.

**Solution:**
Selected Python for the web REST API framework due to its prototyping nature - easy to get a working model up quickly. Chose Go for the MCP server because it's well-suited for APIs and provided an opportunity to learn the language basics while building a production-ready component.

**Lessons Learned:**
Technology choices should consider both immediate development needs and long-term learning goals. Python excelled for rapid prototyping, while Go provided robust API development capabilities.

### Challenge 2: Tool Response Architecture

**Problem:**
The current architecture returns raw tool output as templates rather than processing responses through the LLM for more natural language responses. This was a deliberate scope limitation but creates less conversational user experience.

**Solution:**
Accepted the limitation due to project scope constraints and prioritized other development areas. The current approach returns tool results directly to users without LLM reprocessing.

**Lessons Learned:**
Project scope management sometimes requires accepting architectural compromises. Future development should consider feeding tool results back into the LLM for more natural responses, though this adds complexity to the request/response cycle.

---
## Integration Challenges

### Challenge 1: Service Failure Isolation

**Problem:**
Ensuring that failure in one service doesn't bring down the entire system, while maintaining functionality for services that remain operational.

**Solution:**
Implemented graceful error handling where service failures return user-visible error messages without crashing the entire stack. When a specific service is down, only capabilities that depend on that service are affected. For example, when database is unavailable, weather tool continues working normally.

**Lessons Learned:**
Service isolation is crucial for system reliability. Proper error boundaries prevent cascading failures and maintain partial functionality during outages. However, some services are more critical than others - if the LLM service goes down, practically all functionality would be affected.

### Challenge 2: Type System Integration Between Python and Go

**Problem:**
Python's dynamic nature allows for flexible dictionary structures, while Go's static typing requires strict JSON schema definitions. This created challenges ensuring JSON generated by Python prompts could be properly deserialized in Go.

**Solution:**
Established strong, well-defined JSON schemas for all tool calls. Created explicit Go structs that match expected JSON structure, ensuring consistent serialization/deserialization between the dynamically-typed Python frontend and statically-typed Go backend.

**Lessons Learned:**
Cross-language integration requires careful attention to type system differences. Static typing in Go provides better error detection but requires more upfront design compared to Python's flexibility.

---
## Performance Challenges

### Challenge 1: Concurrent Request Handling

**Problem:**
The system was never tested with concurrent requests, which could reveal performance bottlenecks, particularly with the lazy loading approach for the Whisper model.

**Solution:**
Current implementation works well for single-user development, but concurrent request handling remains untested. The lazy loading of Whisper model would likely become a bottleneck under load.

**Lessons Learned:**
Development testing should include concurrent scenarios to identify potential bottlenecks before production deployment. Lazy loading strategies need reconsideration for multi-user environments.

### Challenge 2: Scalability Planning

**Problem:**
While current performance is acceptable on development hardware, resource usage patterns and performance characteristics under load are unknown.

**Solution:**
Accepted current performance as sufficient for capstone project scope, but identified scalability as a future consideration requiring more detailed analysis and testing.

**Lessons Learned:**
Performance testing should extend beyond single-user scenarios. Understanding resource usage patterns is crucial for planning system scaling and capacity requirements.

---
## Development Workflow Challenges

### Challenge 1: Debugging Distributed System with Abstractions

**Problem:**
Testing individual sections of the architecture was difficult due to the abstractions built throughout the system. The MCP server wasn't designed for direct user access, making traditional debugging approaches challenging.

**Solution:**
Implemented simple testing approach using curl commands to verify proper responses and ensure they matched formats that Python could handle. This allowed isolated testing of MCP server functionality without needing the full stack.

**Lessons Learned:**
When building distributed systems with abstractions, create simple testing mechanisms that can validate individual components independently. Direct API testing with tools like curl provides effective debugging for service isolation.

### Challenge 2: Cross-Language Dependency Management

**Problem:**
Managing dependencies across different programming languages with varying package management approaches.

**Solution:**
Used uv for Python dependency management, which simplified the Python side significantly. Go requires explicit dependency handling in go.mod files, which is more structured but less flexible than Python's approach.

**Lessons Learned:**
Different ecosystems have different philosophies for dependency management. Python's uv provides modern, efficient package management, while Go's explicit approach ensures reproducibility but requires more manual configuration.

---
## Conclusion

The development process for this distributed AI system presented various challenges across technical, architectural, integration, performance, and workflow domains. Each challenge provided valuable learning opportunities and helped shape the final system architecture.

The key takeaway is that building distributed systems requires careful consideration of how different components interact, fail gracefully, and maintain performance under various conditions. While some challenges were resolved through technical solutions, others were managed through strategic decisions about project scope and priorities.

This experience demonstrates the importance of balancing ideal solutions with practical constraints, particularly in academic project settings where time and resources are limited.