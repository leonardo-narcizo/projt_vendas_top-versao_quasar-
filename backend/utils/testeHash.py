from db.db_config import conectar_db, Error
import bcrypt

### esse arquivo servirá para debug. Util caso alguma senha do banco esteja em texto cru
### ai esse arquivo tem a finalidade de mudar essa senha, p hasheada, usando o bcrypt


# Função para gerar o hash bcrypt da senha
def gerar_hash_bcrypt(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Função para atualizar a senha de todos os usuários dentro do intervalo de IDs fornecido
def atualizar_senha_usuario(user_id1, user_id2):
    conexao_db, cursor = conectar_db()
    if conexao_db and cursor:
        try:
            # Seleciona os IDs e senhas em texto claro dos usuários dentro do intervalo especificado
            cursor.execute("SELECT id, password FROM usuarios WHERE id BETWEEN %s AND %s", (user_id1, user_id2))
            usuarios = cursor.fetchall()

            for usuario in usuarios:
                user_id = usuario[0]
                plain_password = usuario[1]
                
                # Gera o hash bcrypt para a senha em texto claro
                hashed_password = gerar_hash_bcrypt(plain_password)

                # Atualiza a senha no banco de dados
                cursor.execute("UPDATE usuarios SET password = %s, is_hashed = 'hashed' WHERE id = %s", (hashed_password, user_id))
                print(f"Senha do usuário com ID {user_id} atualizada com sucesso.")

            conexao_db.commit()

        except Error as e:
            print(f"Erro ao executar a atualização: {e}")

        finally:
            if conexao_db.is_connected():
                cursor.close()
                conexao_db.close()

# Exemplo de uso
if __name__ == "__main__":
    # Suponha que você queira atualizar as senhas dos usuários com IDs de 1 a 5
    atualizar_senha_usuario(22, 83)
