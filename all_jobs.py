import json
import pandas as pd
import datetime
import os


def parcing():
    '''
    Mining data from telegram chanel DevKg
    Recording to parc.json file
    '''
    per_from = str(datetime.datetime.now().date()).split('-')
    per_from[1] = str(int(per_from[1]) - 1)
    per_from[1] = f'0{per_from[1]}' if len(per_from[1]) == 1 else per_from[1]
    os.system(f'snscrape --since {"-".join(per_from)} --jsonl telegram-channel findwork > parc.txt')
    pop_list = ['_type', 'linkPreview', 'outlinks', 'outlinksss']
    new_dict = dict()

    with open('parc.txt', 'r') as file:
        data = file.readlines()
        os.remove('parc.txt')
    

    for item in data:
        new_data = json.loads(item)
        content = new_data.pop('content')
        name = content[:content.find(':')]
        content = {
            'name': content[:content.find(':')],
            'posion': content[content.find(':')+2:content.find('Тип:')], 
            'tip': content[content.find('Тип:')+5:content.find('От') 
                    if 'Неоплачиваемая' not in content else content.find('Неоплачиваемая')]
                    if 'От' in content else content[content.find('Работа'):content.find('офисе')+5],
            'salary': 'Неоплачиваемая' 
                    if 'Неоплачиваемая' in content else content[content.find('От'):content.find('Тэги:')]
                    if 'От' in content else content[content.find('офисе')+5:content.find('Тэги')], 
            'tags': content[content.find('Тэги:')+6:content.find('Требования, контакты и условия тут:')],
            'contact': content[content.find('Требования, контакты и условия тут:'):content.find('Чат')],
            }
        
        new_dict[name] = content

    with open('parc.json', 'w') as file:
        json.dump(new_dict, file, indent=4, ensure_ascii=False)


def xlsx():
    '''
    Work with parc.json file
    Transform to excel format with fields
    '''
    parcing()
    with open('parc.json', 'r') as file:
        data = json.load(file)

    name = []
    posion = []
    tip = []
    val = []
    salary_min = []
    salary_max = []
    period = []
    contact = []

    for i in data.values():
        name.append(i.get('name'))
        posion.append(i.get('posion'))
        tip.append(i.get('tip'))
        c = i.get('contact')
        contact.append(c[c.find('тут:')+4:])
        salary_val = [float(sal) for sal in i.get('salary').split() if sal.isdigit()]
        if len(salary_val) > 1:
            salary_min.append(salary_val[0])
            salary_max.append(salary_val[1])
        else:
            if len(salary_val) == 1:
                salary_min.append(salary_val[0])
                salary_max.append('-')
            else:
                salary_min.append('Неоплачиваемая')
                salary_max.append('-')
        salary = i.get('salary')
        if 'USD' in salary:
            val.append('USD')   
        else:
            if 'KGS' in salary:
                val.append('KGS')
            else:
                if 'RUB' in salary:
                    val.append('RUB')
                else:
                    val.append('-')
        if 'в месяц' in salary.lower():
            period.append('В месяц')   
        else:
            period.append('В час')

    df = pd.DataFrame({
        'Название': name,
        'Позиция': posion,
        'Тип': tip,
        'Валюта': val,
        'Зарплата (мин)': salary_min,
        'Зарплата (макс)': salary_max,
        'Период выплат': period,
        'Ссылка': contact,
        })

    df.to_excel('data.xlsx')
