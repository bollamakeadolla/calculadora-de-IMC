
import re
#Aqui es donde obtenemos la cantidad de personas
personas = int(input( "personas: "))
def isNameValid(name):
    if re.fullmatch(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", name) is None:
        return False
    return True
def isFloatString(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
#Aqui verificamos que la cantidad sea mayor a 0 si no, no tiene sentido pedir nada
while personas > 0:
    try:
        s = input("Elija su sistema de medida imperial o metrico: ")
        match s.lower():
            case "metrico":
                s = "metrico"
            case "imperial":
                s = "imperial"
            case _:
                raise ValueError("Debe elegir imperial o metrico")
        # primer nombre
        n = input("Su primer nombre por favor: ")
        # comprobar si el nombre solo contiene letras o guiones y no está vacío
        if not isNameValid(n):
            raise ValueError("El nombre no es valido")
        # apellido paterno
        a = input("Su apellido paterno por favor: ")
        # comprobar si el apellido solo contiene letras o guiones y no está vacío
        if not isNameValid(a):
            raise ValueError("El apellido no es valido")
        # apellido materno
        am = input("Su apellido materno por favor: ")
        # comprobar si el apellido solo contiene letras o guiones y no está vacío
        if not isNameValid(am):
            raise ValueError("El apellido no es valido")
        # edad
        e = input("Su edad en años por favor: ")
        # quitar las comas
        e = e.replace(",","")
        # comprobar si la edad es un numero entero positivo
        if not e.isdigit()  or int(e) < 0:  
            raise ValueError("La edad debe ser un numero entero positivo y mayor a 0")
        #convertir a int
        e = int(e)
        # masa/peso
        if s == "metrico":
            # kilogramos
            p =input("Su masa en kilogramos por favor: ")
            # comprobar si la masa es un numero positivo y float
            if not isFloatString(p) or float(p) < 0:
                raise ValueError("La masa debe ser un numero positivo con o sin decimales")
            #convertir a float
            p = float(p)
        else:
            #libras
            p = input("Su masa en libras por favor: ")
            # comprobar si el peso es un numero positivo y float
            if not isFloatString(p)  or float(p) < 0:
                raise ValueError("El peso debe ser un numero positivo con o sin decimales")
            #convertir a float y de libras a kilogramos
            p = float(p)*0.453592  
        
        
        #altura
        if s == "metrico":
            #metros
            est = input("Su altura en metros por favor: ")
            # comprobar si la altura es un numero positivo y float
            if not isFloatString(est) or float(est) < 0:
                raise ValueError("La altura debe ser un numero positivo con o sin decimales")
            #convertir a float
            est = float(est)
        else:
            #pulgadas
            est = input("Su altura en pulgadas por favor: ")
            # comprobar si la altura es un numero positivo y float
            if not isFloatString(est) or float(est) < 0:
                raise ValueError("La altura debe ser un numero positivo con o sin decimales")
            #convertir a float y de pulgadas a metros
            est = float(est)*0.0254
    except ValueError as e:
        print(e) 
        print("Por favor, ingrese los datos correctamente")
        # si hay un error, se vuelve a pedir los datos
        continue



    #Aqui calculamos el IMC
    IMC = p / est**2
    # Aqui redondeamos el IMC a 2 decimales
    IMC = round(IMC, 2)
    #Aqui validamos si es mayor o menor de edad
    if(e < 18):
        print("Usted es menor de edad")
    else:
        print("Usted es mayor de edad")
    #Aqui imprimimos el IMC
    print("IMC: " + str(IMC) )

    #Aqui validamos el IMC
    if IMC <= 15.99:
        print("Delgadez severa")
    elif IMC <= 16.99:
        print("Delgadez moderada")
    elif IMC <= 18.49:
        print("Delgadez leve")
    elif IMC <= 24.99:
        print("Normal")
    elif IMC <= 29.99:
        print("Sobrepeso")
    elif IMC <= 34.99:
        print("Obesidad leve")
    elif IMC <= 39.99:
        print("Obesidad media")
    else:
        print("Obesidad morbida")

    #Aqui restamos 1 a la cantidad de personas para terminar o reducir el bucle
    personas = personas - 1