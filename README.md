# Chat Server and Client with Binder Registration

Este projeto implementa um servidor de chat com registro e descoberta de procedimentos utilizando o Binder, que mantém o controle de servidores de chat e seus procedimentos. O servidor de chat permite a criação de salas, registro de usuários, envio e recebimento de mensagens, e a visualização de usuários e salas disponíveis. A comunicação entre o cliente e o servidor é feita via XML-RPC.

## Estrutura do Projeto

1. **Binder (Servidor de Registro de Procedimentos)**:

   - O `Binder` mantém um servidor que registra e retorna procedimentos e suas respectivas localizações (endereço e porta).
   - O `Binder` permite que os outros servidores registrem seus métodos e os clientes os descubram via chamadas remotas.

2. **Chat Server (Servidor de Chat)**:

   - O servidor de chat permite a criação de salas, registro de usuários e comunicação entre os usuários (mensagens privadas e de transmissão).
   - Possui mecanismos de monitoramento de inatividade e remoção de salas vazias.
   - Oferece métodos para enviar e receber mensagens em tempo real.

3. **Chat Client (Cliente de Chat)**:
   - O cliente permite aos usuários se registrar, se conectar a salas de chat, enviar e receber mensagens em tempo real.
   - O cliente interage com o servidor usando comandos simples via terminal, como criar salas, listar salas, enviar mensagens e visualizar usuários.

## Funcionalidades

### Servidor de Chat:

- **Criação de Salas**: O servidor permite a criação de novas salas de chat.
- **Entrada e Saída de Usuários**: Usuários podem se conectar a salas e sair quando necessário.
- **Envio de Mensagens**: Suporte para envio de mensagens de transmissão (broadcast) ou privadas (unicast).
- **Recebimento de Mensagens**: Os clientes podem receber mensagens em tempo real.
- **Exclusão de Salas Vazias**: Salas sem usuários e sem interação por mais de 5 minutos são automaticamente removidas.

### Cliente de Chat:

- **Registro de Usuário**: O cliente permite o registro de um nome de usuário único.
- **Criação de Salas**: O cliente pode criar novas salas.
- **Entrada em Salas**: O cliente pode se conectar a salas de chat existentes.
- **Envio de Mensagens**: O cliente pode enviar mensagens para a sala (broadcast) ou para um usuário específico (unicast).
- **Recebimento de Mensagens em Tempo Real**: O cliente escuta constantemente por novas mensagens.
- **Listagem de Salas e Usuários**: O cliente pode listar salas disponíveis e os usuários conectados a uma sala.

## Como Rodar o Projeto

### 1. Iniciar o Binder

```bash
python binder.py
```

O `Binder` estará disponível por padrão na porta `5000`.

### 2. Iniciar o Servidor de Chat

Antes de rodar o servidor de chat, certifique-se de que o `Binder` está rodando. O servidor de chat registra os métodos no `Binder` e é acessado por clientes.

```bash
python chat_server.py
```

O servidor de chat estará disponível na porta `9000`.

### 3. Iniciar o Cliente de Chat

```bash
python chat_client.py
```

O cliente se conecta automaticamente ao servidor de chat via `Binder`. O cliente permite a interação através de comandos no terminal.

### Comandos do Cliente

- **create**: Cria uma nova sala de chat.
- **join**: Entra em uma sala existente.
- **send**: Envia uma mensagem para a sala ou para um usuário específico.
- **list**: Lista as salas de chat disponíveis.
- **users**: Lista os usuários conectados à sala atual.
- **exit**: Desconecta e encerra o cliente.

### Exemplos de Comandos:

- **Criar uma sala**: `create`
- **Entrar em uma sala**: `join`
- **Enviar uma mensagem**: `send`
- **Listar salas**: `list`
- **Listar usuários na sala atual**: `users`
- **Sair do chat**: `exit`

## Requisitos

- Python 3.x
- Biblioteca `xmlrpc.server` para comunicação via XML-RPC.
- Biblioteca `threading` para operações em segundo plano (escuta de mensagens em tempo real).
- Biblioteca `datetime` para manipulação de timestamps.
