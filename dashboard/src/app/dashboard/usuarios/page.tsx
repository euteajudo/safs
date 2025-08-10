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

// Mock data para demonstração - substituir por dados reais da API
const mockUsuarios = [
  // SAFS
  {
    id: 1,
    unidade: "SAFS",
    nome: "João Silva Santos - Superintendente",
    username: "joao.silva",
    email: "joao.silva@safs.gov.br",
    foto_url: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
    is_active: true,
    is_superuser: true,
    is_chefe_unidade: true,
    is_chefe_setor: false,
    is_funcionario: false,
    created_at: "2024-01-15T10:30:00Z",
    updated_at: "2024-02-10T14:22:00Z"
  },
  {
    id: 2,
    unidade: "SAFS",
    nome: "Patricia Costa Silva",
    username: "patricia.costa",
    email: "patricia.costa@safs.gov.br",
    is_active: true,
    is_superuser: false,
    is_chefe_unidade: false,
    is_chefe_setor: false,
    is_funcionario: true,
    created_at: "2024-01-20T09:15:00Z",
    updated_at: "2024-02-05T16:45:00Z"
  },

  // UACE
  {
    id: 3,
    unidade: "UACE",
    nome: "Maria Oliveira Costa - Chefe UACE",
    username: "maria.oliveira",
    email: "maria.oliveira@safs.gov.br",
    foto_url: "https://images.unsplash.com/photo-1494790108755-2616b332e234?w=150&h=150&fit=crop&crop=face",
    is_active: true,
    is_superuser: false,
    is_chefe_unidade: true,
    is_chefe_setor: false,
    is_funcionario: false,
    created_at: "2024-01-20T09:15:00Z",
    updated_at: "2024-02-05T16:45:00Z"
  },
  {
    id: 4,
    unidade: "UACE",
    nome: "Roberto Almeida Souza",
    username: "roberto.almeida",
    email: "roberto.almeida@safs.gov.br",
    foto_url: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
    is_active: true,
    is_superuser: false,
    is_chefe_unidade: false,
    is_chefe_setor: true,
    is_funcionario: false,
    created_at: "2024-01-18T14:00:00Z",
    updated_at: "2024-02-12T09:25:00Z"
  },
  {
    id: 5,
    unidade: "UACE",
    nome: "Fernanda Santos Lima",
    username: "fernanda.santos",
    email: "fernanda.santos@safs.gov.br",
    is_active: true,
    is_superuser: false,
    is_chefe_unidade: false,
    is_chefe_setor: false,
    is_funcionario: true,
    created_at: "2024-02-01T11:20:00Z",
    updated_at: "2024-02-15T13:30:00Z"
  },

  // UPDE
  {
    id: 6,
    unidade: "UPDE",
    nome: "Carlos Eduardo Lima - Chefe UPDE",
    username: "carlos.lima",
    email: "carlos.lima@safs.gov.br",
    foto_url: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
    is_active: true,
    is_superuser: false,
    is_chefe_unidade: true,
    is_chefe_setor: false,
    is_funcionario: false,
    created_at: "2024-02-01T11:20:00Z",
    updated_at: "2024-02-15T13:30:00Z"
  },
  {
    id: 7,
    unidade: "UPDE",
    nome: "Monica Pereira Santos",
    username: "monica.pereira",
    email: "monica.pereira@safs.gov.br",
    is_active: true,
    is_superuser: false,
    is_chefe_unidade: false,
    is_chefe_setor: false,
    is_funcionario: true,
    created_at: "2024-02-10T08:30:00Z",
    updated_at: "2024-02-20T10:45:00Z"
  },

  // ULOG
  {
    id: 8,
    unidade: "ULOG",
    nome: "Ana Paula Ferreira - Chefe ULOG",
    username: "ana.ferreira",
    email: "ana.ferreira@safs.gov.br",
    is_active: true,
    is_superuser: false,
    is_chefe_unidade: true,
    is_chefe_setor: false,
    is_funcionario: false,
    created_at: "2024-01-10T08:45:00Z",
    updated_at: "2024-01-25T12:10:00Z"
  },
  {
    id: 9,
    unidade: "ULOG",
    nome: "Ricardo Mendes Costa",
    username: "ricardo.mendes",
    email: "ricardo.mendes@safs.gov.br",
    is_active: false,
    is_superuser: false,
    is_chefe_unidade: false,
    is_chefe_setor: false,
    is_funcionario: true,
    created_at: "2024-01-15T14:20:00Z",
    updated_at: "2024-01-30T16:30:00Z"
  }
];

export default function Page() {
  const currentUser = useCurrentUser();
  const hasAccess = canAccessUserManagement(currentUser);
  
  // Filtrar usuários baseado nas permissões do usuário atual
  const filteredUsers = filterUsersByPermissions(currentUser, mockUsuarios);

  // Componente de acesso negado
  if (!hasAccess) {
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
          <div className="flex flex-1 flex-col items-center justify-center p-8">
            <Card className="w-full max-w-md">
              <CardHeader className="text-center">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-red-100 dark:bg-red-900">
                  <IconShieldX className="h-8 w-8 text-red-600 dark:text-red-400" />
                </div>
                <CardTitle className="text-xl font-semibold">Acesso Negado</CardTitle>
              </CardHeader>
              <CardContent className="text-center space-y-4">
                <p className="text-muted-foreground">
                  Você não possui permissão para acessar a gestão de usuários.
                </p>
                <p className="text-sm text-muted-foreground">
                  Esta funcionalidade é restrita aos perfis: <strong>Superusuário</strong>, <strong>Chefe de Unidade</strong> ou <strong>Chefe de Setor</strong>.
                </p>
                <div className="pt-4">
                  <a 
                    href="/dashboard" 
                    className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
                  >
                    Voltar ao Dashboard
                  </a>
                </div>
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
                <DataTable data={filteredUsers} />
              </div>
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
