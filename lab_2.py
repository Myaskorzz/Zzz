data={}
flag = True 
initfile  = r'C:\Users\79940\Desktop\Projects\conf.txt'
with open(initfile , 'r') as f:
    for line in f:
        if line[0] != "#" and line[0] !=';' and line[0] != '\n':
            list = line.split()
            x=len(list)
            if x>1:
                key = list[0]
                value = list[1]
                data[key]= value
            if x == 1:
                key = list[0]
                value = "Значение не задано"
                data[key]= value

            
                
while flag:
    try:
        key = input("Введите ключ>>> ")
        print ("Ключ>>>", key," Значение>>>", data[key])   
    except:
        print("Ключ>>>", key," Значение>>> Такого ключа не существует")
    counter = 0
    i = 2
    while True:
        if counter == 3:
            exit()
        command = input("Повторить? Да\Нет>>> ")
        if command == "Да":
            break
        elif command == "Нет":
            flag = False 
            break
        else: 
            if i == 0:
                print("Попытки кончились,программа завершается ")
            print("Некоректный ввод. Попыток осталось>>>",i)   
            counter+=1 
            i-=1
            
