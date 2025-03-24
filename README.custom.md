# Freqtrade Crypto Trading Bot с BinHV27 стратегией

Этот репозиторий содержит настроенный торговый бот Freqtrade с реализацией популярной стратегии BinHV27.

## Особенности

- Использование стратегии BinHV27 - одной из лучших community-стратегий для Freqtrade
- Настроенные Telegram-уведомления с удобной клавиатурой команд
- Оптимизированные параметры для торговли на Binance Futures
- Режим симуляции (dry-run) для безопасного тестирования

## Настройка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Perlitten/cripto-bot.git
cd cripto-bot
```

2. Создайте файл конфигурации из примера:
```bash
cp config.example.json config.json
```

3. Отредактируйте config.json, добавив свои API ключи и настройки Telegram

4. Установите зависимости и запустите бот:
```bash
# С использованием Docker (рекомендуется)
docker-compose up -d

# Или напрямую через Python
pip install -r requirements.txt
python -m freqtrade trade --config config.json --strategy BinHV27
```

## Параметры торговли

- Максимум одновременных сделок: 3
- Размер ставки: 60 USDT
- Виртуальный баланс (dry-run): 200 USDT
- Режим торговли: фьючерсы (futures)
- Тип маржи: изолированная (isolated)

## Telegram-команды

Бот настроен с удобной клавиатурой в Telegram, включающей следующие команды:
- `/status`, `/profit`, `/balance` - информация о состоянии бота
- `/daily`, `/weekly`, `/monthly` - статистика за разные периоды
- `/trades`, `/performance`, `/locks` - анализ сделок
- `/whitelist`, `/blacklist`, `/logs` - управление списками пар и логи
- `/help`, `/version`, `/start` - справка и информация

## Развертывание

Рекомендуется развертывание на Oracle Cloud Free Tier для бесплатного и стабильного хостинга 24/7.

## Безопасность

- Не храните API ключи в репозитории
- Используйте API ключи только с необходимыми разрешениями
- Настройте ограничение по IP в настройках API ключа на Binance

## Лицензия

Этот проект основан на [Freqtrade](https://github.com/freqtrade/freqtrade) и распространяется под той же лицензией.
