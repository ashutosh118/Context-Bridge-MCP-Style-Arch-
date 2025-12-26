# MCP POC: Modular Context Protocol Demo

## What is this app?
This project demonstrates a local, modular, agentic AI workflow inspired by the Model Context Protocol (MCP) vision. The agentic nature of this app is reflected in its ability to automate workflows and make decisions autonomously. Specifically:

- **Agentic Automation:** APP_TWO acts as an agent by autonomously fetching resources from APP_ONE, processing them locally (e.g., indexing content, querying the LLM), and sending results back to APP_ONE. This demonstrates agent-driven automation in a modular setup.

- **Decision-Making:** APP_TWO dynamically processes content and generates responses based on user queries, showcasing its ability to act independently within the defined workflow.

To further enhance agentic behavior, future iterations could include:
1. **Task Scheduling:** Enabling APP_TWO to periodically fetch and process new files without user intervention.
2. **Multi-Agent Collaboration:** Introducing specialized agents for tasks like indexing, querying, or summarization.
3. **Dynamic Workflow Adaptation:** Allowing APP_TWO to adapt its workflow based on file types or query complexity.

## Workflow Overview
1. **APP_ONE (MCP Resource Server):**
   - Lets you upload files (PDF, CSV, DOCX, etc.)
   - Exposes standardized MCP endpoints:
     - `/list_files` (list available files)
     - `/get_file_content` (fetch file content)
     - `/write_summary` (store results/analysis)
   - Any MCP-compliant client can connect and use these resources

2. **APP_TWO (MCP Client/Agent):**
   - Lists files from APP_ONE using `/list_files`
   - Fetches file content via `/get_file_content`
   - Indexes content in a local vector store (FAISS) for semantic search
   - Lets you ask questions; retrieves relevant context and queries a local LLM (Llama 3 via Ollama)
   - Sends answers/results back to APP_ONE via `/write_summary`
   - Can be replaced by any MCP-compliant client or agent

## How is this MCP-based?
This app has been designed to closely align with the core principles of the Model Context Protocol (MCP):

- **Standardized Context & Resource Exchange:** Both apps communicate using well-defined MCP resource endpoints (`/list_files`, `/get_file_content`, `/write_summary`). This ensures seamless interoperability with any other MCP-compliant client or agent.

- **Modular & Pluggable Architecture:** Each app operates independently. APP_ONE serves as a resource server, while APP_TWO acts as a client/agent. Either app can be extended, replaced, or integrated with other MCP-compliant services without breaking the workflow.

- **Interoperability:** The standardized API allows any MCP-compliant client or agent to connect to APP_ONE and utilize its resources. Similarly, APP_TWO can interact with any MCP-compliant resource server.

- **Agentic Automation:** APP_TWO automates workflows by fetching resources from APP_ONE, processing them locally (e.g., indexing content, querying the LLM), and sending results back to APP_ONE. This demonstrates agent-driven automation in a modular setup.

- **Retrieval-Augmented Generation (RAG):** By leveraging FAISS for local embeddings and vector search, the app provides robust, context-aware answers. This ensures that the LLM operates with relevant context, improving accuracy and relevance.

- **User-Centric Enhancements:** Recent updates include features like clearing the vectorstore, improved dropdown behavior, and query-based result mapping. These changes enhance usability while adhering to MCP principles of modularity and context-driven workflows.

This setup exemplifies the MCP vision by enabling open, modular, agentic, and context-driven AI workflows with true interoperability and extensibility.

## MCP API Spec
See `MCP_API_SPEC.md` for full endpoint documentation and usage examples.

This setup demonstrates the core principles of MCP: open, modular, agentic, and context-driven AI workflows, with true interoperability and extensibility.

- **Credits:** Ashutosh Srivastava