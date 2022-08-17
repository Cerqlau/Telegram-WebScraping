# Telegram-WebScrap

Este projeto foi desenvolvido em Python a fim de realizar iteração com a API do Telegram e webscraping à partir de grupos de envios gratuitos de sinais para IQ. Com esta mesma base e tipo  pode-se efetuar a expansão para qualquer tipo de grupos e futuras análises de dados. 

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

### 📋 Pré-requisitos

```
=> Pyton 3.8 ou superior instalado;
=> Instalar o arquivo "requeriments.txt": pip install -r /path/to/requirements.txt
```

### 🔧 Pré-configurações

É necessário a solicitação da API_ID e API_Hash para se ter acesso a API do telegram. Esta pode ser realizada através do endereço https://my.telegram.org/auth. Após realizar a solicitações necessária faça logout de forma a evitar conflito de informações com a API Telegram.

Ateção: Não transfira estes dados. O código em questão faz a utiliziação do mesmo na biblioteca Telethon, por motivos de segurança pode ser solicitado novamente certo período sem utilizar, mesmo que uma sessão anterior já tenha sido realizada. 

Para verificar o raw name do grupo do telegram procure o link de seu compartilhamento, que deverá se parecer com este: https://t.me/grupofulanodetal o nome final do endereço é o nome real do grupo. Não insira emojis no nome que o código irá veridicar, durante os testes isto se provou contraproducente.


### ⚙️ Executando o programa

Utilize o arquivo "config.txt" na diretório para configurar as informações necessárias.  Lembre-se de que o código e tratamento das informações foi baseado de forma a gerar uma lista em arquivo "CSV" que poderá ser utilizado no bot seguidor de listas desde mesmo github. Entretanto os conceitos apresantados de webscraping, tratamento de dados com o pandas e API podem ser reutilizadas como base e desenvolvimento outros projetos.

Caso seje necessário modifique a nomeclatura que o código irá procurar dentro das mensagens do telegram. Garantindo que seja possível procurar uma expressão que seja utilizada no grupo algo.

Exemplo de utilização e criação de lista estão neste repositório. Pode-se verificar que o nome a expressão inserida na linha session, aparece na mensagagem gerada pelo grupo algo



```
#verifica nos data frames se estes possuem a expressão **SINAIS GRÁTIS** e separa esta em uma nova coluna
session = df[df['text'].str.contains('\*\*SINAIS GRÁTIS\*\*')]
#isolamos os texto da nova coluna para facilitar a procura de padrões 
text = session.iloc[0]['text']
#Padrão para verificação dos sinais no texto onde estes se econtram da seguinte forma 14:25;EUR/GBP;CALL;5 
padrao = r'[0-9]{2}\:[0-9]{2}\;[A-Z]{3}\/[A-Z]{3}\;[A-Z]{1,4}\;[0-9]{1,2}'
#Captura de todo as strings que corresondem ao padrão de sinais 
tratamento1= re.findall(padrao,text)
#Verificação dos sinais e preparação para salvamento
    for item in range(0,len(tratamento1)):
        modifica = re.sub(r'\/','',tratamento1[item])
        index = modifica.find(';',15,18) + 1
        modifica_final= modifica[:index] + 'M'+ modifica[index:] + '\n'
        with open('Scraping_de_grupo_do_telegram_raw.csv','a', encoding='utf-8') as arquivo:
            arquivo.write(str(modifica_final))
        arquivo.close()
        time.sleep(1)

```

### 📨 Distribuição

É possivel efetuar a distribuição para usuários que não possuem pyton instalados em suas máquinas através da biblioteca pyinstaller. 

```
pip install pyinstaller 

```

Efetuar a criação de um arquivo ".spec" através do exemplo de código abaixo

```
pyi-makespec main.py --onefile  --name Telegram-WebScrap-Lista-IQ-exe

```

A compilação poderá ser fetuada conforme código abaixo

```
pyinstaller --clean Telegram-WebScrap-Lista-IQ-exe.spec

```


## 📦 Desenvolvimento

Lauro Cerqueira
LinkdIn: https://www.linkedin.com/in/lauro-cerqueira-70473568/
Instagram : laurorcerqueira

## 🛠️ Construído com

* [API Telegram Auth](https://my.telegram.org/auth)
* [Python 3.8](https://www.python.org/downloads/release/python-380/)
* [Telethon](https://docs.telethon.dev/en/stable/) 
* [Pandas] (https://pandas.pydata.org/docs/index.html)


## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE.md](https://github.com/usuario/projeto/licenca) para detalhes.

## 🎁 

* Conte a outras pessoas sobre este projeto 📢
* Convide alguém da equipe para uma cerveja 🍺 
* Obrigado publicamente 🤓.

