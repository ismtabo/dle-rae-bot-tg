# RAE definitions telegram bot

This repository contains the code of a telegram bot for inline search of definitions for spanish words.
This definitions are obtained from RAE's [Diccionario de la lengua española](https://dle.rae.es/).

The bot is configured using the following environment variables:
| **Env Variable** | **Type** | **Description**                                                            |
| :--------------- | :------- | :------------------------------------------------------------------------- |
| `TG_TOKEN`       | `string` | Telegram token from @BotFather (remember not to commit this configuration) |
| `LOG_LEVEL`      | `string` | Logging level                                                              |

# Dependencies

- Python 3.8+
- Pipenv 2021.5.29+q

# Usage

Install dependencies

```sh
pipenv install
```

Run the bot

```sh
pipenv run python main.py
```

## Authors

- Ismael Taboada Rodero: [@ismtabo](https://github.com/ismtabo)

