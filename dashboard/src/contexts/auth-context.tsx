"use client";

import React, { createContext, useContext, useState } from "react";

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
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  // Mock user data - em produção isso viria da API/localStorage/cookies
  // TESTE: Configurado como SUPERUSUÁRIO para acesso completo ao sistema
  const [user, setUser] = useState<Usuario | null>({
    id: 1,
    nome: "João Silva Santos - Superintendente",
    username: "joao.silva", 
    email: "joao.silva@safs.gov.br",
    unidade: "SAFS", // Superusuário da SAFS
    foto_url: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
    is_active: true,
    is_superuser: true, // SUPERUSUÁRIO - pode fazer tudo
    is_chefe_unidade: true, // Também é chefe de unidade
    is_chefe_setor: false,
    is_funcionario: false,
    created_at: "2024-01-15T10:30:00Z",
    updated_at: "2024-02-10T14:22:00Z"
  });
  
  const [isLoading] = useState(false);

  return (
    <AuthContext.Provider value={{ user, setUser, isLoading }}>
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