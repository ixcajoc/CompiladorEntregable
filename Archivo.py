import tkinter as tk
from tkinter import filedialog

# hola a todos
class SQLPaser:
    def __init__(self):

        self.contenido = "\n"
        self.listaErrores = {}
        self.cantidadLineas = 0

        self.cambiosRealizados = False
        self.direccionArchivo = None 

        self.parsing_table = {
            'S': {
                'CREATE': ['S -> SQLIns'],
                'SELECT': ['S -> SQLIns'],
                'INSERT': ['S -> SQLIns'],
                'UPDATE': ['S -> SQLIns'],
                'DELETE': ['S -> SQLIns'],
                'EOF': ['']
            },
            'SQLIns': {
                'CREATE': ['SQLIns -> Instruccion_Crear'],
                'SELECT': ['SQLIns -> Instruccion_Listar'],
                'INSERT': ['SQLIns -> Instruccion_Insertar'],
                'UPDATE': ['SQLIns -> Instruccion_Actualizar'],
                'DELETE': ['SQLIns -> Instruccion_Eliminar'],
                'EOF': ['']
            },
            'Instruccion_Crear': {
                'CREATE': ['Instruccion_Crear -> Crear_BD', 'Instruccion_Crear -> Crear_TBL', 'Instruccion_Crear -> Crear_IDX']
            },
            # 'Crear_BD': {
            #     'CREATE': ['Crear_BD -> CREATE DATABASE <nombre_BD>;']
            # },
            'Crear_BD': {
                'CREATE': ['Crear_BD -> CREATE DATABASE miDataBase;']
            },
            
            
            

            'Crear_TBL': {
                'CREATE': ['Crear_TBL -> CREATE TABLE <nombre_TBL> (<Columnas_TBL>);']
            },
            'Crear_IDX': {
                'CREATE': ['Crear_IDX -> CREATE INDEX <nombre_IDX> ON <nombre_TBL>(<nombre_COL> <order>);']
            },
            'order': {
                'ASC': ['order -> ASC'],
                'DESC': ['order -> DESC'],
                'EOF': ['order -> ε'],
                '<nombre_COL>': ['order -> ε']
            },
            'Columnas_TBL': {
                '<nombre_COL>': ['Columnas_TBL -> Columna_TBL , Columnas_TBL', 'Columnas_TBL -> Columna_TBL']
            },
            'Columna_TBL': {
                '<nombre_COL>': ['Columna_TBL -> <nombre_COL> <SPACE> <column_definition>']
            },
            'column_definition': {
                'TINYINT': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'SMALLINT': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'MEDIUMINT': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'INT': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'INTEGER': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'BIGINT': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'REAL': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'DOUBLE': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'FLOAT': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'DECIMAL': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'NUMERIC': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'DATE': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'TIME': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'DATETIME': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'VARCHAR': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'TINYTEXT': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'TEXT': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'MEDIUMTEXT': ['column_definition -> <data_type> <SPACE> <data_type_options>'],
                'LONGTEXT': ['column_definition -> <data_type> <SPACE> <data_type_options>']
            },
            'data_type_options': {
                'NOT': ['data_type_options -> NOT NULL'],
                'NULL': ['data_type_options -> NULL'],
                'AUTO_INCREMENT PRIMARY KEY': ['data_type_options -> AUTO_INCREMENT PRIMARY KEY'],
                'PRIMARY KEY': ['data_type_options -> PRIMARY KEY'],
                'EOF': ['data_type_options -> ε'],
                ')': ['data_type_options -> ε']
            },
            'data_type': {
                'TINYINT': ['data_type -> TINYINT(<length>)'],
                'SMALLINT': ['data_type -> SMALLINT(<length>)'],
                'MEDIUMINT': ['data_type -> MEDIUMINT(<length>)'],
                'INT': ['data_type -> INT(<length>)'],
                'INTEGER': ['data_type -> INTEGER(<length>)'],
                'BIGINT': ['data_type -> BIGINT(<length>)'],
                'REAL': ['data_type -> REAL(<length>,<decimals>)'],
                'DOUBLE': ['data_type -> DOUBLE(<length>,<decimals>)'],
                'FLOAT': ['data_type -> FLOAT(<length>,<decimals>)'],
                'DECIMAL': ['data_type -> DECIMAL(<length>,<decimals>)'],
                'NUMERIC': ['data_type -> NUMERIC(<length>,<decimals>)'],
                'DATE': ['data_type -> DATE'],
                'TIME': ['data_type -> TIME'],
                'DATETIME': ['data_type -> DATETIME'],
                'VARCHAR': ['data_type -> VARCHAR(<length>)'],
                'TINYTEXT': ['data_type -> TINYTEXT'],
                'TEXT': ['data_type -> TEXT'],
                'MEDIUMTEXT': ['data_type -> MEDIUMTEXT'],
                'LONGTEXT': ['data_type -> LONGTEXT']
            },
            'Instruccion_Listar': {
                'SELECT': ['Instruccion_Listar -> SELECT <list_FLD> FROM <table_references> <Where> <Group> <OrderBY>']
            },
            'Where': {
                'WHERE': ['Where -> WHERE <SPACE> <condition>'],
                'EOF': ['Where -> ε'],
                'GROUP BY': ['Where -> ε'],
                'ORDER BY': ['Where -> ε']
            },
            'Group': {
                'GROUP BY': ['Group -> GROUP BY <SPACE> <lista_Columnas>'],
                'EOF': ['Group -> ε'],
                'ORDER BY': ['Group -> ε']
            },
            'OrderBY': {
                'ORDER BY': ['OrderBY -> ORDER BY <SPACE> <lista_Columnas> <SPACE> <order>'],
                'EOF': ['OrderBY -> ε']
            },
            'lista_Columnas': {
                '<nombre_COL>': ['lista_Columnas -> <nombre_COL> , <lista_Columnas>', 'lista_Columnas -> <nombre_COL>']
            },
            'list_FLD': {
                '<nombre_FLD>': ['list_FLD -> <nombre_FLD> , <list_FLD>', 'list_FLD -> <nombre_FLD>']
            },
            'table_reference': {
                '<table_factor>': ['table_reference -> <table_factor>', 'table_reference -> <joined_table>']
            },
            'table_factor': {
                '<nombre_TBL>': ['table_factor -> <nombre_TBL> <alias>']
            },
            'alias': {
                'AS': ['alias -> AS <alias_name>'],
                '<alias_name>': ['alias -> <alias_name>', 'alias -> ε'],
                'EOF': ['alias -> ε']
            },
            'joined_table': {
                'INNER JOIN': ['joined_table -> INNER JOIN <table_factor> <join_specification>'],
                'LEFT JOIN': ['joined_table -> LEFT JOIN <table_factor> <join_specification>'],
                'RIGHT JOIN': ['joined_table -> RIGHT JOIN <table_factor> <join_specification>']
            },
            'join_specification': {
                'ON': ['join_specification -> ON <condition>'],
                'EOF': ['join_specification -> ε']
            },
            'condition': {
                '<expr>': ['condition -> <expr> OR <expr>', 'condition -> <expr> || <expr>', 'condition -> <expr> XOR <expr>',
                            'condition -> <expr> AND <expr>', 'condition -> <expr> && <expr>', 'condition -> NOT <expr>',
                            'condition -> ! <expr>', 'condition -> <boolean_primary>']
            },
            'boolean_primary': {
                '<boolean_primary>': ['boolean_primary -> <boolean_primary> IS [NOT] NULL', 'boolean_primary -> <boolean_primary> <COMPARISON_OPERATOR> <simple_expr>',
                                        'boolean_primary -> <boolean_primary> <COMPARISON_OPERATOR> (<subquery>)', 'boolean_primary -> <simple_expr>']
            },
            'simple_expr': {
                '<literal>': ['simple_expr -> <literal>'],
                '<identifier>': ['simple_expr -> <identifier>'],
                '<variable>': ['simple_expr -> <variable>']
            },
            'Instruccion_Insertar': {
                'INSERT': ['Instruccion_Insertar -> INSERT INTO <nombre_TBL> (<lista_Columnas>) VALUES (value_list)']
            },
            'value_list': {
                '<numeric_literal>': ['value_list -> <value>,<value_list>', 'value_list -> <value>'],
                '<string_literal>': ['value_list -> <value>,<value_list>', 'value_list -> <value>']
            },
            'Instruccion_Actualizar': {
                'UPDATE': ['Instruccion_Actualizar -> UPDATE <SPACE> <nombre_TBL_UPD> <SPACE> SET <SPACE> <assignment_list> <Where>']
            },
            'assignment_list': {
                '<Assignment>': ['assignment_list -> <Assignment>,<assignment_list>', 'assignment_list -> <Assignment>']
            },
            'Assignment': {
                '<nombre_COL>': ['Assignment -> <nombre_COL> = <expr_update>']
            },
            'expr_update': {
                '<literal>': ['expr_update -> <literal>'],
                '<identifier>': ['expr_update -> <identifier>'],
                '<variable>': ['expr_update -> <variable>']
            },
            'Instruccion_Eliminar': {
                'DELETE': ['Instruccion_Eliminar -> DELETE FROM <SPACE> <nombre_TBL> <Where>']
            },
            'nombre_BD': {
                '<char_sequence>': ['nombre_BD -> <char_sequence>']
            },
            'nombre_TBL': {
                '<char_sequence>': ['nombre_TBL -> <char_sequence>']
            },
            'nombre_IDX': {
                '<char_sequence>': ['nombre_IDX -> <char_sequence>']
            },
            'nombre_COL': {
                '<char_sequence>': ['nombre_COL -> <char_sequence>']
            },
            'nombre_FLD': {
                '<char_sequence>': ['nombre_FLD -> <char_sequence>']
            },
            'nombre_TBL_UPD': {
                '<char_sequence>': ['nombre_TBL_UPD -> <char_sequence>']
            },
            'alias_name': {
                '<char_sequence>': ['alias_name -> <char_sequence>']
            },
            'identifier': {
                '<char_sequence>': ['identifier -> <char_sequence>']
            },
            'char_sequence': {
                '<char>': ['char_sequence -> <char><char_sequence>', 'char_sequence -> <char>']
            },
            'char': {
                '<LETTER>': ['char -> <LETTER>'],
                '<DIGIT>': ['char -> <DIGIT>'],
                '_': ['char -> _']
            },
            'Length': {
                '<DIGITS>': ['Length -> <DIGITS>']
            },
            'DIGITS': {
                '<DIGIT>': ['DIGITS -> <DIGIT>', 'DIGITS -> <DIGIT><DIGITS>']
            },
            'expr': {
                '<char_sequence>': ['expr -> <char_sequence>', 'expr -> <numeric_expr>']
            },
            'numeric_expr': {
                '<numeric_literal>': ['numeric_expr -> <numeric_literal>', 'numeric_expr -> <arithmetic_expr>']
            },
            'numeric_literal': {
                '<DIGITS>': ['numeric_literal -> <DIGITS><fraction_part>']
            },
            'fraction_part': {
                '.': ['fraction_part -> .<DIGITS>']
            },
            'arithmetic_expr': {
                '<expr>': ['arithmetic_expr -> <expr><ARITHMETIC_OPERATOR><expr>']
            },
            'value': {
                '<numeric_literal>': ['value -> <numeric_literal>', 'value -> <string_literal>']
            },
            'string_literal': {
                '"': ['string_literal -> "<CHAR_SEQUENCE_EXT>"']
            },
            'CHAR_SEQUENCE_EXT': {
                '<char_ext>': ['CHAR_SEQUENCE_EXT -> <char_ext><CHAR_SEQUENCE_EXT>', 'CHAR_SEQUENCE_EXT -> <char_ext>']
            },
            'char_ext': {
                '<LETTER>': ['char_ext -> <LETTER>'],
                '<DIGIT>': ['char_ext -> <DIGIT>'],
                '<OTHER_CHAR>': ['char_ext -> <OTHER_CHAR>'],
                '<SPACE>': ['char_ext -> <SPACE>']
            },
            'literal': {
                '<numeric_literal>': ['literal -> <numeric_literal>'],
                '<string_literal>': ['literal -> <string_literal>']
            },
            'identifier': {
                '<char_sequence>': ['identifier -> <char_sequence>']
            },
            'variable': {
                '<char_sequence>': ['variable -> <char_sequence>']
            },
            'SPACE': {
                ' ': ['SPACE -> " "']
            },
            'OTHER_CHAR': {
                '#': ['OTHER_CHAR -> #'],
                '$': ['OTHER_CHAR -> $'],
                '%': ['OTHER_CHAR -> %'],
                '&': ['OTHER_CHAR -> &'],
                '(': ['OTHER_CHAR -> ('],
                ')': ['OTHER_CHAR -> )'],
                ',': ['OTHER_CHAR -> ,'],
                ';': ['OTHER_CHAR -> ;'],
                '.': ['OTHER_CHAR -> .'],
                '?': ['OTHER_CHAR -> ?'],
                '/': ['OTHER_CHAR -> /'],
                '\\': ['OTHER_CHAR -> \\'],
                '-': ['OTHER_CHAR -> -'],
                '+': ['OTHER_CHAR -> +'],
                '*': ['OTHER_CHAR -> *'],
                '=': ['OTHER_CHAR -> ='],
                '<': ['OTHER_CHAR -> <'],
                '>': ['OTHER_CHAR -> >'],
                '!': ['OTHER_CHAR -> !'],
                ':': ['OTHER_CHAR -> :']
            },
            'LETTER': {
                '<LETTER>': ['LETTER -> a', 'LETTER -> b', 'LETTER -> c', 'LETTER -> d', 'LETTER -> e', 'LETTER -> f',
                            'LETTER -> g', 'LETTER -> h', 'LETTER -> i', 'LETTER -> j', 'LETTER -> k', 'LETTER -> l',
                            'LETTER -> m', 'LETTER -> n', 'LETTER -> o', 'LETTER -> p', 'LETTER -> q', 'LETTER -> r',
                            'LETTER -> s', 'LETTER -> t', 'LETTER -> u', 'LETTER -> v', 'LETTER -> w', 'LETTER -> x',
                            'LETTER -> y', 'LETTER -> z', 'LETTER -> A', 'LETTER -> B', 'LETTER -> C', 'LETTER -> D',
                            'LETTER -> E', 'LETTER -> F', 'LETTER -> G', 'LETTER -> H', 'LETTER -> I', 'LETTER -> J',
                            'LETTER -> K', 'LETTER -> L', 'LETTER -> M', 'LETTER -> N', 'LETTER -> O', 'LETTER -> P',
                            'LETTER -> Q', 'LETTER -> R', 'LETTER -> S', 'LETTER -> T', 'LETTER -> U', 'LETTER -> V',
                            'LETTER -> W', 'LETTER -> X', 'LETTER -> Y', 'LETTER -> Z']
            },
            'DIGIT': {
                '<DIGIT>': ['DIGIT -> 0', 'DIGIT -> 1', 'DIGIT -> 2', 'DIGIT -> 3', 'DIGIT -> 4', 'DIGIT -> 5',
                            'DIGIT -> 6', 'DIGIT -> 7', 'DIGIT -> 8', 'DIGIT -> 9']
            },
            'ARITHMETIC_OPERATOR': {
                '+': ['ARITHMETIC_OPERATOR -> +'],
                '-': ['ARITHMETIC_OPERATOR -> -'],
                '*': ['ARITHMETIC_OPERATOR -> *'],
                '/': ['ARITHMETIC_OPERATOR -> /'],
                '%': ['ARITHMETIC_OPERATOR -> %']
            },
            'COMPARISON_OPERATOR': {
                '=': ['COMPARISON_OPERATOR -> ='],
                '<>': ['COMPARISON_OPERATOR -> <>'],
                '<=': ['COMPARISON_OPERATOR -> <='],
                '>=': ['COMPARISON_OPERATOR -> >='],
                '<': ['COMPARISON_OPERATOR -> <'],
                '>': ['COMPARISON_OPERATOR -> >']
            },
            'SPACE': {
                '<SPACE>': ['SPACE -> " "']
            },
            'EOF': {
                '$': ['EOF -> $']
            }
        }
    
    # Aca descomponemos el arhivo cargado en lineas
    def analizadorSintactico(self):
        line_num = 0
        lines = self.contenido.splitlines()
        self.cantidadLineas = len(lines)
        for line in lines:
            line_num += 1
            line = line.strip() 
            if line:
                self.es_valida(line, line_num)

        line_num = 0

    #aca cada linea se separa por tokens y se comparan en la tabla sintactica
    def es_valida(self, instruccion,nline):
        pila = ['$', 'S']
        entrada = instruccion.split()
        entrada.append('$')
        idx = 0

        while pila:
            simbolo_pila = pila[-1]

            if simbolo_pila in ['$', 'ε']:
                if simbolo_pila == entrada[idx]:
                    pila.pop()
                    idx += 1
                else:
                    self.listaErrores[nline] = f"error en {nline}, no valida"
                    return False
            elif simbolo_pila in self.parsing_table.keys():
                if entrada[idx] in self.parsing_table[simbolo_pila].keys():
                    pila.pop()
                    produccion = self.parsing_table[simbolo_pila][entrada[idx]][0].split(' -> ')[1].split()
                    if produccion != ['ε']:
                        pila.extend(reversed(produccion))
                else:
                    self.listaErrores[nline] = f"error en {nline}, token {entrada[idx]} no valido, se esperaba {simbolo_pila} en {idx}"

                    return False
            else:
                if simbolo_pila == entrada[idx]:
                    pila.pop()
                    idx += 1
                else:
                    # self.listaErrores[nline] = f"error en {nline}, no valida"
                    # self.listaErrores[nline] = f"token {entrada[idx]} no valida, se esperaba "
                    self.listaErrores[nline] = f"error en {nline}, token {entrada[idx]} no valido, se esperaba {simbolo_pila} en {idx}"




                    return False

            self.listaErrores[nline] = f"valida linea {nline}"

        return True


        
    def limpiarVariables(self):
        self.contenido = ""
        self.errores = ""
        self.listaErrores = {}
        self.cantidadLineas = 0


    def abrirArchivo(self):
        direccionArchivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if direccionArchivo:
            with open(direccionArchivo, 'r') as archivo:
                contenido = archivo.read()
            self.direccionArchivo = direccionArchivo
            self.cambiosRealizados = False
            self.vacio = False
            self.cantidadLineas = len(contenido.splitlines())

        return contenido
    
    def marcarCambios(self, contenidoCaja):
        if self.contenido != contenidoCaja:
            self.cambiosRealizados = True 
        else:
            self.cambiosRealizados = False

    def cerrarVentana(self,contenidoCaja,ventana):
        contenido = contenidoCaja
        ventana = ventana

        if self.cambiosRealizados:
            respuesta = tk.messagebox.askyesnocancel("Guardar Cambios", "Deseas guardar los cambios antes de cerrar?")
            if respuesta is None:
                return
            elif respuesta:
                self.guardarArchivo(contenido)
        ventana.destroy()

    def guardarArchivoComo(self,contenidoCaja):
        direccionArchivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if direccionArchivo:
            contenido = contenidoCaja
            with open(direccionArchivo, "w") as archivo:
                archivo.write(contenido)
            self.direccionArchivo = direccionArchivo
            self.cambiosRealizados = False

    def guardarArchivo(self, contenidoCaja):
        if self.direccionArchivo:
            contenido = contenidoCaja
            with open(self.direccionArchivo, "w") as archivo:
                archivo.write(contenido)
            self.cambiosRealizados = False
        else:
            contenido = contenidoCaja
            self.guardarArchivoComo(contenido)
 
    
    def exportarSQL(self, contenido):
        archivo = filedialog.asksaveasfilename(defaultextension=".sql", filetypes=[("SQL files", "*.sql"), ("All files", "*.*")])
    
        if archivo:
            # Guardar el contenido formateado en un archivo .sql
            with open(archivo, 'w') as f:
                f.write(contenido)
            
            tk.messagebox.showinfo("Correcto", "El archivo se ha exportado correctamente")

# Ejemplo de uso
# if __name__ == "__main__":
#     archivo = 'texto.txt'
#     analyze_file(archivo)

    
# if __name__ == "__main__":
#     miObjeto = MetodosArchivo()
    
#     miObjeto.contenido = miObjeto.abrirArchivo()
#     miObjeto.analizadorSintactico()
    
    
    
