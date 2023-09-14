import pulumi
import pulumi_gcp as gcp

from pulumi import Config, export, get_project, get_stack, ResourceOptions, ComponentResource
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import ContainerArgs, EnvVarArgs, PodSpecArgs, PodTemplateSpecArgs, Service, ServicePortArgs, ServiceSpecArgs
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs

class ExposedKubernetesDeploymentArgs:
    def __init__(self,
                 image=None,
                 name=None,
                 website_value=None,
                 port=None,
                 targetPort=None,
                 replicas=1,
                 ):
        self.image = image
        self.name = name
        self.website_value = website_value
        self.port = port
        self.targetPort = targetPort
        self.replicas = replicas

class ExposedKubernetesDeployment(ComponentResource):
    def __init__(self,
                 name: str,
                 args: ExposedKubernetesDeploymentArgs,
                 opts: ResourceOptions = None):
        super().__init__("my:modules:ExposedKubernetesDeployment", name, {}, opts)

        # Create the website deployment.
        labels = { 'app': '{0}-{1}-{2}'.format(args.name, get_project(), get_stack()) }
        deployment = Deployment(args.name,
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
                                        value=args.website_value, 
                                    )
                                ],
                            )
                        ]
                    ),
                ),
            ), opts=ResourceOptions(parent=self, provider=opts.provider)
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
            ), opts=ResourceOptions(parent=self, provider=opts.provider)
        )

        self.register_outputs({})
