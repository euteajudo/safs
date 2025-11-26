"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import * as React from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
// import { Checkbox } from "@/components/ui/checkbox"; // Não utilizado
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";
import { api } from "@/lib/api";
import { testBackendConnection } from "@/lib/test-api";

const catalogoSchema = z.object({
  unidade: z.string().min(1, "Unidade é obrigatória").max(20),
  descritivo_detalhado: z.string().max(4000).optional().or(z.literal("")),
  codigo_master: z.string().min(1, "Código Master é obrigatório").max(20),
  codigo_aghu_hu: z.string().max(20).optional().or(z.literal("")),
  codigo_aghu_meac: z.string().max(20).optional().or(z.literal("")),
  catmat: z.string().max(20).optional().or(z.literal("")),
  codigo_ebserh: z.string().max(20).optional().or(z.literal("")),
  descritivo_resumido: z.string().min(1, "Descritivo resumido é obrigatório").max(300),
  apresentacao: z.string().max(100).optional().or(z.literal("")),
  classificacao_xyz: z.string().max(10).optional().or(z.literal("")),
  // responsavel_tecnico: z.string().max(100).optional().or(z.literal("")), // Removido para evitar conflito
  responsavel_tecnico_id: z.string().optional().or(z.literal("")),
  comprador_id: z.string().optional().or(z.literal("")),
  controlador_id: z.string().optional().or(z.literal("")),
  observacao: z.string().max(255).optional().or(z.literal("")),
});

type CatalogoFormValues = z.infer<typeof catalogoSchema>;

interface User {
  id: string;
  nome: string;
  email?: string;
}

interface Processo {
  id: string;
  numero: string;
  descricao?: string;
}

interface CatalogoFormDialogProps {
  trigger: React.ReactNode;
  item?: z.infer<typeof catalogoSchema> & { 
    id?: number; 
    processo?: Processo;
    processos_adicionais?: Processo[] 
  };
  mode?: "create" | "edit";
  onSuccess?: () => void;
}

export function CatalogoFormDialog({ trigger, item, mode = "create", onSuccess }: CatalogoFormDialogProps) {
  const [open, setOpen] = React.useState(false);
  const [isEditing, setIsEditing] = React.useState(mode === "create");
  const [compradores, setCompradores] = useState<User[]>([]);
  const [controladores, setControladores] = useState<User[]>([]);
  const [responsaveisTecnicos, setResponsaveisTecnicos] = useState<User[]>([]);
  const [, setProcessos] = useState<Processo[]>([]); // processos não usado diretamente
  const [loading, setLoading] = useState(false);
  
  const form = useForm<CatalogoFormValues>({
    resolver: zodResolver(catalogoSchema),
    defaultValues: item ? {
      unidade: item.unidade || "",
      descritivo_detalhado: item.descritivo_detalhado || "",
      codigo_master: item.codigo_master || "",
      codigo_aghu_hu: item.codigo_aghu_hu || "",
      codigo_aghu_meac: item.codigo_aghu_meac || "",
      catmat: item.catmat || "",
      codigo_ebserh: item.codigo_ebserh || "",
      descritivo_resumido: item.descritivo_resumido || "",
      apresentacao: item.apresentacao || "",
      classificacao_xyz: item.classificacao_xyz || "",
      // responsavel_tecnico: item.responsavel_tecnico || "", // Removido
      responsavel_tecnico_id: String(item.responsavel_tecnico_id || ""),
      comprador_id: String(item.comprador_id || ""),
      controlador_id: String(item.controlador_id || ""),
      observacao: item.observacao || "",
    } : {
      unidade: "SAFS",
      descritivo_detalhado: "",
      codigo_master: "",
      codigo_aghu_hu: "",
      codigo_aghu_meac: "",
      catmat: "",
      codigo_ebserh: "",
      descritivo_resumido: "",
      apresentacao: "",
      classificacao_xyz: "",
      // responsavel_tecnico: "", // Removido
      responsavel_tecnico_id: "",
      comprador_id: "",
      controlador_id: "",
      observacao: "",
    },
  });

  // Buscar dados quando o modal abrir e resetar estado de edição
  useEffect(() => {
    if (open) {
      fetchData();
      // Se estiver em modo edit, começa desabilitado
      if (mode === "edit") {
        setIsEditing(false);
      } else {
        // Se estiver em modo create, começa habilitado
        setIsEditing(true);
      }
    }
  }, [open, mode]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const { api } = await import('@/lib/api');
      
      // Buscar todos os usuários (compradores e controladores virão da mesma API)
      const users = await api.get('/v1/users?limit=1000');
      
      // Filtrar usuários por perfil (assumindo que existe uma flag para identificar)
      // Por enquanto, vamos mostrar todos os usuários ativos para ambos os campos
      const activeUsers = users.filter((user: User) => user.is_active);
      const userList = activeUsers.map((user: User) => ({
        id: user.id.toString(),
        nome: user.nome,
        email: user.email
      }));
      
      setCompradores(userList);
      setControladores(userList);
      setResponsaveisTecnicos(userList);

      // Buscar processos de aquisição
      const processos = await api.get('/v1/processos?limit=1000');
      setProcessos(processos.map((processo: Processo) => ({
        id: processo.id.toString(),
        numero: processo.numero_processo_planejamento,
        descricao: processo.objeto_aquisicao
      })));
    } catch (error) {
      console.error('Erro ao buscar dados do backend:', error);
      console.log('Usando dados mockados para desenvolvimento...');
      
      // Dados mockados para desenvolvimento quando o backend não estiver disponível
      setCompradores([
        { id: "1", nome: "João Silva", email: "joao@example.com" },
        { id: "2", nome: "Maria Santos", email: "maria@example.com" },
        { id: "3", nome: "Pedro Oliveira", email: "pedro@example.com" },
      ]);
      setControladores([
        { id: "4", nome: "Ana Costa", email: "ana@example.com" },
        { id: "5", nome: "Carlos Ferreira", email: "carlos@example.com" },
        { id: "6", nome: "Lucia Almeida", email: "lucia@example.com" },
      ]);
      setResponsaveisTecnicos([
        { id: "7", nome: "Roberto Lima", email: "roberto@example.com" },
        { id: "8", nome: "Patricia Souza", email: "patricia@example.com" },
        { id: "9", nome: "Fernando Dias", email: "fernando@example.com" },
      ]);
      setProcessos([
        { id: "1", numero: "23076.001234/2024-01", descricao: "Aquisição de Material Hospitalar" },
        { id: "2", numero: "23076.005678/2024-02", descricao: "Compra de Medicamentos" },
        { id: "3", numero: "23076.009012/2024-03", descricao: "Material de Escritório" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  async function onSubmit(values: CatalogoFormValues) {
    try {
      setLoading(true);
      
      // Preparar dados para envio - VERSÃO SIMPLIFICADA
      const submitData: Record<string, unknown> = {
        unidade: values.unidade,
        codigo_master: values.codigo_master,
        descritivo_resumido: values.descritivo_resumido
      };

      // Adicionar campos opcionais apenas se preenchidos
      if (values.descritivo_detalhado && values.descritivo_detalhado.trim()) {
        submitData.descritivo_detalhado = values.descritivo_detalhado.trim();
      }
      if (values.codigo_aghu_hu && values.codigo_aghu_hu.trim()) {
        submitData.codigo_aghu_hu = values.codigo_aghu_hu.trim();
      }
      if (values.codigo_aghu_meac && values.codigo_aghu_meac.trim()) {
        submitData.codigo_aghu_meac = values.codigo_aghu_meac.trim();
      }
      if (values.catmat && values.catmat.trim()) {
        submitData.catmat = values.catmat.trim();
      }
      if (values.codigo_ebserh && values.codigo_ebserh.trim()) {
        submitData.codigo_ebserh = values.codigo_ebserh.trim();
      }
      if (values.apresentacao && values.apresentacao.trim()) {
        submitData.apresentacao = values.apresentacao.trim();
      }
      if (values.classificacao_xyz && values.classificacao_xyz.trim()) {
        submitData.classificacao_xyz = values.classificacao_xyz.trim();
      }
      if (values.observacao && values.observacao.trim()) {
        submitData.observacao = values.observacao.trim();
      }

      // Tratar relacionamentos apenas se selecionados
      if (values.comprador_id && values.comprador_id.trim() && values.comprador_id !== "") {
        const compradorId = parseInt(values.comprador_id);
        if (!isNaN(compradorId) && compradorId > 0) {
          submitData.comprador_id = compradorId;
        }
      }

      if (values.controlador_id && values.controlador_id.trim() && values.controlador_id !== "") {
        const controladorId = parseInt(values.controlador_id);
        if (!isNaN(controladorId) && controladorId > 0) {
          submitData.controlador_id = controladorId;
        }
      }

      // RESPONSÁVEL TÉCNICO - Tratamento especial para evitar erros
      if (values.responsavel_tecnico_id && values.responsavel_tecnico_id.trim() && values.responsavel_tecnico_id !== "") {
        const responsavelId = parseInt(values.responsavel_tecnico_id);
        if (!isNaN(responsavelId) && responsavelId > 0) {
          // Enviar apenas o campo que o backend consegue processar
          submitData.responsavel_tecnico_id = responsavelId;
        }
      }
      
      // Log simplificado para debug
      console.log("📤 Dados sendo enviados:", {
        ...submitData,
        // Mascarar campos sensíveis se houver
        codigo_master: submitData.codigo_master
      });
      
      if (mode === "edit" && item?.id) {
        console.log("Editando item:", { ...submitData, id: item.id });
        const response = await api.patch(`/v1/catalogo/${item.id}`, submitData);
        console.log('Item editado com sucesso:', response);
        
        // Fechar modal
        setOpen(false);
        
        // Chamar callback para atualizar a lista se existir
        if (onSuccess) {
          onSuccess();
        }
      } else {
        console.log("Criando novo item:", submitData);
        console.log("JSON sendo enviado:", JSON.stringify(submitData));
        
        // Comentado - causava erro por não usar o proxy
        // await testBackendConnection();
        
        const response = await api.post('/v1/catalogo', submitData);
        console.log('Item criado com sucesso:', response);
        
        // Resetar formulário e fechar modal
        form.reset();
        setOpen(false);
        
        // Chamar callback para atualizar a lista se existir
        if (onSuccess) {
          onSuccess();
        }
      }
      
    } catch (error: unknown) {
      console.error('Erro completo ao salvar item:', error);
      const errorObj = error as Error;
      console.error('Tipo do erro:', errorObj?.name);
      console.error('Mensagem do erro:', errorObj?.message);
      if (errorObj?.stack) {
        console.error('Stack do erro:', errorObj.stack);
      }
      
      // Verificar se é erro de rede/CORS
      if (errorObj?.name === 'TypeError' && errorObj?.message?.includes('Failed to fetch')) {
        console.error('Erro de conexão com o backend. Verificando token...');
        const token = localStorage.getItem('token');
        console.log('Token presente:', !!token);
        if (token) {
          console.log('Token:', token.substring(0, 50) + '...');
        }
        alert('Erro de conexão com o servidor. Por favor, verifique se o backend está rodando e tente novamente.');
      } else {
        const errorMessage = errorObj?.message || 'Erro ao salvar item. Verifique os dados e tente novamente.';
        
        // Verificar se é erro de código master duplicado
        if (errorMessage.includes('já existe') || errorMessage.includes('duplicado')) {
          alert(`❌ Código Master já existe!\n\nO código "${values.codigo_master}" já está cadastrado no sistema. Por favor, use um código diferente.`);
        } else if (errorMessage.includes('ID de relacionamento inválido')) {
          alert(`❌ Erro de relacionamento!\n\nVerifique se os usuários selecionados (comprador, controlador, responsável técnico) são válidos.`);
        } else if (errorMessage.includes('Internal Server Error') || errorMessage.includes('500')) {
          alert(`❌ Erro interno do servidor!\n\nOcorreu um erro no servidor. Por favor:\n1. Verifique se todos os campos obrigatórios estão preenchidos\n2. Tente novamente em alguns segundos\n3. Se o problema persistir, contate o administrador`);
        } else {
          alert(`❌ Erro: ${errorMessage}`);
        }
      }
    } finally {
      setLoading(false);
    }
  }

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    if (item) {
      form.reset({
        unidade: item.unidade || "",
        descritivo_detalhado: item.descritivo_detalhado || "",
        codigo_master: item.codigo_master || "",
        codigo_aghu_hu: item.codigo_aghu_hu || "",
        codigo_aghu_meac: item.codigo_aghu_meac || "",
        catmat: item.catmat || "",
        codigo_ebserh: item.codigo_ebserh || "",
        descritivo_resumido: item.descritivo_resumido || "",
        apresentacao: item.apresentacao || "",
        classificacao_xyz: item.classificacao_xyz || "",
        // responsavel_tecnico: item.responsavel_tecnico || "", // Removido
        responsavel_tecnico_id: String(item.responsavel_tecnico_id || ""),
        comprador_id: String(item.comprador_id || ""),
        controlador_id: String(item.controlador_id || ""),
        observacao: item.observacao || "",
      });
    }
    setIsEditing(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[90vh]">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold">
            {mode === "edit" ? "Editar Item do Catálogo" : "Adicionar Novo Item ao Catálogo"}
          </DialogTitle>
          <DialogDescription>
            {mode === "edit" 
              ? `Editando item: ${item?.codigo_master} - ${item?.descritivo_resumido}`
              : "Preencha os campos abaixo para adicionar um novo item ao catálogo de itens do SAFS"}
          </DialogDescription>
        </DialogHeader>
        
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <ScrollArea className="h-[60vh] pr-4">
              <Tabs defaultValue="principal" className="w-full">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="principal">Informações Principais</TabsTrigger>
                  <TabsTrigger value="codigos">Códigos</TabsTrigger>
                  <TabsTrigger value="gestao">Gestão</TabsTrigger>
                </TabsList>

                <TabsContent value="principal" className="space-y-6 mt-6">
                  <Card>
                    <CardContent className="pt-6 space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <FormField
                          control={form.control}
                          name="unidade"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Unidade <span className="text-red-500">*</span>
                              </FormLabel>
                              <FormControl>
                                <Select 
                                  onValueChange={field.onChange} 
                                  defaultValue={field.value}
                                  disabled={!isEditing}
                                >
                                  <SelectTrigger className="focus:ring-2 focus:ring-primary">
                                    <SelectValue placeholder="Selecione a unidade" />
                                  </SelectTrigger>
                                  <SelectContent>
                                    <SelectItem value="ULOG">ULOG</SelectItem>
                                    <SelectItem value="UACE">UACE</SelectItem>
                                  </SelectContent>
                                </Select>
                              </FormControl>
                              <FormDescription className="text-xs">
                                Unidade responsável pelo item
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="classificacao_xyz"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">Classificação XYZ</FormLabel>
                              <Select onValueChange={field.onChange} defaultValue={field.value} disabled={!isEditing}>
                                <FormControl>
                                  <SelectTrigger className="focus:ring-2 focus:ring-primary">
                                    <SelectValue placeholder="Selecione a classificação" />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  <SelectItem value="X">
                                    <div className="flex items-center">
                                      <span className="font-semibold mr-2">X</span>
                                      <span>Alto valor/Alta rotatividade</span>
                                    </div>
                                  </SelectItem>
                                  <SelectItem value="Y">
                                    <div className="flex items-center">
                                      <span className="font-semibold mr-2">Y</span>
                                      <span>Médio valor/Média rotatividade</span>
                                    </div>
                                  </SelectItem>
                                  <SelectItem value="Z">
                                    <div className="flex items-center">
                                      <span className="font-semibold mr-2">Z</span>
                                      <span>Baixo valor/Baixa rotatividade</span>
                                    </div>
                                  </SelectItem>
                                </SelectContent>
                              </Select>
                              <FormDescription className="text-xs">
                                Classificação XYZ do item
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>

                      <FormField
                        control={form.control}
                        name="descritivo_resumido"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-sm font-semibold">
                              Descritivo Resumido <span className="text-red-500">*</span>
                            </FormLabel>
                            <FormControl>
                              <Textarea 
                                placeholder="Descreva resumidamente o item..." 
                                className="min-h-[80px] resize-none focus:ring-2 focus:ring-primary"
                                {...field} 
                                disabled={!isEditing}
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Descrição resumida do item (máx. 300 caracteres)
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={form.control}
                        name="descritivo_detalhado"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-sm font-semibold">
                              Descritivo Detalhado
                            </FormLabel>
                            <FormControl>
                              <Textarea 
                                placeholder="Descreva detalhadamente o item (opcional)..." 
                                className="min-h-[120px] resize-none focus:ring-2 focus:ring-primary"
                                {...field} 
                                disabled={!isEditing}
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Descrição completa e detalhada do item (opcional - máx. 4000 caracteres)
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />


                      <FormField
                        control={form.control}
                        name="apresentacao"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-sm font-semibold">Apresentação</FormLabel>
                            <FormControl>
                              <Input 
                                placeholder="Ex: Caixa com 100 unidades" 
                                className="focus:ring-2 focus:ring-primary"
                                {...field} 
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Forma de apresentação do item
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="codigos" className="space-y-6 mt-6">
                  <Card>
                    <CardContent className="pt-6 space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <FormField
                          control={form.control}
                          name="codigo_master"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Código Master <span className="text-red-500">*</span>
                              </FormLabel>
                              <FormControl>
                                <Input 
                                  placeholder="Ex: 569874" 
                                  className="focus:ring-2 focus:ring-primary"
                                  {...field} 
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Código do item no MASTER
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="catmat"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">CATMAT</FormLabel>
                              <FormControl>
                                <Input 
                                  placeholder="Código CATMAT" 
                                  className="focus:ring-2 focus:ring-primary"
                                  {...field} 
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Catálogo de Materiais do Governo
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <FormField
                          control={form.control}
                          name="codigo_aghu_hu"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">Código AGHU HU</FormLabel>
                              <FormControl>
                                <Input 
                                  placeholder="Código AGHU HU" 
                                  className="focus:ring-2 focus:ring-primary"
                                  {...field} 
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Código no sistema AGHU do Hospital Universitário
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="codigo_aghu_meac"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">Código AGHU MEAC</FormLabel>
                              <FormControl>
                                <Input 
                                  placeholder="Código AGHU MEAC" 
                                  className="focus:ring-2 focus:ring-primary"
                                  {...field} 
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Código no sistema AGHU da Maternidade
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>

                      <div className="w-1/2">
                      <FormField
                        control={form.control}
                        name="codigo_ebserh"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-sm font-semibold">Código EBSERH</FormLabel>
                            <FormControl>
                              <Input 
                                placeholder="Código EBSERH" 
                                className="focus:ring-2 focus:ring-primary"
                                {...field} 
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Código da Empresa Brasileira de Serviços Hospitalares
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="gestao" className="space-y-6 mt-6">
                  <Card>
                    <CardContent className="pt-6 space-y-4">
                      <div className="flex flex-col lg:flex-row lg:space-x-8 space-y-4 lg:space-y-0">
                        <FormField
                          control={form.control}
                          name="comprador_id"
                          render={({ field }) => (
                            <FormItem className="flex-1">
                              <FormLabel className="text-sm font-semibold">Comprador</FormLabel>
                              <Select 
                                onValueChange={field.onChange} 
                                defaultValue={field.value}
                                disabled={loading || !isEditing}
                              >
                                <FormControl>
                                  <SelectTrigger className="focus:ring-2 focus:ring-primary">
                                    <SelectValue placeholder={loading ? "Carregando..." : "Selecione o comprador"} />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  {compradores.map((comprador) => (
                                    <SelectItem key={comprador.id} value={comprador.id}>
                                      {comprador.nome}
                                    </SelectItem>
                                  ))}
                                </SelectContent>
                              </Select>
                              <FormDescription className="text-xs">
                                Responsável pela compra
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="controlador_id"
                          render={({ field }) => (
                            <FormItem className="flex-1">
                              <FormLabel className="text-sm font-semibold">Controlador</FormLabel>
                              <Select 
                                onValueChange={field.onChange} 
                                defaultValue={field.value}
                                disabled={loading || !isEditing}
                              >
                                <FormControl>
                                  <SelectTrigger className="focus:ring-2 focus:ring-primary">
                                    <SelectValue placeholder={loading ? "Carregando..." : "Selecione o controlador"} />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  {controladores.map((controlador) => (
                                    <SelectItem key={controlador.id} value={controlador.id}>
                                      {controlador.nome}
                                    </SelectItem>
                                  ))}
                                </SelectContent>
                              </Select>
                              <FormDescription className="text-xs">
                                Responsável pelo controle
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="responsavel_tecnico_id"
                          render={({ field }) => (
                            <FormItem className="flex-1">
                              <FormLabel className="text-sm font-semibold">Responsável Técnico</FormLabel>
                              <Select 
                                onValueChange={field.onChange} 
                                defaultValue={field.value}
                                disabled={loading || !isEditing}
                              >
                                <FormControl>
                                  <SelectTrigger className="focus:ring-2 focus:ring-primary">
                                    <SelectValue placeholder={loading ? "Carregando..." : "Selecione o responsável técnico"} />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  {responsaveisTecnicos.map((responsavel) => (
                                    <SelectItem key={responsavel.id} value={responsavel.id}>
                                      {responsavel.nome}
                                    </SelectItem>
                                  ))}
                                </SelectContent>
                              </Select>
                              <FormDescription className="text-xs">
                                Responsável técnico pelo item
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                      </div>


                      <FormField
                        control={form.control}
                        name="observacao"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-sm font-semibold">Observações</FormLabel>
                            <FormControl>
                              <Textarea 
                                placeholder="Observações adicionais sobre o item..." 
                                className="min-h-[100px] resize-none focus:ring-2 focus:ring-primary"
                                {...field} 
                              />
                            </FormControl>
                            
                            
                          </FormItem>
                        )}
                      />
                    </CardContent>
                  </Card>
                </TabsContent>
              </Tabs>
            </ScrollArea>

            <DialogFooter className="gap-2">
              {mode === "edit" && !isEditing ? (
                <>
                  <Button 
                    type="button" 
                    variant="outline"
                    onClick={() => setOpen(false)}
                  >
                    Fechar
                  </Button>
                  <Button 
                    type="button"
                    onClick={handleEdit}
                    className="bg-primary hover:bg-primary/90"
                  >
                    Editar
                  </Button>
                </>
              ) : (
                <>
                  <Button 
                    type="button" 
                    variant="outline"
                    onClick={() => {
                      if (mode === "edit") {
                        handleCancel();
                      } else {
                        setOpen(false);
                      }
                    }}
                  >
                    Cancelar
                  </Button>
                  {mode === "create" && (
                    <Button 
                      type="button" 
                      variant="ghost"
                      onClick={() => form.reset()}
                    >
                      Limpar Campos
                    </Button>
                  )}
                  <Button 
                    type="submit"
                    className="bg-primary hover:bg-primary/90"
                    disabled={loading}
                  >
                    {loading 
                      ? "Salvando..." 
                      : mode === "edit" 
                        ? "Salvar Alterações" 
                        : "Salvar Item"
                    }
                  </Button>
                </>
              )}
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}