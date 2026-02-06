# 🧩 aiogram-bot-template

A scalable and well-structured template for building bots with **aiogram**.

---

## 🌐 Localization

The project uses **[aiogram_i18n[runtime]](https://github.com/aiogram/aiogram_i18n)** for text localization.  
All locale files are stored in:

---

## 🧱 Models

The project uses **[msgspec](https://jcristharif.com/msgspec/)** for fast and type-safe JSON serialization and deserialization.

---

## ⚙️ API Requests

All API requests are managed through the **`Api`** class, which uses **aiohttp** under the hood.  
Endpoints are defined in: src/api/interceptors/

Built-in interceptors:

- `on_request_start` — executed before each request  
- `on_request_end` — executed after each request  

These allow for convenient request logging, metrics collection, or pre/post-processing.

---

## 🚀 Features Summary

- 🧩 Modular project structure  
- 🌍 Built-in localization system  
- ⚡ Fast JSON (de)serialization via `msgspec`  
- 🔗 Structured API layer with request interceptors  
- 🧠 Ready for scaling and customization  

---

## 🛠️ Tech Stack

- [aiogram](https://docs.aiogram.dev/)
- [aiogram_i18n](https://github.com/aiogram/aiogram_i18n)
- [aiohttp](https://docs.aiohttp.org/)
- [msgspec](https://jcristharif.com/msgspec/)

---

## ⚙️ Configuration

Before running the bot, make sure to create a **`.env`** file in the project root with the following variables:

```env
TOKEN=your_telegram_bot_token
BASE_URL=https://your.api.url
```
---

> 💡 Use this template as a foundation for your next scalable and maintainable Telegram bot project.