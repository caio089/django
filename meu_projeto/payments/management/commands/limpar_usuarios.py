from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile
from payments.models import Pagamento, Assinatura
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Remove todos os usuários cadastrados do banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('--confirmar', action='store_true', help='Confirma a remoção de todos os usuários')
        parser.add_argument('--manter-admin', action='store_true', help='Mantém apenas o usuário admin')

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('⚠️  ATENÇÃO: REMOÇÃO DE USUÁRIOS'))
        self.stdout.write('=' * 60)
        
        if not options['confirmar']:
            self.stdout.write('❌ ERRO: Esta operação é irreversível!')
            self.stdout.write('💡 Use --confirmar para executar a remoção')
            self.stdout.write('💡 Use --manter-admin para manter apenas o admin')
            return
        
        # Contar usuários antes da remoção
        total_usuarios = User.objects.count()
        total_perfis = Profile.objects.count()
        total_pagamentos = Pagamento.objects.count()
        total_assinaturas = Assinatura.objects.count()
        
        self.stdout.write(f'\n📊 DADOS ATUAIS:')
        self.stdout.write(f'   Usuários: {total_usuarios}')
        self.stdout.write(f'   Perfis: {total_perfis}')
        self.stdout.write(f'   Pagamentos: {total_pagamentos}')
        self.stdout.write(f'   Assinaturas: {total_assinaturas}')
        
        if total_usuarios == 0:
            self.stdout.write('\n✅ Nenhum usuário encontrado no banco de dados')
            return
        
        # Confirmar remoção
        self.stdout.write(f'\n⚠️  CONFIRMAÇÃO:')
        self.stdout.write(f'   Você está prestes a remover {total_usuarios} usuários!')
        self.stdout.write(f'   Esta operação é IRREVERSÍVEL!')
        
        if options['manter_admin']:
            self.stdout.write(f'   ⚠️  Manterá apenas usuários admin/superuser')
        
        # Executar remoção
        try:
            with transaction.atomic():
                if options['manter_admin']:
                    # Manter apenas superusers
                    usuarios_para_remover = User.objects.filter(is_superuser=False)
                    usuarios_mantidos = User.objects.filter(is_superuser=True)
                    
                    self.stdout.write(f'\n🔧 REMOVENDO USUÁRIOS NÃO-ADMIN:')
                    self.stdout.write(f'   Usuários a remover: {usuarios_para_remover.count()}')
                    self.stdout.write(f'   Usuários mantidos: {usuarios_mantidos.count()}')
                    
                    # Remover perfis dos usuários não-admin
                    Profile.objects.filter(user__in=usuarios_para_remover).delete()
                    
                    # Remover pagamentos dos usuários não-admin
                    Pagamento.objects.filter(usuario__in=usuarios_para_remover).delete()
                    
                    # Remover assinaturas dos usuários não-admin
                    Assinatura.objects.filter(usuario__in=usuarios_para_remover).delete()
                    
                    # Remover usuários não-admin
                    usuarios_removidos = usuarios_para_remover.count()
                    usuarios_para_remover.delete()
                    
                else:
                    # Remover todos os usuários
                    self.stdout.write(f'\n🗑️  REMOVENDO TODOS OS USUÁRIOS:')
                    
                    # Remover perfis
                    Profile.objects.all().delete()
                    self.stdout.write('   ✅ Perfis removidos')
                    
                    # Remover pagamentos
                    Pagamento.objects.all().delete()
                    self.stdout.write('   ✅ Pagamentos removidos')
                    
                    # Remover assinaturas
                    Assinatura.objects.all().delete()
                    self.stdout.write('   ✅ Assinaturas removidas')
                    
                    # Remover usuários
                    usuarios_removidos = User.objects.count()
                    User.objects.all().delete()
                    self.stdout.write('   ✅ Usuários removidos')
                
                # Verificar resultado
                usuarios_restantes = User.objects.count()
                perfis_restantes = Profile.objects.count()
                pagamentos_restantes = Pagamento.objects.count()
                assinaturas_restantes = Assinatura.objects.count()
                
                self.stdout.write(f'\n✅ REMOÇÃO CONCLUÍDA!')
                self.stdout.write(f'   Usuários removidos: {usuarios_removidos}')
                self.stdout.write(f'   Usuários restantes: {usuarios_restantes}')
                self.stdout.write(f'   Perfis restantes: {perfis_restantes}')
                self.stdout.write(f'   Pagamentos restantes: {pagamentos_restantes}')
                self.stdout.write(f'   Assinaturas restantes: {assinaturas_restantes}')
                
                if usuarios_restantes == 0:
                    self.stdout.write(f'\n🎯 BANCO LIMPO!')
                    self.stdout.write(f'   Agora você pode criar novos usuários')
                elif options['manter_admin']:
                    self.stdout.write(f'\n🎯 APENAS ADMINS MANTIDOS!')
                    self.stdout.write(f'   Usuários admin/superuser foram preservados')
                
        except Exception as e:
            self.stdout.write(f'\n❌ ERRO durante a remoção: {e}')
            logger.error(f"Erro ao remover usuários: {e}", exc_info=True)
            return
        
        self.stdout.write(f'\n💡 PRÓXIMOS PASSOS:')
        self.stdout.write(f'   1. Crie novos usuários via registro')
        self.stdout.write(f'   2. Ou use: python manage.py createsuperuser')
        self.stdout.write(f'   3. Teste o sistema com usuários novos')
        
        self.stdout.write('\n✅ Script concluído!')
