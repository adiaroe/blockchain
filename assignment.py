person = {'name': 'Adithya','age': 22, 'hobbies':('gyming', 'coding', 'learning')}
name_list = [name['name'] for name in person]
more_20 = all[age['age']>20 for age in person]
copy_name_list = name_list[:]
