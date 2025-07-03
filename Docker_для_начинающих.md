# 🐳 Docker для начинающих
## Полное руководство по контейнеризации

---

## 📋 Содержание

1. [Что такое Docker?](#что-такое-docker)
2. [Основные концепции](#основные-концепции)
3. [Архитектура Docker](#архитектура-docker)
4. [Установка Docker](#установка-docker)
5. [Основные команды](#основные-команды)
6. [Работа с образами](#работа-с-образами)
7. [Работа с контейнерами](#работа-с-контейнерами)
8. [Dockerfile](#dockerfile)
9. [Docker Compose](#docker-compose)
10. [Сети Docker](#сети-docker)
11. [Тома и данные](#тома-и-данные)
12. [Лучшие практики](#лучшие-практики)
13. [Отладка и устранение неполадок](#отладка-и-устранение-неполадок)
14. [Практические примеры](#практические-примеры)
15. [Безопасность](#безопасность)
16. [Мониторинг](#мониторинг)
17. [Интеграция с CI/CD](#интеграция-с-cicd)

---

## 🎯 Что такое Docker?

### Определение
**Docker** — это платформа для разработки, доставки и запуска приложений в контейнерах. Контейнеры — это легковесные, изолированные среды, которые содержат все необходимое для запуска приложения.

### Аналогия с транспортом
```
🚢 Корабль (Docker Engine)
├── 📦 Контейнер 1 (Приложение A)
├── 📦 Контейнер 2 (Приложение B)
└── 📦 Контейнер 3 (База данных)
```

### Преимущества Docker

| Преимущество | Описание |
|-------------|----------|
| **Портативность** | Работает везде одинаково |
| **Изоляция** | Приложения не влияют друг на друга |
| **Эффективность** | Меньше ресурсов, быстрый запуск |
| **Масштабируемость** | Легко копировать и масштабировать |
| **Версионирование** | Контроль версий для приложений |

---

## 🏗️ Основные концепции

### 1. Образ (Image)
**Образ** — это шаблон с инструкциями для создания контейнера.

```
📦 Образ (Image)
├── 🖥️ Операционная система
├── 📚 Приложение
├── ⚙️ Конфигурация
└── 📁 Файлы
```

### 2. Контейнер (Container)
**Контейнер** — это запущенный экземпляр образа.

```
🔄 Образ → Контейнер
📦 nginx:latest → 🚀 nginx-контейнер (работает)
```

### 3. Реестр (Registry)
**Реестр** — это хранилище образов (например, Docker Hub).

```
🌐 Docker Hub
├── 📦 nginx:latest
├── 📦 python:3.9
├── 📦 mysql:8.0
└── 📦 redis:alpine
```

---

## 🏛️ Архитектура Docker

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Client                        │
│  (docker CLI, Docker Desktop, docker-compose)          │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  Docker Daemon                          │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │   Images        │  │  Containers     │              │
│  │   Management    │  │  Management     │              │
│  └─────────────────┘  └─────────────────┘              │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │   Networks      │  │   Volumes       │              │
│  │   Management    │  │   Management    │              │
│  └─────────────────┘  └─────────────────┘              │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                 Container Runtime                       │
│  (containerd, runc)                                    │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                 Host Operating System                   │
│  (Linux Kernel, Windows, macOS)                        │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Установка Docker

### macOS
```bash
# Через Homebrew
brew install --cask docker

# Или скачать с официального сайта
# https://www.docker.com/products/docker-desktop
```

### Ubuntu/Debian
```bash
# Обновить пакеты
sudo apt update

# Установить зависимости
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release

# Добавить GPG ключ Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавить репозиторий
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установить Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER
```

### Windows
```bash
# Скачать Docker Desktop с официального сайта
# https://www.docker.com/products/docker-desktop
```

### Проверка установки
```bash
# Проверить версию Docker
docker --version

# Проверить работу Docker
docker run hello-world
```

---

## 🎮 Основные команды

### Системные команды
```bash
# Информация о системе
docker version          # Версия Docker
docker info             # Подробная информация
docker system df        # Использование диска
docker system prune     # Очистка неиспользуемых ресурсов
```

### Работа с образами
```bash
# Поиск образов
docker search nginx

# Скачивание образа
docker pull nginx:latest

# Просмотр образов
docker images

# Удаление образа
docker rmi nginx:latest
```

### Работа с контейнерами
```bash
# Запуск контейнера
docker run nginx:latest

# Запуск в фоновом режиме
docker run -d nginx:latest

# Запуск с именем
docker run --name my-nginx nginx:latest

# Запуск с портами
docker run -p 8080:80 nginx:latest

# Запуск с переменными окружения
docker run -e MYSQL_ROOT_PASSWORD=secret mysql:8.0

# Просмотр запущенных контейнеров
docker ps

# Просмотр всех контейнеров
docker ps -a

# Остановка контейнера
docker stop my-nginx

# Удаление контейнера
docker rm my-nginx

# Просмотр логов
docker logs my-nginx

# Выполнение команд в контейнере
docker exec -it my-nginx bash
```

---

## 📦 Работа с образами

### Создание образа из Dockerfile
```bash
# Сборка образа
docker build -t my-app:latest .

# Сборка с тегом
docker build -t my-app:v1.0 .

# Сборка без кэша
docker build --no-cache -t my-app:latest .
```

### Экспорт и импорт образов
```bash
# Сохранение образа в файл
docker save -o my-app.tar my-app:latest

# Загрузка образа из файла
docker load -i my-app.tar
```

### Теги образов
```bash
# Добавление тега
docker tag my-app:latest my-app:v1.0

# Удаление тега
docker rmi my-app:v1.0
```

### Многоэтапная сборка
```dockerfile
# Этап сборки
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Этап продакшена
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

---

## 🚀 Работа с контейнерами

### Жизненный цикл контейнера
```
📦 Образ
    ↓
🚀 Создание (docker create)
    ↓
▶️ Запуск (docker start)
    ↓
⏸️ Пауза (docker pause)
    ↓
▶️ Возобновление (docker unpause)
    ↓
⏹️ Остановка (docker stop)
    ↓
🗑️ Удаление (docker rm)
```

### Режимы запуска
```bash
# Интерактивный режим
docker run -it ubuntu:latest bash

# Фоновый режим
docker run -d nginx:latest

# Режим с автоматическим удалением
docker run --rm nginx:latest

# Режим с перезапуском
docker run --restart=always nginx:latest
```

### Управление ресурсами
```bash
# Ограничение памяти
docker run -m 512m nginx:latest

# Ограничение CPU
docker run --cpus=2 nginx:latest

# Ограничение диска
docker run --storage-opt size=10G nginx:latest
```

---

## 📝 Dockerfile

### Структура Dockerfile
```dockerfile
# Базовый образ
FROM ubuntu:20.04

# Метаданные
LABEL maintainer="developer@example.com"
LABEL version="1.0"

# Переменные окружения
ENV NODE_ENV=production
ENV PORT=3000

# Рабочая директория
WORKDIR /app

# Копирование файлов зависимостей
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование исходного кода
COPY . .

# Сборка приложения
RUN npm run build

# Открытие порта
EXPOSE 3000

# Команда запуска
CMD ["npm", "start"]
```

### Инструкции Dockerfile

| Инструкция | Описание | Пример |
|------------|----------|--------|
| `FROM` | Базовый образ | `FROM ubuntu:20.04` |
| `LABEL` | Метаданные | `LABEL version="1.0"` |
| `ENV` | Переменные окружения | `ENV NODE_ENV=production` |
| `WORKDIR` | Рабочая директория | `WORKDIR /app` |
| `COPY` | Копирование файлов | `COPY . .` |
| `ADD` | Копирование с распаковкой | `ADD archive.tar.gz /app/` |
| `RUN` | Выполнение команд | `RUN npm install` |
| `EXPOSE` | Открытие порта | `EXPOSE 3000` |
| `CMD` | Команда по умолчанию | `CMD ["npm", "start"]` |
| `ENTRYPOINT` | Точка входа | `ENTRYPOINT ["nginx"]` |
| `USER` | Пользователь | `USER node` |
| `VOLUME` | Том | `VOLUME /data` |

### Примеры Dockerfile

#### Node.js приложение
```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

#### Python приложение
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

#### Многоэтапная сборка
```dockerfile
# Этап сборки
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Этап продакшена
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

---

## 🎼 Docker Compose

### Что такое Docker Compose?
**Docker Compose** — это инструмент для определения и запуска многоконтейнерных приложений.

### Структура docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - db
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: myapp
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

### Команды Docker Compose
```bash
# Запуск сервисов
docker-compose up

# Запуск в фоновом режиме
docker-compose up -d

# Остановка сервисов
docker-compose down

# Просмотр логов
docker-compose logs

# Пересборка образов
docker-compose build

# Масштабирование сервисов
docker-compose up --scale web=3
```

### Примеры docker-compose.yml

#### Веб-приложение с базой данных
```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### Микросервисная архитектура
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
      - web

  api:
    build: ./api
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    depends_on:
      - db

  web:
    build: ./web
    environment:
      - API_URL=http://api:8000

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## 🌐 Сети Docker

### Типы сетей
```
🌐 Docker Networks
├── 🏠 bridge (по умолчанию)
├── 🏢 host
├── 🔌 none
└── 🏗️ custom
```

### Создание и управление сетями
```bash
# Создание сети
docker network create my-network

# Просмотр сетей
docker network ls

# Информация о сети
docker network inspect my-network

# Удаление сети
docker network rm my-network
```

### Подключение контейнеров к сети
```bash
# Запуск контейнера в сети
docker run --network my-network nginx:latest

# Подключение к сети
docker network connect my-network my-container

# Отключение от сети
docker network disconnect my-network my-container
```

### Примеры конфигурации сети

#### В docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    networks:
      - frontend
      - backend

  api:
    image: my-api:latest
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

#### Создание сети для микросервисов
```bash
# Создание сети для микросервисов
docker network create microservices

# Запуск сервисов в сети
docker run -d --name api --network microservices my-api:latest
docker run -d --name web --network microservices my-web:latest
docker run -d --name db --network microservices postgres:13
```

---

## 💾 Тома и данные

### Типы томов
```
💾 Docker Volumes
├── 📁 Named Volumes (именованные)
├── 📂 Bind Mounts (привязка)
└── 📄 tmpfs (временная файловая система)
```

### Управление томами
```bash
# Создание тома
docker volume create my-volume

# Просмотр томов
docker volume ls

# Информация о томе
docker volume inspect my-volume

# Удаление тома
docker volume rm my-volume
```

### Использование томов
```bash
# Именованный том
docker run -v my-volume:/data nginx:latest

# Привязка директории
docker run -v /host/path:/container/path nginx:latest

# Только для чтения
docker run -v /host/path:/container/path:ro nginx:latest
```

### Примеры использования томов

#### В docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    volumes:
      - ./html:/usr/share/nginx/html:ro
      - nginx_logs:/var/log/nginx

  db:
    image: mysql:8.0
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  nginx_logs:
  mysql_data:
```

#### Резервное копирование данных
```bash
# Создание резервной копии
docker run --rm -v my-volume:/data -v $(pwd):/backup alpine tar czf /backup/my-volume-backup.tar.gz -C /data .

# Восстановление из резервной копии
docker run --rm -v my-volume:/data -v $(pwd):/backup alpine tar xzf /backup/my-volume-backup.tar.gz -C /data
```

---

## ✅ Лучшие практики

### 1. Безопасность образов
```dockerfile
# Использование non-root пользователя
FROM node:16-alpine
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Минимальные привилегии
RUN chmod 755 /app
```

### 2. Оптимизация размера
```dockerfile
# Многоэтапная сборка
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:16-alpine
COPY --from=builder /app/node_modules ./node_modules
COPY . .
```

### 3. Кэширование слоев
```dockerfile
# Копирование зависимостей перед кодом
COPY package*.json ./
RUN npm install
COPY . .
```

### 4. Переменные окружения
```dockerfile
# Использование ARG для build-time переменных
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV
```

### 5. Health checks
```dockerfile
# Проверка здоровья приложения
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

### 6. Логирование
```dockerfile
# Настройка логирования
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
```

---

## 🔧 Отладка и устранение неполадок

### Полезные команды для отладки
```bash
# Просмотр логов
docker logs container_name

# Просмотр логов в реальном времени
docker logs -f container_name

# Выполнение команд в контейнере
docker exec -it container_name bash

# Просмотр информации о контейнере
docker inspect container_name

# Просмотр статистики ресурсов
docker stats

# Просмотр процессов в контейнере
docker top container_name
```

### Частые проблемы и решения

#### 1. Контейнер не запускается
```bash
# Проверка логов
docker logs container_name

# Проверка статуса
docker ps -a

# Запуск в интерактивном режиме
docker run -it image_name bash
```

#### 2. Проблемы с сетью
```bash
# Проверка сетей
docker network ls

# Проверка подключений
docker network inspect network_name

# Тест подключения между контейнерами
docker exec container1 ping container2
```

#### 3. Проблемы с томами
```bash
# Проверка томов
docker volume ls

# Проверка содержимого тома
docker run --rm -v volume_name:/data alpine ls -la /data
```

#### 4. Проблемы с памятью
```bash
# Ограничение памяти
docker run -m 512m image_name

# Просмотр использования ресурсов
docker stats
```

---

## 🛠️ Практические примеры

### 1. Простое веб-приложение
```dockerfile
# Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Docker Demo</title>
</head>
<body>
    <h1>Привет, Docker!</h1>
</body>
</html>
```

```bash
# Сборка и запуск
docker build -t my-web-app .
docker run -p 8080:80 my-web-app
```

### 2. Node.js API
```dockerfile
# Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

```json
// package.json
{
  "name": "my-api",
  "version": "1.0.0",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "^4.17.1"
  }
}
```

```javascript
// app.js
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ message: 'Привет, Docker!' });
});

app.listen(port, () => {
  console.log(`Сервер запущен на порту ${port}`);
});
```

### 3. Python Flask приложение
```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

```txt
# requirements.txt
Flask==2.0.1
```

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Привет, Docker!'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 4. Многоконтейнерное приложение
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:8000

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 🔒 Безопасность

### Основные принципы безопасности
```dockerfile
# 1. Использование non-root пользователя
FROM node:16-alpine
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# 2. Минимальные привилегии
RUN chmod 755 /app

# 3. Обновление пакетов
RUN apk update && apk upgrade

# 4. Удаление ненужных файлов
RUN rm -rf /var/cache/apk/*
```

### Сканирование уязвимостей
```bash
# Сканирование образа
docker scan my-image:latest

# Сканирование с отчетом
docker scan --json my-image:latest > scan-report.json
```

### Безопасные практики
```bash
# Не использовать образы с тегом latest
docker pull nginx:1.21

# Проверять подписи образов
docker pull nginx@sha256:abc123...

# Использовать минимальные базовые образы
FROM alpine:3.14
```

---

## 📊 Мониторинг

### Мониторинг контейнеров
```bash
# Статистика в реальном времени
docker stats

# Статистика конкретного контейнера
docker stats container_name

# Просмотр событий
docker events

# Системная информация
docker system df
```

### Логирование
```bash
# Просмотр логов
docker logs container_name

# Логи с временными метками
docker logs -t container_name

# Логи за последние 10 минут
docker logs --since 10m container_name

# Экспорт логов
docker logs container_name > container.log
```

### Метрики и мониторинг
```yaml
# docker-compose.yml с мониторингом
version: '3.8'

services:
  app:
    image: my-app:latest
    ports:
      - "3000:3000"

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## 🔄 Интеграция с CI/CD

### GitHub Actions
```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t my-app:${{ github.sha }} .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push my-app:${{ github.sha }}
```

### GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - build
  - deploy

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t my-app:$CI_COMMIT_SHA .
    - docker push my-app:$CI_COMMIT_SHA
```

### Jenkins Pipeline
```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t my-app:$BUILD_NUMBER .'
            }
        }
        
        stage('Push') {
            steps {
                sh 'docker push my-app:$BUILD_NUMBER'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
```

---

## 📚 Дополнительные ресурсы

### Официальная документация
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Книги
- "Docker in Action" - Jeff Nickoloff
- "Using Docker" - Adrian Mouat
- "Docker: Up & Running" - Karl Matthias

### Курсы
- Docker Official Tutorial
- Udemy Docker Courses
- Pluralsight Docker Path

### Сообщества
- Docker Community Forums
- Stack Overflow Docker Tag
- Reddit r/docker

---

## 🎯 Заключение

Docker — это мощный инструмент для контейнеризации приложений, который упрощает разработку, развертывание и масштабирование. Освоив основы Docker, вы сможете:

- ✅ Быстро развертывать приложения
- ✅ Обеспечивать консистентность сред
- ✅ Масштабировать приложения
- ✅ Упростить CI/CD процессы
- ✅ Улучшить безопасность

**Начните с простых примеров и постепенно переходите к более сложным сценариям!**

---

*Данное руководство поможет вам начать работу с Docker и освоить основные концепции контейнеризации.* 