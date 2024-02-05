from main import db


class CollectionPlanilhas:
    def __init__(self):
        self.planilhas = []

    def adicionar_planilha(self, planilha):
        self.planilhas.append(planilha)

    def processar_todas_planilhas(self):
        informacoes_gerais = []

        for planilha in self.planilhas:
            informacoes_planilha = planilha.processar_planilha()
            informacoes_gerais.append(informacoes_planilha)

        return informacoes_gerais



class Planilhas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

    def processar_planilha(self):
        if self.categoria == 'Servicos':
            # Lógica específica para planilhas do tipo 'Servicos'
            print('Servicos')
            return {'mensagem': f'Processando planilha de Serviços: {self.nome}'}
        elif self.categoria == 'IGPD':
            # Lógica específica para planilhas do tipo 'IGPD'
            print('IGPD')
            return {'mensagem': f'Processando planilha IGPD: {self.nome}'}
        else:
            # Lógica para outros tipos de planilhas
            print('desconhecida')
            return {'mensagem': f'Processando planilha desconhecida: {self.nome}'}

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
