import streamlit as st
from pypdf import PdfReader, PdfWriter
import io
import json
import google.generativeai as genai

st.set_page_config(page_title="Gerador LME com IA", page_icon="🤖")
st.title("🤖 Gerador Automático de LME com IA")
st.write("Cole a evolução do paciente abaixo e deixe a IA preencher o formulário do SUS.")

api_key = st.text_input("🔑 Cole sua Chave de API do Google (Gemini) aqui:", type="password")
texto_livre = st.text_area("📝 Cole a Anamnese / Evolução Clínica aqui:", height=250)

if st.button("✨ Analisar com IA e Gerar LME"):
    if not api_key or not texto_livre:
        st.error("Por favor, insira sua chave API e o texto clínico.")
    else:
        with st.spinner("A IA está lendo o prontuário e preenchendo o formulário..."):
            try:
                genai.configure(api_key=api_key)
                # Modelo corrigido e com alinhamento perfeito
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"""
                Extraia os dados para preencher um formulário LME. Retorne APENAS um JSON válido.
                Chaves obrigatórias exatas:
                "Nome do paciente", "Peso", "Altura", "CID", "Diagnóstico", "med1", "med2", "Anamnese", "tratamentos prévios".
                Se não houver a informação, deixe em branco "".
                Texto clínico: {texto_livre}
                """
                
                resposta = model.generate_content(prompt)
                
                texto_json = resposta.text.strip().replace("```json", "").replace("```", "")
                dados_ia = json.loads(texto_json)
                
                # Dados fixos
                dados_ia['CNES'] = '7241798'
                dados_ia['Nome do estabelecimento de saúde'] = 'Intervalemed Centro Medico Integrado'
                dados_ia['Text46'] = 'Katia S.A Froufe'
                dados_ia['TextCNS'] = '706.9091.8528.4330'
                dados_ia['Hoje'] = '23/06/2026'
                
                # PDF
                reader = PdfReader("LME_6_meses.pdf")
                writer = PdfWriter()
                writer.append(reader)
                writer.update_page_form_field_values(writer.pages[0], dados_ia)
                
                output_pdf = io.BytesIO()
                writer.write(output_pdf)
                output_pdf.seek(0)
                
                st.success("✅ LME interpretada e gerada com sucesso pela IA!")
                st.download_button(
                    label="📥 Baixar PDF Preenchido",
                    data=output_pdf,
                    file_name="LME_Preenchida.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
