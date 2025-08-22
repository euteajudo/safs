"use client";

import { AppSidebar } from "@/components/app-sidebar";
import { DataTable } from "@/components/data-table-catalogo";
import { SectionCards } from "@/components/section-cards-catalogo";
import { SiteHeader } from "@/components/site-header-catalogo";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { IconShieldX } from "@tabler/icons-react";
import { api } from "@/lib/api";
import { useState, useEffect } from "react";

// Interface para tipagem dos itens do catálogo
interface ItemCatalogo {
  id: number;
  unidade: string;
  descritivo_detalhado?: string;
  codigo_master: string;
  codigo_aghu_hu?: string;
  codigo_aghu_meac?: string;
  catmat?: string;
  codigo_ebserh?: string;
  descritivo_resumido: string;
  apresentacao?: string;
  classificacao_xyz?: string;
  responsavel_tecnico?: string;
  comprador_id?: number;
  controlador_id?: number;
  observacao?: string;
  comprador?: {
    id: number;
    nome: string;
    email: string;
  };
  controlador?: {
    id: number;
    nome: string;
    email: string;
  };
}

export default function Page() {
  const [itens, setItens] = useState<ItemCatalogo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Função para buscar itens da API
  const fetchItens = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.get('/v1/catalogo/');
      setItens(data);
    } catch (err) {
      console.error('Erro ao buscar itens do catálogo:', err);
      setError(err instanceof Error ? err.message : 'Erro ao carregar itens do catálogo');
    } finally {
      setLoading(false);
    }
  };

  // Buscar itens ao carregar o componente
  useEffect(() => {
    fetchItens();
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
              <p className="mt-4 text-gray-600">Carregando itens do catálogo...</p>
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
                  onClick={fetchItens}
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
      style={{
        "--sidebar-width": "calc(var(--spacing) * 72)",
        "--header-height": "calc(var(--spacing) * 12)",
      } as React.CSSProperties}
    >
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader />
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
              <SectionCards />
              <div className="px-4 lg:px-6">
                <DataTable data={itens} onRefresh={fetchItens} />
              </div>
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
