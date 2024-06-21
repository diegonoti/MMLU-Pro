import json
import random
import os

# Cargar el JSON desde una cadena
json_data = '''
[
    {
        "question": "¿Según la hipótesis de Méndez Correa el poblamiento del continente americano se produjo a través de?",
        "options": [
            "A) La Antártida.",
            "B) El Pacífico.",
            "C) El Estrecho de Behring.",
            "D) Groenlandia.",
            "E) Las Islas Aleutianas.",
            "F) El océano Atlántico.",
            "G) El mar Caribe.",
            "H) El océano Índico.",
            "I) El estrecho de Magallanes.",
            "J) La Patagonia."
        ],
        "answer": "A"
    },
    {
        "question": "El gran centro ceremonial de Chavín, de origen multirregional, tiene su asiento principal en el",
        "options": [
            "A) Callejón de Conchucos.",
            "B) Callejón de Huaylas.",
            "C) Valle del Río Mosna.",
            "D) Cañón del Pato.",
            "E) Valle del Río Santa.",
            "F) Valle del Río Rímac.",
            "G) Valle del Río Casma.",
            "H) Callejón de Huancabamba.",
            "I) Valle del Río Huallaga.",
            "J) Valle del Río Marañón."
        ],
        "answer": "C"
    },
    {
        "question": "Durante el precerámico andino en la región de Junín la dieta alimenticia de los cazadores evoluciona de la carne de",
        "options": [
            "A) camélidos al consumo de vegetales.",
            "B) vicuña a la de llama.",
            "C) los cérvidos a la de camélidos.",
            "D) vicuña a la de guanaco.",
            "E) camélidos a la de cérvidos.",
            "F) auquénidos a la de bovinos.",
            "G) cérvidos al consumo de peces.",
            "H) camélidos a la de roedores.",
            "I) roedores a la de cérvidos.",
            "J) équidos a la de camélidos."
        ],
        "answer": "C"
    },
    {
        "question": "De acuerdo con el avance de los estudios arqueológicos, en el Perú el más antiguo edificio ceremonial fue construido en el valle de",
        "options": [
            "A) Cahuachi.",
            "B) Zaña.",
            "C) Supe.",
            "D) Paramonga.",
            "E) Chicama.",
            "F) Rimac.",
            "G) Moche.",
            "H) Chillón.",
            "I) Ica.",
            "J) Chancay."
        ],
        "answer": "C"
    },
    {
        "question": "La tumba del Señor de Sipán pertenece a la Cultura",
        "options": [
            "A) Chimú.",
            "B) Mochica.",
            "C) Vicus.",
            "D) Cupisnique.",
            "E) Tallán.",
            "F) Lambayeque.",
            "G) Paracas.",
            "H) Nasca.",
            "I) Chavín.",
            "J) Recuay."
        ],
        "answer": "B"
    },
    {
        "question": "Los dioses de la cultura Tiahuanaco se caracterizan porque representaban figuras",
        "options": [
            "A) fitomorfas.",
            "B) ornitomorfas.",
            "C) ictiomorfas.",
            "D) antropomorfas.",
            "E) zoomorfas.",
            "F) entomorfas.",
            "G) herpetomorfas.",
            "H) geomorfas.",
            "I) aracnomorfas.",
            "J) astronómicas."
        ],
        "answer": "D"
    },
    {
        "question": "Los antiguos peruanos se preocupaban por tener chacras de cultivo en diferentes pisos ecológicos. ¿Qué es lo que les incentivaba a ello?",
        "options": [
            "A) La práctica de los curacas para el sustento de los ayllus.",
            "B) Seguir con su costumbre ancestral, posiblemente desde el Formativo.",
            "C) Las disposiciones de los incas respecto al abastecimiento de los pobladores.",
            "D) El abastecimiento directo de productos de toda variedad sin intermediarios.",
            "E) Evitar desastres motivados por accidentes naturales, muy comunes en el Perú.",
            "F) La necesidad de ampliar territorios para el cultivo.",
            "G) El intercambio comercial con otras regiones.",
            "H) La búsqueda de nuevas tierras fértiles.",
            "I) El aumento de la población y la demanda de alimentos.",
            "J) El desarrollo de nuevas técnicas agrícolas."
        ],
        "answer": "D"
    },
    {
        "question": "En la economía del Perú antiguo, el acceso a varios pisos altitudinales permitió",
        "options": [
            "A) el control de la reciprocidad.",
            "B) el desarrollo de la hidráulica.",
            "C) la redistribución de bienes.",
            "D) la complementariedad ecológica.",
            "E) la conformación de estados.",
            "F) el intercambio comercial a larga distancia.",
            "G) el desarrollo de la agricultura intensiva.",
            "H) el control político de diferentes regiones.",
            "I) la especialización artesanal.",
            "J) el surgimiento de centros urbanos."
        ],
        "answer": "D"
    },
    {
        "question": "Wari es la síntesis de tres culturas que el permitieron su desarrollo como Imperio, ellas fueron",
        "options": [
            "A) Huarpa – Nasca y Tiahuanaco.",
            "B) Huarpa – Chavín y Aymara.",
            "C) Paracas – Huarpa y Aymara.",
            "D) Huarpa – Nasca y Paracas.",
            "E) Huarpa – Tiahuanaco y Lucanas.",
            "F) Mochica – Huarpa y Tiahuanaco.",
            "G) Nazca – Paracas y Lucanas.",
            "H) Tiahuanaco – Mochica y Huarpa.",
            "I) Chavín – Paracas y Nazca.",
            "J) Aymara – Tiahuanaco y Huarpa."
        ],
        "answer": "A"
    },
    {
        "question": "Wari fue una síntesis de las de las siguientes culturas:",
        "options": [
            "A) Aymara, Huarpa y Tiahuanaco.",
            "B) Paracas, Huarpa y Aymara.",
            "C) Huarpa, Nasca y Tiahuanaco.",
            "D) Lupaca, Huarpa y Aymara.",
            "E) Huarpa, Lupaca y Tiahuanaco.",
            "F) Mochica, Huarpa y Nasca.",
            "G) Chavín, Paracas y Huarpa.",
            "H) Tiahuanaco, Nazca y Paracas.",
            "I) Huarpa, Mochica y Chavín.",
            "J) Aymara, Lupaca y Huarpa."
        ],
        "answer": "C"
    }
]
'''

file_path = os.path.join(os.path.dirname(__file__), 'data/test/preguntas_historia_del_Peru_10_opciones.json')

# Leer el contenido del archivo
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = file.read()

data = json.loads(json_data)

# Paso 1: Cargar la relación entre pregunta, índice de la pregunta dentro de la lista, y la letra de la opción correcta
question_info = []
for i, item in enumerate(data):
    question_info.append((item['question'], i, item['answer']))

# Paso 2: Verificar la distribución actual entre las letras de opciones y plantear cómo debería ser
letter_counts = {}
for _, _, answer in question_info:
    letter_counts[answer] = letter_counts.get(answer, 0) + 1

total_questions = len(question_info)
expected_count = total_questions // 10  # Distribuir entre las 10 opciones

new_answer_mapping = {}
options = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
for question, index, answer in question_info:
    new_answer = options[index % 10]
    new_answer_mapping[index] = new_answer

# Paso 3: Redactar el nuevo documento JSON modificado
for item in data:
    index = data.index(item)
    new_answer = new_answer_mapping[index]
    
    # Mover la respuesta correcta a la nueva letra definida
    correct_option = item['options'][ord(item['answer']) - ord('A')]
    item['options'].remove(correct_option)
    new_options = item['options']
    new_options.insert(options.index(new_answer), correct_option)
    
    # Actualizar las letras de las opciones en el texto
    for i in range(len(new_options)):
        new_options[i] = options[i] + new_options[i][1:]
    
    item['options'] = new_options
    
    # Cambiar el valor de "answer" por la nueva letra definida
    item['answer'] = new_answer

# Imprimir el JSON modificado
modified_json = json.dumps(data, indent=4, ensure_ascii=False)
print(modified_json)

# Guardar el JSON modificado en un archivo
with open('preguntas_historia_del_Peru_10_opciones_modificado_distribuido.json', 'w') as file:
    file.write(modified_json)


# Función para imprimir la nueva distribución de respuestas correctas por opción
def print_new_answer_distribution(data):
    new_letter_counts = {}
    for item in data:
        answer = item['answer']
        new_letter_counts[answer] = new_letter_counts.get(answer, 0) + 1
    
    print("Nueva distribución de respuestas correctas por opción:")
    for letter, count in new_letter_counts.items():
        print(f"{letter}: {count}")

# Llamar a la función para imprimir la nueva distribución de respuestas correctas
print_new_answer_distribution(data)