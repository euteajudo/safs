"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface Usuario {
  id: number;
  nome: string;
  username: string;
  email: string;
  unidade: string;
  foto_url?: string;
  is_active: boolean;
  is_superuser: boolean;
  is_chefe_unidade: boolean;
  is_chefe_setor: boolean;
  is_funcionario: boolean;
  created_at: string;
  updated_at?: string;
}

interface AuthContextType {
  user: Usuario | null;
  setUser: (user: Usuario | null) => void;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<Usuario | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Verificar se há um usuário logado ao carregar a aplicação
  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('token');
      const savedUser = localStorage.getItem('user');
      
      if (token && savedUser) {
        try {
          const userData = JSON.parse(savedUser);
          setUser(userData);
        } catch (error) {
          console.error('Erro ao parser dados do usuário:', error);
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      const { loginApi } = await import('@/lib/api');
      const data = await loginApi(username, password);
      
      // Salvar no localStorage
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      // Também salvar o token em cookies para o middleware
      document.cookie = `token=${data.access_token}; path=/; max-age=86400`; // 24 horas
      
      setUser(data.user);
      
      return true;
    } catch (error) {
      console.error('Erro no login:', error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    // Remover cookie também
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    setUser(null);
    router.push('/login');
  };

  const isAuthenticated = !!user;

  return (
    <AuthContext.Provider value={{ 
      user, 
      setUser, 
      isLoading, 
      login, 
      logout, 
      isAuthenticated 
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

// Hook para facilitar o uso das permissões
export function useCurrentUser() {
  const { user } = useAuth();
  return user;
}