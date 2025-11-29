from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def loan_approved(loan):
    SENDER_EMAIL = settings.SENDER_EMAIL
    DOMAIN = 'community.tornac-dev.com.br'

    message = f"""
        Olá, {loan.borrower.full_name},

        Temos ótimas notícias! O seu pedido para o livro "{loan.book.title}" 
        foi APROVADO pelo usuário {loan.owner.full_name}.

        ─────────────────────────────────────────────────────
        DETALHES DA TRANSAÇÃO:
        • Livro: {loan.book.title}
        • Doador/Proprietário: {loan.owner.full_name}
        ─────────────────────────────────────────────────────

        Para visualizar todos os detalhes da transação, incluindo informações de contato 
        para agendamento de retirada/entrega, acesse a sua área de pedidos:

        {DOMAIN}{reverse('loans:orders_made_list')}

        ─────────────────────────────────────────────────────
        Agradecemos por usar nossa plataforma!

        Atenciosamente,
        A equipe CommunityBooks
        """

    return send_mail(
        subject=f"✅ Pedido Aprovado: Seu pedido para o livro '{loan.book.title}' foi aceito!",
        message=message.strip(),
        from_email=SENDER_EMAIL,
        recipient_list=[loan.borrower.email],
        fail_silently=False
    )