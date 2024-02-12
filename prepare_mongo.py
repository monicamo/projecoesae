from pymongo import MongoClient
from datetime import datetime


def criar_intervalo(inicio, fim):
    return {'inicio': inicio, 'fim': fim}


def preparar_dados_iniciais():
    # Conectar ao MongoDB
    client = MongoClient('localhost', 27017)
    db = client['planilhas']

    # Coleção de instituições
    collection_instituicoes = db['instituicoes']

    collection_instituicoes.delete_many({});

    # Inserir dados iniciais de instituições (exemplo)
    instituicoes_iniciais = [
        {'nome': 'C6 Bank', 'codigo': 'C6'},
        {'nome': 'Instituicao1', 'codigo': 'I1'},
        {'nome': 'Instituicao2', 'codigo': 'I2'},
        {'nome': 'Instituicao3', 'codigo': 'I3'},
        {'nome': 'Instituicao4', 'codigo': 'I4'},
        {'nome': 'Instituicao5', 'codigo': 'I5'},
        {'nome': 'Instituicao6', 'codigo': 'I6'},
        {'nome': 'Instituicao7', 'codigo': 'I7'},
        {'nome': 'Instituicao8', 'codigo': 'I8'},
        {'nome': 'Instituicao9', 'codigo': 'I9'},
        {'nome': 'Instituicao10', 'codigo': 'I10'},
        {'nome': 'Instituicao11', 'codigo': 'I11'},
        {'nome': 'Instituicao12', 'codigo': 'I12'},
        {'nome': 'Instituicao13', 'codigo': 'I13'},
        {'nome': 'Instituicao14', 'codigo': 'I14'},
        {'nome': 'Instituicao15', 'codigo': 'I15'},
        {'nome': 'Instituicao16', 'codigo': 'I16'},
        {'nome': 'Instituicao17', 'codigo': 'I17'},
        {'nome': 'Instituicao18', 'codigo': 'I18'},
        {'nome': 'Instituicao19', 'codigo': 'I19'},
        {'nome': 'Instituicao20', 'codigo': 'I20'},
        {'nome': 'Instituicao21', 'codigo': 'I21'},
        {'nome': 'Instituicao22', 'codigo': 'I22'},
        {'nome': 'Instituicao23', 'codigo': 'I23'},
        {'nome': 'Instituicao24', 'codigo': 'I24'},
        {'nome': 'Instituicao25', 'codigo': 'I25'},
        {'nome': 'Instituicao26', 'codigo': 'I26'},
        {'nome': 'Instituicao27', 'codigo': 'I27'},
        {'nome': 'Instituicao28', 'codigo': 'I28'},
        {'nome': 'Instituicao29', 'codigo': 'I29'},
        {'nome': 'Instituicao30', 'codigo': 'I30'},
    ]

    collection_instituicoes.insert_many(instituicoes_iniciais)



    # Coleção de servicos
    collection_servicos = db['planilhas']

    collection_servicos.delete_many({});

    # Inserir dados iniciais de planilhas (exemplo)
    servicos_iniciais = [
        {
            'nome': 'Servicos',
            'tipo': 'Servicos',
            'codigo': 'SV'
        },
        {
            'nome': 'IGPD',
            'tipo': 'IGPD',
            'codigo': 'IG'
    },
        # Adicione mais planilhas conforme necessário
    ]
    collection_servicos.insert_many(servicos_iniciais)

    # Fechar a conexão com o MongoDB
    client.close()


if __name__ == '__main__':
    preparar_dados_iniciais()
