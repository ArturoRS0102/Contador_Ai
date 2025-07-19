import os
import openai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar la API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    """ Sirve la página principal (index.html). """
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """ Recibe la consulta del usuario y devuelve la respuesta de OpenAI. """
    data = request.json
    pregunta = data.get("pregunta")

    if not pregunta:
        return jsonify({"error": "La pregunta no puede estar vacía."}), 400

    try:
        # --- NUEVO Prompt del Sistema (Asesor Contable) ---
        prompt_sistema = f"""
        Actúa como un asesor contable experto en México con un enfoque educativo. Tu objetivo principal es proporcionar guías claras, explicaciones y nociones generales sobre temas contables para ayudar a los usuarios a entender los procesos.

        Temas a cubrir: Declaraciones de impuestos (anuales, mensuales), facturación (CFDI 4.0), regímenes fiscales (RESICO, actividad empresarial), SAT, deducciones, etc.
        
        Tu tono debe ser profesional, claro y fácil de entender para alguien que no es experto en contabilidad. Puedes dar guías paso a paso si es apropiado.

        IMPORTANTE: NO eres un contador personal y NO ofreces contabilidad como servicio. Tu función es enseñar. Finaliza SIEMPRE tus respuestas con la siguiente advertencia obligatoria: 'Este es un consejo orientativo y educativo. No reemplaza la asesoría personalizada de un contador público certificado, quien debe revisar tu caso específico.'
        """

        # Llamada a la API de OpenAI con más tokens
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": pregunta}
            ],
            max_tokens=450,  # Aumentamos el límite para respuestas más detalladas
            temperature=0.6, 
        )
        
        respuesta_ia = response.choices[0].message.content.strip()
        return jsonify({"respuesta": respuesta_ia})

    except Exception as e:
        print(f"Error al llamar a la API de OpenAI: {e}")
        return jsonify({"error": "Hubo un problema al contactar al asistente. Inténtalo de nuevo."}), 500

if __name__ == "__main__":
    app.run(debug=True)