import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(page_title="Gerador LME", page_icon="🏥")
st.title("🏥 Gerador Automático de LME - SUS")

# Formulário na tela
nome = st.text_input("Nome do Paciente")
col1, col2 = st.columns(2)
with col1:
    peso = st.text_input("Peso (kg)")
with col2:
    altura = st.text_input("Altura (cm)")

cid = st.text_input("CID-10")
diagnostico = st.text_input("Diagnóstico")
med1 = st.text_input("Medicamento 1", "Brometo de Tiotrópio 2,5 mcg + Olodaterol 2,5 mcg")
med2 = st.text_input("Medicamento 2", "Budesonida 200 mcg")
anamnese = st.text_area("Anamnese")
previos = st.text_area("Tratamentos Prévios")

if st.button("Gerar LME (PDF)"):
    if not nome:
        st.error("Por favor, preencha o nome do paciente.")
    else:
        try:
            # Organiza os dados
            dados = {
                'Nome do paciente': nome.upper(),
                'Peso': peso,
                'Altura': altura,
                'CID': cid.upper(),
                'Diagnóstico': diagnostico,
                'med1': med1,
                'med2': med2,
                'Anamnese': anamnese,
                'tratamentos prévios': previos,
                'CNES': '7241798',
                'Nome do estabelecimento de saúde': 'Intervalemed Centro Medico Integrado',
                'Text46': 'Katia S.A Froufe',
                'TextCNS': '706.9091.8528.4330',
                'Hoje': '23/06/2026'
            }

            # Preenche o PDF
            reader = PdfReader("LME_6_meses.pdf")
            writer = PdfWriter()
            writer.append(reader)
            writer.update_page_form_field_values(writer.pages[0], dados)

            # Salva na memória do site para o usuário baixar
            output_pdf = io.BytesIO()
            writer.write(output_pdf)
            output_pdf.seek(0)

            st.success("LME gerada com sucesso! Clique no botão abaixo para baixar.")
            
            st.download_button(
                label="📥 Baixar Arquivo PDF Pronta",
                data=output_pdf,
                file_name=f"LME_{nome.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except FileNotFoundError:
            st.error("Erro: O arquivo 'LME_6_meses.pdf' não foi encontrado no sistema.")
        except Exception as e:
            st.error(f"Erro interno: {e}")