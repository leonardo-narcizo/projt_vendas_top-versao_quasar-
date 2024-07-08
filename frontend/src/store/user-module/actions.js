export async function login({ commit }, { username, password }) {
    try {
      if (username == '' || password == '') {
        commit('setAuthenticationResult', 'Preencha os campos corretamente!')
        return
      }
      const { token, userType, message } = await authenticateUser(username, password);

      if (token) {
        // Atualizando os estados
        commit('setUser', { username });
        commit('setUserType', userType)
        commit('setToken', token);
        commit('setIsAuthenticated', true);  // Define como autenticado
      } else {
        commit('setIsAuthenticated', false);  // Define como não autenticado
      }

      commit('setAuthenticationResult', message);
    } catch (error) {
      console.error('[erro]: ', error);
      commit('setAuthenticationResult', 'Erro ao enviar os dados para API.');
      commit('setIsAuthenticated', false);  // Define como não autenticado
    }
}

async function authenticateUser(username, password) {
    let requestResult = '';
    try {
      const response = await fetch('http://localhost:5000/entrar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });
  
      const data = await response.json();
      requestResult = data.message;
  
      if (requestResult === "Autenticação bem-sucedida!") {
        sessionStorage.setItem('username', username);
        sessionStorage.setItem('token', data.token);
        sessionStorage.setItem('userType', data.user_type)
        return { token: data.token, message: requestResult, userType: data.userType };
      } else {
        // Retorna a mensagem de erro diretamente
        return { token: null,  message: requestResult };
      }
    } catch (err) {
      console.error('[erro]: ', err);
      requestResult = 'Erro ao enviar os dados para API.';
      return { token: null, message: requestResult };
    } finally {
      sessionStorage.setItem('situação', requestResult);
    }
}

export async function signup({ commit }, {username, password, cnpj}) {
  let signupResult = ''

  const requestPJ = {
    new_username: username,
    new_password: password,
    cnpj: cnpj
  }
  const requestPF = {
    new_username: username,
    new_password: password
  }

  // função especifica p essa action
  const choiceRequest = (req1, req2) => {
    if (cnpj != null) {
      return req1
    }
    else {
      return req2
    }
  }
  try {
    const response = await fetch('http://localhost:5000/criarConta', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: 
      JSON.stringify(choiceRequest(requestPJ, requestPF))
    })

    const data =  await response.json()
    signupResult = data.message

    if (signupResult === 'Usuário criado com sucesso!') {
      commit('setIsCreated', true)
    }
  }
  catch (err) {
    console.error('[erro]: ', err),
    signupResult = 'Erro ao enviar os dados ao servidor.'
  }
  finally {
    commit('setSignupResult', signupResult)
  }
}
  