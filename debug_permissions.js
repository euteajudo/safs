// Script de debug para testar nossa função de validação
const currentUser = {
  id: 1,
  username: "admin",
  nome: "Administrador do Sistema",
  email: "admin@safs.gov.br",
  unidade: "SAFS",
  is_active: true,
  is_superuser: true,
  is_chefe_unidade: true,
  is_chefe_setor: false,
  is_funcionario: false
};

const selectedRoles = {
  is_superuser: true,
  is_chefe_unidade: false,
  is_chefe_setor: false,
  is_funcionario: false
};

function validateUserRoles(currentUser, selectedRoles) {
  if (!currentUser || !currentUser.is_active) {
    return { isValid: false, errors: ['Usuário não está ativo'] };
  }

  const errors = [];

  console.log('Current user is_superuser:', currentUser.is_superuser, typeof currentUser.is_superuser);
  console.log('Selected roles is_superuser:', selectedRoles.is_superuser, typeof selectedRoles.is_superuser);

  // Verificar se o usuário atual pode atribuir superusuário
  if (selectedRoles.is_superuser && !currentUser.is_superuser) {
    console.log('❌ Erro: Superusuário check failed');
    errors.push('Apenas superusuários podem criar outros superusuários');
  } else {
    console.log('✅ Superusuário check passed');
  }

  // Verificar se apenas uma role principal está selecionada
  const roleCount = [
    selectedRoles.is_superuser,
    selectedRoles.is_chefe_unidade,
    selectedRoles.is_chefe_setor,
    selectedRoles.is_funcionario
  ].filter(Boolean).length;

  console.log('Role count:', roleCount);

  if (roleCount === 0) {
    errors.push('Pelo menos uma permissão deve ser selecionada');
  }

  if (roleCount > 1) {
    errors.push('Apenas uma permissão principal pode ser selecionada por vez');
  }

  return {
    isValid: errors.length === 0,
    errors: errors.length > 0 ? errors : undefined
  };
}

console.log('=== TESTE DE VALIDAÇÃO ===');
const result = validateUserRoles(currentUser, selectedRoles);
console.log('Resultado:', result);