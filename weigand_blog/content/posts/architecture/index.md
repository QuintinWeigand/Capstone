---
Title: Capstone Architecture Discussion
Date: 2025-09-26
draft: "false"
---

---

# Table of Contents
1. [Dependencies](#dependencies)
2. [LangChain](#langchain)
3. [OpenAI Whisper](#openai-whisper)
4. [Ollama](#ollama)
5. [Architecture](#architecture)

---

## Dependencies

The architecture I will be following relies on several key tools and frameworks:
- [LangChain](https://python.langchain.com/docs/introduction/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Ollama](https://github.com/ollama/ollama)

I will go deeper into these in the next few sections.

---

## LangChain

**LangChain** serves as the central orchestrator for our system. It helps determine whether a user’s input requires an action or a response from a language model. Using LangChain, we can build custom actions tailored to our specific needs, allowing the agent to be more dynamic and context-aware.

---

## OpenAI Whisper

Later in the project, I plan to integrate **Whisper**, an open-source speech-to-text library from OpenAI. Whisper will allow users to interact with our system via voice commands, converting speech into text that the LangChain-driven agent can process. This enables a more natural and flexible user interface beyond traditional text input.

---

## Ollama

**Ollama** is an open-source framework that enables us to run large language models locally on our own machines. This gives us more control over the models, reduces reliance on cloud services, and can help improve response times and data privacy.

---

# Architecture

As I begin work on the Capstone project, I want to outline my initial vision for the system architecture. To help visualize this, I’ve created a mockup diagram of our proposed architecture.

![architecture_mockup](architecture_mockup.png)

---

