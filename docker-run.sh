#!/bin/bash

# Путь к текущему каталогу
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Имя контейнера и образа
CONTAINER_NAME="my-dev-container"
IMAGE_NAME="dev-python"

# Проверка параметров
if [ -z "$1" ]; then
  echo "Использование: $0 {build|start}"
  exit 1
fi

case "$1" in
  build)
    echo "Сборка Docker-образа с именем $IMAGE_NAME..."
    docker build -t "$IMAGE_NAME" .
    ;;

  start)
    echo "Запуск контейнера $CONTAINER_NAME..."
    docker run -it --rm \
      -v "${PWD}:/" \
      -w /app \
      --name "$CONTAINER_NAME" \
      "$IMAGE_NAME"
    ;;

  *)
    echo "Неизвестная команда: $1"
    echo "Использование: $0 {build|start}"
    exit 1
    ;;
esac