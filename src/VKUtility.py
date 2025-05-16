from src.DataPrinter import DataPrinter
from src.TokenManager import TokenManager
from src.VKAPIHandler import VKAPIHandler


class VKUtility:
    def __init__(self):
        self.token_manager = TokenManager()
        self.printer = DataPrinter()
        self.vk = None
        self.current_user = None
        self.commands = {
            'help': "Показать список команд",
            'info': "Информация о пользователе",
            'friends': "Список друзей",
            'albums': "Фотоальбомы",
            'exit': "Выход из программы"
        }

    def _initialize_api(self):
        token = self.token_manager.load_token()

        if not token:
            token = input("Введите ваш VK API токен: ").strip()
            if input(
                    "Сохранить токен для будущих запусков? (y/n): ").lower() in [
                'y', 'д']:
                self.token_manager.save_token(token)

        self.vk = VKAPIHandler(token)
        try:
            self.current_user = self.vk.get_user_info('')
            print(
                f"\n✅ Авторизация успешна! Добро пожаловать, {self.current_user['first_name']}!")
        except Exception as e:
            print(f"❌ Ошибка авторизации: {e}")
            raise e

    def _show_help(self):
        print("\nДоступные команды:")
        for cmd, desc in self.commands.items():
            print(f"▶ {cmd.ljust(8)} - {desc}")

    def _process_command(self, command):
        if command == 'exit':
            print("\nДо свидания! 👋")
            return False
        elif command == 'help':
            self._show_help()
        elif command in ['info', 'friends', 'albums']:
            self._handle_user_command(command)
        else:
            print("❌ Неизвестная команда. Введите 'help' для справки")
        return True

    def _handle_user_command(self, command):
        user_input = input(
            "Введите ID или имя пользователя (Enter для текущего): ").strip()

        user_id = None
        if user_input:
            if user_input.isdigit():  # Если введен числовой ID
                user_id = int(user_input)
            else:  # Если введен screen_name
                try:
                    user_id = self.vk.resolve_screen_name(user_input)
                    if not user_id:
                        print("😞 Пользователь не найден")
                        return
                except Exception as e:
                    print(f"⛔ Ошибка поиска пользователя: {e}")
                    return
        else:
            user_id = self.current_user['id']

        try:
            if command == 'info':
                user_info = self.vk.get_user_info(user_id)
                self.printer.print_user_info(
                    user_info) if user_info else print(
                    "😞 Пользователь не найден")
            elif command == 'friends':
                self.printer.print_friends(self.vk.get_friends(user_id))
            elif command == 'albums':
                self.printer.print_albums(self.vk.get_albums(user_id))
        except Exception as e:
            print(f"⛔ Ошибка: {e}")

    def run(self):
        try:
            self._initialize_api()
        except:
            return

        self._show_help()

        while True:
            try:
                command = input("\n🏁 Введите команду: ").strip().lower()
                if not self._process_command(command):
                    break
            except KeyboardInterrupt:
                print("\n🚫 Прервано пользователем")
                break