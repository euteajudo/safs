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
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { IconPlus, IconSearch, IconX, IconTrash } from "@tabler/icons-react";

import catalogoData from "@/app/dashboard/data-catalogo.json";

const processoSchema = z.object({
  unidade: z.enum(["ULOG", "UACE", "UPDE", "SAFS"], {
    required_error: "Selecione uma unidade",
  }),
  objeto_aquisicao: z.string().min(1, "Objeto da aquisição é obrigatório").max(500),
  numero_processo_planejamento: z.string().min(1, "Número do processo de planejamento é obrigatório").max(50),
  numero_item: z.string().optional(),
  codigo_master: z.string().optional(),
  status_processo_planejamento: z.enum(["Em andamento", "Finalizado", "Cancelado", "Pendente"], {
    required_error: "Selecione um status",
  }),
  numero_processo_compra_centralizada: z.string().max(50).optional().or(z.literal("")),
  status_compra_centralizada: z.enum(["undefined", "Não iniciada", "Em andamento", "Finalizada", "Cancelada"]).optional().or(z.literal("")),
  observacao: z.string().max(1000).optional().or(z.literal("")),
  itens_selecionados: z.array(z.object({
    id: z.number(),
    codigo_master: z.string(),
    descricao: z.string(),
    unidade: z.string(),
    marca: z.string().optional(),
    quantidade: z.number().min(1, "Quantidade deve ser maior que 0"),
  })).optional().default([]),
});

interface ItemCatalogo {
  id: number;
  unidade: string;
  marca?: string;
  codigo_master: string;
  descricao: string;
  apresentacao?: string;
  classificacao_xyz?: string;
}

type ProcessoFormValues = z.infer<typeof processoSchema>;

interface ProcessoFormDialogProps {
  trigger: React.ReactNode;
  processo?: ProcessoFormValues & { id?: number };
  mode?: "create" | "edit";
}

export function ProcessoFormDialog({ trigger, processo, mode = "create" }: ProcessoFormDialogProps) {
  const [open, setOpen] = React.useState(false);
  const [isEditing, setIsEditing] = React.useState(mode === "create");
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredItems, setFilteredItems] = useState<ItemCatalogo[]>([]);
  const [selectedItem, setSelectedItem] = useState<ItemCatalogo | null>(null);
  const [quantidade, setQuantidade] = useState<number>(1);
  
  const form = useForm<ProcessoFormValues>({
    resolver: zodResolver(processoSchema),
    defaultValues: processo ? {
      unidade: (processo.unidade as "ULOG" | "UACE" | "UPDE" | "SAFS") || "ULOG",
      objeto_aquisicao: processo.objeto_aquisicao || "",
      numero_processo_planejamento: processo.numero_processo_planejamento || "",
      numero_item: processo.numero_item || "",
      codigo_master: processo.codigo_master || "",
      status_processo_planejamento: (processo.status_processo_planejamento as "Em andamento" | "Finalizado" | "Cancelado" | "Pendente") || "Em andamento",
      numero_processo_compra_centralizada: processo.numero_processo_compra_centralizada || "",
      status_compra_centralizada: (processo.status_compra_centralizada as "undefined" | "Não iniciada" | "Em andamento" | "Finalizada" | "Cancelada") || "undefined",
      observacao: processo.observacao || "",
      itens_selecionados: processo.itens_selecionados || [],
    } : {
      unidade: "ULOG",
      objeto_aquisicao: "",
      numero_processo_planejamento: "",
      numero_item: "",
      codigo_master: "",
      status_processo_planejamento: "Em andamento",
      numero_processo_compra_centralizada: "",
      status_compra_centralizada: "undefined",
      observacao: "",
      itens_selecionados: [],
    },
  });

  // Resetar estado de edição quando o modal abrir
  useEffect(() => {
    if (open) {
      if (mode === "edit") {
        setIsEditing(false);
      } else {
        setIsEditing(true);
      }
    }
  }, [open, mode]);

  // Filtrar itens do catálogo baseado na busca
  useEffect(() => {
    if (searchTerm.trim() === "") {
      setFilteredItems([]);
      return;
    }

    const items = catalogoData.filter(item => 
      item.codigo_master.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.descricao.toLowerCase().includes(searchTerm.toLowerCase())
    ).slice(0, 10); // Limitar a 10 resultados

    setFilteredItems(items);
  }, [searchTerm]);

  const atualizarCamposAutomaticos = (itens: any[]) => {
    if (itens.length === 0) {
      form.setValue("codigo_master", "");
      form.setValue("numero_item", "");
      return;
    }

    // Se há apenas um item, usar seu código master e número 001
    if (itens.length === 1) {
      form.setValue("codigo_master", itens[0].codigo_master);
      form.setValue("numero_item", "001");
    } else {
      // Se há múltiplos itens, concatenar códigos master e usar numeração sequencial
      const codigosMaster = itens.map(item => item.codigo_master).join(", ");
      const numeroItem = `001-${String(itens.length).padStart(3, '0')}`;
      
      form.setValue("codigo_master", codigosMaster.length > 50 ? `${codigosMaster.substring(0, 47)}...` : codigosMaster);
      form.setValue("numero_item", numeroItem);
    }
  };

  const adicionarItem = () => {
    if (!selectedItem) return;
    
    const itensSelecionados = form.getValues("itens_selecionados") || [];
    const itemJaAdicionado = itensSelecionados.find(item => item.id === selectedItem.id);
    
    if (itemJaAdicionado) {
      alert("Item já foi adicionado ao processo!");
      return;
    }

    const novoItem = {
      id: selectedItem.id,
      codigo_master: selectedItem.codigo_master,
      descricao: selectedItem.descricao,
      unidade: selectedItem.unidade,
      marca: selectedItem.marca,
      quantidade: quantidade,
    };

    const novosItens = [...itensSelecionados, novoItem];
    form.setValue("itens_selecionados", novosItens);
    
    // Atualizar campos automáticos
    atualizarCamposAutomaticos(novosItens);
    
    // Resetar seleção
    setSelectedItem(null);
    setSearchTerm("");
    setQuantidade(1);
    setFilteredItems([]);
  };

  const removerItem = (itemId: number) => {
    const itensSelecionados = form.getValues("itens_selecionados") || [];
    const itensAtualizados = itensSelecionados.filter(item => item.id !== itemId);
    form.setValue("itens_selecionados", itensAtualizados);
    
    // Atualizar campos automáticos
    atualizarCamposAutomaticos(itensAtualizados);
  };

  const getUnidadeStyle = (unidade: string) => {
    switch (unidade) {
      case "ULOG":
        return "text-orange-500 border-orange-500";
      case "UACE":
        return "text-green-500 border-green-500";
      case "UPDE":
        return "text-red-400 border-red-400";
      case "SAFS":
        return "text-stone-950 border-stone-950 dark:text-stone-50 dark:border-stone-50";
      default:
        return "text-gray-500 border-gray-500";
    }
  };

  function onSubmit(values: ProcessoFormValues) {
    if (mode === "edit") {
      console.log("Editando processo:", { ...values, id: processo?.id });
      // TODO: Implementar atualização via API
    } else {
      console.log("Criando novo processo:", values);
      // TODO: Implementar criação via API
    }
    form.reset();
    setOpen(false);
  }

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    if (processo) {
      form.reset({
        unidade: (processo.unidade as "ULOG" | "UACE" | "UPDE" | "SAFS") || "ULOG",
        objeto_aquisicao: processo.objeto_aquisicao || "",
        numero_processo_planejamento: processo.numero_processo_planejamento || "",
        numero_item: processo.numero_item || "",
        codigo_master: processo.codigo_master || "",
        status_processo_planejamento: (processo.status_processo_planejamento as "Em andamento" | "Finalizado" | "Cancelado" | "Pendente") || "Em andamento",
        numero_processo_compra_centralizada: processo.numero_processo_compra_centralizada || "",
        status_compra_centralizada: (processo.status_compra_centralizada as "undefined" | "Não iniciada" | "Em andamento" | "Finalizada" | "Cancelada") || "undefined",
        observacao: processo.observacao || "",
        itens_selecionados: processo.itens_selecionados || [],
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
            {mode === "edit" ? "Editar Processo" : "Adicionar Novo Processo"}
          </DialogTitle>
          <DialogDescription>
            {mode === "edit" 
              ? `Editando processo: ${processo?.numero_processo_planejamento}`
              : "Preencha os campos abaixo para adicionar um novo processo ao sistema"}
          </DialogDescription>
        </DialogHeader>
        
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <ScrollArea className="h-[60vh] pr-4">
              <Tabs defaultValue="principal" className="w-full">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="principal">Informações do Processo</TabsTrigger>
                  <TabsTrigger value="itens">Itens do Processo</TabsTrigger>
                  <TabsTrigger value="compra">Compra Centralizada</TabsTrigger>
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
                                    <SelectValue placeholder="Selecione uma unidade" />
                                  </SelectTrigger>
                                  <SelectContent>
                                    <SelectItem value="ULOG">ULOG - Unidade de Logística</SelectItem>
                                    <SelectItem value="UACE">UACE - Unidade de Acompanhamento e Controle</SelectItem>
                                    <SelectItem value="UPDE">UPDE - Unidade de Planejamento e Desenvolvimento</SelectItem>
                                    <SelectItem value="SAFS">SAFS - Superintendência de Administração</SelectItem>
                                  </SelectContent>
                                </Select>
                              </FormControl>
                              <FormDescription className="text-xs">
                                Unidade responsável pelo processo
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="status_processo_planejamento"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Status do Planejamento <span className="text-red-500">*</span>
                              </FormLabel>
                              <FormControl>
                                <Select 
                                  onValueChange={field.onChange} 
                                  defaultValue={field.value}
                                  disabled={!isEditing}
                                >
                                  <SelectTrigger className="focus:ring-2 focus:ring-primary">
                                    <SelectValue placeholder="Selecione o status" />
                                  </SelectTrigger>
                                  <SelectContent>
                                    <SelectItem value="Em andamento">Em andamento</SelectItem>
                                    <SelectItem value="Finalizado">Finalizado</SelectItem>
                                    <SelectItem value="Cancelado">Cancelado</SelectItem>
                                    <SelectItem value="Pendente">Pendente</SelectItem>
                                  </SelectContent>
                                </Select>
                              </FormControl>
                              <FormDescription className="text-xs">
                                Status atual do processo de planejamento
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>

                      <FormField
                        control={form.control}
                        name="numero_processo_planejamento"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-sm font-semibold">
                              Número do Processo de Planejamento <span className="text-red-500">*</span>
                            </FormLabel>
                            <FormControl>
                              <Input 
                                placeholder="Ex: 23481.000123/2024-15" 
                                className="focus:ring-2 focus:ring-primary font-mono"
                                {...field} 
                                disabled={!isEditing}
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Número único do processo no sistema de planejamento
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={form.control}
                        name="objeto_aquisicao"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-sm font-semibold">
                              Objeto da Aquisição <span className="text-red-500">*</span>
                            </FormLabel>
                            <FormControl>
                              <Textarea 
                                placeholder="Descreva detalhadamente o objeto da aquisição..." 
                                className="min-h-[100px] resize-none focus:ring-2 focus:ring-primary"
                                {...field} 
                                disabled={!isEditing}
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Descrição completa e detalhada do que será adquirido
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                        <div className="flex items-start gap-3">
                          <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-blue-600 font-semibold text-sm">ℹ</span>
                          </div>
                          <div>
                            <h4 className="text-sm font-semibold text-blue-900 mb-1">
                              Códigos Master e Números de Item
                            </h4>
                            <p className="text-sm text-blue-700">
                              Os códigos master e números dos itens serão preenchidos automaticamente 
                              baseados nos itens selecionados na aba <strong>"Itens do Processo"</strong>. 
                              Adicione os itens na próxima aba para completar o processo.
                            </p>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="itens" className="space-y-6 mt-6">
                  <Card>
                    <CardContent className="pt-6 space-y-4">
                      <div className="space-y-4">
                        <div className="flex items-center gap-2">
                          <h3 className="text-lg font-semibold">Adicionar Itens ao Processo</h3>
                          <Badge variant="outline" className="text-xs">
                            {form.watch("itens_selecionados")?.length || 0} itens selecionados
                          </Badge>
                        </div>
                        
                        {/* Campo de busca */}
                        <div className="space-y-2">
                          <Label className="text-sm font-semibold">Buscar Item no Catálogo</Label>
                          <div className="relative">
                            <IconSearch className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                            <Input
                              placeholder="Digite o código master ou descrição do item..."
                              value={searchTerm}
                              onChange={(e) => setSearchTerm(e.target.value)}
                              className="pl-10 focus:ring-2 focus:ring-primary"
                              disabled={!isEditing}
                            />
                          </div>
                        </div>

                        {/* Resultados da busca */}
                        {filteredItems.length > 0 && (
                          <div className="space-y-2">
                            <Label className="text-sm font-semibold">Resultados da Busca</Label>
                            <div className="max-h-60 overflow-y-auto border rounded-md">
                              {filteredItems.map((item) => (
                                <div
                                  key={item.id}
                                  className={`p-3 border-b last:border-b-0 cursor-pointer hover:bg-gray-50 ${
                                    selectedItem?.id === item.id ? 'bg-blue-50 border-blue-200' : ''
                                  }`}
                                  onClick={() => setSelectedItem(item)}
                                >
                                  <div className="flex items-start justify-between gap-3">
                                    <div className="flex-1">
                                      <div className="flex items-center gap-2 mb-1">
                                        <code className="text-sm font-mono bg-gray-100 px-2 py-1 rounded">
                                          {item.codigo_master}
                                        </code>
                                        <Badge 
                                          variant="outline" 
                                          className={`${getUnidadeStyle(item.unidade)} px-2 py-1 text-xs`}
                                        >
                                          {item.unidade}
                                        </Badge>
                                      </div>
                                      <p className="text-sm text-gray-900 leading-tight">{item.descricao}</p>
                                      {item.marca && (
                                        <p className="text-xs text-gray-500 mt-1">Marca: {item.marca}</p>
                                      )}
                                    </div>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Adicionar item selecionado */}
                        {selectedItem && isEditing && (
                          <div className="space-y-3 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                            <div className="flex items-center gap-2">
                              <h4 className="text-sm font-semibold">Item Selecionado</h4>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => {
                                  setSelectedItem(null);
                                  setSearchTerm("");
                                  setFilteredItems([]);
                                }}
                              >
                                <IconX className="h-4 w-4" />
                              </Button>
                            </div>
                            <div className="text-sm">
                              <div className="flex items-center gap-2 mb-1">
                                <code className="bg-gray-100 px-2 py-1 rounded">{selectedItem.codigo_master}</code>
                                <Badge variant="outline" className={`${getUnidadeStyle(selectedItem.unidade)} px-2 py-1 text-xs`}>
                                  {selectedItem.unidade}
                                </Badge>
                              </div>
                              <p className="text-gray-900">{selectedItem.descricao}</p>
                            </div>
                            <div className="flex items-center gap-3">
                              <div className="flex items-center gap-2">
                                <Label className="text-sm">Quantidade:</Label>
                                <Input
                                  type="number"
                                  min="1"
                                  value={quantidade}
                                  onChange={(e) => setQuantidade(Math.max(1, parseInt(e.target.value) || 1))}
                                  className="w-20 text-center"
                                />
                              </div>
                              <Button
                                type="button"
                                onClick={adicionarItem}
                                size="sm"
                                className="bg-primary hover:bg-primary/90"
                              >
                                <IconPlus className="h-4 w-4 mr-2" />
                                Adicionar Item
                              </Button>
                            </div>
                          </div>
                        )}

                        {/* Painel com informações geradas automaticamente */}
                        {form.watch("itens_selecionados")?.length > 0 && (
                          <div className="space-y-3 p-4 bg-green-50 border border-green-200 rounded-lg">
                            <h4 className="text-sm font-semibold text-green-900">Campos Preenchidos Automaticamente</h4>
                            <div className="grid grid-cols-2 gap-4 text-sm">
                              <div>
                                <span className="font-medium text-green-800">Código Master:</span>
                                <div className="mt-1 p-2 bg-white border border-green-300 rounded font-mono text-xs">
                                  {form.watch("codigo_master") || "Não definido"}
                                </div>
                              </div>
                              <div>
                                <span className="font-medium text-green-800">Número do Item:</span>
                                <div className="mt-1 p-2 bg-white border border-green-300 rounded font-mono text-xs">
                                  {form.watch("numero_item") || "Não definido"}
                                </div>
                              </div>
                            </div>
                            <p className="text-xs text-green-700">
                              Estes campos são atualizados automaticamente baseados nos itens selecionados.
                            </p>
                          </div>
                        )}

                        {/* Lista de itens selecionados */}
                        {form.watch("itens_selecionados")?.length > 0 && (
                          <div className="space-y-3">
                            <Label className="text-sm font-semibold">
                              Itens Adicionados ao Processo ({form.watch("itens_selecionados")?.length})
                            </Label>
                            <div className="space-y-2 max-h-60 overflow-y-auto border rounded-md p-2">
                              {form.watch("itens_selecionados")?.map((item, index) => (
                                <div
                                  key={`${item.id}-${index}`}
                                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border"
                                >
                                  <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                      <code className="text-sm font-mono bg-white px-2 py-1 rounded">
                                        {item.codigo_master}
                                      </code>
                                      <Badge 
                                        variant="outline" 
                                        className={`${getUnidadeStyle(item.unidade)} px-2 py-1 text-xs`}
                                      >
                                        {item.unidade}
                                      </Badge>
                                      <Badge variant="secondary" className="text-xs">
                                        Qtd: {item.quantidade}
                                      </Badge>
                                    </div>
                                    <p className="text-sm text-gray-900">{item.descricao}</p>
                                    {item.marca && (
                                      <p className="text-xs text-gray-500 mt-1">Marca: {item.marca}</p>
                                    )}
                                  </div>
                                  {isEditing && (
                                    <Button
                                      type="button"
                                      variant="ghost"
                                      size="sm"
                                      onClick={() => removerItem(item.id)}
                                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                    >
                                      <IconTrash className="h-4 w-4" />
                                    </Button>
                                  )}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="compra" className="space-y-6 mt-6">
                  <Card>
                    <CardContent className="pt-6 space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <FormField
                          control={form.control}
                          name="numero_processo_compra_centralizada"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Número do Processo de Compra Centralizada
                              </FormLabel>
                              <FormControl>
                                <Input 
                                  placeholder="Ex: 23000.012345/2024-11" 
                                  className="focus:ring-2 focus:ring-primary font-mono"
                                  {...field} 
                                  disabled={!isEditing}
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Número do processo no sistema de compras (opcional)
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="status_compra_centralizada"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Status da Compra Centralizada
                              </FormLabel>
                              <FormControl>
                                <Select 
                                  onValueChange={field.onChange} 
                                  value={field.value || ""}
                                  disabled={!isEditing}
                                >
                                  <SelectTrigger className="focus:ring-2 focus:ring-primary">
                                    <SelectValue placeholder="Selecione o status" />
                                  </SelectTrigger>
                                  <SelectContent>
                                    <SelectItem value="undefined">Não definido</SelectItem>
                                    <SelectItem value="Não iniciada">Não iniciada</SelectItem>
                                    <SelectItem value="Em andamento">Em andamento</SelectItem>
                                    <SelectItem value="Finalizada">Finalizada</SelectItem>
                                    <SelectItem value="Cancelada">Cancelada</SelectItem>
                                  </SelectContent>
                                </Select>
                              </FormControl>
                              <FormDescription className="text-xs">
                                Status atual da compra centralizada (opcional)
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
                                placeholder="Observações adicionais sobre o processo..." 
                                className="min-h-[100px] resize-none focus:ring-2 focus:ring-primary"
                                {...field} 
                                disabled={!isEditing}
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Informações complementares e observações importantes sobre o processo
                            </FormDescription>
                            <FormMessage />
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
                  >
                    {mode === "edit" ? "Salvar Alterações" : "Salvar Processo"}
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