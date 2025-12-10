from fabric import task
import os

# @task
# def clean(c, docs=False, bytecode=False, extra=""):
#     patterns = ["build"]
#     if docs:
#         patterns.append("docs/_build")
#     if bytecode:
#         patterns.append("**/*.pyc")
#     if extra:
#         patterns.append(extra)
#     for pattern in patterns:
#         c.run(f"rm -rf {pattern}")


@task
def setup_cloudflare(c):
    # https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/local-management/create-local-tunnel/
    c.run("brew install cloudflared")


# cloudflared tunnel login
# cloudflared tunnel create -h
# cloudflared service install
# cloudflared tunnel route dns basd basd.asd.com
# vim: create the file .cloudflared/config.yml
# cloudflared tunnel ingress validate

# brew install cloudflare-warp


@task
def setup_homebrew(c):
    print("Setting up Kubespot for Mac...")

    print("Installing depedencies...")
    out = c.run("which brew", hide=True)
    if "not found" in out.stdout:
        print("Homebrew not found. Installing Homebrew...")
        # TODO: Install Homebrew
    else:
        c.run("brew upgrade")

    c.run("brew install minikube gh")


@task
def setup_minikube_github_actions(c):
    c.run("KUBECONFIG=./kubeconfig helm delete -n github arc arc-runner-set", warn=True)

    c.run("minikube delete", warn=True)

    # CPUS=$(( $(sysctl -n hw.ncpu) - 1 ))
    # MEMORY_GB=$($)sysctl -n hw.memsize | awk '{ printf "%.2f\n", $1/1024/1024/1024 }) - 1)
    c.run("minikube start --cpus=6 --memory=14G --disk-size=300g --driver qemu")
    c.run("KUBECONFIG=$HOME/kubeconfig minikube update-context")

    c.run(
        "helm repo add actions-runner-controller https://actions-runner-controller.github.io/actions-runner-controller"
    )
    c.run("helm repo update")

    # https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml
    c.run(
        "helm upgrade --install arc --create-namespace --namespace github oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller"
    )

    github_config_url = os.environ["KUBESPOT_FOR_MAC_GITHUB_ACTIONS_CONFIG_URL"]
    github_pat = os.environ["KUBESPOT_FOR_MAC_GITHUB_ACTIONS_PAT"]

    c.run(
        f"""helm upgrade --install arc-runner-set \
          --namespace github --create-namespace \
          --set githubConfigUrl="{github_config_url}" \
          --set githubConfigSecret.github_token="{github_pat}" \
          --set containerMode.type=dind \
          --set containerMode.kubernetesModeWorkVolumeClaim.resources.requests.storage="5Gi" \
          oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set"""
    )
