matrizLogin = [["julian","pedro","mara","carla"], ["213","5346","6933","5004"]]

def login():
    intentos = 0  
    exito = False
    while intentos < 3 and exito == False:
        print("\nInicio de Sesion \n")
        user = input("\nIngresar nombre de usuario: ").lower()
        #Revisa si el user se encuentra dentro de la matriz
        if user in matrizLogin[0]: 
            #Si el user se encuentra en la matriz, devuelve en indice
            i=matrizLogin[0].index(user)  
            contra = input("Ingresar contraseña: ")
            #Si la contraseña coincide con el indice del user
            if contra == matrizLogin[1][i]:
                #El login es exitoso
                print("\nLogin exitoso")
                exito = True
            else:
                #Si la contraseña no coincide, se pierde un intento
                print("Contraseña incorrecta")
                intentos += 1
        else:
            #Si el user no coincide, se pierde un intento
            print("nombre de usuario incorrecto")
            intentos += 1
        if intentos == 2:
            print("\nUltimo intento")
    return exito
