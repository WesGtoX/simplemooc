from django.shortcuts import render


def home(request):
    """
    1º parâmetro é o 'request'.
    2º parâmetro 'home.html', é o nome do template.
    3º parâmetro passei um dicionário que são as variaveis que ficaram disponiveis no template.
    """
    return render(request, 'home.html')


def contact(request):
    return render(request, 'contact.html')
