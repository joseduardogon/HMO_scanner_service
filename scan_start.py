import twain
import logging

def list_scanners():
    try:
        # Init manager
        sm = twain.SourceManager(0)
        # Get scanner list
        sources = sm.GetSourceList()
        if not sources:
            print("Nenhum scanner TWAIN encontrado.")
            return
        print("Scanners TWAIN disponíveis:")
        for index, source in enumerate(sources):
            print(f"{index + 1}: {source}")
        # Select first
        ss = sm.OpenSource(sources[0])
        # Get image
        ss.RequestAcquire(0, 0)
        # Transfer image
        rv = ss.XferImageNatively()
        if rv:
            handle, count = rv
            # Save image as BMP
            twain.DIBToBMFile(handle, 'teste_digitalizacao.bmp')
            print("Digitalização concluída com sucesso. Imagem salva como 'teste_digitalizacao.bmp'.")
        else:
            print("Falha na transferência da imagem.")
        # Close source
        ss.close()
        # Close manager
        sm.destroy()
    except Exception as e:
        logging.error(f"Erro ao acessar o scanner: {e}")

if __name__ == "__main__": list_scanners()

user_input = None
while user_input != "1":
    user_input = input("digite 1 para sair: ")