# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "invoke",
# ]
# ///

from invoke import task


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
def setup(c):
    print("Setting up Kubespot for Mac...")

    print("Installing depedencies...")
    out = c.run("which brew", hide=True)
    if "not found" in out.stdout:
        print("Homebrew not found. Installing Homebrew...")
        # TODO:
    else:
        c.run("brew upgrade")
