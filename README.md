# Projeto Dundie Rewards

[![CI](https://github.com/rochacbruno/dundie-rewards/actions/workflows/main.yml/badge.svg)](https://github.com/rochacbruno/dundie-rewards/actions/workflows/main.yml)

Nós fomos contratados pela Dunder Mifflin, grande fabricante de papéis para desenvolver um sistema
de recompensas para seus colaboradores.

Michael, o gerente da empresa quer aumentar a motivação dos funcionários oferecendo um sistema
de pontos que os funcionários podem acumular de acordo com as suas metas atingidas, bonus oferecidos
pelo gerente e os funcionários podem também trocam pontos entre sí.

O funcionário pode uma vez a cada ano resgatar seus pontos em um cartão de crédito para gastar onde
quiserem.

Acordamos em contrato que o MVP (Minimum Viable Product) será uma versão para ser executada no terminal
e que no futuro terá também as interfaces UI, web e API.

Os dados dos funcionários atuais serão fornecidos em um arquivo que pode ser no formato .csv ou .json
e este mesmo arquivo poderá ser usado para versões futuras. `Nome, Depto, Cargo, Email`


## Installation

```py
pip install seunome-dundie
```

```py
pip install -e `.[dev]`
```

## Usage on CLI

```py
dundie --help
```

![](./assets/dundie.gif)


## Usage on desktop

```bash
dundie-app
```

https://github.com/user-attachments/assets/3ba418ac-7ac8-4bc8-a0ee-615eaec7f431


## Usage on web browser

```bash
dundie-app --web
```

then open http://127.0.0.1:5000/

## Usage on Android or iOS


TIP: If running on a Mac you can replace `--android` with `--ios`

```bash
uv run flet run --android dundie/app.py

App is running on: http://192.168.1.132:8551/dundie/app.py

█████████████████████████████████████████
█████████████████████████████████████████
████ ▄▄▄▄▄ █   ▄█ █ ▀▄▄▄ ▀█ ▀█ ▄▄▄▄▄ ████
████ █   █ █▀█ ▄ █▀█▀▄ ▀▄ █ ▄█ █   █ ████
████ █▄▄▄█ ███▄▄▄  ██▄ ▀▄▄ ▄ █ █▄▄▄█ ████
████▄▄▄▄▄▄▄█ ▀▄█ ▀ █▄▀▄█▄█ ▀ █▄▄▄▄▄▄▄████
████ █  ▀▄▄▄█ ▀██▄██▀  ▀█▄█ ██ ▀█ ▀▄▄████
████▀▄▄█▄▀▄█▀▀█  ▀  ▀▄▄▀ ██ █ █ ▄ █ ▀████
██████ ▄▀ ▄█ ▀▀▄▄██▄▀▀ █ ▄▀▀█▄ ██▄█ ▄████
█████▀    ▄█   ▀▄ ▄▄ █▄▄▀▀██ ▀ ▀▀█ ██████
█████  ▄▀▀▄▀▄▀█▄▀█▄  ▀ ▄▀ ▀▀   █  ▄█▀████
████▄▀▄▀ ▀▄▄▀█▄▀█ ▀▄█ ██▄██▀ ▀▀▄ █▄██████
████ █▄ ▀ ▄ ▄ ▄▄█ █▀██ ▄ █▀█▄█▀█ ▄ █▀████
█████▀▄▄█▄▄ ▀█▀█  ██ █▄▀▄▄  ▄█▄▄█ ▄ ▄████
████▄█▄▄█▄▄█▀▀▄ ▀▀█▄▄ ▄ █▀▄▀ ▄▄▄  █▀▄████
████ ▄▄▄▄▄ █ ▄ █▄▄▀▄▀█▀▄▀▀   █▄█ ▀▀▀▀████
████ █   █ █▀  ▀ ▄ ██▄█ ▀█ ▄ ▄▄ ▄▀▄██████
████ █▄▄▄█ █▄█▀▀▄▀▄▀▀█▄  █▄ ██  ▀  █▀████
████▄▄▄▄▄▄▄█▄▄███▄█▄█▄███▄██████▄████████
█████████████████████████████████████████
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

Install `flet` app on your mobile and then scan the QRCode, your computer and phone must be in the same Wifi network.

More on https://flet.dev/docs/publish