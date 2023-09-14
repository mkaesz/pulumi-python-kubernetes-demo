import pulumi
import pulumi_gcp as gcp

from pulumi import Config, export, get_project, get_stack, Output
from pulumi_gcp.config import project, zone
from pulumi_gcp.container import Cluster, ClusterNodeConfigArgs
from pulumi_kubernetes import Provider

from deployment import ExposedKubernetesDeploymentArgs, ExposedKubernetesDeployment
import container_image

# Read in some configurable settings for the cluster.
config = Config(None)

NODE_COUNT = config.get_int('node_count') or 3
NODE_MACHINE_TYPE = config.get('node_machine_type') or 'n1-standard-1'

WEBSITE_VALUE = Config("website").require("value")

# Create the GKE cluster.
k8s_cluster = Cluster('gke-cluster',
    initial_node_count=NODE_COUNT,
    node_config=ClusterNodeConfigArgs(
        machine_type=NODE_MACHINE_TYPE,
    ),
)

# Create a GKE-style Kubeconfig.
k8s_info = Output.all(k8s_cluster.name, k8s_cluster.endpoint, k8s_cluster.master_auth)
k8s_config = k8s_info.apply(
    lambda info: """apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {0}
    server: https://{1}
  name: {2}
contexts:
- context:
    cluster: {2}
    user: {2}
  name: {2}
current-context: {2}
kind: Config
preferences: {{}}
users:
- name: {2}
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: gke-gcloud-auth-plugin
      installHint: Install gke-gcloud-auth-plugin for use with kubectl by following
        https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
      provideClusterInfo: true
""".format(info[2]['cluster_ca_certificate'], info[1], '{0}_{1}_{2}'.format(project, zone, info[0])))

# Make a Kubernetes provider instance that uses our cluster from above.
k8s_provider = Provider('gke_k8s', kubeconfig=k8s_config)

deployment = ExposedKubernetesDeployment('website',
    ExposedKubernetesDeploymentArgs(
        image=container_image.image.image_name,
        name='website',
        website_value=WEBSITE_VALUE,
        port=80,
        targetPort=8080,
        replicas=1,
    ), opts=pulumi.ResourceOptions(provider=k8s_provider)
)

export('kubeconfig', k8s_config)
export('ingress_ip', deployment.ingress.status.apply(lambda status: status.load_balancer.ingress[0].ip))
