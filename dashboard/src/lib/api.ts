/**
 * Utilitário para fazer requisições autenticadas para a API
 */

// URL da API - usar proxy do Next.js para evitar problemas de CORS
const BASE_URL = '/api/backend';

// Função para obter o token do localStorage
const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

// Configuração padrão para requisições autenticadas
const getAuthHeaders = (): HeadersInit => {
  const token = getToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  
  return headers;
};

// Função auxiliar para lidar com erros de resposta
const handleResponse = async (response: Response) => {
  if (!response.ok) {
    // Se o token expirou (401), redirecionar para login
    if (response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
      throw new Error('Sessão expirada');
    }
    
    let errorMessage;
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorData.message || 'Erro na requisição';
    } catch {
      errorMessage = `Erro ${response.status}: ${response.statusText}`;
    }
    
    throw new Error(errorMessage);
  }
  
  // Para respostas 204 (No Content), retornar null ao invés de tentar fazer JSON parse
  if (response.status === 204) {
    return null;
  }
  
  // Para outras respostas, tentar fazer JSON parse
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return response.json();
  }
  
  // Se não for JSON, retornar texto
  return response.text();
};

// Função para obter a URL base dinamicamente
const getApiUrl = () => {
  // SOLUÇÃO DE EMERGÊNCIA: Usar proxy do Next.js
  const apiUrl = BASE_URL; // '/api/backend' - proxy para localhost:8000
  
  console.log('🎯 URL da API (via proxy):', apiUrl);
  return apiUrl;
};

// Funções para fazer requisições autenticadas
export const api = {
  // GET request
  get: async (endpoint: string) => {
    const url = getApiUrl();
    const fullUrl = `${url}${endpoint}`;
    const headers = getAuthHeaders();
    
    console.log('🔄 GET Request:', {
      endpoint,
      fullUrl,
      headers: { ...headers, Authorization: headers.Authorization ? '[TOKEN PRESENT]' : '[NO TOKEN]' }
    });
    
    try {
      const response = await fetch(fullUrl, {
        method: 'GET',
        headers,
      });
      
      console.log('📥 GET Response:', {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok,
        headers: Object.fromEntries(response.headers.entries())
      });
      
      return handleResponse(response);
    } catch (error) {
      console.error('❌ GET Request Failed:', {
        endpoint,
        fullUrl,
        error: error.message,
        stack: error.stack
      });
      throw error;
    }
  },

  // POST request
  post: async (endpoint: string, data?: any) => {
    const url = getApiUrl();
    const fullUrl = `${url}${endpoint}`;
    const headers = getAuthHeaders();
    
    console.log('🔄 POST Request:', {
      endpoint,
      fullUrl,
      headers: { ...headers, Authorization: headers.Authorization ? '[TOKEN PRESENT]' : '[NO TOKEN]' },
      data: data ? JSON.stringify(data, null, 2) : 'No data'
    });
    
    try {
      const response = await fetch(fullUrl, {
        method: 'POST',
        headers,
        body: data ? JSON.stringify(data) : undefined,
      });
      
      console.log('📥 POST Response:', {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok,
        headers: Object.fromEntries(response.headers.entries())
      });
      
      return handleResponse(response);
    } catch (error) {
      console.error('❌ POST Request Failed:', {
        endpoint,
        fullUrl,
        error: error.message,
        stack: error.stack,
        data
      });
      throw error;
    }
  },

  // PUT request
  put: async (endpoint: string, data?: any) => {
    const url = getApiUrl();
    const response = await fetch(`${url}${endpoint}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: data ? JSON.stringify(data) : undefined,
    });
    return handleResponse(response);
  },

  // PATCH request
  patch: async (endpoint: string, data?: any) => {
    const url = getApiUrl();
    const response = await fetch(`${url}${endpoint}`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: data ? JSON.stringify(data) : undefined,
    });
    return handleResponse(response);
  },

  // DELETE request
  delete: async (endpoint: string) => {
    const url = getApiUrl();
    const response = await fetch(`${url}${endpoint}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // POST com FormData (para uploads)
  postFormData: async (endpoint: string, formData: FormData) => {
    const token = getToken();
    const headers: HeadersInit = {};
    
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
    
    const url = getApiUrl();
    const response = await fetch(`${url}${endpoint}`, {
      method: 'POST',
      headers,
      body: formData,
    });
    return handleResponse(response);
  },
};

// Função específica para login (não requer autenticação)
export const loginApi = async (username: string, password: string) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const url = getApiUrl();
  const response = await fetch(`${url}/v1/token`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Erro no login');
  }

  return response.json();
};