import sudoku
from random import choice
from mapas import MAPAS
import mensajes

TECHO = ''' 
  ┌─────┬──────┬──────┐
  │1 2 3│ 4 5 6│ 7 8 9│ '''  
PISO= """  └─────┴──────┴──────┘"""
PISO_INTERMEDIO="""  ├─────┼──────┼──────┤"""
PARED_VERTICAL ='│'
PARED_HORIZONTAL ='─'
PARED_VERTICAL_CON_UNION = '├'
PARED_HORIZONTAL_CON_UNION = '┤'
PARED_HORIZONTAL_VERTICAL = '┼'

LISTA_LETRAS = ['a','b','c','d','e','f','g','h','i']

def filtrar_respuesta(respuesta):
    """Esta funcion se encarga de filtrar la respuesta del usuario para que no se tomen en cuenta letras o numero no validos"""
    
    return "".join((filter(lambda caracter: caracter in LISTA_LETRAS or (caracter.isdigit() and int(caracter) != sudoku.VACIO), respuesta)))

def mostrar_sudoku(sudoku_actual):
    
    """Esta funcion muestra el sudoku de manera que el usuario pueda
    identificar el estado actual de juego y que reconozca que valores puede ingresar"""
    
    print("  "+TECHO)
    for columna in range(sudoku.ANCHO_TABLERO):
        if columna % sudoku.ANCHO_CUADRANTE == 0:
            print(PISO_INTERMEDIO)
        for fila in range(sudoku.ALTO_TABLERO):
            if fila == 0:
                print(str(LISTA_LETRAS[columna])+ " " + PARED_VERTICAL + str(sudoku_actual[columna][fila]), end=" ")
            elif fila == len(sudoku_actual[columna])-1:
                print(str(sudoku_actual[columna][fila]) + PARED_VERTICAL, end=" ")    
            elif (fila+1) % sudoku.ALTO_CUADRANTE == 0:
                print(str(sudoku_actual[columna][fila]) + PARED_VERTICAL, end = " ")
            else:
                print(str(sudoku_actual[columna][fila]), end =" ")
        print(' ')
    print(PISO)
    
def pedir_accion(sudoku_actual):
    """Esta funcion se encarga de pedirle al usuario una accion INGRESAR, BORRAR O SALIR (La opcion ingresar solo esta disponible
       si hay movimientos posibles en el estado de juego actual). Ademas valida todo lo que el usuario ingresa"""
    
    if sudoku.hay_movimientos_posibles(sudoku_actual):
        respuesta = input(mensajes.INGRESAR_ACCION_TRES_OPCIONES).lower()
        while respuesta not in (mensajes.INGRESAR, mensajes.BORRAR, mensajes.SALIR): 
            respuesta = input(mensajes.OPCION_INGRESADA_INCORRECTA).lower()        
    
    else:
        respuesta = input(mensajes.INGRESAR_ACCION_DOS_OPCIONES).lower()
        while respuesta != mensajes.BORRAR or respuesta != mensajes.SALIR:
            respuesta = input(mensajes.OPCION_INGRESADA_INCORRECTA).lower()
    
    return respuesta
    
def pedir_movimiento(sudoku_actual, accion_pedida):
    """Esta funcion se encarga de pedirla un movimiento al usuario. Si la accion pedida fue INGRESAR te pide una fila, columna, valor
        pero si la accion fue BORRAR solo pide fila, columna. Ademas valida todo lo que el usuaro ingresa"""
    
    if accion_pedida == mensajes.INGRESAR:
        respuesta = filtrar_respuesta(input(mensajes.PEDIR_MOVIMIENTO_INGRESO_VALOR).lower())
        while len(respuesta) != 3 or (not respuesta[0] in LISTA_LETRAS) or not(respuesta[1:].isdigit() and 0 < int(respuesta[1]) <= sudoku.ANCHO_TABLERO and int(respuesta[2]) != sudoku.VACIO):
            respuesta = filtrar_respuesta(input(mensajes.OPCION_INGRESADA_INCORRECTA))
        fila, columna, valor = respuesta
        
        return LISTA_LETRAS.index(fila), int(columna)-1, int(valor)
    
    else:
        respuesta = filtrar_respuesta(input(mensajes.PEDIR_MOVIMIENTO_BORRAR_VALOR).lower())
        while len(respuesta) != 2 or (not respuesta[0] in LISTA_LETRAS) or not(respuesta[1].isdigit() and (0 < int(respuesta[1])) <= sudoku.ANCHO_TABLERO):
            respuesta =  filtrar_respuesta(input(mensajes.OPCION_INGRESADA_INCORRECTA))
        fila, columna = respuesta
        
        return LISTA_LETRAS.index(fila), int(columna)-1
    
def main():
    """Esta funcion te muestra un sudoku al azar de los mapas e interactura con el usuario dejandole
    ingresar un valor (solo te deja si el valor es valido y si hay algun valor posible) o borrar un valor. Le pide acciones
    al usuario hasta que este termine el sudoku correctamente o decida salir del mismo"""
    
    """muestra juego"""
    sudoku_actual = sudoku.crear_juego(choice(MAPAS))
    sudoku_original = sudoku.copiar_sudoku(sudoku_actual)
    print(mensajes.BIENVENIDA)
    while not sudoku.esta_terminado(sudoku_actual):
        mostrar_sudoku(sudoku_actual)
        accion = pedir_accion(sudoku_actual)
        
        if accion == mensajes.SALIR:
            "el usuario decidio salir"
            break
        
        if accion == mensajes.INGRESAR:
            "el usuario decidio ingresar un valor"
            
            fila, columna, valor = pedir_movimiento(sudoku_actual, accion)
            
            "validamos que el movimiento no modifique el sudoku original o que sea invalido"
            while sudoku.obtener_valor(sudoku_original, fila, columna) != sudoku.VACIO or not sudoku.es_movimiento_valido(sudoku_actual, fila, columna, valor):
                print(mensajes.OPCION_INGRESADA_INVALIDA)
                fila, columna, valor = pedir_movimiento(sudoku_actual, accion)
                
            sudoku_actual = sudoku.insertar_valor(sudoku_actual, fila, columna, valor)
        
        if accion == mensajes.BORRAR:
            "el usuario decidio borrar un valor"
            
            fila, columna = pedir_movimiento(sudoku_actual, accion)
            
            "validamos que el movimiento no modifique el sudoku original"
            while sudoku.obtener_valor(sudoku_original, fila, columna) != sudoku.VACIO:
                print(mensajes.OPCION_INGRESADA_INVALIDA)
                fila, columna = pedir_movimiento(sudoku_actual, accion)
                
            sudoku_actual = sudoku.borrar_valor(sudoku_actual, fila, columna)
            
    if sudoku.esta_terminado(sudoku_actual):
        print(mensajes.GANASTE)
        
    else:
        print(mensajes.SALISTE)
            
main()      
        

