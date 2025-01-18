import twain
import os
import logging
from datetime import datetime

def list_scanners():
    try:
        # Initialize Source Manager
        sm = twain.SourceManager(0)
        
        # Get scanner list
        sources = sm.GetSourceList()
        if not sources:
            print("Nenhum scanner TWAIN encontrado.")
            return

        print("Scanners TWAIN disponíveis:")
        for index, source in enumerate(sources):
            print(f"{index + 1}: {source}")

        # Select scanner
        selected_scanner = int(input("Selecione o Scanner: ")) - 1
        if selected_scanner < 0 or selected_scanner >= len(sources):
            print("Opção inválida.")
            return

        ss = sm.OpenSource(sources[selected_scanner])

        # Get batch name
        batch_name = input("Digite o nome do lote: ").strip()
        if not batch_name:
            print("Nome do lote inválido.")
            return

        # Create output directory
        output_dir = os.path.join(os.getcwd(), batch_name)
        os.makedirs(output_dir, exist_ok=True)

        image_counter = 1
        prefix_name = "SAME"
        print("Pressione Enter para iniciar a digitalização ou digite 'sair' para encerrar.")

        while True:
            command = input("Pronto para digitalizar (Enter para continuar ou 'sair' para encerrar): ").strip()
            if command.lower() == 'sair':
                break

            # Acquire image
            ss.RequestAcquire(0, 0)

            # Transfer image
            rv = ss.XferImageNatively()
            if rv:
                handle, count = rv

                # Generate file name
                date_str = datetime.now().strftime("%d%m%y")
                file_name = f"{prefix_name}_{image_counter:04d}_{date_str}.tiff"
                file_path = os.path.join(output_dir, file_name)

                # Save image as TIFF
                twain.DIBToBMFile(handle, file_path)
                print(f"Imagem salva: {file_path}")

                image_counter += 1
            else:
                print("Falha na transferência da imagem.")

        # Close source and manager
        ss.close()
        sm.destroy()
        print(f"Digitalização do lote '{batch_name}' concluída.")

    except Exception as e:
        logging.error(f"Erro ao acessar o scanner: {e}")

if __name__ == "__main__":
    list_scanners()

    user_input = None
    while user_input != "1":
        user_input = input("Digite 1 para sair: ")
