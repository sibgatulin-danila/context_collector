#!/bin/bash

# Имя контейнера и образа
IMAGE_NAME="context-collector-image"
CONTAINER_NAME="context-collector-container"

# Проверка на наличие аргумента
if [ -z "$1" ]; then
  echo "Без аргументов — выполняю build и start..."
  docker build -t "$IMAGE_NAME" .
  docker run --rm \
    -v "${PWD}:/context_collector" \
    --name "$CONTAINER_NAME" \
    "$IMAGE_NAME"
else
  case "$1" in
    build)
      echo "Сборка Docker-образа с именем $IMAGE_NAME..."
      docker build -t "$IMAGE_NAME" .
      ;;

    start)
      echo "Запуск контейнера $CONTAINER_NAME..."
      docker run --rm \
        -v "${PWD}:/context_collector" \
        --name "$CONTAINER_NAME" \
        "$IMAGE_NAME"
      ;;

    *)
      echo "Неизвестная команда: $1"
      echo "Использование: $0 {build|start}"
      exit 1
      ;;
  esac
fi