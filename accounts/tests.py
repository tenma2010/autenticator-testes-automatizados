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
