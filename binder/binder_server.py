from xmlrpc.server import SimpleXMLRPCServer

class Binder:
    def __init__(self):
        self.procedures = {}

    def register_procedure(self, procedure_name, address, port):
        self.procedures[procedure_name] = (address, port)
        print(f"Procedure '{procedure_name}' registered at {address}:{port}")
        return True

    def lookup_procedure(self, procedure_name):
        return self.procedures.get(procedure_name, None)

def main():
    server = SimpleXMLRPCServer(("localhost", 5000))
    binder = Binder()
    server.register_function(binder.register_procedure, "register_procedure")
    server.register_function(binder.lookup_procedure, "lookup_procedure")
    print("Binder server running on port 5000...")
    server.serve_forever()

if __name__ == "__main__":
    main()
