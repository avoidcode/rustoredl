## RuStoreDL
Утилита для быстрого поиска и скачивания пакетов приложений Android (.apk) из RuStore.

### Установка

```sh
git clone https://github.com/avoidcode/rustoredl.git
```
Установка с помощью `pip3`

```sh
cd rustoredl
pip3 install .
```
Установка с помощью `setuptools`
```sh
cd rustoredl
python setup.py install
```

### Использование

```
$ rustoredl --help
usage: rustoredl [-h] {search,download,getlink} ...

Downloads an Android application by given package name from RuStore

positional arguments:
  {search,download,getlink}
    search              Search packages on RuStore by application name
    download            Download apk by package name immediately
    getlink             Get direct download link for apk by package name

options:
  -h, --help            show this help message and exit
```

### Поиск

![image](https://github.com/avoidcode/rustoredl/assets/51087676/13a6dd86-d86b-4f6d-b87b-4b5bdba95feb)



### Скачивание по имени пакета

![image](https://github.com/avoidcode/rustoredl/assets/51087676/49eea155-1ea9-477d-9132-73ce52f4c134)

### Получение прямой ссылки на скачивание

![image](https://github.com/avoidcode/rustoredl/assets/51087676/9433e806-43f8-494e-8a23-767c83ac161e)


