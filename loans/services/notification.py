from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

DOMAIN = 'community.tornac-dev.com.br'
EMAIL_HOST_USER = 'dev@localhost'

def approve(loan):
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

        {DOMAIN}{reverse('orders:submitted')}

        ─────────────────────────────────────────────────────
        Agradecemos por usar nossa plataforma!

        Atenciosamente,
        A equipe CommunityBooks
        """

    return send_mail(
        subject=f"Pedido Aprovado: Seu pedido para o livro '{loan.book.title}' foi aceito!",
        message=message.strip(),
        from_email=EMAIL_HOST_USER,
        recipient_list=[loan.borrower.email],
        fail_silently=False
    )


def sent(loan):
    message = f"""
        Olá, {loan.borrower.full_name},

        Ótima notícia! O livro "{loan.book.title}" que você solicitou 
        foi ENVIADO para o seu endereço cadastrado.

        ─────────────────────────────────────────────────────
        DETALHES DO ENVIO:
        • Livro: {loan.book.title}
        • Remetente: {loan.owner.full_name}
        • Status: Enviado
        ─────────────────────────────────────────────────────

        Fique atento(a) aos prazos de entrega da transportadora. 
        Recomendamos que você acompanhe a entrega através do código de rastreio 
        (se fornecido pelo remetente).

        Para visualizar todos os detalhes da transação e informações de contato 
        do remetente, acesse a sua área de pedidos:

        {DOMAIN}{reverse('loans:submitted')}

        ─────────────────────────────────────────────────────
        DICAS IMPORTANTES:
        • Verifique se há avisos de entrega em sua residência
        • Mantenha seu telefone disponível para contato
        • Em caso de atraso, entre em contato com o remetente

        Atenciosamente,
        A equipe CommunityBooks
        """
    
    return send_mail(
        subject=f"Emprestimo atualizado: O livro '{loan.book.title}' foi enviado para o seu endereço!",
        message=message.strip(),
        from_email=EMAIL_HOST_USER,
        recipient_list=[loan.borrower.email],
        fail_silently=False
    )


def delivered(loan):
    message = f"""
        Olá, {loan.owner.full_name},

        Confirmamos que seu livro "{loan.book.title}" 
        foi recebido por {loan.borrower.full_name}.

        ─────────────────────────────────────────────────────
        STATUS DO EMPRÉSTIMO:
        • Livro: {loan.book.title}
        • Recebido por: {loan.borrower.full_name}
        • Status: Em posse do destinatário
        ─────────────────────────────────────────────────────

        O ciclo de compartilhamento foi iniciado com sucesso! 
        Agora é aguardar o prazo de leitura e a devolução.

        Para gerenciar este empréstimo ou ver outros pedidos:
        {DOMAIN}{reverse('loans:received')}

        Obrigado por fazer parte desta comunidade de leitores!

        Equipe CommunityBooks
        """
    
    return send_mail(
        subject=f"Emprestimo Atualizado: Seu livro '{loan.book.title}' foi entregue!",
        message=message.strip(),
        from_email=EMAIL_HOST_USER,
        recipient_list=[loan.owner.email],
        fail_silently=False
    )


def returned(loan):
    message = f"""
        Olá, {loan.owner.full_name},

        Boas notícias! O livro "{loan.book.title}" que você emprestou 
        está a CAMINHO de volta para você.

        ─────────────────────────────────────────────────────
        STATUS DE DEVOLUÇÃO:
        • Livro: {loan.book.title}
        • Devolvido por: {loan.borrower.full_name}
        • Status: Em transporte de volta
        • Data do envio: {timezone.now()}
        ─────────────────────────────────────────────────────

        {loan.borrower.full_name} confirmou o envio do livro de volta 
        para o seu endereço cadastrado.

        Fique atento(a) aos prazos de entrega da transportadora. 
        Recomendamos que você acompanhe a entrega através do código de rastreio 
        (se fornecido pelo remetente).

        Para visualizar todos os detalhes ou entrar em contato com 
        {loan.borrower.full_name}, acesse sua área de pedidos:

        {DOMAIN}{reverse('orders:received')}

        ─────────────────────────────────────────────────────
        DICAS PARA O RECEBIMENTO:
        • Verifique se há avisos de entrega em sua residência
        • Mantenha seu telefone disponível para contato
        • Confirme o recebimento quando o livro chegar
        • Verifique o estado de conservação do livro

        Atenciosamente,
        A equipe CommunityBooks
        """
    
    return send_mail(
        subject=f"Encomenda: Seu livro '{loan.book.title}' está à caminho do seu endereço!",
        message=message.strip(),
        from_email=EMAIL_HOST_USER,
        recipient_list=[loan.owner.email],
        fail_silently=False
    )


def completed(loan):
    message = f"""
        Olá, {loan.borrower.full_name},

        Agradecemos por devolver o livro "{loan.book.title}"!
        
        O ciclo de empréstimo foi concluído com sucesso. 
        {loan.owner.full_name} será notificado quando o livro chegar.

        Esperamos que você tenha aproveitado a leitura e 
        que faça parte novamente da nossa comunidade de compartilhamento!

        Atenciosamente,
        Equipe CommunityBooks
        """
    
    return send_mail(
        subject=f"Emprestimo fechado: O emprestimo '{loan.id}' foi fechado!",
        message=message.strip(),
        from_email=EMAIL_HOST_USER,
        recipient_list=[loan.borrower.email],
        fail_silently=False
    )