# ----------------------------------------------------------------------------
# ShipHelm Copyright 2020-2023 by Gameplex Software and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------
import docker

class helmdocker:
    def __init__(remote_address = None, remote_is_TLS = None):
        try:
            helmdocker.client = docker.from_env()
        except:
            helmdocker.client = docker.from_env(base_url=remote_address, tls=remote_is_TLS)

    @staticmethod
    def get_running_containers():
        return helmdocker.client.containers.list()

    @staticmethod
    def get_container_by_id(container_id):
        return helmdocker.client.containers.get(container_id)

    @staticmethod
    def get_container_stats(container_id):
        container = helmdocker.client.containers.get(container_id)
        stats = container.stats(stream=False)
        return stats

    @staticmethod
    def get_container_ports(container_id):
        container = helmdocker.client.containers.get(container_id)
        ports = container.attrs['NetworkSettings']['Ports']
        return ports

    @staticmethod
    def search_containers(name):
        return helmdocker.containers.list(filters={"name": name})

    @staticmethod
    def change_container_ports(container_id, ports):
        container = helmdocker.client.containers.get(container_id)
        container.reload()
        container.ports.update(ports)

    @staticmethod
    def rename_container(container_id, new_name):
        container = helmdocker.client.containers.get(container_id)
        container.rename(new_name)

    @staticmethod
    def add_container_to_network(container_id, network_name):
        network = helmdocker.client.networks.get(network_name)
        container = helmdocker.client.containers.get(container_id)
        network.connect(container)

    @staticmethod
    def remove_container_from_network(container_id, network_name):
        network = helmdocker.client.networks.get(network_name)
        container = helmdocker.client.containers.get(container_id)
        network.disconnect(container)

    @staticmethod
    def create_network(network_name):
        helmdocker.client.networks.create(network_name)

    @staticmethod
    def delete_network(network_name):
        network = helmdocker.client.networks.get(network_name)
        network.remove()

    @staticmethod
    def run_container(image, command=None, detach=False, ports=None, environment=None, volumes=None):
        container = helmdocker.client.containers.run(
            image=image,
            command=command,
            detach=detach,
            ports=ports,
            environment=environment,
            volumes=volumes
        )
        return container

    @staticmethod
    def get_container_environment(container_id):
        container = helmdocker.client.containers.get(container_id)
        environment = container.attrs['Config']['Env']
        return environment

    @staticmethod
    def set_container_environment(container_id, environment):
        container = helmdocker.client.containers.get(container_id)
        container.reload()
        container.update(env=environment)

    @staticmethod
    def get_container_volumes(container_id):
        container = helmdocker.client.containers.get(container_id)
        volumes = container.attrs['HostConfig']['Binds']
        return volumes

    @staticmethod
    def set_container_volumes(container_id, volumes):
        container = helmdocker.client.containers.get(container_id)
        container.reload()
        container.update(binds=volumes)