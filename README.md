# merge-logs-migrator
## - DB migration and merge-logs tool written in python3.


## 1. Merge logs

JSONL format, timestamp in ascending order:
```sh
{"timestamp": "2021-02-26 08:59:20", "log_level": "INFO", "message": "Hello"}
{"timestamp": "2021-02-26 09:01:14", "log_level": "INFO", "message": "Crazy"}
{"timestamp": "2021-02-26 09:03:36", "log_level": "INFO", "message": "World!"}
```

## Usage

```sh
merge_logs.py <path/to/log1> <path/to/log2> -o <path/to/merged/log>
```


## 2. DB migration

План миграции:

1. Добавляем колонку (безопасная операция, не создает блокировок).
```sh
ALTER TABLE old_table ADD COLUMN name_id IF NOT EXISTS;

ALTER TABLE ADD CONSTRAINT FOREIGN KEY — небезопасная операция,
```
но можно объявить как NOT VALID и потом сделать ALTER TABLE VALIDATE CONSTRAINT.</br>
и позволит избежать блокировок.

```sh
CREATE TABLE name IF NOT EXISTS (
	id serial PRIMARY KEY,
	name VARCHAR ( 50 ) UNIQUE NOT NULL );
```

2. Написать откат и изменение бизнес логики с новой column и таблицей ( deploy )</br>
проверить состояние бд с помощью объекта MetaData в python.


3. Перезаписываем данные из старой колонки в новую. используем триггер или скрипт</br>
Все изменения делать батчами (batch insert, batch update).


4. Проблему с клиентами service A и B можно решить -</br>
сначала работа сервиса осуществляется через новый столбик,</br> 
а в случае эксепшена - через старый.
   
   Новые данные записываются уже правильно, без необходимости обновления.</br>
   Обновить клиенты service A и B по одному и перезапустить.


5. Удаление column


6. добавить Stairway test


```sh
./migrator.py migrate -host 127.0.0.1 -u username -p password -db test
```

Supported commands
- `generate migration [migrationName]` &mdash; Create up and down migration files, 
  provide an optional name
- `migrate` &mdash; Run migration on given server
  provide server connection details specified below
- `rollback` &mdash; Rollback the server to the previous migration
- `version` &mdash; Get the current version your server has migrated to
