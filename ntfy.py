import httpx

NTFY_TOPICS = ["eva04", "nodashackathon"]

async def broadcast_to_ntfy(agent_id: str, context: str, task_id: int):
    # f-string για να εμφανίζονται οι μεταβλητές κανονικά
    msg_text = f"📱 [HITL Request]\nID: {task_id}\nAgent: {agent_id}\nContext: {context}"
    
    async with httpx.AsyncClient() as client:
        for topic in NTFY_TOPICS:
            try:
                await client.post(
                    f"https://ntfy.sh/{topic}",
                    data=msg_text.encode('utf-8'),
                    headers={
                        "Title": "New Approval Required",
                        "Priority": "high",
                        "Tags": "envelope"
                    }
                )
            except Exception as e:
                print(f"Error: {e}")