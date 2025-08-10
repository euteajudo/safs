"use client";

import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header-usuarios";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { useCurrentUser } from "@/contexts/auth-context";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { IconUser, IconEdit, IconLock } from "@tabler/icons-react";
import { useState } from "react";
import { PerfilFormDialog } from "@/components/perfil-form-dialog";

export default function PerfilPage() {
  const currentUser = useCurrentUser();
  const [showEditDialog, setShowEditDialog] = useState(false);

  if (!currentUser) {
    return (
      <SidebarProvider>
        <AppSidebar variant="inset" />
        <SidebarInset>
          <SiteHeader />
          <div className="flex flex-1 flex-col items-center justify-center p-8">
            <Card className="w-full max-w-md">
              <CardContent className="text-center p-6">
                <p className="text-muted-foreground">
                  Usuário não encontrado. Faça login novamente.
                </p>
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
              <div className="px-4 lg:px-6">
                <div className="max-w-4xl mx-auto space-y-6">
                  {/* Header */}
                  <div className="flex items-center justify-between">
                    <div>
                      <h1 className="text-2xl font-bold tracking-tight">Meu Perfil</h1>
                      <p className="text-muted-foreground">
                        Visualize e edite suas informações pessoais
                      </p>
                    </div>
                    <PerfilFormDialog
                      trigger={
                        <Button>
                          <IconEdit className="h-4 w-4 mr-2" />
                          Editar Perfil
                        </Button>
                      }
                      user={currentUser}
                    />
                  </div>

                  <div className="grid gap-6 md:grid-cols-2">
                    {/* Informações Pessoais */}
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                          <IconUser className="h-5 w-5" />
                          Informações Pessoais
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="flex items-center space-x-4">
                          <Avatar className="h-16 w-16">
                            <AvatarImage src={currentUser.foto_url} alt={currentUser.nome} />
                            <AvatarFallback className="text-lg">
                              {currentUser.nome.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()}
                            </AvatarFallback>
                          </Avatar>
                          <div className="space-y-1">
                            <h3 className="font-semibold text-lg">{currentUser.nome}</h3>
                            <p className="text-sm text-muted-foreground">@{currentUser.username}</p>
                          </div>
                        </div>
                        
                        <div className="space-y-3">
                          <div>
                            <label className="text-sm font-medium text-muted-foreground">Email</label>
                            <p className="text-sm">{currentUser.email}</p>
                          </div>
                          
                          <div>
                            <label className="text-sm font-medium text-muted-foreground">Unidade</label>
                            <div className="mt-1">
                              <Badge variant="outline" className={
                                currentUser.unidade === "ULOG" ? "text-orange-500 border-orange-500" :
                                currentUser.unidade === "UACE" ? "text-green-500 border-green-500" :
                                currentUser.unidade === "UPDE" ? "text-red-400 border-red-400" :
                                currentUser.unidade === "SAFS" ? "text-stone-950 border-stone-950 dark:text-stone-50 dark:border-stone-50" :
                                "text-gray-500 border-gray-500"
                              }>
                                {currentUser.unidade}
                              </Badge>
                            </div>
                          </div>
                          
                          <div>
                            <label className="text-sm font-medium text-muted-foreground">Status</label>
                            <div className="mt-1">
                              <Badge variant={currentUser.is_active ? "outline" : "secondary"} 
                                     className={currentUser.is_active ? "text-green-600 border-green-600" : "text-red-600 border-red-600"}>
                                {currentUser.is_active ? "Ativo" : "Inativo"}
                              </Badge>
                            </div>
                          </div>
                          
                          <div>
                            <label className="text-sm font-medium text-muted-foreground">Membro desde</label>
                            <p className="text-sm">{new Date(currentUser.created_at).toLocaleDateString('pt-BR')}</p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    {/* Permissões e Segurança */}
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                          <IconLock className="h-5 w-5" />
                          Permissões e Segurança
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div>
                          <label className="text-sm font-medium text-muted-foreground">Perfis de Acesso</label>
                          <div className="mt-2 flex flex-wrap gap-2">
                            {currentUser.is_superuser && (
                              <Badge variant="outline" className="text-purple-600 border-purple-600">
                                Superusuário
                              </Badge>
                            )}
                            {currentUser.is_chefe_unidade && (
                              <Badge variant="outline" className="text-blue-600 border-blue-600">
                                Chefe de Unidade
                              </Badge>
                            )}
                            {currentUser.is_chefe_setor && (
                              <Badge variant="outline" className="text-indigo-600 border-indigo-600">
                                Chefe de Setor
                              </Badge>
                            )}
                            {currentUser.is_funcionario && (
                              <Badge variant="outline" className="text-gray-600 border-gray-600">
                                Funcionário
                              </Badge>
                            )}
                            {!currentUser.is_superuser && !currentUser.is_chefe_unidade && !currentUser.is_chefe_setor && !currentUser.is_funcionario && (
                              <Badge variant="secondary">
                                Sem perfil específico
                              </Badge>
                            )}
                          </div>
                        </div>
                        
                        <div className="pt-4 border-t">
                          <p className="text-sm text-muted-foreground mb-3">
                            Para alterar sua senha ou foto, use o botão "Editar Perfil" acima.
                          </p>
                          <p className="text-xs text-muted-foreground">
                            <strong>Nota:</strong> Nome, email, username e perfis de acesso só podem ser alterados por um administrador do sistema.
                          </p>
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  {/* Estatísticas rápidas */}
                  <div className="grid gap-4 md:grid-cols-3">
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium">Itens Controlados</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="text-2xl font-bold text-primary">
                          {Math.floor(Math.random() * 100) + 10}
                        </div>
                        <p className="text-xs text-muted-foreground">
                          Itens sob sua responsabilidade
                        </p>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium">Processos Ativos</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="text-2xl font-bold text-primary">
                          {Math.floor(Math.random() * 25) + 5}
                        </div>
                        <p className="text-xs text-muted-foreground">
                          Processos em andamento
                        </p>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium">Última Atualização</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="text-sm font-medium">
                          {currentUser.updated_at ? 
                            new Date(currentUser.updated_at).toLocaleDateString('pt-BR') : 
                            "Nunca"}
                        </div>
                        <p className="text-xs text-muted-foreground">
                          Última vez que editou o perfil
                        </p>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}