import openai
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
# Configurar la API de OpenAI

os.environ['OpenAI_API_KEY'] 
client = OpenAI()
# Preguntas adicionales con solo 5 opciones
preguntas_adicionales = [
    {
        "question": "En el segundo gobierno de Fernando Belaúnde Terry (1980-1985), el país comenzó a experimentar una grave crisis económica, por lo que fue necesario iniciar la construcción de una serie de obras de infraestructura para dinamizar la economía. Una de las obras importantes fue la construcción",
        "options": [
            "A) de la represa Gallito Ciego.",
            "B) del complejo Chavimochic.",
            "C) del oleoducto norperuano.",
            "D) de la siderúrgica de Chimbote.",
            "E) de la hidroeléctrica de Carhuaquero."
        ],
        "answer": "E"
    },
    {
        "question": "Huari, una cultura muy importante de la Sierra Central, está ubicada dentro del Horizonte Medio. En relación con sus orígenes, de acuerdo con los estudios arqueológicos, los huaris recibieron la influencia de algunas culturas correspondientes a los Desarrollos Regionales como, por ejemplo,",
        "options": [
            "A) yaro.",
            "B) moche.",
            "C) chavín.",
            "D) nasca.",
            "E) chimú."
        ],
        "answer": "D"
    },
    {
        "question": "El yanaconaje fue una institución prehispánica vinculada al trabajo de servidumbre que los españoles rescataron, desvirtuaron y mantuvieron a su favor. Esta continuó a lo largo de la República durante el siglo xix, manteniéndose aún vigente y vigorosa en parte del siglo xx, cuando fue abolida mediante",
        "options": [
            "A) sentencia del Tribunal Agrario.",
            "B) ley agraria del Congreso.",
            "C) decreto de urgencia en la agricultura.",
            "D) decreto supremo en la agricultura.",
            "E) la Ley de Reforma Agraria."
        ],
        "answer": "E"
    },
    {
        "question": "Alrededor del prestigioso y estratégico Templo de Chavín de Huántar se congregaban diversos grupos de peregrinos portando productos traídos de diferentes puntos del territorio de los Andes. Los arqueólogos consideran que poblaciones de la Selva baja y alta llevaban hojas de coca, plumas de aves, maderas y posiblemente alucinógenos; de la serranía, minerales, como la obsidiana; y, de la Costa, sal, conchas y algodón. En virtud de lo anterior se puede concluir que, además de su función propiamente ritual como oráculo, el templo se constituyó en un centro",
        "options": [
            "A) urbano de dominio guerrero.",
            "B) de intercambio de productos.",
            "C) de actividades domésticas.",
            "D) asociado al culto al agua.",
            "E) de control de pisos ecológicos."
        ],
        "answer": "B"
    },
    {
        "question": "Las Leyes Nuevas fueron proclamadas por el rey Carlos I en 1542, disponiendo la instalación de una audiencia en Lima, como máximo organismo judicial del Perú; estaría presidida por el virrey con poderes administrativos y judiciales, las mismas que regularían la posición de los encomenderos. Los españoles que habían recibido encomiendas se opusieron a su aplicación, rebelándose contra la autoridad del Rey, pues consideraron que estas disposiciones /n I. recortaban los privilegios adquiridos por sus servicios a la Corona. /n II. imponían controles a su aprovechamiento de la mano de obra indígena. /n III. permitían entregar encomiendas hereditarias a los grupos criollos. /n IV. facultaban solo al virrey la potestad de repartir indios como vasallos.",
        "options": [
            "A) I, II y IV",
            "B) I, II y III ",
            "C) solo I",
            "D) I, III y IV",
            "E) solo I y II",
        ],
        "answer": "E"
    },
    {
        "question": "El primer gobierno de Fernando Belaúnde Terry (1963 -1968) se caracterizó por la búsqueda de soluciones a los difíciles problemas sociales y económicos del país, como el atraso y abandono del agro, la inequidad del ingreso que ampliaba las brechas de pobreza y la ausencia del Estado en el territorio nacional por la falta de infraestructura. Aunque su gobierno intentó realizar reformas renovadoras, uno de los factores políticos que explica los obstáculos que enfrentó fue la",
        "options": [
            "A) posición de empresas extranjeras, como la International Petroleum Company.",
            "B) presión que ejercieron los altos jefes militares en contra de su gobierno.",
            "C) persistente oposición del partido aprista, el odriismo y grupos oligárquicos.",
            "D) movilización de las guerrillas de izquierda en diversas regiones del país.",
            "E) derrota en las elecciones municipales de Lima debido al triunfo de Luis Bedoya."
        ],
        "answer": "C"
    },
    {
        "question": "Las razones con las que se ha desacreditado la teoría que sostenía el origen autóctono del hombre americano se basan en evidencias arqueológicas, ecológicas, genéticas, culturales y lingüísticas. Estás han llevado a los investigadores a concluir que el arribo del Homo sapiens sapiens a este continente se produjo por medio de oleadas migratorias que provinieron /nI. del noroeste de Asia. /nII. de islas de Oceanía. /nIII. de África occidental.",
        "options": [
            "A) Solo I",
            "B) Solo I y II ",
            "C) I, II y III",
            "D) Solo II",
            "E) Solo I y III",
        ],
        "answer": "B"
    },
    {
        "question": "Hace aproximadamente diez mil años, nuestra costa continental era más ancha pues el mar se había retirado como consecuencia de las glaciaciones, permitiendo el tránsito de individuos dispersos. Posteriormente, como parte de la dinámica de la Tierra, sucede un fenómeno contrario, conocido como",
        "options": [
            "A) Eoceno.",
            "B) Pleistoceno.",
            "C) Mioceno.",
            "D) Oligoceno.",
            "E) Holoceno."
        ],
        "answer": "E"
    },
    {
        "question": "Luego de la derrota de la Gran Rebelión, los curacas de sangre que apoyaron a Condorcanqui perdieron sus títulos, fueron reemplazados por curacas intrusos – criollos, peninsulares y mestizos – que desconocían la reciprocidad y redistribución andinas. Frente a este desequilibrio, los alcaldes varayocs adquirieron mayor importancia, pero, a diferencia de la nobleza indígena, eran elegidos solo anualmente de entre los indígenas del común. De acuerdo con lo anterior, se puede concluir que, en el periodo posterior a la Gran Rebelión, /n I. se debilitaron los liderazgos étnicos indígenas, pese al fortalecimiento de la figura del varayoc. /n II. los curacas intrusos contribuyeron a debilitar políticamente a las comunidades indígenas. /n III. los varayocs fortalecieron el liderazgo étnico, pese a la presencia de curacas intrusos. /n IV. los varayocs buscaron reemplazar a los curacas de sangre, sin lograr compensar su prestigio y poder.",
        "options": [
            "A) I, II y IV",
            "B) II, III y IV",
            "C) solo I y II",
            "D) solo I y IV",
            "E) I, III y IV"
        ],
        "answer": "A"
    }
]


def get_completion(prompt: str):
    final_prompt = [
        {
            "role": "system",
            "content": "You are a knowledge expert, you are supposed to answer the multi-choice question to derive your final answer as `The answer is ...`."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=final_prompt,
        temperature=0.1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return response.choices[0].message.content

def generar_opciones_adicionales(pregunta):
    prompt = f"Pregunta: {pregunta['question']}\nOpciones existentes: {', '.join(pregunta['options'])}\nGenera cinco opciones adicionales relevantes para esta pregunta."
    response_text = get_completion(prompt)
    nuevas_opciones = [line.strip() for line in response_text.split('\n') if line.strip() and not line.startswith("Claro")]
    return nuevas_opciones[:5]
# Añadir las opciones adicionales a las preguntas
for pregunta in preguntas_adicionales:
    nuevas_opciones = generar_opciones_adicionales(pregunta)
    if len(nuevas_opciones) >= 5:
        pregunta['options'].extend(nuevas_opciones[:5])
    else:
        pregunta['options'].extend(nuevas_opciones)
        # Completar con opciones genéricas si faltan
        opciones_genericas = ["F) Opción F.", "G) Opción G.", "H) Opción H.", "I) Opción I.", "J) Opción J."]
        pregunta['options'].extend(opciones_genericas[:10-len(pregunta['options'])])

# Guardar el JSON actualizado
json_path_updated = 'preguntas_historia_del_peru_10_opciones_actualizado.json'
with open(json_path_updated, 'w', encoding='utf-8') as f:
    json.dump(preguntas_adicionales, f, ensure_ascii=False, indent=4)

print("Preguntas actualizadas y guardadas en JSON exitosamente.")
