## RuStoreDL
Утилита для быстрого поиска и скачивания пакетов приложений Android (.apk) из RuStore. Поддреживаемая версия Python $\geq$ 3.6

### Установка

```sh
git clone https://github.com/avoidcode/rustoredl.git
```
Установка с помощью `pip3`

```sh
cd rustoredl
pip install .
```
Установка с помощью `setuptools`
```sh
cd rustoredl
python setup.py install
```

### Использование

```
$ rustoredl --help
usage: rustoredl [-h] [-l] {search,download} ...

Downloads an Android application by given package name from RuStore

positional arguments:
  {search,download}
    search           Search packages on RuStore by name
    download         Download apk by package name immediately

options:
  -h, --help         show this help message and exit
  -l, --link-only    Get direct download link, skip downloading
```

### Поиск

![image](https://github.com/avoidcode/rustoredl/assets/51087676/dff3782c-db5e-4951-94d0-ec6f00d2f34d)


### Скачивание по имени пакета

![image](https://github.com/avoidcode/rustoredl/assets/51087676/07ff9e69-a3a8-4863-ab30-35ec01da5494)
