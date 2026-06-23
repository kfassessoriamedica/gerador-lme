import streamlit as st
from pypdf import PdfReader, PdfWriter
import io
import json
import google.generativeai as genai

st.set_page_config(page_title="Gerador LME com IA", page_icon="🤖")
st.title("🤖 Gerador Automático de LME com IA")
st.write("Cole a evolução do paciente abaixo e deixe a IA preencher o formulário do SUS.")

# Interface limpa: Apenas a chave de segurança e o texto livre
api_key = st.text_input("🔑 Cole sua Chave de API do Google (Gemini) aqui:", type="password")
texto_livre = st.text_area("📝 Cole a Anamnese / Evolução Clínica aqui:", height=250, placeholder="Ex: Paciente Lourdes, 70 anos, peso 68kg, altura 158cm. DPOC grave com indicação de...")

if st.button("✨ Analisar com IA e Gerar LME"):
    if not api_key or not texto_livre:
        st.error("Por favor, insira sua chave API e o texto clínico.")
    else:
        with st.spinner("A IA está lendo o prontuário e preenchendo o formulário..."):
            try:
                # 1. Configura a comunicação com a IA
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 2. Pede para a IA extrair os dados organizados
                prompt = f"""
                Aja como um assistente médico. Leia o texto abaixo e extraia os dados para preencher um formulário LME.
                Retorne APENAS um objeto JSON válido, sem formatação markdown ou textos adicionais. 
                As chaves obrigatórias são exatamente estas:
                "Nome do paciente", "Peso", "Altura", "CID", "Diagnóstico", "med1", "med2", "Anamnese", "tratamentos prévios".
                Se faltar alguma informação no texto, deixe o valor em branco "".
                
                Texto clínico:
                {texto_livre}
                """
                
                resposta = model.generate_content(prompt)
                
                # 3. Organiza os dados lidos pela IA
                texto_json = resposta.text.strip().replace('```json', '').replace('
```', '')
                dados_ia = json.loads(texto_json)
                
                # Adiciona os seus dados fixos (Médica e Clínica)
                dados_ia['CNES'] = '7241798'
                dados_ia['Nome do estabelecimento de saúde'] = 'Intervalemed Centro Medico Integrado'
                dados_ia['Text46'] = 'Katia S.A Froufe'
                dados_ia['TextCNS'] = '706.9091.8528.4330'
                dados_ia['Hoje'] = '23/06/2026'
                
                # 4. Injeta tudo no PDF
                reader = PdfReader("LME_6_meses.pdf")
                writer = PdfWriter()
                writer.append(reader)
                writer.update_page_form_field_values(writer.pages[0], dados_ia)
                
                # 5. Disponibiliza para Download
                output_pdf = io.BytesIO()
                writer.write(output_pdf)
                output_pdf.seek(0)
                
                st.success("✅ LME interpretada e gerada com sucesso pela IA!")
                st.download_button(
                    label="📥 Baixar PDF Preenchido",
                    data=output_pdf,
                    file_name=f"LME_{dados_ia.get('Nome do paciente', 'Paciente').replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
