# davidsousa/email_utils.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_email(remetente, senha, destinatario, assunto, corpo): 
    """
    Função para enviar e-mail usando o servidor SMTP do Gmail.

    Parâmetros:
    remetente (str): Endereço de e-mail do remetente.
    senha (str): Senha do remetente.
    destinatario (str): Endereço de e-mail do destinatário.
    assunto (str): Assunto do e-mail.
    corpo (str): Corpo do e-mail.
    """
    servidor_smtp = 'smtp.gmail.com'
    porta_smtp = 587
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(corpo, 'plain'))
    
    try:
        servidor = smtplib.SMTP(host=servidor_smtp, port=porta_smtp)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, mensagem.as_string())
        servidor.quit()
        print("Email enviado com sucesso para", destinatario)
    except Exception as e:
        print("Erro ao enviar o e-mail:", e)
