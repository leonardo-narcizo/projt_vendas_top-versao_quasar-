export function getIsAuthenticated(state) {
    return state.isAuthenticated;
}
  
  export function getAuthenticationResult(state) {
    return state.authenticationResult;
}
  
export function getLogoutUser(state) {
  return state // Retorna todo o objeto de 'state'
}

export function getSignupResult(state) {
  return state.signupResult
}

export function getIsCreated(state) {
  return state.isCreated
}

export function getUserType(state) {
  return state.userType
}