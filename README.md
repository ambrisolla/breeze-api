# breeze-api

My personal rest API.

## prerequisites

- external MySQL database;
- docker;

## Features

- token authentication;
- personal budget control;

## How to use

Clone this repo:
```bash
$ git clone git@github.com:ambrisolla/brisa-api.git
cd brisa-api
docker-compose -d up
```

## Database configuration

```sql
CREATE TABLE `budget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` varchar(45) DEFAULT NULL,
  `_type` varchar(45) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `description` varchar(512) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6116 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `budget_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `_type` varchar(10) DEFAULT NULL,
  `uid` varchar(45) DEFAULT NULL,
  `color` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `user_token` (
  `uid` varchar(255) NOT NULL,
  `token` varchar(128) DEFAULT NULL,
  `token_birth` datetime DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `user_id_UNIQUE` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

```

