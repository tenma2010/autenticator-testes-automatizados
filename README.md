# README - Autenticator Testes Automatizados

## Sobre o Repositório
Este repositório contém testes automatizados para a tela de login e cadastro do sistema **Autenticator**. Ele foi criado para atender ao desafio técnico proposto.

## Estrutura do Projeto

```
 autenticator-testes-automatizados/
├──accounts/
│   ├──tests.py  # Arquivo de testes automatizados
├──autenticator/
│   ├── settings.py  # Configurações do projeto Django
│   ├──urls.py  # URLs do sistema
├─manage.py  # Arquivo de gerenciamento do Django
├──requirements.txt  # Dependências do projeto
├──README.md  # Instruções de uso
```

## Requisitos
- Python 3.8+
- Django
- Selenium (para testes com navegador, se necessário)
- pytest (para rodar os testes de forma simplificada)

## Instalação
Clone o repositório e instale as dependências:

```bash
git clone https://github.com/tenma2010/autenticator-testes-automatizados
cd autenticator-testes-automatizados
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Execução dos Testes
Após configurar o ambiente virtual, execute os testes:

```bash
python manage.py test accounts
```

Ou usando **pytest**:

```bash
pytest accounts/tests.py
```

## Testes Implementados
- **Login com credenciais válidas**
- **Login com credenciais inválidas**
- **Cadastro com usuário já cadastrado**
- **Cadastro com e-mail já cadastrado**
- **Cadastro com senhas não coincidentes**

## Arquivo de Testes - `tests.py`

```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="usuario_teste", 
            email="teste@email.com", 
            password="Senha123!"
        )

    def test_login_valido(self):
        response = self.client.post(reverse('login'), {
            'username': 'usuario_teste',
            'password': 'Senha123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento esperado
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_invalido(self):
        response = self.client.post(reverse('login'), {
            'username': 'usuario_teste',
            'password': 'SenhaErrada'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credenciais inválidas")

    def test_cadastro_usuario_existente(self):
        response = self.client.post(reverse('register'), {
            'username': 'usuario_teste',
            'email': 'teste@email.com',
            'password1': 'Senha123!',
            'password2': 'Senha123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuário já existe")

    def test_cadastro_email_existente(self):
        response = self.client.post(reverse('register'), {
            'username': 'novo_usuario',
            'email': 'teste@email.com',
            'password1': 'Senha123!',
            'password2': 'Senha123!'
        }, follow=True)  # Agora segue o redirecionamento automaticamente
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email já cadastrado")
        
    def test_cadastro_senhas_diferentes(self):
        response = self.client.post(reverse('register'), {
            'username': 'novo_usuario',
            'email': 'novo@email.com',
            'password1': 'Senha123!',
            'password2': 'SenhaErrada'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "As senhas não coincidem")

```

Caso tenha dúvidas, entre em contato! 🚀
