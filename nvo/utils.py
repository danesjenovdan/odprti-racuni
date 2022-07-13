from nvo.models import RevenueCategory, ExpensesCategory
revenue_data = {
    'model': RevenueCategory,
    'nodes': [
        {'name': 'Total prihodki', 'order': 1, 'allow_additional_name': False},
        {'name': 'Tržna dejavnost', 'order': 2, 'allow_additional_name': False},
        {'name': 'Sponzorstvo', 'order': 1, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Produkti in storitve', 'order': 2, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Donacije in subvencije', 'order': 3, 'allow_additional_name': False},
        {'name': 'Donacije', 'order': 1, 'parent': 4, 'allow_additional_name': False},
        {'name': 'Javna sredstva', 'order': 2, 'parent': 4, 'allow_additional_name': False},
        {'name': 'Državna sredstva', 'order': 1, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Občinska sredstva', 'order': 2, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Evropska sredstva', 'order': 3, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Sredstva drugih držav', 'order': 4, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Zasebne fundacije', 'order': 3, 'parent': 4, 'allow_additional_name': False},
        {'name': 'Članarine', 'order': 4, 'parent': 4, 'allow_additional_name': False},
        {'name': 'Drugo', 'order': 5, 'instructions': 'Vnesi dodatno ime ki se bo prikazovalo poleg texta Drugo <vaš text>', 'parent': 4, 'allow_additional_name': True},
        {'name': 'Drugi prihodki', 'order': 4, 'allow_additional_name': False},
        {'name': '----', 'order': 1, 'instructions': 'Vnesi dodatno ime ki se bo prikazovalo', 'parent': 14, 'allow_additional_name': True},
]}

expenses_data = {
    'model': ExpensesCategory,
    'nodes': [
        {'name': 'Total odhodki', 'order': 1, 'allow_additional_name': False},
        {'name': 'Material in storitev', 'order': 2, 'allow_additional_name': False},
        {'name': 'Redno delovanje', 'order': 1, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Zunanje storitve in izvajalci', 'order': 2, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Potni stroški', 'order': 3, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Drugo (blabla)', 'order': 4, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Delo', 'order': 3, 'allow_additional_name': False},
        {'name': 'Plače', 'order': 1, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Pokojninska in druga socialna zavarovanja', 'order': 2, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Drugo', 'order': 3, 'parent': 6, 'allow_additional_name': True},
        {'name': 'Drugi odhodki', 'order': 4, 'allow_additional_name': False},
        {'name': '----', 'order': 1, 'instructions': 'Vnesi dodatno ime ki se bo prikazovalo', 'parent': 10, 'allow_additional_name': True},
       
]}
financial_data = [revenue_data, expenses_data]

def create_financial_tree(year_id, organization_id):
    for item in financial_data:
        create_financial_tree_for_model(
            item['nodes'],
            item['model'],
            year_id,
            organization_id
        )

def create_financial_tree_for_model(data, model, year_id, organization_id):
    for element in data:
        if 'parent' in element.keys():
            parent = parent=data[element['parent']]['object']
        else:
            parent = None
        obj = model(
            name=element['name'],
            organization_id=organization_id,
            year_id=year_id,
            order=element['order'],
            parent=parent,
            allow_additional_name=element['allow_additional_name'])
        obj.save()
        element['object'] = obj
        if 'instructions' in element.keys():
            obj.instructions=element['instructions']
        obj.save()
