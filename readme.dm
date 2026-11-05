## Инструкция по запуску

### 1. Клонирование проекта

```bash
git clone https://github.com/YOUR_USERNAME/TestTask.git
cd TestTask
```

### 2. Создание виртуального окружения

```bash
python -m venv .venv
```

### 3. Активация виртуального окружения (Windows PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Установка зависимостей

```bash
python -m pip install -r requirements.txt
```

### 5. Установка Chromium

```bash
python -m playwright install chromium
```

### 6. Запуск программы

```bash
python capture_video.py
```

Результаты выполнения сохраняются в папке `video/` в формате `.webm`.

**Требования:** Python 3.9+, подключение к интернету.