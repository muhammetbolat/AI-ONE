from container import IocContainer
application = IocContainer.applicationWrapper()

#if __name__ == "__main__":
#    application.run()

neural_network_service = IocContainer.neural_network_service()

if __name__ == "__main__":
    neural_network_service.run_training_operation()
