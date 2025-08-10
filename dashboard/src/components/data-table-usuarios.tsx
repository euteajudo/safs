"use client"

import * as React from "react"
import {
  IconChevronDown,
  IconChevronLeft,
  IconChevronRight,
  IconChevronsLeft,
  IconChevronsRight,
  IconDotsVertical,
  IconLayoutColumns,
  IconPlus,
  IconFilter,
  IconSearch,
  IconDownload,
  IconX,
} from "@tabler/icons-react"
import {
  ColumnDef,
  ColumnFiltersState,
  flexRender,
  getCoreRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  SortingState,
  useReactTable,
  VisibilityState,
} from "@tanstack/react-table"
import { z } from "zod"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
  DropdownMenuLabel,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { UsuarioFormDialog } from "@/components/usuario-form-dialog"
import { useCurrentUser } from "@/contexts/auth-context"
import { canEditSpecificUser } from "@/lib/permissions"

export const schema = z.object({
  id: z.number(),
  unidade: z.string(),
  nome: z.string(),
  username: z.string(),
  email: z.string(),
  foto_url: z.string().optional(),
  is_active: z.boolean(),
  is_superuser: z.boolean(),
  is_chefe_unidade: z.boolean(),
  is_chefe_setor: z.boolean(),
  is_funcionario: z.boolean(),
  created_at: z.string(),
  updated_at: z.string().optional(),
})

interface Usuario {
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

const createColumns = (currentUser: Usuario | null): ColumnDef<z.infer<typeof schema>>[] => [
  {
    id: "select",
    header: ({ table }) => (
      <div className="flex items-center justify-center">
        <Checkbox
          checked={
            table.getIsAllPageRowsSelected() ||
            (table.getIsSomePageRowsSelected() && "indeterminate")
          }
          onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
          aria-label="Select all"
        />
      </div>
    ),
    cell: ({ row }) => (
      <div className="flex items-center justify-center">
        <Checkbox
          checked={row.getIsSelected()}
          onCheckedChange={(value) => row.toggleSelected(!!value)}
          aria-label="Select row"
        />
      </div>
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "foto_url",
    header: "Foto",
    cell: ({ row }) => (
      <Avatar className="h-8 w-8">
        <AvatarImage src={row.original.foto_url} alt={row.original.nome} />
        <AvatarFallback className="text-xs">
          {row.original.nome.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()}
        </AvatarFallback>
      </Avatar>
    ),
    enableSorting: false,
  },
  {
    accessorKey: "id",
    header: "ID",
    cell: ({ row }) => (
      <div className="text-xs font-mono text-muted-foreground">
        #{row.original.id}
      </div>
    ),
  },
  {
    accessorKey: "nome",
    header: "Nome",
    cell: ({ row }) => {
      return (
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="link" className="text-foreground w-fit px-0 text-left h-auto">
              {row.original.nome}
            </Button>
          </SheetTrigger>
          <SheetContent className="w-[500px] sm:w-[540px] pl-8 pr-6">
            <SheetHeader>
              <SheetTitle className="flex items-center gap-3">
                <Avatar className="h-12 w-12">
                  <AvatarImage src={row.original.foto_url} alt={row.original.nome} />
                  <AvatarFallback>
                    {row.original.nome.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <h3 className="text-lg font-semibold">{row.original.nome}</h3>
                  <p className="text-sm text-muted-foreground">{row.original.unidade}</p>
                </div>
              </SheetTitle>
              <SheetDescription>
                Estatísticas e informações detalhadas do usuário
              </SheetDescription>
            </SheetHeader>
            
            <div className="mt-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Itens Controlados</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-primary">
                      {Math.floor(Math.random() * 100) + 10}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Itens sob responsabilidade
                    </p>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Processos de Planejamento</CardTitle>
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
              </div>
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm font-medium">Informações do Usuário</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Username:</span>
                    <span className="text-sm text-muted-foreground font-mono">{row.original.username}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Email:</span>
                    <span className="text-sm text-muted-foreground">{row.original.email}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Status:</span>
                    <Badge variant={row.original.is_active ? "outline" : "secondary"} 
                           className={row.original.is_active ? "text-green-600 border-green-600" : "text-red-600 border-red-600"}>
                      {row.original.is_active ? "Ativo" : "Inativo"}
                    </Badge>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Criado em:</span>
                    <span className="text-sm text-muted-foreground">
                      {new Date(row.original.created_at).toLocaleDateString('pt-BR')}
                    </span>
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm font-medium">Permissões do Sistema</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    {row.original.is_superuser && (
                      <Badge variant="outline" className="text-purple-600 border-purple-600 justify-center">
                        Superusuário
                      </Badge>
                    )}
                    {row.original.is_chefe_unidade && (
                      <Badge variant="outline" className="text-blue-600 border-blue-600 justify-center">
                        Chefe de Unidade
                      </Badge>
                    )}
                    {row.original.is_chefe_setor && (
                      <Badge variant="outline" className="text-indigo-600 border-indigo-600 justify-center">
                        Chefe de Setor
                      </Badge>
                    )}
                    {row.original.is_funcionario && (
                      <Badge variant="outline" className="text-gray-600 border-gray-600 justify-center">
                        Funcionário
                      </Badge>
                    )}
                  </div>
                  {!row.original.is_superuser && !row.original.is_chefe_unidade && !row.original.is_chefe_setor && !row.original.is_funcionario && (
                    <div className="text-center text-sm text-muted-foreground py-2">
                      Nenhuma permissão especial atribuída
                    </div>
                  )}
                </CardContent>
              </Card>
              
              <div className="pt-4">
                {canEditSpecificUser(currentUser, row.original) && (
                  <UsuarioFormDialog
                    trigger={
                      <Button className="w-full">
                        Editar Usuário
                      </Button>
                    }
                    user={row.original}
                    mode="edit"
                  />
                )}
                {!canEditSpecificUser(currentUser, row.original) && (
                  <div className="text-center text-sm text-muted-foreground py-3">
                    Sem permissão para editar este usuário
                  </div>
                )}
              </div>
            </div>
          </SheetContent>
        </Sheet>
      )
    },
    enableHiding: false,
  },
  {
    accessorKey: "unidade",
    header: "Unidade",
    cell: ({ row }) => {
      const unidade = row.original.unidade;
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
      
      return (
        <Badge variant="outline" className={`${getUnidadeStyle(unidade)} px-2 py-1 text-xs font-medium`}>
          {unidade}
        </Badge>
      );
    },
  },
  {
    accessorKey: "username",
    header: "Username",
    cell: ({ row }) => (
      <div className="font-mono text-sm">
        {row.original.username}
      </div>
    ),
  },
  {
    accessorKey: "email",
    header: "Email",
    cell: ({ row }) => (
      <div className="text-sm text-muted-foreground">
        {row.original.email}
      </div>
    ),
  },
  {
    accessorKey: "is_active",
    header: "Status",
    cell: ({ row }) => (
      <Badge variant={row.original.is_active ? "outline" : "secondary"} className={row.original.is_active ? "text-green-600 border-green-600" : "text-red-600 border-red-600"}>
        {row.original.is_active ? "Ativo" : "Inativo"}
      </Badge>
    ),
  },
  {
    accessorKey: "is_superuser",
    header: "Superusuário",
    cell: ({ row }) => (
      row.original.is_superuser ? (
        <Badge variant="outline" className="text-purple-600 border-purple-600">
          Super
        </Badge>
      ) : null
    ),
  },
  {
    accessorKey: "is_chefe_unidade",
    header: "Chefe Unidade",
    cell: ({ row }) => (
      row.original.is_chefe_unidade ? (
        <Badge variant="outline" className="text-blue-600 border-blue-600">
          Chefe Un.
        </Badge>
      ) : null
    ),
  },
  {
    accessorKey: "is_chefe_setor",
    header: "Chefe Setor",
    cell: ({ row }) => (
      row.original.is_chefe_setor ? (
        <Badge variant="outline" className="text-indigo-600 border-indigo-600">
          Chefe Set.
        </Badge>
      ) : null
    ),
  },
  {
    accessorKey: "is_funcionario",
    header: "Funcionário",
    cell: ({ row }) => (
      row.original.is_funcionario ? (
        <Badge variant="outline" className="text-gray-600 border-gray-600">
          Funcionário
        </Badge>
      ) : null
    ),
  },
  {
    accessorKey: "created_at",
    header: "Data Criação",
    cell: ({ row }) => (
      <div className="text-xs text-muted-foreground">
        {new Date(row.original.created_at).toLocaleDateString('pt-BR')}
      </div>
    ),
  },
]

export function DataTable({
  data,
}: {
  data: Usuario[]
}) {
  const currentUser = useCurrentUser()
  const [rowSelection, setRowSelection] = React.useState({})
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({})
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [globalFilter, setGlobalFilter] = React.useState("")
  const [pagination, setPagination] = React.useState({
    pageIndex: 0,
    pageSize: 10,
  })
  const [unidadeFilter, setUnidadeFilter] = React.useState("")

  const columns = createColumns(currentUser)
  
  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      columnVisibility,
      rowSelection,
      columnFilters,
      globalFilter,
      pagination,
    },
    getRowId: (row) => row.id.toString(),
    enableRowSelection: true,
    onRowSelectionChange: setRowSelection,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    onGlobalFilterChange: setGlobalFilter,
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
  })

  const exportToExcel = () => {
    import("xlsx").then((XLSX) => {
      const ws = XLSX.utils.json_to_sheet(
        table.getFilteredRowModel().rows.map((row) => ({
          ID: row.original.id,
          Unidade: row.original.unidade,
          Nome: row.original.nome,
          Username: row.original.username,
          Email: row.original.email,
          Status: row.original.is_active ? "Ativo" : "Inativo",
          Superusuario: row.original.is_superuser ? "Sim" : "Não",
          "Chefe Unidade": row.original.is_chefe_unidade ? "Sim" : "Não",
          "Chefe Setor": row.original.is_chefe_setor ? "Sim" : "Não",
          Funcionario: row.original.is_funcionario ? "Sim" : "Não",
          "Data Criação": new Date(row.original.created_at).toLocaleDateString('pt-BR'),
        }))
      );
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Usuarios");
      XLSX.writeFile(wb, "usuarios.xlsx");
    });
  };

  return (
    <div className="w-full space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="relative flex items-center">
            <IconSearch className="absolute left-3 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Buscar por Nome, Email ou Username..."
              value={globalFilter ?? ""}
              onChange={(event) => setGlobalFilter(String(event.target.value))}
              className="w-110 pl-10 h-10 bg-gray-50 border-gray-200 rounded-lg shadow-sm focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all duration-200"
            />
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm">
                <IconFilter className="h-4 w-4" />
                <span className="hidden lg:inline">Filtros</span>
                {(unidadeFilter || 
                  columnFilters.some(f => f.id === "is_active") ||
                  columnFilters.some(f => f.id === "is_superuser") ||
                  columnFilters.some(f => f.id === "is_chefe_unidade") ||
                  columnFilters.some(f => f.id === "is_chefe_setor") ||
                  columnFilters.some(f => f.id === "is_funcionario")) && (
                  <Badge className="ml-2 h-4 px-1.5 bg-primary text-white">
                    {[
                      unidadeFilter,
                      columnFilters.some(f => f.id === "is_active"),
                      columnFilters.some(f => f.id === "is_superuser"),
                      columnFilters.some(f => f.id === "is_chefe_unidade"),
                      columnFilters.some(f => f.id === "is_chefe_setor"),
                      columnFilters.some(f => f.id === "is_funcionario")
                    ].filter(Boolean).length}
                  </Badge>
                )}
                <IconChevronDown className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-64">
              {/* Filtro por Unidade */}
              <div className="px-2 py-2">
                <Label className="text-xs font-medium text-muted-foreground">Unidade</Label>
                <Select
                  value={unidadeFilter}
                  onValueChange={(value) => {
                    if (value === "all") {
                      setUnidadeFilter("")
                      table.getColumn("unidade")?.setFilterValue(undefined)
                    } else {
                      setUnidadeFilter(value)
                      table.getColumn("unidade")?.setFilterValue(value)
                    }
                  }}
                >
                  <SelectTrigger className="h-8 text-xs mt-1">
                    <SelectValue placeholder="Todas as unidades" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todas</SelectItem>
                    <SelectItem value="ULOG">ULOG</SelectItem>
                    <SelectItem value="UACE">UACE</SelectItem>
                    <SelectItem value="UPDE">UPDE</SelectItem>
                    <SelectItem value="SAFS">SAFS</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <DropdownMenuSeparator />

              <DropdownMenuLabel>Status</DropdownMenuLabel>
              <DropdownMenuCheckboxItem
                checked={columnFilters.some(f => f.id === "is_active" && f.value === true)}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setColumnFilters(prev => [...prev.filter(f => f.id !== "is_active"), { id: "is_active", value: true }])
                  } else {
                    setColumnFilters(prev => prev.filter(f => !(f.id === "is_active" && f.value === true)))
                  }
                }}
              >
                Usuários Ativos
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={columnFilters.some(f => f.id === "is_active" && f.value === false)}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setColumnFilters(prev => [...prev.filter(f => f.id !== "is_active"), { id: "is_active", value: false }])
                  } else {
                    setColumnFilters(prev => prev.filter(f => !(f.id === "is_active" && f.value === false)))
                  }
                }}
              >
                Usuários Inativos
              </DropdownMenuCheckboxItem>
              
              <DropdownMenuSeparator />
              <DropdownMenuLabel>Permissões</DropdownMenuLabel>
              <DropdownMenuCheckboxItem
                checked={columnFilters.some(f => f.id === "is_superuser" && f.value === true)}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setColumnFilters(prev => [...prev.filter(f => f.id !== "is_superuser"), { id: "is_superuser", value: true }])
                  } else {
                    setColumnFilters(prev => prev.filter(f => !(f.id === "is_superuser" && f.value === true)))
                  }
                }}
              >
                Superusuários
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={columnFilters.some(f => f.id === "is_chefe_unidade" && f.value === true)}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setColumnFilters(prev => [...prev.filter(f => f.id !== "is_chefe_unidade"), { id: "is_chefe_unidade", value: true }])
                  } else {
                    setColumnFilters(prev => prev.filter(f => !(f.id === "is_chefe_unidade" && f.value === true)))
                  }
                }}
              >
                Chefes de Unidade
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={columnFilters.some(f => f.id === "is_chefe_setor" && f.value === true)}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setColumnFilters(prev => [...prev.filter(f => f.id !== "is_chefe_setor"), { id: "is_chefe_setor", value: true }])
                  } else {
                    setColumnFilters(prev => prev.filter(f => !(f.id === "is_chefe_setor" && f.value === true)))
                  }
                }}
              >
                Chefes de Setor
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={columnFilters.some(f => f.id === "is_funcionario" && f.value === true)}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setColumnFilters(prev => [...prev.filter(f => f.id !== "is_funcionario"), { id: "is_funcionario", value: true }])
                  } else {
                    setColumnFilters(prev => prev.filter(f => !(f.id === "is_funcionario" && f.value === true)))
                  }
                }}
              >
                Funcionários
              </DropdownMenuCheckboxItem>

              {/* Limpar Filtros */}
              {(unidadeFilter || 
                columnFilters.some(f => f.id === "is_active") ||
                columnFilters.some(f => f.id === "is_superuser") ||
                columnFilters.some(f => f.id === "is_chefe_unidade") ||
                columnFilters.some(f => f.id === "is_chefe_setor") ||
                columnFilters.some(f => f.id === "is_funcionario")) && (
                <>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    onClick={() => {
                      setUnidadeFilter("")
                      table.getColumn("unidade")?.setFilterValue(undefined)
                      setColumnFilters([])
                    }}
                    className="text-sm"
                  >
                    <IconX className="mr-2 h-4 w-4" />
                    Limpar Filtros
                  </DropdownMenuItem>
                </>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
          
          <Button variant="outline" size="sm" onClick={exportToExcel}>
            <IconDownload className="h-4 w-4" />
            <span className="hidden lg:inline">Exportar Excel</span>
            <span className="lg:hidden">Excel</span>
          </Button>
          
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm">
                <IconLayoutColumns className="h-4 w-4" />
                <span className="hidden lg:inline">Personalizar Colunas</span>
                <span className="lg:hidden">Colunas</span>
                <IconChevronDown className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              {table
                .getAllColumns()
                .filter(
                  (column) =>
                    typeof column.accessorFn !== "undefined" &&
                    column.getCanHide()
                )
                .map((column) => {
                  return (
                    <DropdownMenuCheckboxItem
                      key={column.id}
                      className="capitalize"
                      checked={column.getIsVisible()}
                      onCheckedChange={(value) =>
                        column.toggleVisibility(!!value)
                      }
                    >
                      {column.id === "nome" ? "Nome" :
                       column.id === "unidade" ? "Unidade" :
                       column.id === "username" ? "Username" :
                       column.id === "email" ? "Email" :
                       column.id === "is_active" ? "Status" :
                       column.id === "is_superuser" ? "Superusuário" :
                       column.id === "is_chefe_unidade" ? "Chefe Unidade" :
                       column.id === "is_chefe_setor" ? "Chefe Setor" :
                       column.id === "is_funcionario" ? "Funcionário" :
                       column.id === "created_at" ? "Data Criação" :
                       column.id}
                    </DropdownMenuCheckboxItem>
                  )
                })}
            </DropdownMenuContent>
          </DropdownMenu>
          
          <UsuarioFormDialog
            trigger={
              <Button size="sm">
                <IconPlus className="h-4 w-4" />
                <span className="hidden lg:inline">Adicionar Usuário</span>
                <span className="lg:hidden">Adicionar</span>
              </Button>
            }
            mode="create"
          />
        </div>
      </div>

      <div className="overflow-hidden rounded-lg border">
        <Table>
          <TableHeader className="bg-muted sticky top-0 z-10">
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id} colSpan={header.colSpan}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  )
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id} data-state={row.getIsSelected() && "selected"}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  Nenhum usuário encontrado.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <div className="flex items-center justify-between">
        <div className="text-muted-foreground hidden flex-1 text-sm lg:flex">
          {table.getFilteredSelectedRowModel().rows.length} de{" "}
          {table.getFilteredRowModel().rows.length} usuário(s) selecionado(s).
        </div>
        <div className="flex w-full items-center gap-8 lg:w-fit">
          <div className="hidden items-center gap-2 lg:flex">
            <Label htmlFor="rows-per-page" className="text-sm font-medium">
              Linhas por página
            </Label>
            <Select
              value={`${table.getState().pagination.pageSize}`}
              onValueChange={(value) => {
                table.setPageSize(Number(value))
              }}
            >
              <SelectTrigger size="sm" className="w-20" id="rows-per-page">
                <SelectValue
                  placeholder={table.getState().pagination.pageSize}
                />
              </SelectTrigger>
              <SelectContent side="top">
                {[10, 20, 30, 40, 50].map((pageSize) => (
                  <SelectItem key={pageSize} value={`${pageSize}`}>
                    {pageSize}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex w-fit items-center justify-center text-sm font-medium">
            Página {table.getState().pagination.pageIndex + 1} de{" "}
            {table.getPageCount()}
          </div>
          <div className="ml-auto flex items-center gap-2 lg:ml-0">
            <Button
              variant="outline"
              className="hidden h-8 w-8 p-0 lg:flex"
              onClick={() => table.setPageIndex(0)}
              disabled={!table.getCanPreviousPage()}
            >
              <span className="sr-only">Ir para primeira página</span>
              <IconChevronsLeft />
            </Button>
            <Button
              variant="outline"
              className="size-8"
              size="icon"
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
            >
              <span className="sr-only">Página anterior</span>
              <IconChevronLeft />
            </Button>
            <Button
              variant="outline"
              className="size-8"
              size="icon"
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
            >
              <span className="sr-only">Próxima página</span>
              <IconChevronRight />
            </Button>
            <Button
              variant="outline"
              className="hidden size-8 lg:flex"
              size="icon"
              onClick={() => table.setPageIndex(table.getPageCount() - 1)}
              disabled={!table.getCanNextPage()}
            >
              <span className="sr-only">Ir para última página</span>
              <IconChevronsRight />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}