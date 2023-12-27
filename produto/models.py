from django.conf import settings
from PIL import Image
import os
from django.db import models
from pprint import pprint
from django.utils.text import slugify



class Produto(models.Model):
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m', blank=True, null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(default=0, verbose_name="Preço")
    preco_marketing_promocional = models.FloatField(default=0, verbose_name="Preço Promo")
    tipo = models.CharField(
        default='V', max_length=1, choices=(
            ('V', 'Variável'), 
            ('S', 'Simples')
        ),
    )

    def get_preco_formatado(self):
        return f'R$ {self.preco_marketing:.2f}'.replace('.', ',')
    get_preco_formatado.short_description = 'Preço'  # Dando um nome ao método para ser apresentado no painel de produtos do Django-Admin

    def get_preco_promocional_formatado(self):
        return f'R$ {self.preco_marketing_promocional:.2f}'.replace('.', ',')
    get_preco_promocional_formatado.short_description = 'Preço Promo'

    # Retorna o campo nome(dos produtos) quando este modelo é chamado, exemplo: QuerySet: <Produto: Celular> 
    def __str__(self):
        return self.nome
    
    
    # Como o método estático não depende de uma instância específica, ele não tem acesso aos atributos específicos de uma instância. 
    # Em vez disso, ele opera com base em seus próprios parâmetros ou lógica interna e é geralmente usado para funcionalidades que 
    # estão associadas à classe como um todo, não a uma instância específica dela.
    @staticmethod
    def resize_imagem(original_img, new_width=800):
        # Recebe a imagem e manda para o diretório MEDIA_ROOT definido em settings.py de loja_project
        # img_full_path ---> É transformada em uma URL, por isso pegamos o: original_img.name do arquivo.
        img_full_path = os.path.join(settings.MEDIA_ROOT, original_img.name)
        img_pil = Image.open(img_full_path)  # Exemplo de retorno desta variável: (L:266, A:148)
        original_width, original_height = img_pil.size  # Pega o tamanho da img (retorna uma tupla) atribui de acordo com os índices.
        new_height = round((new_width * original_height) / original_width)  # Round --> Para retornar o inteiro mais próximo, precisa ser inteiro.

        # Executa o bloco IF apenas se a condição for True...
        if new_width >= original_width:
            # print()
            # print('Retornando, largura original MENOR ou IGUAL que nova largura! (método resize_image() - Produto Model)')
            # print()
            img_pil.close()
            return  # Execução do método resize_imagem será encerrada aqui mesmo. Sem continuar para as linhas subsequentes
        
        nova_imagem = img_pil.resize((new_width, new_height), Image.LANCZOS)  # Redimensiona a imagem com os novos parametros(New-w, New-h)
        
        # Salva a nova img por cima da original, passando o caminho que será salva, otimização e qualidade.
        nova_imagem.save(img_full_path, optimize=True, quality=60)  
        img_pil.close()
        # print()
        # print('Imagem foi redimensionada com sucesso! (método resize_image() - Produto Model)')
        # print()


    def save(self, *args, **kwargs):
        # Criando um slug automático para cada novo Produto cadastrado
        if not self.slug:
            slug = f'{slugify(self.nome)}'  # Exeplo: camiseta-python-e-legal
            self.slug = slug

        # Chama o super da classe pai para realmente salvar o produto cadastrado no DJANDO-ADMIN
        super().save(*args, *kwargs)

        max_image_size = 800  # Tamanho máximo da imagem

        # Depois de chamar o método save do super (produto foi salvo), 
        # Verifica se foi enviado também uma imagem, ou seja, se existe uma imagem naquele produto
        # se sim, faz todo o bloco do if...
        if self.imagem:
            self.resize_imagem(self.imagem, max_image_size)



class Variacao(models.Model):
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
    

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  # Deletar produto -> todas variações deste de produto será apagada também.
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.nome or self.produto.nome  # Nome da variação ou nome do produto que contém essa variação