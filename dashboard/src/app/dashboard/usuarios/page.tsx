"use client";

import { AppSidebar } from "@/components/app-sidebar";
import { DataTable } from "@/components/data-table-usuarios";
import { SectionCards } from "@/components/section-cards-usuarios";
import { SiteHeader } from "@/components/site-header-usuarios";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { useCurrentUser } from "@/contexts/auth-context";
import { canAccessUserManagement, filterUsersByPermissions } from "@/lib/permissions";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { IconShieldX } from "@tabler/icons-react";
import { api } from "@/lib/api";
import { useState, useEffect } from "react";

// Interface para tipagem dos usuários
interface User {
  id: number;
  unidade: string;
  nome: string;
  username: string;
  email: string;
  foto_url?: string;
  is_active: boolean;
  is_superuser: boolean;
  is_chefe_unidade: boolean;
  is_chefe_setor: boolean;
  is_funcionario: boolean;
  created_at: string;
  updated_at?: string;
}

export default function Page() {
  const currentUser = useCurrentUser();
  const [usuarios, setUsuarios] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Função para buscar usuários da API
  const fetchUsuarios = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.get('/v1/users/');
      setUsuarios(data);
    } catch (err) {
      console.error('Erro ao buscar usuários:', err);
      setError(err instanceof Error ? err.message : 'Erro ao carregar usuários');
    } finally {
      setLoading(false);
    }
  };

  // Buscar usuários ao carregar o componente
  useEffect(() => {
    fetchUsuarios();
  }, []);

  // Mostrar loading
  if (loading) {
    return (
      <SidebarProvider
        style={{
          "--sidebar-width": "calc(var(--spacing) * 72)",
          "--header-height": "calc(var(--spacing) * 12)",
        } as React.CSSProperties}
      >
        <AppSidebar variant="inset" />
        <SidebarInset>
          <SiteHeader />
          <div className="flex flex-1 flex-col items-center justify-center">
            <div className="text-center">
              <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary mx-auto"></div>
              <p className="mt-4 text-gray-600">Carregando usuários...</p>
            </div>
          </div>
        </SidebarInset>
      </SidebarProvider>
    );
  }

  // Mostrar erro se houver
  if (error) {
    return (
      <SidebarProvider
        style={{
          "--sidebar-width": "calc(var(--spacing) * 72)",
          "--header-height": "calc(var(--spacing) * 12)",
        } as React.CSSProperties}
      >
        <AppSidebar variant="inset" />
        <SidebarInset>
          <SiteHeader />
          <div className="flex flex-1 flex-col items-center justify-center">
            <Card className="max-w-md">
              <CardHeader>
                <CardTitle className="text-red-600 flex items-center gap-2">
                  <IconShieldX className="h-5 w-5" />
                  Erro ao Carregar
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-4">{error}</p>
                <button 
                  onClick={fetchUsuarios}
                  className="w-full bg-primary text-white px-4 py-2 rounded hover:bg-primary/90"
                >
                  Tentar Novamente
                </button>
              </CardContent>
            </Card>
          </div>
        </SidebarInset>
      </SidebarProvider>
    );
  }

  return (
    <SidebarProvider
      style={
        {
          "--sidebar-width": "calc(var(--spacing) * 72)",
          "--header-height": "calc(var(--spacing) * 12)",
        } as React.CSSProperties
      }
    >
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader />
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
              <SectionCards />
              <div className="px-4 lg:px-6">
                <DataTable data={usuarios} onRefresh={fetchUsuarios} />
              </div>
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
