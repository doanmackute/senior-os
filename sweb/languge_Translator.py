from loadConfig import *

class Translator:
    def __init__(self):
        self.langConfigDB = load_sweb_config_json()
        self.language_keys = ["en","cz","de"]
        self.current_language = self.langConfigDB["language"]["default_language"]
        # Set current language is english =0 , CZ = 1, DE = 2
        self.current_language_index = 0

    def toggle_language(self):
        # Increase the index to change the language
        self.current_language_index += 1
        # If we reached the end of the list, go back
        if self.current_language_index >= len(self.language_keys):
            self.current_language_index = 0
        # Change current language after this function called
        self.current_language = self.language_keys[self.current_language_index]

    # Get text from .json acroding Key value
    def get_text(self, nameButton):
        key = f"sweb_{self.current_language}_{nameButton}"
        return self.langConfigDB["text"].get(key, f"No translation found for {key}")
    
    # Get audio from .json acroding Key value
    def get_audio(self, nameButton):
        key = f"sweb_{self.current_language}_{nameButton}"
        return self.langConfigDB["audio"].get(key, f"No translation found for {key}")

    # Get state of current language
    def get_current_language(self):
        return self.language_keys[self.current_language_index]