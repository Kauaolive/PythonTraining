import os
import logging

logging.basicConfig(filename='renomeacao_arquivos.log', level=logging.INFO)

def buscar_arquivos(diretorio, nomes_arquivos):
    arquivos_encontrados = {}
    for nome in nomes_arquivos:
        caminho = os.path.join(diretorio, nome)

        if os.path.isfile(caminho):
            arquivos_encontrados[nome] = caminho
            logging.info(f"Arquivo encontrado: {caminho}")
            continue

        nome_sem_extensao = os.path.splitext(nome)[0]
        subpasta = os.path.join(diretorio, nome_sem_extensao)
        caminho_subpasta = os.path.join(subpasta, nome)

        if os.path.isdir(subpasta) and os.path.isfile(caminho_subpasta):
            arquivos_encontrados[nome] = caminho_subpasta
            logging.info(f"Arquivo encontrado em subpasta: {caminho_subpasta}")
        else:
            logging.warning(f"Arquivo não encontrado: {nome}")
    return arquivos_encontrados

def solicitar_novos_nomes_em_ordem(arquivos_encontrados):
    print("\nArquivos encontrados:")
    for i, nome in enumerate(arquivos_encontrados.keys(), start=1):
        print(f"{i}. {nome}")
    
    print("\nInsira os novos nomes dos arquivos na ordem listada acima, separados por vírgulas ou novas linhas:")
    novos_nomes_input = input("Novos nomes (cole da sua coluna do Excel):\n").strip()

    novos_nomes = [nome.strip() for nome in novos_nomes_input.replace(',', '\n').splitlines() if nome.strip()]

    if len(novos_nomes) != len(arquivos_encontrados):
        print("A quantidade de novos nomes não corresponde à quantidade de arquivos. Tente novamente.")
        return solicitar_novos_nomes_em_ordem(arquivos_encontrados)
    
    return dict(zip(arquivos_encontrados.keys(), novos_nomes))

def renomear_arquivos(diretorio_origem, diretorio_destino, arquivos_encontrados, novos_nomes):
    os.makedirs(diretorio_destino, exist_ok=True)  

    for nome_original, caminho_antigo in arquivos_encontrados.items():
        novo_caminho = os.path.join(diretorio_destino, novos_nomes[nome_original])
        try:
            os.rename(caminho_antigo, novo_caminho)
            logging.info(f"{nome_original} foi renomeado para {novos_nomes[nome_original]}")
            print(f"{nome_original} renomeado para {novos_nomes[nome_original]} e salvo em '{diretorio_destino}'")
        except Exception as e:
            logging.error(f"Erro ao renomear {nome_original}: {e}")
            print(f"Erro ao renomear {nome_original}: {e}")

def main():
    diretorio_origem = 'downloads/'
    diretorio_destino = 'arquivosProntos/'
    os.makedirs(diretorio_origem, exist_ok=True)

    print("Insira os nomes dos arquivos para buscar, separados por vírgulas ou novas linhas:")
    nomes_arquivos_input = input("Nomes dos arquivos originais (cole da sua coluna do Excel):\n").strip()
    nomes_arquivos = [nome.strip() for nome in nomes_arquivos_input.replace(',', '\n').splitlines() if nome.strip()]

    arquivos_encontrados = buscar_arquivos(diretorio_origem, nomes_arquivos)

    if not arquivos_encontrados:
        print("Nenhum dos arquivos especificados foi encontrado.")
        return

    novos_nomes = solicitar_novos_nomes_em_ordem(arquivos_encontrados)

    renomear_arquivos(diretorio_origem, diretorio_destino, arquivos_encontrados, novos_nomes)
    print("Processo de renomeação concluído.")

if __name__ == "__main__":
    main()
