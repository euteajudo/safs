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
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from "@/components/ui/select";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { IconUpload, IconUser } from "@tabler/icons-react";
import { useCurrentUser } from "@/contexts/auth-context";
import { canCreateUserForUnit, getAssignableRoles, validateRoleAssignment } from "@/lib/permissions";
import { api } from "@/lib/api";

const usuarioSchema = z.object({
  unidade: z.enum(["ULOG", "UACE", "UPDE", "SAFS"]),
  nome: z.string().min(1, "Nome é obrigatório").max(100),
  username: z.string().min(3, "Username deve ter pelo menos 3 caracteres").max(50),
  email: z.string().email("Email inválido"),
  foto_url: z.string().optional(),
  senha: z.string().min(6, "Senha deve ter pelo menos 6 caracteres").max(100),
  confirmar_senha: z.string().min(6, "Confirmação de senha é obrigatória"),
  is_active: z.boolean().default(true),
  is_superuser: z.boolean().default(false),
  is_chefe_unidade: z.boolean().default(false),
  is_chefe_setor: z.boolean().default(false),
  is_funcionario: z.boolean().default(false),
}).refine((data) => data.senha === data.confirmar_senha, {
  message: "Senhas não coincidem",
  path: ["confirmar_senha"],
});

// Schema para edição (sem senha obrigatória)
const usuarioEditSchema = z.object({
  unidade: z.enum(["ULOG", "UACE", "UPDE", "SAFS"]),
  nome: z.string().min(1, "Nome é obrigatório").max(100),
  username: z.string().min(3, "Username deve ter pelo menos 3 caracteres").max(50),
  email: z.string().email("Email inválido"),
  foto_url: z.string().optional(),
  senha: z.string().optional(),
  confirmar_senha: z.string().optional(),
  is_active: z.boolean().default(true),
  is_superuser: z.boolean().default(false),
  is_chefe_unidade: z.boolean().default(false),
  is_chefe_setor: z.boolean().default(false),
  is_funcionario: z.boolean().default(false),
}).refine((data) => {
  // Se senha foi fornecida, deve ter confirmação
  if (data.senha && data.senha.length > 0) {
    return data.senha === data.confirmar_senha && data.senha.length >= 6;
  }
  return true;
}, {
  message: "Senhas não coincidem ou senha muito curta",
  path: ["confirmar_senha"],
});

type UsuarioFormValues = z.infer<typeof usuarioSchema>;
type UsuarioEditFormValues = z.infer<typeof usuarioEditSchema>;

interface UsuarioFormDialogProps {
  trigger: React.ReactNode;
  user?: UsuarioEditFormValues & { id?: number; unidade?: string; foto_url?: string };
  mode?: "create" | "edit";
  onSuccess?: () => void; // Callback chamado após sucesso na operação
}

export function UsuarioFormDialog({ trigger, user, mode = "create", onSuccess }: UsuarioFormDialogProps) {
  const [open, setOpen] = React.useState(false);
  const [isEditing, setIsEditing] = React.useState(mode === "create");
  const [loading, setLoading] = useState(false);
  const [previewImage, setPreviewImage] = React.useState<string | null>(user?.foto_url || null);
  const currentUser = useCurrentUser();
  
  const schema = mode === "create" ? usuarioSchema : usuarioEditSchema;
  
  const form = useForm<UsuarioFormValues | UsuarioEditFormValues>({
    resolver: zodResolver(schema),
    defaultValues: user ? {
      unidade: (user.unidade as "ULOG" | "UACE" | "UPDE" | "SAFS") || "ULOG",
      nome: user.nome || "",
      username: user.username || "",
      email: user.email || "",
      foto_url: user.foto_url || "",
      senha: "",
      confirmar_senha: "",
      is_active: user.is_active ?? true,
      is_superuser: user.is_superuser ?? false,
      is_chefe_unidade: user.is_chefe_unidade ?? false,
      is_chefe_setor: user.is_chefe_setor ?? false,
      is_funcionario: user.is_funcionario ?? false,
    } : {
      // Para chefes de unidade, definir automaticamente a unidade deles
      unidade: (currentUser?.is_chefe_unidade && !currentUser?.is_superuser) ? 
        (currentUser?.unidade as "ULOG" | "UACE" | "UPDE" | "SAFS") : "ULOG" as const,
      nome: "",
      username: "",
      email: "",
      foto_url: "",
      senha: "",
      confirmar_senha: "",
      is_active: true,
      is_superuser: false,
      is_chefe_unidade: false,
      is_chefe_setor: false,
      is_funcionario: false,
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

  async function onSubmit(values: UsuarioFormValues | UsuarioEditFormValues) {
    // Validar se as permissões selecionadas são válidas
    const selectedRoles = {
      is_superuser: values.is_superuser,
      is_chefe_unidade: values.is_chefe_unidade,
      is_chefe_setor: values.is_chefe_setor,
      is_funcionario: values.is_funcionario,
    };
    
    const validation = validateRoleAssignment(currentUser, selectedRoles);
    
    if (!validation.isValid) {
      const errorMessage = validation.errors ? validation.errors.join(', ') : 'Erro de validação de permissões';
      alert(`Erro de permissão: ${errorMessage}`);
      return;
    }
    
    // Preparar dados para envio (remover confirmar_senha)
    const { confirmar_senha, ...userData } = values;
    
    try {
      setLoading(true);
      
      if (mode === "edit") {
        console.log("Editando usuário:", { ...userData, id: user?.id });
        await api.put(`/v1/users/${user?.id}`, userData);
        alert('Usuário editado com sucesso!');
      } else {
        console.log("Criando novo usuário:", userData);
        await api.post('/v1/users/', userData);
        alert('Usuário criado com sucesso!');
      }
      
      form.reset();
      setOpen(false);
      
      // Chamar callback de sucesso se fornecido
      if (onSuccess) {
        onSuccess();
      }
      
    } catch (error) {
      console.error('Erro ao salvar usuário:', error);
      alert(`Erro ao ${mode === "edit" ? "editar" : "criar"} usuário: ${error instanceof Error ? error.message : 'Erro desconhecido'}`);
    } finally {
      setLoading(false);
    }
  }

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    if (user) {
      form.reset({
        unidade: (user.unidade as "ULOG" | "UACE" | "UPDE" | "SAFS") || "ULOG",
        nome: user.nome || "",
        username: user.username || "",
        email: user.email || "",
        foto_url: user.foto_url || "",
        senha: "",
        confirmar_senha: "",
        is_active: user.is_active ?? true,
        is_superuser: user.is_superuser ?? false,
        is_chefe_unidade: user.is_chefe_unidade ?? false,
        is_chefe_setor: user.is_chefe_setor ?? false,
        is_funcionario: user.is_funcionario ?? false,
      });
      setPreviewImage(user.foto_url || null);
    }
    setIsEditing(false);
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result as string;
        setPreviewImage(result);
        form.setValue("foto_url", result);
      };
      reader.readAsDataURL(file);
    }
  };

  // Determinar quais unidades o usuário atual pode selecionar
  const getAvailableUnits = () => {
    const allUnits = [
      { value: "ULOG", label: "ULOG - Unidade de Logística" },
      { value: "UACE", label: "UACE - Unidade de Acompanhamento e Controle de Estoque" },
      { value: "UPDE", label: "UPDE - Unidade de Planejamento e Dimensionamento de Estoque" },
      { value: "SAFS", label: "SAFS - Setor de Abastecimento Farmacêutico e Suprimentos" },
    ];

    // Superusuário pode criar para todas as unidades
    if (currentUser?.is_superuser) {
      return allUnits;
    }

    // Chefe de unidade só pode criar para sua própria unidade
    if (currentUser?.is_chefe_unidade) {
      return allUnits.filter(unit => unit.value === currentUser.unidade);
    }

    // Chefe de setor só pode atribuir perfil de funcionário, Chefe de unidade e responsável técnico
    if (currentUser?.is_chefe_setor) {
      return allUnits.filter(unit => unit.value === currentUser.unidade || unit.value === "ULOG" || unit.value === "UPDE" || unit.value === "UACE" || unit.value === "SAFS");
    }

    return allUnits;
  };

  const availableUnits = getAvailableUnits();
  
  // Obter quais permissões o usuário atual pode atribuir
  const assignableRoles = getAssignableRoles(currentUser);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[90vh]">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold">
            {mode === "edit" ? "Editar Usuário" : "Adicionar Novo Usuário"}
          </DialogTitle>
          <DialogDescription>
            {mode === "edit" 
              ? `Editando usuário: ${user?.nome}`
              : "Preencha os campos abaixo para adicionar um novo usuário ao sistema"}
          </DialogDescription>
        </DialogHeader>
        
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <ScrollArea className="h-[60vh] pr-4">
              <Tabs defaultValue="dados" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="dados">Dados Pessoais</TabsTrigger>
                  <TabsTrigger value="permissoes">Permissões</TabsTrigger>
                </TabsList>

                <TabsContent value="dados" className="space-y-6 mt-6">
                  <Card>
                    <CardContent className="pt-6 space-y-4">
                      {/* Foto do usuário */}
                      <div className="flex flex-col items-center space-y-4">
                        <div className="flex flex-col items-center space-y-2">
                          <Avatar className="h-24 w-24">
                            <AvatarImage src={previewImage || undefined} />
                            <AvatarFallback className="bg-muted">
                              <IconUser className="h-12 w-12 text-muted-foreground" />
                            </AvatarFallback>
                          </Avatar>
                          {isEditing && (
                            <div className="flex flex-col items-center space-y-2">
                              <input
                                type="file"
                                accept="image/*"
                                onChange={handleImageUpload}
                                className="hidden"
                                id="photo-upload"
                              />
                              <Button
                                type="button"
                                variant="outline"
                                size="sm"
                                onClick={() => document.getElementById('photo-upload')?.click()}
                              >
                                <IconUpload className="h-4 w-4 mr-2" />
                                Upload Foto
                              </Button>
                            </div>
                          )}
                        </div>
                      </div>

                      <FormField
                        control={form.control}
                        name="unidade"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-sm font-semibold">
                              Unidade <span className="text-red-500">*</span>
                            </FormLabel>
                            <Select 
                              onValueChange={field.onChange} 
                              defaultValue={field.value}
                              disabled={!isEditing}
                            >
                              <FormControl>
                                <SelectTrigger className="focus:ring-2 focus:ring-primary">
                                  <SelectValue placeholder="Selecione uma unidade" />
                                </SelectTrigger>
                              </FormControl>
                              <SelectContent>
                                {availableUnits.map((unit) => (
                                  <SelectItem key={unit.value} value={unit.value}>
                                    {unit.label}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                            <FormDescription className="text-xs">
                              Unidade organizacional do usuário
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      
                      <div className="grid grid-cols-2 gap-4">
                        <FormField
                          control={form.control}
                          name="nome"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Nome Completo <span className="text-red-500">*</span>
                              </FormLabel>
                              <FormControl>
                                <Input 
                                  placeholder="Ex: João Silva dos Santos" 
                                  className="focus:ring-2 focus:ring-primary"
                                  {...field} 
                                  disabled={!isEditing}
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Nome completo do usuário
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="username"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Nome de Usuário <span className="text-red-500">*</span>
                              </FormLabel>
                              <FormControl>
                                <Input 
                                  placeholder="Ex: joao.silva" 
                                  className="focus:ring-2 focus:ring-primary"
                                  {...field} 
                                  disabled={!isEditing}
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Nome único para login (apenas letras, números, underscore e ponto)
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>

                      <FormField
                        control={form.control}
                        name="email"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-sm font-semibold">
                              Email <span className="text-red-500">*</span>
                            </FormLabel>
                            <FormControl>
                              <Input 
                                type="email"
                                placeholder="joao.silva@exemplo.com" 
                                className="focus:ring-2 focus:ring-primary"
                                {...field} 
                                disabled={!isEditing}
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Email único para comunicação e recuperação de senha
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <div className="grid grid-cols-2 gap-4">
                        <FormField
                          control={form.control}
                          name="senha"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                {mode === "create" ? "Senha" : "Nova Senha"} 
                                {mode === "create" && <span className="text-red-500">*</span>}
                              </FormLabel>
                              <FormControl>
                                <Input 
                                  type="password"
                                  placeholder={mode === "create" ? "Mínimo 6 caracteres" : "Deixe vazio para manter atual"} 
                                  className="focus:ring-2 focus:ring-primary"
                                  {...field} 
                                  disabled={!isEditing}
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                {mode === "create" ? "Senha deve ter pelo menos 6 caracteres" : "Deixe vazio para não alterar"}
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="confirmar_senha"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Confirmar Senha 
                                {mode === "create" && <span className="text-red-500">*</span>}
                              </FormLabel>
                              <FormControl>
                                <Input 
                                  type="password"
                                  placeholder="Digite a senha novamente" 
                                  className="focus:ring-2 focus:ring-primary"
                                  {...field} 
                                  disabled={!isEditing}
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Confirmação da senha
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="permissoes" className="space-y-6 mt-6">
                  <Card>
                    <CardContent className="pt-6 space-y-4">
                      <div className="grid grid-cols-2 gap-6">
                        <div className="space-y-4">
                          <h3 className="text-sm font-semibold text-gray-900">Status</h3>
                          
                          <FormField
                            control={form.control}
                            name="is_active"
                            render={({ field }) => (
                              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                                <FormControl>
                                  <Checkbox
                                    checked={field.value}
                                    onCheckedChange={field.onChange}
                                    disabled={!isEditing}
                                  />
                                </FormControl>
                                <div className="space-y-1 leading-none">
                                  <FormLabel className="text-sm font-medium">
                                    Usuário Ativo
                                  </FormLabel>
                                  <FormDescription className="text-xs">
                                    Define se o usuário pode acessar o sistema
                                  </FormDescription>
                                </div>
                              </FormItem>
                            )}
                          />
                        </div>

                        <div className="space-y-4">
                          <h3 className="text-sm font-semibold text-gray-900">Níveis de Acesso</h3>
                          
                          {assignableRoles.includes('superuser') && (
                            <FormField
                              control={form.control}
                              name="is_superuser"
                              render={({ field }) => (
                                <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                                  <FormControl>
                                    <Checkbox
                                      checked={field.value}
                                      onCheckedChange={field.onChange}
                                      disabled={!isEditing}
                                    />
                                  </FormControl>
                                  <div className="space-y-1 leading-none">
                                    <FormLabel className="text-sm font-medium">
                                      Superusuário
                                    </FormLabel>
                                    <FormDescription className="text-xs">
                                      Acesso completo ao sistema
                                    </FormDescription>
                                  </div>
                                </FormItem>
                              )}
                            />
                          )}

                          {assignableRoles.includes('chefe_unidade') && (
                            <FormField
                              control={form.control}
                              name="is_chefe_unidade"
                              render={({ field }) => (
                                <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                                  <FormControl>
                                    <Checkbox
                                      checked={field.value}
                                      onCheckedChange={field.onChange}
                                      disabled={!isEditing}
                                    />
                                  </FormControl>
                                  <div className="space-y-1 leading-none">
                                    <FormLabel className="text-sm font-medium">
                                      Chefe de Unidade
                                    </FormLabel>
                                    <FormDescription className="text-xs">
                                      Gerencia uma unidade organizacional
                                    </FormDescription>
                                  </div>
                                </FormItem>
                              )}
                            />
                          )}

                          {assignableRoles.includes('chefe_setor') && (
                            <FormField
                              control={form.control}
                              name="is_chefe_setor"
                              render={({ field }) => (
                                <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                                  <FormControl>
                                    <Checkbox
                                      checked={field.value}
                                      onCheckedChange={field.onChange}
                                      disabled={!isEditing}
                                    />
                                  </FormControl>
                                  <div className="space-y-1 leading-none">
                                    <FormLabel className="text-sm font-medium">
                                      Chefe de Setor
                                    </FormLabel>
                                    <FormDescription className="text-xs">
                                      Gerencia um setor específico
                                    </FormDescription>
                                  </div>
                                </FormItem>
                              )}
                            />
                          )}

                          {assignableRoles.includes('funcionario') && (
                            <FormField
                              control={form.control}
                              name="is_funcionario"
                              render={({ field }) => (
                                <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                                  <FormControl>
                                    <Checkbox
                                      checked={field.value}
                                      onCheckedChange={field.onChange}
                                      disabled={!isEditing}
                                    />
                                  </FormControl>
                                  <div className="space-y-1 leading-none">
                                    <FormLabel className="text-sm font-medium">
                                      Funcionário
                                    </FormLabel>
                                    <FormDescription className="text-xs">
                                      Acesso básico como funcionário
                                    </FormDescription>
                                  </div>
                                </FormItem>
                              )}
                            />
                          )}
                          
                          {assignableRoles.length === 0 && (
                            <div className="text-center text-sm text-muted-foreground py-4 border border-dashed rounded-lg">
                              Você não possui permissão para atribuir perfis a outros usuários
                            </div>
                          )}
                        </div>
                      </div>
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
                    {loading ? "Salvando..." : (mode === "edit" ? "Salvar Alterações" : "Criar Usuário")}
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