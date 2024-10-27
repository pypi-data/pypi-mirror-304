import pandas as pd
import math
from thermo.chemical import Chemical 


def  fluidos_db():
    fluidos =['methane', 'ethane', 'propane', 'butane', 'isopentane', 
                 'hexane', 'heptane', 'octane', 'nonane', 'decane']
    print("Lista de fluidos de hidrocarburos disponible: \n")
    for i, fluido in enumerate (fluidos, 1):
        print(f"{i}.- {fluido}")



def propiedades_fluidos():
    fluidos =['methane', 'ethane', 'propane', 'butane', 'isopentane', 
                 'hexane', 'heptane', 'octane', 'nonane', 'decane']
    prop_fluidos = []
    for prop in fluidos:
        chemical = Chemical(prop)
        prop_fluidos.append({
            "Fluido_Nombre": prop.title(),
            "Formula": chemical.formula,
            "Tc (K)": chemical.Tc,
            "Pc (Pa)": chemical.Pc,
            "PM (g/mol)":chemical.MW,
            "Vc ":chemical.Vc
        })
    df=pd.DataFrame(prop_fluidos)
    print("Las propiedades de los fludios son las siguientes: \n")
    print(df)


def calculate_mldt(fluido1,fluido2):
    try:
        temp_ff1 = float(input(f"Indica la temperatura de entrada del fluido frio {fluido1}: "))
        temp_ff2 = float(input(f"Indica la temperatura de salida del fluido frio {fluido1}: "))
        temp_fc1 = float(input(f"Indica la temperatura de entrada del fluido caliente {fluido2}: "))
        temp_fc2 = float(input(f"Indica la temperatura de salida del fluido caliente {fluido2}: "))
        if temp_ff2>temp_fc2:
            print("Esto no es posible, la temperatura de salida del fluido frio no puede ser superior a la temperatura de salida del fluido caliente. Por vaor intentalo de nuevo\n")
            return calculate_mldt()
        u_t1 = temp_ff1
        u_t2 = temp_ff2
        u_T1 = temp_fc1
        u_T2 = temp_fc2
        try:
            delta_T1 = u_T2-u_t1
            delta_T2 =  u_T1-u_t2
            mldt = (delta_T2-delta_T1)/math.log(delta_T2/delta_T1)
            print(f"La temperatura media logaritmica es {mldt} °F")
        except ValueError:
            print("Error: las diferencias de temperatura deben ser positivas.\n")
            return calculate_mldt()
        mldtValue = mldt
        print(f"La temperatura media logaritmica es {mldtValue} °F")
        return mldtValue 
    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número.\n")
        return calculate_mldt()

    

 



