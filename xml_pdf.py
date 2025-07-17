from pdfminer.high_level import extract_text
from lxml import etree
import re

def extrair_metadados(pdf_path):
    """
    Função para extrair metadados básicos do PDF, como título, autor, etc.
    """
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument

    with open(pdf_path, "rb") as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        metadata = document.info[0]  # Metadados do primeiro documento

    return metadata

def texto_para_xml(texto, xml_output_path):
    """
    Função para converter o texto extraído do PDF em um XML estruturado.
    """
    root = etree.Element("documento")

    # Adicionar metadados ao XML
    metadata = extrair_metadados()
    metadados_elem = etree.SubElement(root, "metadados")
    for key, value in metadata.items():
        meta_elem = etree.SubElement(metadados_elem, key)
        meta_elem.text = value

    # Adicionar conteúdo extraído no corpo do XML
    corpo = etree.SubElement(root, "corpo")
    corpo.text = texto

    # Gerar e salvar o XML
    tree = etree.ElementTree(root)
    tree.write(xml_output_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print(f"Arquivo XML gerado: {xml_output_path}")

def extrair_tabelas(texto):
    """
    Função para tentar identificar tabelas no texto extraído do PDF e transformá-las em uma estrutura de listas.
    """
    linhas = texto.split("\n")
    tabelas = []

    for linha in linhas:
        # Tente identificar padrões de tabelas por espaços em branco (exemplo simples)
        if re.match(r'^\d+\s+\w+', linha):  # Esse padrão pode ser ajustado dependendo da tabela
            tabelas.append(linha.split())

    return tabelas

def pdf_para_xml(pdf_path, xml_output_path):
    """
    Função principal que converte um PDF para XML.
    """
    # Extrair texto do PDF
    texto = extract_text(pdf_path)

    # Extrair tabelas, se houver
    tabelas = extrair_tabelas(texto)

    # Adicionar as tabelas ao XML, se encontradas
    if tabelas:
        root = etree.Element("documento")
        tabelas_elem = etree.SubElement(root, "tabelas")
        for tabela in tabelas:
            tabela_elem = etree.SubElement(tabelas_elem, "tabela")
            tabela_elem.text = " ".join(tabela)

        # Salvar o XML com tabelas
        tree = etree.ElementTree(root)
        tree.write(xml_output_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        print(f"Arquivo XML com tabelas gerado: {xml_output_path}")
    else:
        texto_para_xml(texto, xml_output_path)

# Exemplo de uso
pdf_para_xml('exemplo.pdf', 'saida.xml')
