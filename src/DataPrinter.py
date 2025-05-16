class DataPrinter:
    @staticmethod
    def print_user_info(user_info):
        print("\nИнформация о пользователе:")
        print(f"👤 Имя: {user_info.get('first_name', 'Не указано')}")
        print(f"📖 Фамилия: {user_info.get('last_name', 'Не указано')}")
        print(f"🎂 Дата рождения: {user_info.get('bdate', 'Не указана')}")
        print(
            f"🏙️ Город: {user_info.get('city', {}).get('title', 'Не указан')}")
        print(
            f"🌍 Страна: {user_info.get('country', {}).get('title', 'Не указана')}")

    @staticmethod
    def print_friends(friends):
        print(f"\n🎎 Всего друзей: {len(friends)}")
        for i, friend in enumerate(friends[:10], 1):
            print(
                f"{i}. {friend.get('first_name', '')} {friend.get('last_name', '')}")
        if len(friends) > 10:
            print("... и другие")

    @staticmethod
    def print_albums(albums):
        print(f"\n📸 Всего альбомов: {len(albums)}")
        for album in albums:
            print(
                f"- {album.get('title', 'Без названия')} (Количество фотографий: {album.get('size', 0)})")