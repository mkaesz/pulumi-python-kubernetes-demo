# pulumi-python-kubernetes-demo
This example deploy a GKE cluster and a simple website application onto it by using Pulumi and Python.

## Prerequisites

1. [Install Pulumi](https://www.pulumi.com/docs/get-started/install/)
1. [Configure Pulumi for Google Cloud](https://www.pulumi.com/docs/intro/cloud-providers/gcp/setup/)
1. [Configure Pulumi for Python](https://www.pulumi.com/docs/intro/languages/python/)

## Deploying and running the program

1. Create a new stack:

    ```bash
    $ pulumi stack init
    ```

1. Set the Google Cloud project and region

    ```bash
    $ pulumi config set gcp:project msk-pub
    $ pulumi config set gcp:region europe-west3
    ```
1. Configure the value to be shown on the website

    ```bash
    $ pulumi config set website:value mkaesz
    ```

1. Run `pulumi up` to preview and deploy the changes:

    ```bash
    $ pulumi up -y
    Previewing update (dev)

    View in Browser (Ctrl+O): https://app.pulumi.com/mkaesz/pulumi-python-kubernetes-demo/dev/previews/367cea8c-fb85-47c0-95f5-206e91543ae3

         Type                                       Name                               Plan
    +   pulumi:pulumi:Stack                        pulumi-python-kubernetes-demo-dev  create
    +   ├─ my:modules:ExposedKubernetesDeployment  website                            create
    +   │  ├─ kubernetes:core/v1:Service           website                            create
    +   │  └─ kubernetes:apps/v1:Deployment        website                            create
    +   ├─ gcp:container:Cluster                   gke-cluster                        create
    +   └─ pulumi:providers:kubernetes             gke_k8s                            create


    Outputs:
        ingress_ip: output<string>
        kubeconfig: output<string>

    Resources:
        + 6 to create

    Updating (dev)

    View in Browser (Ctrl+O): https://app.pulumi.com/mkaesz/pulumi-python-kubernetes-demo/dev/updates/20

        Type                                       Name                               Status
    +   pulumi:pulumi:Stack                        pulumi-python-kubernetes-demo-dev  created (386s)
    +   ├─ my:modules:ExposedKubernetesDeployment  website                            created (0.80s)
    +   │  ├─ kubernetes:core/v1:Service           website                            created (45s)
    +   │  └─ kubernetes:apps/v1:Deployment        website                            created (30s)
    +   ├─ gcp:container:Cluster                   gke-cluster                        created (337s)
    +   └─ pulumi:providers:kubernetes             gke_k8s                            created (0.45s)


    Outputs:
        ingress_ip: "34.159.224.190"
        kubeconfig: [secret]

    Resources:
        + 6 created

    Duration: 6m28s
    ```

1. Get the IP address of the newly-created instance from the stack's outputs: 

    ```bash
    $ pulumi stack output ingress_ip
    34.159.224.190 
    ```

1. Check to see that the website is up and is showing the configured value:

    ```bash
    $ curl http://$(pulumi stack output ingress_ip)
    Hello World mkaesz
    ```

1. Change the value that should be shown on the website

    ```bash
    $ pulumi config set website:value mkaesz-abc123
    ```

1. Run `pulumi up` again to preview and deploy the changes:

    ```bash
    $ pulumi up -y
    Previewing update (dev)

    View in Browser (Ctrl+O): https://app.pulumi.com/mkaesz/pulumi-python-kubernetes-demo/dev/previews/89def2be-fc86-49e6-89ce-a43acebc7386

        Type                                       Name                               Plan       Info
        pulumi:pulumi:Stack                        pulumi-python-kubernetes-demo-dev
        └─ my:modules:ExposedKubernetesDeployment  website
    ~      └─ kubernetes:apps/v1:Deployment        website                            update     [diff: ~spec]


    Resources:
        ~ 1 to update
        5 unchanged

    Updating (dev)

    View in Browser (Ctrl+O): https://app.pulumi.com/mkaesz/pulumi-python-kubernetes-demo/dev/updates/21

        Type                                       Name                               Status            Info
        pulumi:pulumi:Stack                        pulumi-python-kubernetes-demo-dev
        └─ my:modules:ExposedKubernetesDeployment  website
    ~      └─ kubernetes:apps/v1:Deployment        website                            updated (24s)     [diff: ~spec]


    Outputs:
        ingress_ip: "34.159.224.190"
        kubeconfig: [secret]

    Resources:
        ~ 1 updated
        5 unchanged

    Duration: 29s

1. Check to see that the website is up and is showing the new configured value:

    ```bash
    $ curl http://$(pulumi stack output ingress_ip)
    Hello World mkaesz-abc123
    ```

1. Destroy the stack:

    ```bash
    $ pulumi destroy -y
    Previewing destroy (dev)

    View in Browser (Ctrl+O): https://app.pulumi.com/mkaesz/pulumi-python-kubernetes-demo/dev/previews/a9fc9567-1713-43ef-a126-140262e4013e

        Type                                       Name                               Plan
    -   pulumi:pulumi:Stack                        pulumi-python-kubernetes-demo-dev  delete
    -   ├─ pulumi:providers:kubernetes             gke_k8s                            delete
    -   ├─ my:modules:ExposedKubernetesDeployment  website                            delete
    -   │  ├─ kubernetes:core/v1:Service           website                            delete
    -   │  └─ kubernetes:apps/v1:Deployment        website                            delete
    -   └─ gcp:container:Cluster                   gke-cluster                        delete


    Outputs:
    - ingress_ip: "34.159.224.190"
    - kubeconfig: [secret]

    Resources:
        - 6 to delete

    Destroying (dev)

    View in Browser (Ctrl+O): https://app.pulumi.com/mkaesz/pulumi-python-kubernetes-demo/dev/updates/22

        Type                                       Name                               Status
    -   pulumi:pulumi:Stack                        pulumi-python-kubernetes-demo-dev  deleted
    -   ├─ pulumi:providers:kubernetes             gke_k8s                            deleted (0.37s)
    -   ├─ my:modules:ExposedKubernetesDeployment  website                            deleted
    -   │  ├─ kubernetes:core/v1:Service           website                            deleted (32s)
    -   │  └─ kubernetes:apps/v1:Deployment        website                            deleted (32s)
    -   └─ gcp:container:Cluster                   gke-cluster                        deleted (232s)


    Outputs:
    - ingress_ip: "34.159.224.190"
    - kubeconfig: [secret]

    Resources:
        - 6 deleted

    Duration: 4m29s

    The resources in the stack have been deleted, but the history and configuration associated with the stack are still maintained.
    If you want to remove the stack completely, run `pulumi stack rm dev`. 
    ```

1. Remove the stack:

    ```bash
    $ pulumi stack rm dev
    This will permanently remove the 'dev' stack!
    Please confirm that this is what you'd like to do by typing `dev`: dev
    Stack 'dev' has been removed!
    ``` 
