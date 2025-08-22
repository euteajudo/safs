"use client";

import * as React from "react";
import { IconFolder, IconUsers } from "@tabler/icons-react";

import { NavMain } from "@/components/nav-main";
import { NavUser } from "@/components/nav-user";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { ChartNetwork } from "lucide-react";
import { NotebookText } from "lucide-react";
import { ShoppingCart } from "lucide-react";
import { ChartNoAxesColumnIncreasing } from "lucide-react";
import { useCurrentUser } from "@/contexts/auth-context";

const baseNavItems = [
  {
    title: "Página Inicial",
    url: "/dashboard",
    icon: ChartNetwork,
  },
  {
    title: "Catálogo SAFS",
    url: "/dashboard/catalogo",
    icon: NotebookText,
  },
  {
    title: "Processos de Planejamento",
    url: "/dashboard/processos",
    icon: IconFolder,
  },
  {
    title: "Controle de Empenhos",
    url: "/dashboard/empenhos",
    icon: ShoppingCart,
  },
  {
    title: "Usuários",
    url: "/dashboard/usuarios",
    icon: IconUsers,
    requiresAdminAccess: true,
  },
];

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const currentUser = useCurrentUser();
  
  // Mostrar todos os itens do menu - acesso livre
  const filteredNavItems = baseNavItems;

  const userData = {
    name: currentUser?.nome || "Usuário",
    email: currentUser?.email || "usuario@email.com", 
    avatar: currentUser?.foto_url || "https://via.placeholder.com/150",
  };

  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <a href="#">
                <ChartNoAxesColumnIncreasing className="!size-5" />
                <span className="text-base font-semibold">
                  Sistema de Gestão do SAFS
                </span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={filteredNavItems} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={userData} />
      </SidebarFooter>
    </Sidebar>
  );
}
