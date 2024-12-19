import xmlrpc.server
import xmlrpc.client


class Binder:
    def __init__(self, host="localhost", port=5000):
        self.server = xmlrpc.server.SimpleXMLRPCServer((host, port),allow_none=True)
        self.procedures = {}
        self.server.register_function(self.register_procedure, "register_procedure")
        self.server.register_function(self.lookup_procedure, "lookup_procedure")
        print(f"Binder iniciado em {host}:{port}")

    def register_procedure(self, procedure_name, address, port):
        """Registra um procedimento com nome, IP e porta."""
        self.procedures[procedure_name] = (address, port)
        print(f"Registrado {procedure_name} -> {address}:{port}")
        return f"Procedimento '{procedure_name}' registrado com sucesso."

    def lookup_procedure(self, procedure_name):
        """Retorna endereço e porta do procedimento registrado."""
        return self.procedures.get(procedure_name, None)

    def run(self):
        """Executa o servidor do Binder."""
        self.server.serve_forever()

if __name__ == "__main__":
    binder = Binder()
    binder.run()
