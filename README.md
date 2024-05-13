# BOT PJE

## DESCRIÇÃO
Este bot é para estração de dados do sistema PJE.<br><br> Primeiramente, ele busca por dados na pasta `read\`, onde o usuário deve colocar uma planilha válida. O bot, então deve entrar no site, com os dados no arquivo `.env` fazer o login no sistema, e então vasculhar o site em busca dos dados pré-estabelecidos para, assim, extraí-los. Com os dados extraídos, o bot deve salvar os em um banco de dados para que possam ser devidamente tratados.<br><br> Por fim, todos os dados são salvos em uma planilha Excel.

## TECNOLOGIAS USADAS
- [Python 3.11](https://www.python.org/) (Linguagem de programação)
- [Pandas 2.2.2](https://pandas.pydata.org/) (Tratamento de dados)
- [Selenium 4.20.0](https://www.selenium.dev/) (Automação de navegador)
- [SQLite3](https://www.sqlite.org/) (Armazenamento de dados)

## PRIMEIRO PASSO
Primeiramente, o usuário deve colar/arrastar o arquivo `.xlsx` com a planilha Excel, com a formatação correta, que deseja pesquisar.<br><br>
![20240513_102439](https://github.com/FranciscoAlveJr/Bot-PJE/assets/65497402/4e233f32-da6a-45d4-ac87-fb9cb823c97f)

## EXECUTANDO
Ao executar o bot, uma tela de prompt é aberta, onde é perguntado se deseja seguir com o login que está salvo.
![Captura de tela 2024-05-12 103420](https://github.com/FranciscoAlveJr/Bot-PJE/assets/65497402/408c32d4-b2ba-41c7-b621-ed725f2d2814)
<br>
<br>
Se o usuário digitar "n", o bot irá solicitar uma novo login e uma nova senha, caso contrário, ele irá seguir direto para a automação do navegador.
![login_senha](https://github.com/FranciscoAlveJr/Bot-PJE/assets/65497402/a2d347dc-4d08-406e-bab0-a487a41b1e7d)
<br>
<br>
O bot, então, começará o processo de automação, abrindo o navegador na página programada.
![abrir_navegador](https://github.com/FranciscoAlveJr/Bot-PJE/assets/65497402/5a8f5349-1c32-4275-b569-d351689efca9)
<br>
<br>
Enquanto isso, alguns dados do processo vão sendo mostrados.
![terminal](https://github.com/FranciscoAlveJr/Bot-PJE/assets/65497402/bc38a514-50c5-43fd-be8e-b6a431264139)
<br>
<br>
Enquanto o programa não finaliza, os dados ficarão armazenados em uma subpasta com o nome do arquivo localizado na pasta `read/`.
![Captura de tela 2024-05-13 121055](https://github.com/FranciscoAlveJr/Bot-PJE/assets/65497402/007f7fab-4ca9-4987-a5a6-a39ebedb76f5)
<br>
Dentro da subpasta, com os dados armazenados, eles poderão ser devidamente tratados.
![Captura de tela 2024-05-13 121214](https://github.com/FranciscoAlveJr/Bot-PJE/assets/65497402/da6459a8-77ac-4355-b4a5-31e729ee6254)

## ENCERRANDO
Finalmente, com os dados devidamente tratados e o bot tendo lido a última linha da planilha de origem, ele, então, salva os dados extraídos em arquivos Excel previamente estabelecidos.
![Captura de tela 2024-05-13 122012](https://github.com/FranciscoAlveJr/Bot-PJE/assets/65497402/a5967b3e-fd72-418f-958f-41e49a3842cb)
