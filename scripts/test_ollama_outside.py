"""Отправляет запросы с хоста в Ollama в одиночном и пакетном режимах."""

from __future__ import annotations

import argparse
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"
DEFAULT_TIMEOUT = 120
PRESET_MESSAGES = [
    "Вы выиграли iPhone! Срочно перейдите по ссылке и заберите приз.",
    "Мама, это мой новый номер. Срочно переведи 5000 на карту.",
    "Напоминаем о записи к врачу завтра в 10:30.",
    "Ваш счет заблокирован. Подтвердите данные по ссылке.",
    "Код подтверждения для входа: 483921. Никому не сообщайте.",
    "Только сегодня: кредит без отказа, оформите за 5 минут.",
    "Ваш заказ #8345 передан в доставку, ожидайте курьера.",
    "Срочно оплатите задолженность, иначе номер будет отключен.",
    "Спасибо за покупку! Ваш чек доступен в приложении.",
    "Поздравляем! Вы выбраны для получения денежного бонуса.",
]


def call_ollama(prompt: str) -> dict:
    """Вызывает HTTP API Ollama и возвращает распарсенный JSON-ответ."""
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def print_result(prompt: str, data: dict) -> None:
    """Печатает отправленный запрос и ответ Ollama в удобном формате."""
    print(f"Sent message: {prompt}")
    print(f"Model: {data.get('model')}")
    print(f"Response: {data.get('response', '').strip()}")
    print("-" * 80)


def run_single(prompt: str) -> None:
    """Отправляет один пользовательский промпт в Ollama и печатает результат."""
    data = call_ollama(prompt)
    print_result(prompt, data)


def run_batch() -> None:
    """Отправляет 10 предустановленных промптов в Ollama и печатает результаты."""
    for idx, message in enumerate(PRESET_MESSAGES, start=1):
        print(f"[{idx}/10]")
        data = call_ollama(
            f"Определи, является ли сообщение спамом, и кратко объясни почему: {message}"
        )
        print_result(message, data)


def build_parser() -> argparse.ArgumentParser:
    """Создает CLI-парсер аргументов для одиночного и пакетного режимов."""
    parser = argparse.ArgumentParser(
        description="Отправка пользовательских и предустановленных запросов в Ollama в Docker."
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Пользовательское сообщение/промпт для одиночной отправки.",
    )
    parser.add_argument(
        "--batch10",
        action="store_true",
        help="Запустить 10 предустановленных запросов и вывести сообщение и ответ для каждого.",
    )
    return parser


def main() -> None:
    """Запускает CLI-скрипт в одиночном режиме или в пакетном режиме."""
    parser = build_parser()
    args = parser.parse_args()

    if args.batch10:
        run_batch()
        return

    prompt = args.prompt
    if not prompt:
        prompt = input("Введите сообщение для отправки в Ollama: ").strip()
    if not prompt:
        raise ValueError("Пустой запрос. Передайте --prompt или введите сообщение в интерактивном режиме.")

    run_single(prompt)


if __name__ == "__main__":
    main()
