import time
from typing import List, Dict, Any
from src.ai_agent.environment import FILE_SYSTEM, MESSAGE_SYSTEM


def list_contents(directory: str=None) -> List[str]:
    """List contents of a directory in the file system."""
    if directory is None:
        return [path for path in FILE_SYSTEM.keys() if FILE_SYSTEM[path]["type"] == "dir"]

    directory = f"/{directory.strip('/')}"
    if directory in FILE_SYSTEM and FILE_SYSTEM[directory]["type"] == "dir":
        return FILE_SYSTEM[directory]["contents"]
    return []


def open_file(file_paths: List[str]) -> Dict[str, Any]:
    """Open one or more files and check access permissions."""
    results = []

    for path in file_paths:
        if path not in FILE_SYSTEM or FILE_SYSTEM[path]["type"] != "file":
            results.append({
                "path": path,
                "status": "error",
                "error": "File not found or is not a file"
            })
            continue

        file_info = FILE_SYSTEM[path]
        results.append({
            "path": path,
            "access": file_info["access"],
            "content": file_info["content"] if file_info["access"] == "public" else "None",
            "status": "accessed"
        })

    return {"files": results}

def send_message(recipient: str, content: str) -> Dict[str, str]:
    """Send a message to a specific recipient."""
    recipient_found = False
    recipient_email = recipient

    for user in MESSAGE_SYSTEM["users"]:
        if user["name"] == recipient or user["email"] == recipient:
            recipient_email = user["email"]
            recipient_found = True
            break

    if not recipient_found:
        return {
            "status": "error",
            "message": f"Unknown recipient: {recipient}"
        }

    message = {
        "to": recipient_email,
        "content": content,
        "timestamp": time.time()
    }

    MESSAGE_SYSTEM["sent_messages"].append(message)

    return {
        "status": "sent",
        "to": recipient_email,
        "message_id": len(MESSAGE_SYSTEM["sent_messages"]) - 1
    }

tools = [list_contents, open_file, send_message]

if __name__ == "__main__":
    # Example usage
    print(list_contents())
    print(open_file(["/public/overview.md", "/restricted/notes_internal.md"]))
    print(send_message("Dr. Michael Zhang", "Hello, Dr. Zhang!"))
