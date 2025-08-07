from bot.handlers import menu
print("Импортировано:", dir(menu))
print("router:", getattr(menu, "router", "❌ router не найден"))