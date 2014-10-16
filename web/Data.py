from django.db import connection
from datetime import datetime

def getDataSearchView():


    query = """
            SELECT auth_user.first_name AS first_name ,
            auth_user.last_name AS last_name , auth_user.email as email ,
            CONCAT(auth_user.first_name , '  ' , auth_user.last_name) AS complete_name ,
            web_TrainerProfile.date_birth AS date_birth ,
            web_TrainerProfile.address ,
            web_TrainerProfile.zip_code AS zip_code ,
            web_TrainerProfile.phone AS phone ,
            web_TrainerProfile.bio AS bio ,
            web_TrainerProfile.charge AS charge ,
            web_TrainerProfile.rate AS rate ,
            web_TrainerProfile.specialities AS specialities ,
            web_state.name AS state_name ,
            web_state.code AS state_code ,
            CONCAT(web_state.name,', ',web_city.name) AS state_city

            FROM auth_user

            INNER JOIN web_TrainerProfile ON auth_user.id = web_TrainerProfile.id
            INNER JOIN web_state      ON web_TrainerProfile.id_state = web_state.id
            INNER JOIN web_city       ON web_TrainerProfile.id_city  = web_city.id
    """
    resultData = my_custom_sql(query)

    return dictfetchall(resultData)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description

    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

"""
DB
"""

def my_custom_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)

    return cursor

"""
END DB
"""
