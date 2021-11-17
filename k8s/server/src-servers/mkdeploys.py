import os
import glob
import subprocess

def write_deployment(config, name, redi=""):
    os.makedirs(f"deployments/{name}", exist_ok=True)
    for template in glob.glob("deployments/template/*"):
        with open(template, "r") as f_in:
            text = f_in.read()
            if template[-3:] != ".sh":
                # Strip comments from templates
                text = "\n".join([l for l in text.split("\n") if l[:1] != "#"])
            # Replace placeholders
            text = text.replace("NODE_PLACEHOLDER", config["node"])
            text = text.replace("NVME_PLACEHOLDER", "\n".join([f"oss.space public {n}" for n in config["nvmes"]]))
            text = text.replace("NAME_PLACEHOLDER", name)
            text = text.replace("REDI_PLACEHOLDER", redi)
            text = text.replace("INTF_PLACEHOLDER", config["interface"])
            text = text.replace("PORT_PLACEHOLDER", config["port"])
        with open(template.replace("/template/", f"/{name}/"), "w") as f_out:
            f_out.write(text)

def __get_deployments():
    return [d for d in glob.glob("deployments/*") if d != "deployments/template"]

if __name__ == "__main__":
    for old_deployment in __get_deployments():
        for f in glob.glob(f"{old_deployment}/*"):
            os.remove(f)
        os.rmdir(old_deployment)

    src_configs = [
        {
            "node": "k8s-gen4-07.ultralight.org", 
            "port": "2094",
            "interface": "enp33s0.3911",
            "nvmes": ["/nvme1/", "/nvme2/", "/nvme3/"]
        }, 
        {
            "node": "k8s-gen4-07.ultralight.org", 
            "port": "2095",
            "interface": "enp33s0.3912",
            "nvmes": ["/nvme4/", "/nvme5/", "/nvme6/"]
        }, 
        {
            "node": "dtn-man239.northwestern.edu", 
            "port": "2094",
            "interface": "p1p1",
            "nvmes": ["/nvme1/", "/nvme2/", "/nvme3/"]
        }, 
        {
            "node": "dtn-man239.northwestern.edu", 
            "port": "2095",
            "interface": "p4p2",
            "nvmes": ["/nvme4/", "/nvme5/", "/nvme6/"]
        }, 
    ]

    kube_cmd = subprocess.Popen(
        'kubectl get pods -l k8s-app=src-redi -o jsonpath="{.items[0].status.podIP}"'.split(),
        stdout = subprocess.PIPE
    )
    src_redi, _ = kube_cmd.communicate()
    src_redi = src_redi[1:-1].decode("utf-8") # remove quotation marks and decode
    for i, src_config in enumerate(src_configs):
        N = src_config["node"].split(".")[0].split("-")[-1]
        write_deployment(src_config, f"src-origin-{N}-{src_config['interface']}", redi=src_redi)

    with open("Makefile", "w") as f_out:
        f_out.write("delete:\n")
        for new_deployment in __get_deployments():
            f_out.write(f"\t- kubectl delete -k ./{new_deployment}\n")
        f_out.write("create:\n")
        for new_deployment in __get_deployments():
            f_out.write(f"\t- kubectl apply -k ./{new_deployment}\n")
