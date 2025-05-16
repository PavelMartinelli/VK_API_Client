import os


class TokenManager:
    def __init__(self, filename='token.txt'):
        self.filename = filename

    def load_token(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    return f.read().strip()
            return None
        except Exception as e:
            print(f"Ошибка чтения токена: {e}")
            return None

    def save_token(self, token):
        try:
            with open(self.filename, 'w') as f:
                f.write(token)
            print("🔑 Токен успешно сохранён в файл")
        except Exception as e:
            print(f"Ошибка сохранения токена: {e}")