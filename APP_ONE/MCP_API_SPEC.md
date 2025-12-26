# MCP Resource API Specification

## Endpoints

### 1. Upload File
- **POST /upload_file**
- Request: multipart/form-data, file
- Response: { filename, path }

### 2. List Files
- **GET /list_files**
- Response: { files: [filename, ...] }

### 3. Get File Content
- **GET /get_file_content?filename=...**
- Response: { filename, content }

### 4. Write Summary
- **POST /write_summary**
- Request: { filename, result }
- Response: { status }

## Example Usage
- List files: `GET /list_files`
- Get content: `GET /get_file_content?filename=dummy.pdf`
- Upload: `POST /upload_file` (with file)
- Write summary: `POST /write_summary` (with JSON body)

## Transport
- HTTP (can be extended to JSON-RPC or WebSockets)

## Interoperability
- Any MCP-compliant client can use these endpoints to interact with the resource server.
