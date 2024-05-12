# Bot PJE

## DESCRIÇÃO
Este bot é para estração de dados do sistema PJE.<br><br> Primeiramente, ele busca por dados na pasta `read\`, onde o usuário deve colocar uma planilha válida. O bot, então deve entrar no site, com os dados no arquivo `.env` fazer o login no sistema, e então vasculhar o site em busca dos dados pré-estabelecidos para, assim, extraí-los. Com os dados extraídos, o bot deve salvar os em um banco de dados para que possam ser devidamente tratados.<br><br> Por fim, todos os dados são salvos em uma planilha Excel.

## TECNOLOGIAS USADAS
- [Python 3.11](https://www.python.org/)
- [Pandas 2.2.2](https://pandas.pydata.org/)
- [Selenium 4.20.0](https://www.selenium.dev/)
- [SQLite3](https://www.sqlite.org/)

## PASTA READ
Primeiramente, o usuário deve colar/arrastar o arquivo `.xlsx` com a planilha Excel, com a formatação correta, que deseja pesquisar.<br><br>
*[Imagem ilustrativa]*

## EXECUTANDO
Ao executar bot, uma tela de prompt é aberta, onde é perguntado se deseja seguit com o login que está salvo.
![Captura de tela 2024-05-12 103420](https://github.com/FranciscoAlveJr/Bot-PJE/assets/65497402/408c32d4-b2ba-41c7-b621-ed725f2d2814)
<br>
<br>
Se o usuário digitar "n", o bot irá solicitar uma novo login e uma nova senha.
