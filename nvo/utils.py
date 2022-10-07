from nvo.models import RevenueCategory, ExpensesCategory

revenue_data = {
    'model': RevenueCategory,
    'nodes': [
        {'name': 'Skupni prihodki', 'order': 1, 'allow_additional_name': False},
        {'name': 'Tržna dejavnost', 'parent': 0, 'order': 2, 'allow_additional_name': False},
        {'name': 'Sponzorstva', 'order': 3, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Produkti in storitve', 'order': 4, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Donacije in subvencije', 'parent': 0, 'order': 5, 'allow_additional_name': False},
        {'name': 'Donacije fizičnih oseb', 'order': 6, 'parent': 4, 'allow_additional_name': False},
        {'name': 'Javna sredstva', 'order': 7, 'parent': 4, 'allow_additional_name': False},
        {'name': 'Državna sredstva', 'order': 8, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Občinska sredstva', 'order': 9, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Evropska sredstva', 'order': 10, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Sredstva drugih držav', 'order': 11, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Zasebne fundacije', 'order': 12, 'parent': 4, 'allow_additional_name': False},
        {'name': 'Članarine', 'order': 13, 'parent': 4, 'allow_additional_name': False},
        {'name': 'Drugo', 'order': 14, 'instructions': 'Vnesi dodatno ime ki se bo prikazovalo poleg texta Drugo <vaš text>', 'parent': 4, 'allow_additional_name': True},
        {'name': 'Drugi prihodki', 'order': 15, 'parent': 0, 'allow_additional_name': True, 'instructions': 'Vnesi dodatno ime ki se bo prikazovalo'},
]}

expenses_data = {
    'model': ExpensesCategory,
    'nodes': [
        {'name': 'Skupni odhodki', 'order': 1, 'allow_additional_name': False},
        {'name': 'Materiali in storitve', 'parent': 0,'order': 2, 'allow_additional_name': False},
        {'name': 'Redno delovanje', 'order': 3, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Zunanje storitve in izvajalci', 'order': 4, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Potni stroški', 'order': 5, 'parent': 1, 'allow_additional_name': False},
        {'name': 'Drugo', 'order': 6, 'parent': 1, 'allow_additional_name': True},
        {'name': 'Delo', 'order': 7, 'parent': 0, 'allow_additional_name': False},
        {'name': 'Plače', 'order': 8, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Pokojninska in druga socialna zavarovanja', 'order': 9, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Drugo', 'order': 10, 'parent': 6, 'allow_additional_name': False},
        {'name': 'Drugi odhodki', 'order': 11, 'parent': 0, 'allow_additional_name': True, 'instructions': 'Vnesi dodatno ime ki se bo prikazovalo'},
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

def clean_chart_data(data):
    '''
    Recursively cleans financial data to be able to draw the chart.
    '''
    if len(data['children']) > 0:
        data['value'] = None
        data['children'] = [clean_chart_data(child) for child in data['children']]
    elif 'amount' in data.keys():
        data['value'] = data['amount']
    
    return data
