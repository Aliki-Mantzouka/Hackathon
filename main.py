from fastapi import FastAPI
import httpx

app = FastAPI()

# ΡΥΘΜΙΣΕΙΣ (Βάλε τα δικά σου στοιχεία εδώ)
VIBER_TOKEN = "YOUR_VIBER_TOKEN"  # Άφησέ το έτσι αν δεν έχεις πάρει ακόμα
MY_VIBER_ID = "YOUR_VIBER_ID"
NTFY_TOPIC = "nodashackathon"  # Αυτό που άνοιξες στο κινητό σου

@app.get("/")
def home():
    return {"message": "Multi-Channel HITL Gateway is Online!"}

@app.post("/agent-input")
async def receive_from_agent(data: dict):
    content = data.get("content", "Human input required")
    urgency = data.get("urgency", "normal")
    message = f"🚨 [{urgency.upper()}]: {content}"

    results = {}

    async with httpx.AsyncClient() as client:
        # 1. ΑΠΟΣΤΟΛΗ ΣΤΟ NTFY (Το σίγουρο)
        try:
            ntfy_res = await client.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=message.encode('utf-8'))
            results["ntfy"] = "Success" if ntfy_res.status_code == 200 else "Failed"
        except Exception as e:
            results["ntfy"] = f"Error: {str(e)}"

        # 2. ΑΠΟΣΤΟΛΗ ΣΤΟ VIBER (Μόνο αν υπάρχει Token)
        if VIBER_TOKEN != "YOUR_VIBER_TOKEN":
            viber_url = "https://chatapi.viber.com/pa/send_message"
            viber_payload = {
                "receiver": MY_VIBER_ID,
                "type": "text",
                "sender": {"name": "HITL Gateway"},
                "text": message
            }
            try:
                viber_res = await client.post(viber_url, json=viber_payload, headers={"X-Viber-Auth-Token": VIBER_TOKEN})
                results["viber"] = viber_res.json()
            except Exception as e:
                results["viber"] = f"Error: {str(e)}"
        else:
            results["viber"] = "Skipped (No Token provided)"

    return {"status": "Processing complete", "channels": results}