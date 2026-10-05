# NordLine Happ Routing

## Файлы маршрутизации

**GeoIP — IP-адреса и подсети:**

```text
https://cdn.jsdelivr.net/gh/ALFiX01/NordLine-HappRouting@main/dat/geoip.dat
```

**GeoSite — домены:**

```text
https://cdn.jsdelivr.net/gh/ALFiX01/NordLine-HappRouting@main/dat/geosite.dat
```

[Скачать geoip.dat напрямую](https://raw.githubusercontent.com/ALFiX01/NordLine-HappRouting/main/dat/geoip.dat) · [Скачать geosite.dat напрямую](https://raw.githubusercontent.com/ALFiX01/NordLine-HappRouting/main/dat/geosite.dat)

## О проекте

**NordLine Happ Routing** — набор списков IP-адресов, подсетей и доменов для настройки маршрутизации в Happ.

Списки объединены в категории, которые можно использовать в правилах маршрутизации: направлять выбранный трафик через VPN, подключаться напрямую или блокировать соединения. Действие для каждой категории задаётся в настройках маршрутизации клиента — сами DAT-файлы содержат списки, а не готовые правила.

- **GeoIP** содержит IPv4/IPv6 адреса и подсети CIDR.
- **GeoSite** содержит домены и правила их сопоставления.
- Готовые **DAT** доступны для подключения по ссылкам выше.
- Исходные **TXT** можно просматривать и редактировать в репозитории.

## Использование в Happ

1. В настройках маршрутизации укажите ссылку на `geoip.dat` для GeoIP и на `geosite.dat` для GeoSite.
2. Загрузите или обновите файлы в приложении.
3. Добавьте нужные категории в правила маршрутизации и выберите для них действие.

Примеры обращения к категориям:

| Список | Категория | В правиле |
| --- | --- | --- |
| GeoIP | `DIRECT` | `geoip:direct` |
| GeoIP | `PRIVATE` | `geoip:private` |
| GeoSite | `TELEGRAM` | `geosite:telegram` |
| GeoSite | `YOUTUBE` | `geosite:youtube` |

Полный состав категорий и правил доступен в [geoip.txt](txt/geoip.txt) и [geosite.txt](txt/geosite.txt).

> jsDelivr кеширует файлы: новая версия может появиться с задержкой. Если нужно получить актуальный файл напрямую из репозитория, используйте ссылки на скачивание выше.

## Структура репозитория

| Папка | Содержимое |
| --- | --- |
| [`dat/`](dat/) | Готовые файлы маршрутизации для Happ |
| [`txt/`](txt/) | Исходные списки с категориями |
| [`scripts/`](scripts/) | Конвертер TXT → DAT |
| [`tests/`](tests/) | Проверки конвертера |

## Обновление списков

Редактируйте `txt/geoip.txt` или `txt/geosite.txt` и сохраняйте изменения в ветку `main`. GitHub Actions автоматически проверит списки, пересоберёт DAT и сохранит обновлённые файлы в `dat/`.

[Статус сборки](https://github.com/ALFiX01/NordLine-HappRouting/actions) · [Ручной запуск сборки](https://github.com/ALFiX01/NordLine-HappRouting/actions/workflows/build-dat.yml)

При ошибке в TXT сборка остановится с указанием строки; существующие DAT не заменяются.

### Формат исходников

Категория начинается с заголовка в квадратных скобках. Например, для GeoIP:

```text
[PRIVATE]
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
```

Для GeoSite:

```text
[TELEGRAM]
domain:telegram.org
domain:t.me
```

Поддерживаемые типы доменных правил:

| Тип | Сопоставление |
| --- | --- |
| `domain:` | Домен и его поддомены |
| `full:` | Точное имя домена |
| `plain:` | Подстрока в имени домена |
| `regex:` | Регулярное выражение |

Пустые строки и комментарии с `#` в начале пропускаются. Поддерживается UTF-8 с BOM и без него. Атрибуты доменов не поддерживаются.

### Локальная сборка

Требуется Python 3.10 или новее. Дополнительные пакеты не нужны.

```sh
python -m unittest discover -s tests -v
python scripts/build_dat.py
```
