## Инструкция по запуску

### 1. Клонирование проекта
git clone https://github.com/YOUR_USERNAME/TestTask.git
cd TestTask

### 2. Создание виртуального окружения
python -m venv .venv

### 3. Активация виртуального окружения (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

### 4. Установка зависимостей
python -m pip install -r requirements.txt

### 5. Установка Chromium
python -m playwright install chromium

### 6. Запуск программы
python capture_video.py

Результаты выполнения сохраняются в папке `video/` в формате `.webm`.

**Требования:** Python 3.9+, подключение к интернету.
