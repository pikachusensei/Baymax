def get_reply(user_text:str)->str:
    """get reply from user"""
    text=user_text.lower()
    if "headache" in text:
        return "Navratna tel lagao"
    elif "tired" in text:
        return "so jao balak"
    else:
        return "kya bol rhe balak, aao jara kopche me"
    