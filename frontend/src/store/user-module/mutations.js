export function setUser(state, { username }) {
    state.user = { username };
    state.isAuthenticated = true
  }
  
export function setUserType(state, userType) {
  state.userType = userType
}

export function setToken(state, token) {
    state.token = token;
  }
  
export function setAuthenticationResult(state, result) {
    state.authenticationResult = result;
  }

export function setIsAuthenticated(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated;
  }
  
// Zera tudo novamente para o state inicial
export function logout(state) {
    state.user = null;
    state.userType = null
    state.isAuthenticated = false;
    state.token = null;
    state.authenticationResult = '';

    function removeMultipleItems(items) {
      items.forEach(item => {
        sessionStorage.removeItem(item)
      });
    }

    removeMultipleItems(['situação', 'username', 'token', 'userType'])

  }

export function setSignupResult(state, result) {
  state.signupResult = result
}

export function setIsCreated(state, result) {
  state.isCreated = result
}
  