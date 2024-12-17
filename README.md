### **1. Estrutura do Projeto**

O projeto está organizado da seguinte maneira:

```bash
chat_rpc/
│
├── binder/                 # Binder Centralizado para registro e descoberta dos métodos RPC
│   └── binder_server.py    # Código principal do binder
│
├── server/                 # Servidor principal do chat
│   ├── chat_server.py      # Servidor que gerencia salas, usuários e mensagens
│   ├── room_manager.py     # Classe para gerenciar salas
│   ├── message_manager.py  # Classe para gerenciar mensagens
│   └── __init__.py         # Inicializador do pacote server
│
├── client/                 # Cliente que interage com o servidor
│   ├── chat_client.py      # Código principal do cliente
│   └── client_interface.py # Interface para o usuário no terminal
│
├── README.md               # Documentação do projeto
└── requirements.txt        # Dependências necessárias
```

---

### **2. Descrição dos Códigos**

#### **2.1 Binder (`binder/binder_server.py`)**

O **Binder** é um servidor centralizado que gerencia o registro e a descoberta dos métodos RPC. Ele utiliza a biblioteca `xmlrpc.server` para expor métodos aos clientes e ao servidor.

**Métodos Disponíveis:**

- `register_procedure(procedure_name, address, port)`:  
  Registra um método remoto com um nome, endereço IP e porta.
- `lookup_procedure(procedure_name)`:  
  Retorna o endereço e a porta associados ao método remoto.

**Execução:**

```bash
python binder/binder_server.py
```

O binder roda na porta **5000**.

---

#### **2.2 Servidor (`server/`)**

O servidor gerencia salas, usuários e mensagens do chat. Ele se comunica com o **Binder** para registrar seus métodos RPC e expô-los aos clientes.

##### **2.2.1 `chat_server.py`**

- **Funções Principais:**
  - `create_room(room_name)`: Cria uma sala nova.
  - `join_room(username, room_name)`: Adiciona um usuário em uma sala existente.
  - `send_message(username, room_name, message, recipient=None)`:  
    Envia mensagens públicas (broadcast) ou privadas (unicast).
  - `receive_messages(username, room_name)`: Retorna mensagens destinadas ao usuário.
  - `list_rooms()`: Lista todas as salas ativas.
  - `list_users(room_name)`: Mostra os usuários conectados em uma sala.

##### **2.2.2 `room_manager.py`**

Gerencia as salas e seus estados.

- **Métodos:**
  - `create_room(room_name)`: Cria uma sala.
  - `join_room(username, room_name)`: Adiciona um usuário na lista de conectados.
  - `list_users(room_name)`: Retorna os usuários de uma sala.
  - `clean_inactive_rooms(timeout_minutes=5)`: Remove salas inativas.

##### **2.2.3 `message_manager.py`**

Gerencia o histórico de mensagens.

- **Métodos:**
  - `add_message(room_data, username, content, recipient=None)`:  
    Adiciona uma mensagem (broadcast ou unicast).
  - `get_messages_for_user(room_data, username)`:  
    Filtra mensagens públicas e privadas para o usuário.

**Execução:**

```bash
python server/chat_server.py
```

O servidor roda na porta **8000**.

---

#### **2.3 Cliente (`client/`)**

O cliente permite a interação do usuário com o sistema de chat.

##### **2.3.1 `chat_client.py`**

Gerencia a comunicação com o **Binder** e o servidor RPC. O cliente permite:

- Registrar o usuário com um **username**.
- Criar e entrar em salas.
- Enviar mensagens (broadcast ou unicast).
- Listar salas e usuários.
- Buscar mensagens periodicamente a cada **2 segundos**.

##### **2.3.2 `client_interface.py`**

Responsável pela interface no terminal. Define os comandos disponíveis:

- `create [room_name]`: Cria uma nova sala.
- `join [room_name]`: Entra em uma sala existente.
- `send [mensagem]`: Envia uma mensagem para todos (broadcast).
- `send @username [mensagem]`: Envia uma mensagem privada (unicast).
- `list rooms`: Lista todas as salas ativas.
- `list users`: Lista os usuários na sala atual.
- `exit`: Encerra a conexão.

**Execução:**

```bash
python client/chat_client.py
```

---

### **3. Instalação e Execução**

#### **3.1 Pré-requisitos**

Instale as dependências com o comando:

```bash
pip install -r requirements.txt
```

**Arquivo `requirements.txt`:**

```plaintext
xmlrpc
```

---

#### **3.2 Fluxo de Execução**

1. **Iniciar o Binder** (Porta 5000):

```bash
python binder/binder_server.py
```

2. **Iniciar o Servidor** (Porta 8000):

```bash
python server/chat_server.py
```

3. **Executar o Cliente**:

Em múltiplos terminais, inicie o cliente:

```bash
python client/chat_client.py
```

---

### **4. Comandos do Cliente**

- `create [nome_da_sala]` → Cria uma sala nova.
- `join [nome_da_sala]` → Entra em uma sala existente.
- `send [mensagem]` → Envia mensagem pública para todos os usuários da sala.
- `send @username [mensagem]` → Envia mensagem privada para um usuário específico.
- `list rooms` → Lista todas as salas ativas.
- `list users` → Lista os usuários conectados na sala atual.
- `exit` → Sai do sistema.

---

### **5. Observações Técnicas**

- As mensagens públicas (broadcast) têm um limite de **50 mensagens** armazenadas.
- Salas sem usuários conectados por mais de **5 minutos** são removidas automaticamente.
- O cliente busca mensagens novas do servidor a cada **2 segundos**.

---

### **6. Exemplo de Uso**

**Comandos em um cliente:**

```plaintext
Digite seu username: joao
Comandos disponíveis:
> create sala1
Sala 'sala1' criada com sucesso.
> join sala1
Usuário 'joao' entrou na sala 'sala1'.
> send Olá, pessoal!
Mensagem enviada.
> send @maria Oi, Maria!
Mensagem enviada para Maria.
> list rooms
Salas disponíveis: ['sala1']
> list users
Usuários na sala: ['joao']
> exit
```

---

### **7. Conclusão**

Este sistema de chat modular utiliza **RPC** em Python, com um **Binder Centralizado**, um servidor estruturado e um cliente simples e interativo. As classes auxiliares `RoomManager` e `MessageManager` garantem a organização do código e o gerenciamento eficiente de salas e mensagens.
