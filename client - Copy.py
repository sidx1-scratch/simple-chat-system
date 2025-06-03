import time
import threading
from supabase import create_client, Client

SUPABASE_URL = ""
SUPABASE_KEY = ""

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def poll_for_messages(email):
    seen = set()
    while True:
        try:
            response = supabase.from_("messages").select("*").eq("to_email", email).execute()
            if hasattr(response, "error") and response.error is not None:
                print(f"Error polling messages: {response.error}")
            else:
                messages = response.data or []
                for msg in messages:
                    msg_id = msg.get("id")
                    if msg_id not in seen:
                        print(f"\nNew message from {msg['from_email']}: {msg['content']}")
                        seen.add(msg_id)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error polling messages: {e}")
            time.sleep(0.5)

def send_message(from_email):
    try:
        to = input("To: ").strip()
        content = input("Message: ").strip()
        if not to or not content:
            print("To and Message cannot be empty!")
            return
        data = {
            "from_email": from_email,
            "to_email": to,
            "content": content,
        }
        response = supabase.from_("messages").insert(data).execute()
        if hasattr(response, "error") and response.error is not None:
            print(f"❌ Failed to send: {response.error}")
        else:
            print("✅ Message sent")
    except Exception as e:
        print(f"Error sending message: {e}")

def main():
    email = input("Enter your email: ").strip()
    if not email:
        print("Email is required.")
        return

    threading.Thread(target=poll_for_messages, args=(email,), daemon=True).start()

    while True:
        cmd = input("Type 'send' to message someone, or 'exit' to quit: ").strip().lower()
        if cmd == "send":
            send_message(email)
        elif cmd == "exit":
            print("Exiting...")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
