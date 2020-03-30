print("КАЛЕКАлятор")
flag = True
while flag:
    operate = input("Выбери знак (+,-,*,/)")
    val_1 =  int(input("x="))
    val_2 = int(input("y="))
    if operate == '+':
        result = val_1 + val_2
    elif operate == '-':
        result = val_1 - val_2
    elif operate == '*':
        result = val_1 * val_2
    elif operate == '/':
        if val_2 != 0:
            result = val_1/val_2
        elif val_2==0:
            result = "На ноль делить нельзя"
    else:
        result = "Неверный знак"
  
    print(result)
    counter = 0
    while True:
        if counter == 3:
            exit()
        command = input("Продолжить? Да\Нет ")
        if command == "Да":
            break
        elif command == "Нет":
            flag = False 
            break
        else:    
            counter+=1 
        
      

