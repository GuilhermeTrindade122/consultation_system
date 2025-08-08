import redis
import psycopg2

# Conexão dos Bancos
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

conn = psycopg2.connect(
    host ='localhost',
    database ='db_redis',
    user = 'admin',
    password = 'admin' 
)

cursor = conn.cursor()


# Menu de Consulta
def menu():
    print('''
        ---Menu De Consultas de Produtos---
        1 - Buscar Produto por ID
        2 - Listar Produtos em cache
        3 Sair'
    ''')

opcao = '' 
while opcao != '3':
    menu()
    opcao = input("Digite a opção desejada: ")
    if opcao == '1':
        id_produto = input("Digite o ID do produto: ")
        produto = r.hgetall(id_produto)
        if produto:
            print(f"Produto encontrado no cache: {produto}")
        else:
            print("Produto não encontrado no cache. Buscando no banco de dados...")
            cursor.execute(f"SELECT nome,preco FROM produtos WHERE id = {id_produto}")
            resultado = cursor.fetchone()
            if resultado:
                print(f"Produto encontrado no banco de dados: Nome: {resultado[0]}, Preço: {resultado[1]}")
                r.hset(id_produto, mapping={
                    'nome': resultado[0],
                    'preco': str(resultado[1])
                })
                print(f"Produto adicionado ao cache.")
                r.expire(id_produto,60)
            else:
                print("Produto não encontrado no banco de dados.")
    elif opcao == '2':
        produtos_cache = r.keys('*')
        for nome_produto in produtos_cache:
            produto = r.hgetall(nome_produto)
            print(f"Nome: {produto['nome']}, Preço: {produto['preco']}")
    elif opcao == '3':
        print("Saindo do menu de consultas.")
        break
    else:
        print("Opção inválida. Tente novamente.")