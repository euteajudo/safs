"use client"

import * as React from "react"
import {
  closestCenter,
  DndContext,
  KeyboardSensor,
  MouseSensor,
  TouchSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
  type UniqueIdentifier,
} from "@dnd-kit/core"
import { restrictToVerticalAxis } from "@dnd-kit/modifiers"
import {
  arrayMove,
  SortableContext,
  useSortable,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"
import {
  IconChevronDown,
  IconChevronLeft,
  IconChevronRight,
  IconChevronsLeft,
  IconChevronsRight,
  IconCircleCheckFilled,
  IconDotsVertical,
  IconDownload,
  IconFilter,
  IconGripVertical,
  IconLayoutColumns,
  IconLoader,
  IconPlus,
  IconSearch,
  IconTrendingUp,
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
  Row,
  SortingState,
  useReactTable,
  VisibilityState,
} from "@tanstack/react-table"
import { toast } from "sonner"
import { z } from "zod"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
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
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import { CatalogoFormDialog } from "@/components/catalogo-form-dialog"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts"
import * as XLSX from 'xlsx'

export const schema = z.object({
  id: z.number(),
  unidade: z.string(),
  marca: z.string().optional(),
  embalagem: z.string().optional(),
  codigo_master: z.string(),
  codigo_aghu_hu: z.string().optional(),
  codigo_aghu_meac: z.string().optional(),
  catmat: z.string().optional(),
  codigo_ebserh: z.string().optional(),
  descricao: z.string(),
  apresentacao: z.string().optional(),
  classificacao_xyz: z.string().optional(),
  comprador_id: z.number().optional(),
  controlador_id: z.number().optional(),
  processo_ids: z.array(z.number()).optional(),
  observacao: z.string().optional(),
  // Campos calculados/relacionados
  comprador_nome: z.string().optional(),
  controlador_nome: z.string().optional(),
  processo: z.object({
    id: z.number(),
    numero_processo_planejamento: z.string(),
    objeto_aquisicao: z.string().optional(),
  }).optional(),
  processos_adicionais: z.array(z.object({
    id: z.number(),
    numero_processo_planejamento: z.string(),
    objeto_aquisicao: z.string().optional(),
  })).optional(),
})

// Create a separate component for the drag handle
function DragHandle({ id }: { id: number }) {
  const { attributes, listeners } = useSortable({
    id,
  })

  return (
    <Button
      {...attributes}
      {...listeners}
      variant="ghost"
      size="icon"
      className="text-muted-foreground size-7 hover:bg-transparent"
    >
      <IconGripVertical className="text-muted-foreground size-3" />
      <span className="sr-only">Drag to reorder</span>
    </Button>
  )
}

function ObservacaoModal({ observacao, codigoMaster }: { observacao?: string, codigoMaster: string }) {
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
          <DialogTitle>Observações do Item</DialogTitle>
          <DialogDescription>
            Código Master: {codigoMaster}
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <div className="text-sm">
            {observacao ? (
              <p className="whitespace-pre-wrap leading-relaxed">{observacao}</p>
            ) : (
              <p className="text-muted-foreground italic">Nenhuma observação registrada para este item.</p>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

function EbserhDetailsSheet({ codigoEbserh, codigoMaster, descricao }: { 
  codigoEbserh?: string, 
  codigoMaster: string, 
  descricao: string 
}) {
  // Dados mockados para o gráfico de consumo dos últimos 12 meses
  const consumoData = [
    { mes: 'Jan', quantidade: 120 },
    { mes: 'Fev', quantidade: 98 },
    { mes: 'Mar', quantidade: 150 },
    { mes: 'Abr', quantidade: 134 },
    { mes: 'Mai', quantidade: 167 },
    { mes: 'Jun', quantidade: 145 },
    { mes: 'Jul', quantidade: 188 },
    { mes: 'Ago', quantidade: 201 },
    { mes: 'Set', quantidade: 176 },
    { mes: 'Out', quantidade: 223 },
    { mes: 'Nov', quantidade: 189 },
    { mes: 'Dez', quantidade: 156 },
  ];

  // Dados mockados para estoque
  const estoqueInfo = {
    emEstoque: 250,
    empenhada: 50,
    aReceber: 100,
    preEmpenhada: 25,
    aEmpenhar: 75,
    fimVigencia: "31/12/2024"
  };

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button 
          variant="ghost" 
          className="p-0 h-auto font-mono text-sm text-foreground hover:text-primary cursor-pointer"
        >
          {codigoEbserh || "-"}
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="w-[600px] sm:max-w-[600px]">
        <SheetHeader className="pl-6">
          <SheetTitle>Detalhes EBSERH</SheetTitle>
          <SheetDescription>
            {codigoMaster} - {descricao}
          </SheetDescription>
        </SheetHeader>
        
        <div className="py-6 px-6 space-y-6">
          {/* Gráfico de consumo */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Consumo dos Últimos 12 Meses</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={consumoData}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="mes" 
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis 
                    tick={{ fontSize: 12 }}
                    label={{ value: 'Quantidade', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip 
                    labelFormatter={(label) => `Mês: ${label}`}
                    formatter={(value) => [value, 'Quantidade']}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="quantidade" 
                    stroke="#2563eb" 
                    strokeWidth={2}
                    dot={{ fill: '#2563eb', strokeWidth: 2, r: 4 }}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Informações de estoque */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Informações de Estoque</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-muted/50 rounded-lg p-4">
                <div className="text-sm text-muted-foreground">QTD em estoque</div>
                <div className="text-2xl font-bold text-green-600">{estoqueInfo.emEstoque}</div>
              </div>
              <div className="bg-muted/50 rounded-lg p-4">
                <div className="text-sm text-muted-foreground">QTD empenhada</div>
                <div className="text-2xl font-bold text-orange-600">{estoqueInfo.empenhada}</div>
              </div>
              <div className="bg-muted/50 rounded-lg p-4">
                <div className="text-sm text-muted-foreground">QTD a receber</div>
                <div className="text-2xl font-bold text-blue-600">{estoqueInfo.aReceber}</div>
              </div>
              <div className="bg-muted/50 rounded-lg p-4">
                <div className="text-sm text-muted-foreground">QTD pré-empenhada</div>
                <div className="text-2xl font-bold text-purple-600">{estoqueInfo.preEmpenhada}</div>
              </div>
              <div className="bg-muted/50 rounded-lg p-4">
                <div className="text-sm text-muted-foreground">QTD a empenhar</div>
                <div className="text-2xl font-bold text-yellow-600">{estoqueInfo.aEmpenhar}</div>
              </div>
              <div className="bg-muted/50 rounded-lg p-4">
                <div className="text-sm text-muted-foreground">Fim de vigência</div>
                <div className="text-2xl font-bold text-red-600">{estoqueInfo.fimVigencia}</div>
              </div>
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  )
}

const columns: ColumnDef<z.infer<typeof schema>>[] = [
  {
    accessorKey: "codigo_master",
    header: "Código Master",
    cell: ({ row }) => (
      <CatalogoFormDialog
        trigger={
          <Button 
            variant="link" 
            className="p-0 h-auto font-mono text-sm text-foreground hover:text-primary"
          >
            {row.original.codigo_master}
          </Button>
        }
        item={row.original}
        mode="edit"
      />
    ),
    enableHiding: false,
  },
  {
    accessorKey: "descricao",
    header: "Descrição",
    cell: ({ row }) => (
      <div className="max-w-xs truncate" title={row.original.descricao}>
        {row.original.descricao}
      </div>
    ),
  },
  {
    accessorKey: "unidade",
    header: "Unidade",
    cell: ({ row }) => {
      const isULOG = row.original.unidade === 'ULOG';
      const colorClass = isULOG ? 'text-orange-500 border-orange-500' : 'text-green-500 border-green-500';
      
      return (
        <Badge variant="outline" className={`${colorClass} px-1.5`}>
          {row.original.unidade}
        </Badge>
      )
    },
  },
  {
    accessorKey: "marca",
    header: "Marca",
    cell: ({ row }) => (
      <div className="text-sm text-muted-foreground">
        {row.original.marca || "-"}
      </div>
    ),
  },
  {
    accessorKey: "embalagem",
    header: "Embalagem",
    cell: ({ row }) => (
      <div className="text-sm text-muted-foreground">
        {row.original.embalagem || "-"}
      </div>
    ),
  },
  {
    accessorKey: "apresentacao",
    header: "Apresentação",
    cell: ({ row }) => (
      <div className="text-sm text-muted-foreground max-w-32 truncate" title={row.original.apresentacao}>
        {row.original.apresentacao || "-"}
      </div>
    ),
  },
  {
    accessorKey: "classificacao_xyz",
    header: "Classificação XYZ",
    cell: ({ row }) => {
      const classificacao = row.original.classificacao_xyz;
      if (!classificacao) return <span className="text-muted-foreground">-</span>;
      
      const colorClass = classificacao === 'X' ? 'bg-sky-500 text-white' : 
                        classificacao === 'Y' ? 'bg-rose-500 text-white' : 
                        'bg-lime-400 text-black';
      
      return (
        <Badge className={colorClass}>
          {classificacao}
        </Badge>
      )
    },
  },
  {
    accessorKey: "catmat",
    header: "CATMAT",
    cell: ({ row }) => (
      <div className="text-sm font-mono">
        {row.original.catmat || "-"}
      </div>
    ),
  },
  {
    accessorKey: "codigo_aghu_hu",
    header: "AGHU HU",
    cell: ({ row }) => (
      <div className="text-sm font-mono">
        {row.original.codigo_aghu_hu || "-"}
      </div>
    ),
  },
  {
    accessorKey: "codigo_aghu_meac",
    header: "AGHU MEAC",
    cell: ({ row }) => (
      <div className="text-sm font-mono">
        {row.original.codigo_aghu_meac || "-"}
      </div>
    ),
  },
  {
    accessorKey: "codigo_ebserh",
    header: "EBSERH",
    cell: ({ row }) => (
      <EbserhDetailsSheet 
        codigoEbserh={row.original.codigo_ebserh}
        codigoMaster={row.original.codigo_master}
        descricao={row.original.descricao}
      />
    ),
  },
  {
    accessorKey: "comprador",
    header: "Comprador",
    cell: ({ row }) => {
      return (
        <div className="text-sm">
          {row.original.comprador_nome || (
            <span className="text-muted-foreground italic">Não atribuído</span>
          )}
        </div>
      )
    },
  },
  {
    accessorKey: "controlador",
    header: "Controlador",
    cell: ({ row }) => {
      return (
        <div className="text-sm">
          {row.original.controlador_nome || (
            <span className="text-muted-foreground italic">Não atribuído</span>
          )}
        </div>
      )
    },
  },
  {
    accessorKey: "processos",
    header: "Processos",
    cell: ({ row }) => {
      const processo = row.original.processo;
      const processosAdicionais = row.original.processos_adicionais || [];
      const todosProcessos = [];
      
      if (processo) {
        todosProcessos.push({ ...processo, isPrincipal: true });
      }
      
      todosProcessos.push(...processosAdicionais.map(p => ({ ...p, isPrincipal: false })));
      
      if (todosProcessos.length === 0) {
        return <span className="text-muted-foreground italic">Nenhum processo</span>;
      }
      
      return (
        <div className="max-w-48 space-y-1">
          {todosProcessos.slice(0, 3).map((processo, index) => (
            <div key={`${processo.id}-${processo.isPrincipal}`} className="text-xs">
              <div className="font-mono text-primary flex items-center gap-1">
                {processo.numero_processo_planejamento}
                {processo.isPrincipal && (
                  <span className="bg-blue-100 text-blue-800 px-1 rounded text-xs">Principal</span>
                )}
              </div>
              {processo.objeto_aquisicao && (
                <div className="text-muted-foreground truncate" title={processo.objeto_aquisicao}>
                  {processo.objeto_aquisicao}
                </div>
              )}
            </div>
          ))}
          {todosProcessos.length > 3 && (
            <div className="text-xs text-muted-foreground">
              +{todosProcessos.length - 3} mais
            </div>
          )}
        </div>
      );
    },
  },
  {
    accessorKey: "observacao",
    header: "Observações",
    cell: ({ row }) => (
      <ObservacaoModal 
        observacao={row.original.observacao}
        codigoMaster={row.original.codigo_master}
      />
    ),
  },
]

function DraggableRow({ row }: { row: Row<z.infer<typeof schema>> }) {
  const { transform, transition, setNodeRef, isDragging } = useSortable({
    id: row.original.id,
  })

  return (
    <TableRow
      data-state={row.getIsSelected() && "selected"}
      data-dragging={isDragging}
      ref={setNodeRef}
      className="relative z-0 data-[dragging=true]:z-10 data-[dragging=true]:opacity-80"
      style={{
        transform: CSS.Transform.toString(transform),
        transition: transition,
      }}
    >
      {row.getVisibleCells().map((cell) => (
        <TableCell key={cell.id}>
          {flexRender(cell.column.columnDef.cell, cell.getContext())}
        </TableCell>
      ))}
    </TableRow>
  )
}

export function DataTable({
  data: initialData,
}: {
  data: z.infer<typeof schema>[]
}) {
  const [data, setData] = React.useState(() => initialData)
  const [rowSelection, setRowSelection] = React.useState({})
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({})
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  )
  const [globalFilter, setGlobalFilter] = React.useState("")
  const [sorting, setSorting] = React.useState<SortingState>([])
  
  // Estados para filtros específicos
  const [unidadeFilter, setUnidadeFilter] = React.useState<string>("")
  const [classificacaoFilter, setClassificacaoFilter] = React.useState<string>("")
  const [compradorFilter, setCompradorFilter] = React.useState<string>("")
  const [controladorFilter, setControladorFilter] = React.useState<string>("")
  const [pagination, setPagination] = React.useState({
    pageIndex: 0,
    pageSize: 10,
  })
  const sortableId = React.useId()
  const sensors = useSensors(
    useSensor(MouseSensor, {}),
    useSensor(TouchSensor, {}),
    useSensor(KeyboardSensor, {})
  )

  const dataIds = React.useMemo<UniqueIdentifier[]>(
    () => data?.map(({ id }) => id) || [],
    [data]
  )

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
      const codigoMaster = row.getValue("codigo_master") as string;
      const descricao = row.getValue("descricao") as string;
      
      return (
        codigoMaster?.toLowerCase().includes(value.toLowerCase()) ||
        descricao?.toLowerCase().includes(value.toLowerCase())
      );
    },
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
  })

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event
    if (active && over && active.id !== over.id) {
      setData((data) => {
        const oldIndex = dataIds.indexOf(active.id)
        const newIndex = dataIds.indexOf(over.id)
        return arrayMove(data, oldIndex, newIndex)
      })
    }
  }

  function exportToExcel() {
    // Pegar apenas os dados visíveis na página atual
    const visibleRows = table.getRowModel().rows;
    
    // Preparar os dados para exportação
    const exportData = visibleRows.map(row => ({
      'Código Master': row.original.codigo_master,
      'Descrição': row.original.descricao,
      'Unidade': row.original.unidade,
      'Marca': row.original.marca || '',
      'Embalagem': row.original.embalagem || '',
      'Apresentação': row.original.apresentacao || '',
      'Classificação XYZ': row.original.classificacao_xyz || '',
      'CATMAT': row.original.catmat || '',
      'AGHU HU': row.original.codigo_aghu_hu || '',
      'AGHU MEAC': row.original.codigo_aghu_meac || '',
      'EBSERH': row.original.codigo_ebserh || '',
      'Comprador': row.original.comprador_nome || '',
      'Controlador': row.original.controlador_nome || '',
      'Processo Principal': row.original.processo?.numero_processo_planejamento || '',
      'Processos Adicionais': row.original.processos_adicionais?.map(p => p.numero_processo_planejamento).join(', ') || '',
      'Observações': row.original.observacao || ''
    }));

    // Criar workbook e worksheet
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(exportData);

    // Configurar largura das colunas
    const colWidths = [
      { wch: 15 }, // Código Master
      { wch: 40 }, // Descrição
      { wch: 10 }, // Unidade
      { wch: 20 }, // Marca
      { wch: 15 }, // Embalagem
      { wch: 25 }, // Apresentação
      { wch: 12 }, // Classificação XYZ
      { wch: 15 }, // CATMAT
      { wch: 15 }, // AGHU HU
      { wch: 15 }, // AGHU MEAC
      { wch: 15 }, // EBSERH
      { wch: 20 }, // Comprador
      { wch: 20 }, // Controlador
      { wch: 25 }, // Processo Principal
      { wch: 30 }, // Processos Adicionais
      { wch: 30 }  // Observações
    ];
    ws['!cols'] = colWidths;

    // Adicionar worksheet ao workbook
    XLSX.utils.book_append_sheet(wb, ws, 'Catálogo SAFS');

    // Gerar nome do arquivo com data atual
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
    const fileName = `catalogo-safs-${dateStr}.xlsx`;

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
              placeholder="Buscar por Código Master ou Descrição..."
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
                <IconFilter />
                <span className="hidden lg:inline">Filtros</span>
                <span className="lg:hidden">Filtros</span>
                {(unidadeFilter || classificacaoFilter || compradorFilter || controladorFilter) && (
                  <Badge className="ml-2 h-4 px-1.5 bg-primary text-white">
                    {[unidadeFilter, classificacaoFilter, compradorFilter, controladorFilter].filter(Boolean).length}
                  </Badge>
                )}
                <IconChevronDown />
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
                  </SelectContent>
                </Select>
              </div>
              
              <DropdownMenuSeparator />
              
              {/* Filtro Classificação XYZ */}
              <DropdownMenuCheckboxItem
                checked={classificacaoFilter === "X"}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setClassificacaoFilter("X")
                    table.getColumn("classificacao_xyz")?.setFilterValue("X")
                  } else {
                    setClassificacaoFilter("")
                    table.getColumn("classificacao_xyz")?.setFilterValue(undefined)
                  }
                }}
              >
                Classificação: X
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={classificacaoFilter === "Y"}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setClassificacaoFilter("Y")
                    table.getColumn("classificacao_xyz")?.setFilterValue("Y")
                  } else {
                    setClassificacaoFilter("")
                    table.getColumn("classificacao_xyz")?.setFilterValue(undefined)
                  }
                }}
              >
                Classificação: Y
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={classificacaoFilter === "Z"}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setClassificacaoFilter("Z")
                    table.getColumn("classificacao_xyz")?.setFilterValue("Z")
                  } else {
                    setClassificacaoFilter("")
                    table.getColumn("classificacao_xyz")?.setFilterValue(undefined)
                  }
                }}
              >
                Classificação: Z
              </DropdownMenuCheckboxItem>
              
              <DropdownMenuSeparator />
              
              {/* Filtro Comprador com Dropdown */}
              <div className="px-2 py-2">
                <Label className="text-xs font-medium text-muted-foreground">Comprador</Label>
                <Select
                  value={compradorFilter}
                  onValueChange={(value) => {
                    if (value === "all") {
                      setCompradorFilter("")
                      table.getColumn("comprador")?.setFilterValue(undefined)
                    } else {
                      setCompradorFilter(value)
                      table.getColumn("comprador")?.setFilterValue(value)
                    }
                  }}
                >
                  <SelectTrigger className="h-8 text-xs mt-1">
                    <SelectValue placeholder="Todos os compradores" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todos</SelectItem>
                    <SelectItem value="João Silva">João Silva</SelectItem>
                    <SelectItem value="Maria Santos">Maria Santos</SelectItem>
                    <SelectItem value="Pedro Oliveira">Pedro Oliveira</SelectItem>
                    <SelectItem value="Ana Costa">Ana Costa</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <DropdownMenuSeparator />
              
              {/* Filtro Controlador com Dropdown */}
              <div className="px-2 py-2">
                <Label className="text-xs font-medium text-muted-foreground">Controlador</Label>
                <Select
                  value={controladorFilter}
                  onValueChange={(value) => {
                    if (value === "all") {
                      setControladorFilter("")
                      table.getColumn("controlador")?.setFilterValue(undefined)
                    } else {
                      setControladorFilter(value)
                      table.getColumn("controlador")?.setFilterValue(value)
                    }
                  }}
                >
                  <SelectTrigger className="h-8 text-xs mt-1">
                    <SelectValue placeholder="Todos os controladores" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todos</SelectItem>
                    <SelectItem value="João Silva">João Silva</SelectItem>
                    <SelectItem value="Maria Santos">Maria Santos</SelectItem>
                    <SelectItem value="Carlos Ferreira">Carlos Ferreira</SelectItem>
                    <SelectItem value="Ana Costa">Ana Costa</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              {/* Limpar Filtros */}
              {(unidadeFilter || classificacaoFilter || compradorFilter || controladorFilter) && (
                <>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    onClick={() => {
                      setUnidadeFilter("")
                      setClassificacaoFilter("")
                      setCompradorFilter("")
                      setControladorFilter("")
                      table.getColumn("unidade")?.setFilterValue(undefined)
                      table.getColumn("classificacao_xyz")?.setFilterValue(undefined)
                      table.getColumn("comprador")?.setFilterValue(undefined)
                      table.getColumn("controlador")?.setFilterValue(undefined)
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
            <IconDownload />
            <span className="hidden lg:inline">Exportar Excel</span>
          </Button>

          {/* Menu de Personalizar Colunas */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm">
                <IconLayoutColumns />
                <span className="hidden lg:inline">Personalizar Colunas</span>
                <span className="lg:hidden">Colunas</span>
                <IconChevronDown />
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
                      {column.id}
                    </DropdownMenuCheckboxItem>
                  )
                })}
            </DropdownMenuContent>
          </DropdownMenu>
          <CatalogoFormDialog
            trigger={
              <Button size="sm">
                <IconPlus className="h-4 w-4" />
                <span className="hidden lg:inline">Adicionar Item</span>
                <span className="lg:hidden">Adicionar</span>
              </Button>
            }
          />
        </div>
      </div>
      <div className="relative flex flex-col gap-4 overflow-auto px-4 lg:px-6 mt-3">
        <div className="overflow-hidden rounded-lg border">
          <DndContext
            collisionDetection={closestCenter}
            modifiers={[restrictToVerticalAxis]}
            onDragEnd={handleDragEnd}
            sensors={sensors}
            id={sortableId}
          >
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
              <TableBody className="**:data-[slot=table-cell]:first:w-8">
                {table.getRowModel().rows?.length ? (
                  <SortableContext
                    items={dataIds}
                    strategy={verticalListSortingStrategy}
                  >
                    {table.getRowModel().rows.map((row) => (
                      <DraggableRow key={row.id} row={row} />
                    ))}
                  </SortableContext>
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
          </DndContext>
        </div>
        <div className="flex items-center justify-between px-4">
          <div className="text-muted-foreground hidden flex-1 text-sm lg:flex">
            {table.getFilteredRowModel().rows.length} itens no total
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


