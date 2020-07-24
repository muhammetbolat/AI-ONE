from abc import ABC, abstractmethod


class ControllerBase(ABC):
    def register_api_endpoints(self, base_route: str, add_endpoint):
        for route in self.endpoints():
            add_endpoint(endpoint=f'{base_route}{route.get("endpoint")}',
                         endpoint_name=route.get("endpoint_name"),
                         handler=route.get("handler"),
                         methods=route.get("methods")
                         )
        pass

    @abstractmethod
    def endpoints(self) -> []:
        pass
