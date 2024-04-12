# RuStoreDL
Утилита для быстрого поиска и скачивания пакетов приложений Android (.apk) из RuStore

### Установка

Клонируем репозиторий

```
$ git clone https://github.com/avoidcode/rustoredl.git
```

Устанавливаем с помощью `pip`

```
$ cd rustoredl
$ pip install .
```
или `setuptools`
```
$ python setup.py install
```

## Использование

### Поиск

![image](https://github.com/avoidcode/rustoredl/assets/51087676/8140f5e0-82df-4b5b-859d-541352c96417)

### Скачивание по имени пакета

![image](https://github.com/avoidcode/rustoredl/assets/51087676/07ff9e69-a3a8-4863-ab30-35ec01da5494)

```
$ rustoredl --help
usage: rustoredl [-h] {search,download} ...

Downloads an Android application by given package name from RuStore

positional arguments:
  {search,download}
    search           Search packages on RuStore by name
    download         Download apk by package name immediately

options:
  -h, --help         show this help message and exit
```