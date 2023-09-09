import pulumi
import pulumi_gcp as gcp

from pulumi import Config, export, get_project, get_stack, Output, ResourceOptions, ComponentResource
from pulumi_kubernetes import Provider
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import ContainerArgs, EnvVarArgs, PodSpecArgs, PodTemplateSpecArgs, Service, ServicePortArgs, ServiceSpecArgs
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs

WEBSITE_VALUE = Config("website").require("value")

class DeploymentArgs:

    def __init__(self,
                 image=None,
                 name=None,
                 port=None,
                 targetPort=None,
                 replicas=1,
                 k8s_provider=None
                 ):
        self.image = image
        self.name = name
        self.port = port
        self.targetPort = targetPort
        self.replicas = replicas
        self.k8s_provider = k8s_provider

class ExposedKubernetesDeployment(ComponentResource):
    def __init__(self,
                 name: str,
                 args: DeploymentArgs,
                 opts: ResourceOptions = None):
        super().__init__("my:modules:ExposedKubernetesDeployment", name, {}, opts)

        # Create the website deployment.
        labels = { 'app': '{0}-{1}-{2}'.format(args.name, get_project(), get_stack()) }
        website = Deployment(args.name,
            spec=DeploymentSpecArgs(
                selector=LabelSelectorArgs(match_labels=labels),
                replicas=args.replicas,
                template=PodTemplateSpecArgs(
                    metadata=ObjectMetaArgs(labels=labels),
                    spec=PodSpecArgs(
                        containers=[
                            ContainerArgs(
                                name=args.name, 
                                image=args.image, 
                                env=[
                                    EnvVarArgs(
                                        name="PULUMI_CFG_VALUE",
                                        value=WEBSITE_VALUE, 
                                    )
                                ],
                            )
                        ]
                    ),
                ),
            ), opts=ResourceOptions(parent=self, provider=args.k8s_provider)
        )


        # Expose the deployment as a public service.
        self.ingress = Service(args.name,
            spec=ServiceSpecArgs(
                type='LoadBalancer',
                selector=labels,
                ports=[
                    ServicePortArgs(
                        port=args.port, 
                        target_port=args.targetPort
                    )
                ],
            ), opts=ResourceOptions(parent=self, provider=args.k8s_provider)
        )

        self.register_outputs({})
