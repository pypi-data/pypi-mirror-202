# s = kd.cl.secrets.get("awscreds").decode_all()
import kubernetes_dynamic as kd
from kubernetes_dynamic.models.common import V1ObjectMeta
from kubernetes_dynamic.models.secret import V1Secret


class AssemblyInstance(kd.ResourceItem):
    pass


class MyClient(kd.K8sClient):
    @property
    def assemblies(self):
        """Get assemblies API."""
        return self.get_api("assemblies", object_type=AssemblyInstance)


def test_integration():
    cl = MyClient()
    cl.assemblies.get()
    for a in cl.assemblies.watch(name="kodbc-assembly"):
        print(a.object.metadata.labels)

    svc = kd.cl.services.read("kodbc-assembly-dap-dap")
    svc.get_pods()

    pod = kd.cl.pods.read("insights-keycloak-0")
    pod.exec("ls", container="keycloak")

    kd.cl.pods.find("insights")

    item = V1Secret(metadata=V1ObjectMeta(name="my-secret", labels={"key": "atti"}))
    item.set("item", "value")
    item.create_()
    item.refresh_()
    item.exists()
    kd.cl.secrets.delete(label_selector="key=atti", namespace="kxi")
    item.create_()
    item.delete_()

    for line in pod.logs(
        container="keycloak",
    ):
        print(line)
