from telethon.sync import TelegramClient
import datetime, os, re,time, configparser
import pandas as pd

def configuracao():
    arquivo = configparser.RawConfigParser()
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, 'config.txt')
    arquivo.read(initfile)
    return{'api_id':arquivo.get('telegram', 'api_id'),
    'api_hash':arquivo.get('telegram', 'api_hash'),
    'telegram_scraping':arquivo.get('telegram', 'telegram_scraping')}

def Sinais_telegram_Scraping():
    config = configuracao()
    #configuração para conexão com o telegram 
    api_id = int(config['api_id']) #api_id deve ser criada previamente  e inserida como long e não como string 
    api_hash = str(config['api_hash']) #api_hash deve ser inserida como string 
    telegransinais = str(config['telegram_scraping'])#nome do telegran de onde será efetuado a respagem dos sinais 
    chats = [telegransinais] 
    client =  TelegramClient('None', api_id, api_hash) #utilização da API do Telegram e a lib Telethon para estabelecer comunicação 
    df = pd.DataFrame() # dataframe para armazenanmento das informações recolhidadas
    tratamento1=[]
    #looping de scraping
    for chat in chats:
        #realizando conexão com o servidor, pode ser necessário a confirmarção do celular do usuário de acordo com API do Telegram
        with TelegramClient('None', api_id, api_hash) as client:
            # no grupo selecionado ele verifica somente as ultimas mensagens enviadas na data de hoje 
            for message in client.iter_messages(chat, offset_date=datetime.date.today() , reverse=True):
                #organiza os dados em grupos para melhor serem identificados no data frame
                data = { "group" : chat, "sender" : message.sender_id, "text" : message.text, "date" : message.date}
                temp_df = pd.DataFrame(data, index=[1])
                #realiza o imput dos dados no data frame do pandas
                df = df.append(temp_df)

    df['date'] = df['date'].dt.tz_localize(None)
    print ('\n\n')
    session = ""
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
    print('Primeira etapa concluída')

def organiza_tabelas_csv():
    #função para cruação de um novo dataframe 
    #necessário a inserir o parâmetro header = None pois o arquvio csv em questão não possui cabeçalho
    tabela = pd.read_csv('Scraping_de_grupo_do_telegram_raw.csv',encoding='utf-8',sep=';',header=None) 
    df = pd.DataFrame(data = tabela)
    df2= pd.DataFrame(list(zip(df[3], df[1], df[0], df[2])))
    for item in range(0,len(df2[0])):
        modifica_final = str(df2.iat[item,0])+ ';' + str(df2.iat[item,1])+ ';' + str(df2.iat[item,2]) +';'+ str(df2.iat[item,3] +'\n')
        with open('Scraping_de_grupo_do_telegram_ajustado.csv','a', encoding= 'utf-8' ) as arquivo:
            arquivo.write(str(modifica_final))
        arquivo.close()
        time.sleep(1)
    print('Tarefa Exceudada com sucesso, lista gerada e salva para o bot sequidor de lista')

Sinais_telegram_Scraping()
time.sleep(1)
organiza_tabelas_csv()
