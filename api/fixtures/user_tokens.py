from api.models.user import User
from api.models.category import Category
from api.serializers import UserSerializer
import random
import json
# import xlrd

FILE_NAME = "Load_data.xlsx"


def process_rows(sheet):
    headers = []
    head = True
    rows = {}
    for row in range(sheet.nrows):  
        if head:
            for header in sheet.row_values(row):
                headers.append(header)
            head = False
        else:
                for index, value in enumerate(sheet.row_values(row)):
                    if headers[index] != "" or value != "":
                        if row not in rows:
                            rows[row] = {}
                        rows[row][headers[index]] = value
    return rows.values()

def process_columns(sheet):
    headers = []
    head = True
    cols = {}
    header = ''
    for col in range(sheet.ncols):  
        for value in sheet.col_values(col):
            if head:
                header = value
                cols[header] = [] 
                head = False
            else:
                if value != '':
                    cols[header].append(value)
        head = True
    return cols

# def importing_skill_category():
#     data = []
#     workbook = xlrd.open_workbook(FILE_NAME)
#     categories_sheet = workbook.sheet_by_name('CATEGORIAS')
#     skills_sheet = workbook.sheet_by_name('HABILIDADES')
#     main_categories = {}
#     categories = process_rows(categories_sheet)
#     pk = 1
#     main_pk = 1
#     for category in categories:
#         if category['MAIN'] != '':
#             category_form = {"model": "api.Category",
#                             'pk': pk,
#                             'fields':{'name': category['CATEGORIAS'], 'main_category': True}}
#             main_categories[category['CATEGORIAS']] = pk
#             main_pk = pk
#         else:
#             category_form = {"model": "api.Category",
#                             'pk': pk,
#                             'fields': {'name': category['CATEGORIAS'], 'main_category': False , 'category': main_pk}}

#         data.append(category_form)
#         pk += 1
    
#     skills = process_columns(skills_sheet)
#     pk = 1
#     for skill in skills.keys():
#         if skill in main_categories.keys():
#             category_id = main_categories[skill]
#             for k in skills[skill]:
#                 skill_form = {"model": "api.Skill",
#                             'pk': pk,
#                             'fields': {'name': k, 'category': category_id}}
#                 data.append(skill_form)
#                 pk += 1
        
#     with open("api/fixtures/category_skillSeed2.json", "w") as file:
#         json.dump(data, file)
    

def userSeed():

    datas = [
        {
        "first_name": "Tomas",
        "last_name": "Fuentes",
        "username": "tifuentes",
        "email": "tifuentes@tenecesito.cl",
        "password": "tenecesito",
        "profession": "Ingeniero Civil Industrial",
        "register_status": 1
        },
        {
        "first_name": "Francisco",
        "last_name": "Miranda",
        "username": "fmiranda",
        "email": "frmiranda@uc.cl",
        "password": "tenecesito",
        "profession": "Ingeniero Civil Industrial",
        "register_status": 1
        },
        {
        "first_name": "Tomas",
        "last_name": "Correa",
        "username": "tacorrea",
        "email": "tacorrea@uc.cl",
        "password": "tenecesito",
        "profession": "Ingeniero Civil Industrial",
        "register_status": 1
        },
        {
        "first_name": "Benjamin",
        "last_name": "Delpiano",
        "username": "bidelp",
        "email": "bidelp@uc.cl",
        "password": "tenecesito",
        "profession": "Ingeniero Civil Industrial",
        "register_status": 1
        }]
        
    for data in datas:
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            instance, token = serializer.save()
            userData = serializer.data
            token = str(token).replace("(<Token: ", "").replace(">, True)", "")
            userData["oauth_token"] = token
