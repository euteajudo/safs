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
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { IconUpload, IconUser, IconX } from "@tabler/icons-react";

const perfilSchema = z.object({
  nome: z.string().optional(), // Campo somente leitura
  username: z.string().optional(), // Campo somente leitura
  email: z.string().optional(), // Campo somente leitura
  foto_url: z.string().optional(),
  senha_atual: z.string().optional(),
  nova_senha: z.string().optional(),
  confirmar_nova_senha: z.string().optional(),
}).refine((data) => {
  // Se nova senha foi fornecida, deve ter confirmação e senha atual
  if (data.nova_senha && data.nova_senha.length > 0) {
    return data.nova_senha === data.confirmar_nova_senha && 
           data.nova_senha.length >= 6 && 
           data.senha_atual && data.senha_atual.length > 0;
  }
  return true;
}, {
  message: "Para alterar a senha: confirme a nova senha, digite a senha atual e a nova senha deve ter pelo menos 6 caracteres",
  path: ["confirmar_nova_senha"],
});

type PerfilFormValues = z.infer<typeof perfilSchema>;

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

interface PerfilFormDialogProps {
  trigger: React.ReactNode;
  user: Usuario;
}

export function PerfilFormDialog({ trigger, user }: PerfilFormDialogProps) {
  const [open, setOpen] = React.useState(false);
  const [loading, setLoading] = useState(false);
  const [previewImage, setPreviewImage] = React.useState<string | null>(user?.foto_url || null);
  
  const form = useForm<PerfilFormValues>({
    resolver: zodResolver(perfilSchema),
    defaultValues: {
      nome: user.nome || "",
      username: user.username || "",
      email: user.email || "",
      foto_url: user.foto_url || "",
      senha_atual: "",
      nova_senha: "",
      confirmar_nova_senha: "",
    },
  });

  function onSubmit(values: PerfilFormValues) {
    setLoading(true);
    
    // Preparar dados para envio - apenas campos permitidos para edição
    const userData: any = {
      foto_url: values.foto_url, // Única informação pessoal editável
    };
    
    // Se nova senha foi fornecida, incluir dados de alteração de senha
    if (values.nova_senha && values.nova_senha.length > 0) {
      userData.senha_atual = values.senha_atual;
      userData.nova_senha = values.nova_senha;
    }
    
    console.log("Atualizando perfil do usuário (apenas foto e senha):", { ...userData, id: user.id });
    // TODO: Implementar atualização via API
    
    // Simular delay da API
    setTimeout(() => {
      setLoading(false);
      form.reset({
        nome: user.nome,
        username: user.username,
        email: user.email,
        foto_url: values.foto_url,
        senha_atual: "",
        nova_senha: "",
        confirmar_nova_senha: "",
      });
      setOpen(false);
      alert("Perfil atualizado com sucesso!");
    }, 1000);
  }

  const handleCancel = () => {
    form.reset({
      nome: user.nome || "",
      username: user.username || "",
      email: user.email || "",
      foto_url: user.foto_url || "",
      senha_atual: "",
      nova_senha: "",
      confirmar_nova_senha: "",
    });
    setPreviewImage(user.foto_url || null);
    setOpen(false);
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validar tamanho do arquivo (5MB = 5 * 1024 * 1024 bytes)
      const maxSize = 5 * 1024 * 1024;
      if (file.size > maxSize) {
        alert("Arquivo muito grande! O tamanho máximo permitido é 5MB.");
        event.target.value = ""; // Limpar seleção
        return;
      }

      // Validar tipo do arquivo
      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
      if (!allowedTypes.includes(file.type)) {
        alert("Formato não permitido! Use apenas JPG, PNG ou GIF.");
        event.target.value = ""; // Limpar seleção
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result as string;
        setPreviewImage(result);
        form.setValue("foto_url", result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent className="max-w-3xl max-h-[90vh]">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold">
            Editar Meu Perfil
          </DialogTitle>
          <DialogDescription>
            Atualize suas informações pessoais e altere sua senha se necessário
          </DialogDescription>
        </DialogHeader>
        
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <ScrollArea className="h-[60vh] pr-4">
              <Tabs defaultValue="dados" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="dados">Informações Pessoais</TabsTrigger>
                  <TabsTrigger value="seguranca">Segurança</TabsTrigger>
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
                              Alterar Foto
                            </Button>
                            <p className="text-xs text-muted-foreground text-center max-w-xs">
                              Formatos aceitos: JPG, PNG, GIF<br/>
                              Tamanho máximo: 5MB<br/>
                              Recomendado: 400x400 pixels
                            </p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4">
                        <FormField
                          control={form.control}
                          name="nome"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Nome Completo
                              </FormLabel>
                              <FormControl>
                                <Input 
                                  placeholder="Ex: João Silva dos Santos" 
                                  className="bg-muted text-muted-foreground cursor-not-allowed"
                                  {...field}
                                  disabled
                                  readOnly
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Informação protegida - somente administradores podem alterar
                              </FormDescription>
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="username"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Nome de Usuário
                              </FormLabel>
                              <FormControl>
                                <Input 
                                  placeholder="Ex: joao.silva" 
                                  className="bg-muted text-muted-foreground cursor-not-allowed"
                                  {...field}
                                  disabled
                                  readOnly
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Informação protegida - somente administradores podem alterar
                              </FormDescription>
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
                              Email
                            </FormLabel>
                            <FormControl>
                              <Input 
                                type="email"
                                placeholder="joao.silva@exemplo.com" 
                                className="bg-muted text-muted-foreground cursor-not-allowed"
                                {...field}
                                disabled
                                readOnly
                              />
                            </FormControl>
                            <FormDescription className="text-xs">
                              Informação protegida - somente administradores podem alterar
                            </FormDescription>
                          </FormItem>
                        )}
                      />
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="seguranca" className="space-y-6 mt-6">
                  <Card>
                    <CardContent className="pt-6 space-y-4">
                      <div className="space-y-4">
                        <div className="pb-2 border-b">
                          <h3 className="text-sm font-semibold text-gray-900">Alterar Senha</h3>
                          <p className="text-xs text-muted-foreground">
                            Deixe os campos em branco se não deseja alterar a senha
                          </p>
                        </div>
                        
                        <FormField
                          control={form.control}
                          name="senha_atual"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="text-sm font-semibold">
                                Senha Atual
                              </FormLabel>
                              <FormControl>
                                <Input 
                                  type="password"
                                  placeholder="Digite sua senha atual"
                                  className="focus:ring-2 focus:ring-primary"
                                  {...field}
                                />
                              </FormControl>
                              <FormDescription className="text-xs">
                                Necessário para confirmar a alteração da senha
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <div className="grid grid-cols-2 gap-4">
                          <FormField
                            control={form.control}
                            name="nova_senha"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel className="text-sm font-semibold">
                                  Nova Senha
                                </FormLabel>
                                <FormControl>
                                  <Input 
                                    type="password"
                                    placeholder="Mínimo 6 caracteres"
                                    className="focus:ring-2 focus:ring-primary"
                                    {...field}
                                  />
                                </FormControl>
                                <FormDescription className="text-xs">
                                  Deixe vazio para não alterar
                                </FormDescription>
                                <FormMessage />
                              </FormItem>
                            )}
                          />

                          <FormField
                            control={form.control}
                            name="confirmar_nova_senha"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel className="text-sm font-semibold">
                                  Confirmar Nova Senha
                                </FormLabel>
                                <FormControl>
                                  <Input 
                                    type="password"
                                    placeholder="Digite a nova senha novamente"
                                    className="focus:ring-2 focus:ring-primary"
                                    {...field}
                                  />
                                </FormControl>
                                <FormDescription className="text-xs">
                                  Confirmação da nova senha
                                </FormDescription>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                        </div>
                      </div>
                      
                      <div className="mt-6 p-4 bg-muted/50 rounded-lg border border-dashed">
                        <h4 className="text-sm font-medium mb-2 text-amber-600">⚠️ Informações importantes:</h4>
                        <ul className="text-xs text-muted-foreground space-y-1">
                          <li>• Sua unidade organizacional: <strong>{user.unidade}</strong></li>
                          <li>• <strong>Nome, username e email</strong> são protegidos - somente administradores podem alterar</li>
                          <li>• Você pode alterar apenas sua <strong>foto</strong> e <strong>senha</strong></li>
                          <li>• Os perfis de acesso são definidos pela administração do sistema</li>
                        </ul>
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>
              </Tabs>
            </ScrollArea>

            <DialogFooter className="gap-2">
              <Button 
                type="button" 
                variant="outline"
                onClick={handleCancel}
                disabled={loading}
              >
                Cancelar
              </Button>
              <Button 
                type="button" 
                variant="ghost"
                onClick={() => form.reset()}
                disabled={loading}
              >
                Limpar Alterações
              </Button>
              <Button 
                type="submit"
                className="bg-primary hover:bg-primary/90"
                disabled={loading}
              >
                {loading ? "Salvando..." : "Salvar Alterações"}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}