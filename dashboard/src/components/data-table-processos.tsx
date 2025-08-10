"use client"

import * as React from "react"
import {
  IconChevronDown,
  IconChevronLeft,
  IconChevronRight,
  IconChevronsLeft,
  IconChevronsRight,
  IconDownload,
  IconFilter,
  IconLayoutColumns,
  IconPlus,
  IconSearch,
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
import * as XLSX from 'xlsx'

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
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
import { ProcessoFormDialog } from "@/components/processo-form-dialog"

import catalogoData from "@/app/dashboard/data-catalogo.json"

export const schema = z.object({
  id: z.number(),
  unidade: z.string(),
  objeto_aquisicao: z.string(),
  numero_processo_planejamento: z.string(),
  numero_item: z.string(),
  codigo_master: z.string(),
  status_processo_planejamento: z.string(),
  numero_processo_compra_centralizada: z.string().optional(),
  status_compra_centralizada: z.string().optional(),
  observacao: z.string().optional(),
})

function ObservacaoModal({ observacao, numeroProcesso }: { observacao?: string, numeroProcesso: string }) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button 
          variant="ghost" 
          className="p-0 h-auto text-left justify-start w-full text-sm text-muted-foreground hover:text-foreground"
        >
          <div className="max-w-48 truncate">
            {observacao || "-"}
          </div>
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Observações do Processo</DialogTitle>
          <DialogDescription>
            Processo: {numeroProcesso}
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <div className="text-sm">
            {observacao ? (
              <p className="whitespace-pre-wrap leading-relaxed">{observacao}</p>
            ) : (
              <p className="text-muted-foreground italic">Nenhuma observação registrada para este processo.</p>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

const getStatusStyle = (status: string) => {
  switch (status) {
    case "Em andamento":
      return "text-blue-600 border-blue-600 bg-blue-50";
    case "Finalizado":
      return "text-green-600 border-green-600 bg-green-50";
    case "Cancelado":
      return "text-red-600 border-red-600 bg-red-50";
    case "Pendente":
      return "text-orange-600 border-orange-600 bg-orange-50";
    case "Não iniciada":
      return "text-gray-500 border-gray-500 bg-gray-50";
    case "Finalizada":
      return "text-green-600 border-green-600 bg-green-50";
    case "Cancelada":
      return "text-red-600 border-red-600 bg-red-50";
    default:
      return "text-gray-500 border-gray-500 bg-gray-50";
  }
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

// Função para buscar itens relacionados ao processo (simulado)
const getItensDoProcesso = (numeroProcesso: string) => {
  // Simular itens do processo baseado no catálogo
  // Na implementação real, isso viria da API
  const itensSimulados = catalogoData
    .filter(() => Math.random() > 0.3) // Simula alguns itens relacionados
    .slice(0, Math.floor(Math.random() * 5) + 2) // Entre 2 e 6 itens por processo
    .map((item, index) => ({
      id: item.id,
      numero_item: `${String(index + 1).padStart(3, '0')}`,
      codigo_master: item.codigo_master,
      descricao: item.descricao,
      unidade: item.unidade,
      marca: item.marca,
      apresentacao: item.apresentacao,
      quantidade: Math.floor(Math.random() * 100) + 1,
    }));
  
  return itensSimulados;
};

const columns: ColumnDef<z.infer<typeof schema>>[] = [
  {
    accessorKey: "numero_processo_planejamento",
    header: "Processo Planejamento",
    cell: ({ row }) => (
      <ProcessoFormDialog
        trigger={
          <Button 
            variant="link" 
            className="p-0 h-auto font-mono text-sm text-foreground hover:text-primary"
          >
            {row.original.numero_processo_planejamento}
          </Button>
        }
        processo={row.original}
        mode="edit"
      />
    ),
    enableHiding: false,
  },
  {
    accessorKey: "unidade",
    header: "Unidade",
    cell: ({ row }) => (
      <Badge variant="outline" className={`${getUnidadeStyle(row.original.unidade)} px-2 py-1 text-xs font-medium`}>
        {row.original.unidade}
      </Badge>
    ),
  },
  {
    accessorKey: "objeto_aquisicao",
    header: "Objeto da Aquisição",
    cell: ({ row }) => {
      const itensDoProcesso = getItensDoProcesso(row.original.numero_processo_planejamento);
      
      return (
        <Sheet>
          <SheetTrigger asChild>
            <Button 
              variant="link" 
              className="text-foreground w-fit px-0 text-left h-auto max-w-xs"
            >
              <div className="truncate" title={row.original.objeto_aquisicao}>
                {row.original.objeto_aquisicao}
              </div>
            </Button>
          </SheetTrigger>
          <SheetContent className="w-[600px] sm:w-[700px] pl-8 pr-6">
            <SheetHeader>
              <SheetTitle className="flex items-start gap-3">
                <div>
                  <h3 className="text-lg font-semibold">{row.original.objeto_aquisicao}</h3>
                  <p className="text-sm text-muted-foreground font-mono">
                    {row.original.numero_processo_planejamento}
                  </p>
                </div>
              </SheetTitle>
              <SheetDescription>
                Detalhes do processo e itens relacionados
              </SheetDescription>
            </SheetHeader>
            
            <div className="mt-6 space-y-4">
              {/* Informações do Processo */}
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Informações do Processo</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Unidade:</span>
                    <Badge variant="outline" className={`${getUnidadeStyle(row.original.unidade)} px-2 py-1 text-xs font-medium`}>
                      {row.original.unidade}
                    </Badge>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Status Planejamento:</span>
                    <Badge 
                      variant="outline" 
                      className={`${getStatusStyle(row.original.status_processo_planejamento)} px-2 py-1 text-xs font-medium`}
                    >
                      {row.original.status_processo_planejamento}
                    </Badge>
                  </div>
                  {row.original.numero_processo_compra_centralizada && (
                    <div className="flex justify-between">
                      <span className="text-sm font-medium">Compra Centralizada:</span>
                      <span className="text-sm text-muted-foreground font-mono">
                        {row.original.numero_processo_compra_centralizada}
                      </span>
                    </div>
                  )}
                  {row.original.status_compra_centralizada && row.original.status_compra_centralizada !== "undefined" && (
                    <div className="flex justify-between">
                      <span className="text-sm font-medium">Status Compra:</span>
                      <Badge 
                        variant="outline" 
                        className={`${getStatusStyle(row.original.status_compra_centralizada)} px-2 py-1 text-xs font-medium`}
                      >
                        {row.original.status_compra_centralizada}
                      </Badge>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Lista de Itens */}
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">
                    Itens do Processo ({itensDoProcesso.length})
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {itensDoProcesso.map((item, index) => (
                      <div
                        key={`${item.id}-${index}`}
                        className="flex items-start justify-between p-3 bg-gray-50 rounded-lg border"
                      >
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-2">
                            <Badge variant="secondary" className="text-xs font-mono">
                              Item: {item.numero_item}
                            </Badge>
                            <Badge variant="outline" className="text-xs font-mono">
                              {item.codigo_master}
                            </Badge>
                            <Badge 
                              variant="outline" 
                              className={`${getUnidadeStyle(item.unidade)} px-2 py-1 text-xs`}
                            >
                              {item.unidade}
                            </Badge>
                          </div>
                          <p className="text-sm text-gray-900 mb-1 leading-tight">
                            {item.descricao}
                          </p>
                          <div className="flex items-center gap-4 text-xs text-muted-foreground">
                            {item.marca && <span>Marca: {item.marca}</span>}
                            {item.apresentacao && <span>Apresentação: {item.apresentacao}</span>}
                            <span className="font-semibold text-primary">Qtd: {item.quantidade}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Observações */}
              {row.original.observacao && (
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Observações</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
                      {row.original.observacao}
                    </p>
                  </CardContent>
                </Card>
              )}
            </div>
          </SheetContent>
        </Sheet>
      );
    },
    enableHiding: false,
  },
  {
    accessorKey: "status_processo_planejamento",
    header: "Status Planejamento",
    cell: ({ row }) => (
      <Badge 
        variant="outline" 
        className={`${getStatusStyle(row.original.status_processo_planejamento)} px-2 py-1 text-xs font-medium`}
      >
        {row.original.status_processo_planejamento}
      </Badge>
    ),
  },
  {
    accessorKey: "numero_processo_compra_centralizada",
    header: "Compra Centralizada",
    cell: ({ row }) => (
      <div className="text-sm font-mono">
        {row.original.numero_processo_compra_centralizada || "-"}
      </div>
    ),
  },
  {
    accessorKey: "status_compra_centralizada",
    header: "Status Compra",
    cell: ({ row }) => {
      if (!row.original.status_compra_centralizada || row.original.status_compra_centralizada === "undefined") {
        return <span className="text-muted-foreground">-</span>;
      }
      return (
        <Badge 
          variant="outline" 
          className={`${getStatusStyle(row.original.status_compra_centralizada)} px-2 py-1 text-xs font-medium`}
        >
          {row.original.status_compra_centralizada}
        </Badge>
      );
    },
  },
  {
    accessorKey: "observacao",
    header: "Observações",
    cell: ({ row }) => (
      <ObservacaoModal 
        observacao={row.original.observacao}
        numeroProcesso={row.original.numero_processo_planejamento}
      />
    ),
  },
]

export function DataTable({
  data,
}: {
  data: z.infer<typeof schema>[]
}) {
  const [rowSelection, setRowSelection] = React.useState({})
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({})
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
  const [globalFilter, setGlobalFilter] = React.useState("")
  const [sorting, setSorting] = React.useState<SortingState>([])
  
  // Estados para filtros específicos
  const [unidadeFilter, setUnidadeFilter] = React.useState<string>("")
  const [statusPlanejamentoFilter, setStatusPlanejamentoFilter] = React.useState<string>("")
  const [statusCompraFilter, setStatusCompraFilter] = React.useState<string>("")
  const [pagination, setPagination] = React.useState({
    pageIndex: 0,
    pageSize: 10,
  })

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
    onGlobalFilterChange: setGlobalFilter,
    onColumnVisibilityChange: setColumnVisibility,
    onPaginationChange: setPagination,
    globalFilterFn: (row, columnId, value) => {
      const numeroProcesso = row.getValue("numero_processo_planejamento") as string;
      const objetoAquisicao = row.getValue("objeto_aquisicao") as string;
      const codigoMaster = row.getValue("codigo_master") as string;
      
      return (
        numeroProcesso?.toLowerCase().includes(value.toLowerCase()) ||
        objetoAquisicao?.toLowerCase().includes(value.toLowerCase()) ||
        codigoMaster?.toLowerCase().includes(value.toLowerCase())
      );
    },
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
  })

  function exportToExcel() {
    // Pegar apenas os dados visíveis na página atual
    const visibleRows = table.getRowModel().rows;
    
    // Preparar os dados para exportação
    const exportData = visibleRows.map(row => ({
      'Processo Planejamento': row.original.numero_processo_planejamento,
      'Unidade': row.original.unidade,
      'Objeto da Aquisição': row.original.objeto_aquisicao,
      'Item': row.original.numero_item,
      'Código Master': row.original.codigo_master,
      'Status Planejamento': row.original.status_processo_planejamento,
      'Compra Centralizada': row.original.numero_processo_compra_centralizada || '',
      'Status Compra': row.original.status_compra_centralizada || '',
      'Observações': row.original.observacao || ''
    }));

    // Criar workbook e worksheet
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(exportData);

    // Configurar largura das colunas
    const colWidths = [
      { wch: 25 }, // Processo Planejamento
      { wch: 10 }, // Unidade
      { wch: 40 }, // Objeto da Aquisição
      { wch: 10 }, // Item
      { wch: 15 }, // Código Master
      { wch: 20 }, // Status Planejamento
      { wch: 25 }, // Compra Centralizada
      { wch: 20 }, // Status Compra
      { wch: 30 }  // Observações
    ];
    ws['!cols'] = colWidths;

    // Adicionar worksheet ao workbook
    XLSX.utils.book_append_sheet(wb, ws, 'Processos SAFS');

    // Gerar nome do arquivo com data atual
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
    const fileName = `processos-safs-${dateStr}.xlsx`;

    // Fazer download
    XLSX.writeFile(wb, fileName);
  }

  return (
    <div className="w-full flex-col justify-start gap-6">
      <div className="flex items-center justify-between px-4 lg:px-6 mt-3">
        <div className="flex items-center gap-2">
          <div className="relative flex items-center">
            <IconSearch className="absolute left-3 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Buscar por Processo, Objeto ou Código Master..."
              value={globalFilter ?? ""}
              onChange={(event) => setGlobalFilter(String(event.target.value))}
              className="w-110 pl-10 h-10 bg-gray-50 border-gray-200 rounded-lg shadow-sm focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all duration-200"
            />
          </div>
        </div>
        <div className="flex items-center gap-2">
          {/* Menu de Filtros */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm">
                <IconFilter className="h-4 w-4" />
                <span className="hidden lg:inline">Filtros</span>
                <span className="lg:hidden">Filtros</span>
                {(unidadeFilter || statusPlanejamentoFilter || statusCompraFilter) && (
                  <Badge className="ml-2 h-4 px-1.5 bg-primary text-white">
                    {[unidadeFilter, statusPlanejamentoFilter, statusCompraFilter].filter(Boolean).length}
                  </Badge>
                )}
                <IconChevronDown className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-64">
              {/* Filtro Unidade com Dropdown */}
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
              
              {/* Filtro Status Planejamento */}
              <div className="px-2 py-2">
                <Label className="text-xs font-medium text-muted-foreground">Status Planejamento</Label>
                <Select
                  value={statusPlanejamentoFilter}
                  onValueChange={(value) => {
                    if (value === "all") {
                      setStatusPlanejamentoFilter("")
                      table.getColumn("status_processo_planejamento")?.setFilterValue(undefined)
                    } else {
                      setStatusPlanejamentoFilter(value)
                      table.getColumn("status_processo_planejamento")?.setFilterValue(value)
                    }
                  }}
                >
                  <SelectTrigger className="h-8 text-xs mt-1">
                    <SelectValue placeholder="Todos os status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todos</SelectItem>
                    <SelectItem value="Em andamento">Em andamento</SelectItem>
                    <SelectItem value="Finalizado">Finalizado</SelectItem>
                    <SelectItem value="Cancelado">Cancelado</SelectItem>
                    <SelectItem value="Pendente">Pendente</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <DropdownMenuSeparator />
              
              {/* Filtro Status Compra */}
              <div className="px-2 py-2">
                <Label className="text-xs font-medium text-muted-foreground">Status Compra</Label>
                <Select
                  value={statusCompraFilter}
                  onValueChange={(value) => {
                    if (value === "all") {
                      setStatusCompraFilter("")
                      table.getColumn("status_compra_centralizada")?.setFilterValue(undefined)
                    } else {
                      setStatusCompraFilter(value)
                      table.getColumn("status_compra_centralizada")?.setFilterValue(value)
                    }
                  }}
                >
                  <SelectTrigger className="h-8 text-xs mt-1">
                    <SelectValue placeholder="Todos os status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todos</SelectItem>
                    <SelectItem value="Não iniciada">Não iniciada</SelectItem>
                    <SelectItem value="Em andamento">Em andamento</SelectItem>
                    <SelectItem value="Finalizada">Finalizada</SelectItem>
                    <SelectItem value="Cancelada">Cancelada</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              {/* Limpar Filtros */}
              {(unidadeFilter || statusPlanejamentoFilter || statusCompraFilter) && (
                <>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    onClick={() => {
                      setUnidadeFilter("")
                      setStatusPlanejamentoFilter("")
                      setStatusCompraFilter("")
                      table.getColumn("unidade")?.setFilterValue(undefined)
                      table.getColumn("status_processo_planejamento")?.setFilterValue(undefined)
                      table.getColumn("status_compra_centralizada")?.setFilterValue(undefined)
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

          {/* Botão de Download */}
          <Button 
            variant="outline" 
            size="sm"
            onClick={exportToExcel}
            title="Baixar planilha dos dados visíveis"
          >
            <IconDownload className="h-4 w-4" />
            <span className="hidden lg:inline">Exportar Excel</span>
            <span className="lg:hidden">Excel</span>
          </Button>

          {/* Menu de Personalizar Colunas */}
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
                      {column.id === "numero_processo_planejamento" ? "Processo Planejamento" :
                       column.id === "unidade" ? "Unidade" :
                       column.id === "objeto_aquisicao" ? "Objeto da Aquisição" :
                       column.id === "status_processo_planejamento" ? "Status Planejamento" :
                       column.id === "numero_processo_compra_centralizada" ? "Compra Centralizada" :
                       column.id === "status_compra_centralizada" ? "Status Compra" :
                       column.id === "observacao" ? "Observações" :
                       column.id}
                    </DropdownMenuCheckboxItem>
                  )
                })}
            </DropdownMenuContent>
          </DropdownMenu>
          
          <ProcessoFormDialog
            trigger={
              <Button size="sm">
                <IconPlus className="h-4 w-4" />
                <span className="hidden lg:inline">Adicionar Processo</span>
                <span className="lg:hidden">Adicionar</span>
              </Button>
            }
            mode="create"
          />
        </div>
      </div>
      <div className="relative flex flex-col gap-4 overflow-auto px-4 lg:px-6 mt-3">
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
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() && "selected"}
                  >
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
                    Nenhum resultado encontrado.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
        <div className="flex items-center justify-between px-4">
          <div className="text-muted-foreground hidden flex-1 text-sm lg:flex">
            {table.getFilteredRowModel().rows.length} processos no total
          </div>
          <div className="flex w-full items-center gap-8 lg:w-fit">
            <div className="hidden items-center gap-2 lg:flex">
              <Label htmlFor="rows-per-page" className="text-sm font-medium">
                Itens por página
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
                <span className="sr-only">Go to first page</span>
                <IconChevronsLeft />
              </Button>
              <Button
                variant="outline"
                className="size-8"
                size="icon"
                onClick={() => table.previousPage()}
                disabled={!table.getCanPreviousPage()}
              >
                <span className="sr-only">Go to previous page</span>
                <IconChevronLeft />
              </Button>
              <Button
                variant="outline"
                className="size-8"
                size="icon"
                onClick={() => table.nextPage()}
                disabled={!table.getCanNextPage()}
              >
                <span className="sr-only">Go to next page</span>
                <IconChevronRight />
              </Button>
              <Button
                variant="outline"
                className="hidden size-8 lg:flex"
                size="icon"
                onClick={() => table.setPageIndex(table.getPageCount() - 1)}
                disabled={!table.getCanNextPage()}
              >
                <span className="sr-only">Go to last page</span>
                <IconChevronsRight />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}