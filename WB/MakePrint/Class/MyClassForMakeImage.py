class ModelWithAddin:
    def __init__(self, model, brand,compatibility,name,modelAddin, cameraType, price, caseType) -> None:
        self.colorList = []
        self.cameraType = cameraType
        self.model = model
        self.brand = brand
        self.compatibility = compatibility
        self.name = name
        self.modelAddin = modelAddin
        self.price = price
        self.description = '''Чехол для {} является отличным аксессуаром, а также украшением смартфона. Благодаря прилеганию к корпусу чехол {} отлично защищает ваш телефон , а также очень удобен в использовании. Чехол для телефона также может стать отличным подарком на любой праздник (день рождения, новый год, 23 февраля, 8 марта) благодаря отличному дизайну и красивому виду. Чехол бампер или чехол накладка {} очень удобен в использовании.Данный чехол имеет рисунок нанесённый по специальной технологии ультрафиолетовой печати. Он не стирается, не выгорает на солнце и не изнашивается без специального воздействия на него.Рисунок нанесён поверх чехла. Что позволяет почувствовать его и не скрывает всю красоту принта.'''.format(*modelAddin.split('#') if len(modelAddin.split('#')) == 3 else (modelAddin.split('#')[0],'',''))
        self.TNVED = '3926909709'
        self.equipment = 'Чехол для {} 1 штука'.format(modelAddin.split('#')[0])
        self.reason = 'женщине на день рождения# ребенку на день рождения# мужчине на день рождения'
        self.special = 'защитный чехол#противоударный'
        self.lock = 'нет застежки'
        self.type = 'Накладка'
        self.caseType = caseType

    def setGlobalSiliconAddin(self):
        pass