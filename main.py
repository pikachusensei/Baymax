# main.py
from stt.stt_whisper import transcribe_audio
from engine.rule_based import get_reply
from tts.tts_engine import speak_hi
from health.health_module import check_vitals
from control.actions import perform_action
from utils.logger import log_conversation

def main():
    print("👋 Baymax is online...say BYE to exit")

    while True:


        # Step 1: Get user speech → text
        user_text = transcribe_audio()
        print(f"🗣️ You said: {user_text}")

        if "bye" in user_text.lower():
            print("👋 Baymax is offline...goodbye!")
            break

        # Step 2: Conversation Engine → reply
        reply = get_reply(user_text)

        # Step 3: Health check (mock vitals)
        vitals = {"heart_rate": 105}
        health_msg = check_vitals(vitals)

        # Step 4: Final Baymax reply
        final_reply = f"{reply} {health_msg}"
        print(f"🤖 Baymax: {final_reply}")

        # Step 5: Speak the reply
        speak_hi(final_reply)

        # Step 6: Trigger control action
        perform_action("wave")

        # Step 7: Log everything
        log_conversation(user_text, final_reply)

if __name__ == "__main__":
    main()
