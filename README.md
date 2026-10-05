# NordLine Happ Routing

Исходные списки находятся в `txt/`, готовые файлы для Happ — в `dat/`.

## Обновление

1. Измените `txt/geoip.txt` или `txt/geosite.txt` и сохраните в ветку `main`.
2. GitHub Actions проверит списки, соберёт DAT и сохранит обновлённые файлы отдельным коммитом.
3. Статус сборки: [Actions](https://github.com/ALFiX01/NordLine-HappRouting/actions).

Можно запустить сборку вручную: Actions → Build DAT → Run workflow.
Pull request проверяется без сохранения DAT в `main`.
Если TXT некорректен, сборка завершается с указанием строки, существующие DAT не заменяются.
Если ветка запрещает прямые коммиты от GitHub Actions, потребуется разрешить их или изменить процесс на PR.

## Формат TXT

Категории задаются заголовками `[DIRECT]`, `[PRIVATE]` и т. п.
В `geoip.txt` строки содержат IPv4/IPv6 адреса или CIDR.
В `geosite.txt` поддерживаются `domain:`, `full:`, `plain:`, `regex:`.
Пустые строки и комментарии, начинающиеся с `#`, пропускаются; UTF-8 BOM поддерживается.
Категории сохраняются в верхнем регистре. Атрибуты доменов не поддерживаются.
Конвертер обрабатывает два файла: `geoip.txt` и `geosite.txt`.

## Локальная сборка

Нужен Python 3.10 или новее, без дополнительных пакетов:

```sh
python -m unittest discover -s tests -v
python scripts/build_dat.py
```

DAT записываются в формате Protobuf GeoIPList / GeoSiteList, совместимом с Xray и Happ.

## Ссылки для Happ

GeoIP:

```text
https://cdn.jsdelivr.net/gh/ALFiX01/NordLine-HappRouting@main/dat/geoip.dat
```

GeoSite:

```text
https://cdn.jsdelivr.net/gh/ALFiX01/NordLine-HappRouting@main/dat/geosite.dat
```

После переноса старые ссылки без `/dat/` следует заменить.
jsDelivr может отдавать предыдущую версию из кеша. Прямые ссылки:

- https://raw.githubusercontent.com/ALFiX01/NordLine-HappRouting/main/dat/geoip.dat
- https://raw.githubusercontent.com/ALFiX01/NordLine-HappRouting/main/dat/geosite.dat
