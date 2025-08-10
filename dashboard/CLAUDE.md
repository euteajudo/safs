# Padrões de Desenvolvimento - Dashboard SAFS

## Estrutura Visual de Formulários

Sempre que solicitado um formulário, seguir este padrão visual:

### 1. **Componente Base**
- Usar `Dialog` (modal pop-up) ao invés de Drawer
- Importar de `@/components/ui/dialog`
- Modal centralizado com `max-w-4xl` para formulários extensos

### 2. **Organização dos Campos**
- Agrupar campos relacionados em **Tabs** quando houver muitos campos
- Usar `Card` e `CardContent` para agrupar visualmente campos relacionados
- Grid responsivo: `grid-cols-2` ou `grid-cols-3` conforme necessidade

### 3. **Estilização dos Campos**
- **Labels**: `text-sm font-semibold`
- **Campos obrigatórios**: `<span className="text-red-500">*</span>`
- **Descrições**: `text-xs` com `FormDescription`
- **Inputs**: `focus:ring-2 focus:ring-primary`
- **Textareas**: `min-h-[100px] resize-none`

### 4. **Validação**
- Usar `react-hook-form` com `zodResolver`
- Mensagens de erro claras em português
- Validações apropriadas para cada tipo de campo

### 5. **Layout do Modal**
```tsx
<Dialog>
  <DialogContent className="max-w-4xl max-h-[90vh]">
    <DialogHeader>
      <DialogTitle className="text-2xl font-bold">
      <DialogDescription>
    </DialogHeader>
    
    <Form>
      <ScrollArea className="h-[60vh] pr-4">
        <Tabs> // Se necessário
          <TabsList>
          <TabsContent>
            <Card>
              <CardContent className="pt-6 space-y-4">
                // Campos do formulário
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </ScrollArea>
      
      <DialogFooter className="gap-2">
        <Button variant="outline">Cancelar</Button>
        <Button variant="ghost">Limpar</Button>
        <Button className="bg-primary">Salvar</Button>
      </DialogFooter>
    </Form>
  </DialogContent>
</Dialog>
```

### 6. **Componentes UI Necessários**
- Dialog, DialogContent, DialogHeader, DialogFooter, DialogTitle, DialogDescription
- Form, FormField, FormItem, FormLabel, FormControl, FormDescription, FormMessage
- Input, Textarea, Select
- Button com variantes: outline, ghost, default
- Card, CardContent para agrupamento
- Tabs, TabsList, TabsTrigger, TabsContent quando apropriado
- ScrollArea para conteúdo extenso

### 7. **Boas Práticas**
- Estado controlado com `useState` para open/close do modal
- Reset do formulário após submissão bem-sucedida
- Console.log dos valores para debug durante desenvolvimento
- Comentário TODO para implementação futura da API
- Responsividade com grid system do Tailwind

## Tecnologias e Ferramentas

- **Framework**: Next.js 15 com App Router
- **Linguagem**: TypeScript
- **Estilização**: Tailwind CSS
- **Componentes UI**: shadcn/ui
- **Formulários**: react-hook-form + zod
- **Ícones**: @tabler/icons-react e lucide-react

## Estrutura do Projeto

```
dashboard/
├── src/
│   ├── app/
│   │   ├── dashboard/
│   │   │   └── catalogo/
│   │   │       └── page.tsx
│   ├── components/
│   │   ├── ui/          # Componentes base do shadcn/ui
│   │   └── *.tsx        # Componentes específicos do app
│   └── lib/
│       └── utils.ts     # Utilitários (cn para classes)
```

## Banco de Dados

- **PostgreSQL** com SQLAlchemy
- Modelos Python definidos em arquivos .py separados
- Campos do formulário devem corresponder aos modelos do banco

## Design System e Padrões Visuais

### Botões "Adicionar" - Padrão Obrigatório
**SEMPRE usar esta estrutura para botões de adicionar:**
```tsx
<Button size="sm">
  <IconPlus className="h-4 w-4" />
  <span className="hidden lg:inline">Adicionar [Nome]</span>
  <span className="lg:hidden">Adicionar</span>
</Button>
```

### Campo de Busca - Padrão Obrigatório
**SEMPRE usar esta estrutura para campos de busca em tabelas:**
```tsx
<div className="relative flex items-center">
  <IconSearch className="absolute left-3 h-4 w-4 text-gray-400" />
  <Input
    placeholder="Buscar por [critérios específicos]..."
    value={globalFilter ?? ""}
    onChange={(event) => setGlobalFilter(String(event.target.value))}
    className="w-110 pl-10 h-10 bg-gray-50 border-gray-200 rounded-lg shadow-sm focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all duration-200"
  />
</div>
```

### Cores das Tags/Badges das Unidades - FIXAS
**NUNCA alterar essas cores:**
```tsx
// Função para aplicar cores das unidades
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

// Aplicação em badges
<Badge variant="outline" className={`${getUnidadeStyle(unidade)} px-2 py-1 text-xs font-medium`}>
  {unidade}
</Badge>
```

### Disposição dos Botões nas Tabelas - Ordem Obrigatória
**SEMPRE manter esta sequência exata:**
```tsx
<div className="flex items-center gap-2">
  {/* 1º - FILTROS */}
  <DropdownMenu>
    <DropdownMenuTrigger asChild>
      <Button variant="outline" size="sm">
        <IconFilter className="h-4 w-4" />
        <span className="hidden lg:inline">Filtros</span>
        <IconChevronDown className="h-4 w-4" />
      </Button>
    </DropdownMenuTrigger>
  </DropdownMenu>
  
  {/* 2º - EXPORTAR EXCEL */}
  <Button variant="outline" size="sm" onClick={exportToExcel}>
    <IconDownload className="h-4 w-4" />
    <span className="hidden lg:inline">Exportar Excel</span>
    <span className="lg:hidden">Excel</span>
  </Button>
  
  {/* 3º - PERSONALIZAR COLUNAS */}
  <DropdownMenu>
    <DropdownMenuTrigger asChild>
      <Button variant="outline" size="sm">
        <IconLayoutColumns className="h-4 w-4" />
        <span className="hidden lg:inline">Personalizar Colunas</span>
        <span className="lg:hidden">Colunas</span>
        <IconChevronDown className="h-4 w-4" />
      </Button>
    </DropdownMenuTrigger>
  </DropdownMenu>
  
  {/* 4º - ADICIONAR ITEM/USUÁRIO */}
  <FormDialog
    trigger={
      <Button size="sm">
        <IconPlus className="h-4 w-4" />
        <span className="hidden lg:inline">Adicionar [Nome]</span>
        <span className="lg:hidden">Adicionar</span>
      </Button>
    }
  />
</div>
```

### Regras de Responsividade para Botões
- **Desktop**: Mostrar texto completo
- **Mobile**: Mostrar texto abreviado
- **Ícones**: Sempre `h-4 w-4` para consistência
- **Gap**: Sempre `gap-2` entre botões

### Padrões de Variants de Botões
- **Botão Principal (Adicionar)**: `size="sm"` sem variant (primary)
- **Botões Secundários**: `variant="outline" size="sm"`
- **Botão de Upload**: `variant="outline" size="sm"`

## Próximas Implementações

### Funcionalidades Pendentes
- [ ] Integração com API real
- [ ] Sistema de notificações
- [ ] Logs de auditoria
- [ ] Relatórios avançados
- [ ] Sistema de backup