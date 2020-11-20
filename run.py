
if __name__ == '__main__':
    from app import create_app, manager
    print('Inicializando a aplicação...')
    create_app()
    manager.run()
