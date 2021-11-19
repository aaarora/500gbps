import os
import glob
import subprocess

def write_deployment(config, name, redi="", deployment_dir="deployments", template_dir="template"):
    os.makedirs(f"{deployment_dir}/{name}", exist_ok=True)
    for template in glob.glob(f"{template_dir}/*"):
        with open(template, "r") as f_in:
            text = f_in.read()
            if template[-3:] != ".sh":
                # Strip comments from templates
                text = "\n".join([l for l in text.split("\n") if l[:1] != "#"])
            # Replace placeholders
            text = text.replace("NODE_PLACEHOLDER", config["node"])
            text = text.replace("NVME_PLACEHOLDER", "\n".join([f"oss.space public {n}" for n in config["nvmes"]]))
            text = text.replace("NAME_PLACEHOLDER", name)
            text = text.replace("REDI_PLACEHOLDER", f"{redi}:{config['redi_port']}")
            text = text.replace("INTF_PLACEHOLDER", config["interface"])
            text = text.replace("PORT_PLACEHOLDER", config["port"])
            text = text.replace("VLAN_PLACEHOLDER", config["vlan"])
        with open(template.replace(f"{template_dir}/", f"{deployment_dir}/{name}/"), "w") as f_out:
            f_out.write(text)

def write_deployments(configs, base_dir="servers", server_name="origin", redi_name="redi"):
    os.makedirs(base_dir, exist_ok=True)
    deployment_dir = f"{base_dir}/deployments"
    for old_deployment in __get_deployments(deployment_dir):
        for f in glob.glob(f"{old_deployment}/*"):
            os.remove(f)
        os.rmdir(old_deployment)

    kube_cmd = subprocess.Popen(
        ["kubectl", "get", "pods", "-l", f"k8s-app={redi_name}", "-o", 'jsonpath="{.items[0].status.podIP}"'],
        stdout = subprocess.PIPE
    )
    redi, _ = kube_cmd.communicate()
    redi = redi[1:-1].decode("utf-8") # remove quotation marks and decode
    for i, config in enumerate(configs):
        N = config["node"].split(".")[0].split("-")[-1]
        write_deployment(
            config, 
            f"{server_name}-{N}-{config['interface'].replace('.', '-')}", 
            redi=redi,
            deployment_dir=deployment_dir
        )

    with open(f"{base_dir}/Makefile", "w") as f_out:
        f_out.write("delete:\n")
        for new_deployment in __get_deployments(deployment_dir):
            local_path = new_deployment.replace(f"{base_dir}/", "")
            f_out.write(f"\t- kubectl delete -k ./{local_path}\n")
        f_out.write("create:\n")
        for new_deployment in __get_deployments(deployment_dir):
            local_path = new_deployment.replace(f"{base_dir}/", "")
            f_out.write(f"\t- kubectl apply -k ./{local_path}\n")

def __get_deployments(deployment_dir="deployments"):
    return [d for d in glob.glob(f"{deployment_dir}/*")]

if __name__ == "__main__":
    dst_configs = [
        {
            "node": "k8s-gen4-01.sdsc.optiputer.net", 
            "port": "2094",
            "interface": "enp1s0f0",
            "vlan": "10.16.23.5",
            "redi_port": "2213",
            "nvmes": ["/nvme1/", "/nvme2/", "/nvme3/"]
        }, 
        {
            "node": "k8s-gen4-01.sdsc.optiputer.net", 
            "port": "2095",
            "interface": "enp1s0f1",
            "vlan": "10.16.25.5",
            "redi_port": "2213",
            "nvmes": ["/nvme4/", "/nvme5/", "/nvme6/"]
        }, 
        {
            "node": "k8s-gen4-01.sdsc.optiputer.net", 
            "port": "2096",
            "interface": "enp33s0f0",
            "vlan": "10.0.11.5",
            "redi_port": "2213",
            "nvmes": ["/nvme7/", "/nvme8/", "/nvme9/"]
        }, 
        {
            "node": "k8s-gen4-01.sdsc.optiputer.net", 
            "port": "2097",
            "interface": "enp33s0f1",
            "vlan": "10.0.12.5",
            "redi_port": "2213",
            "nvmes": ["/nvme10/", "/nvme11/", "/nvme12/"]
        }, 
        {
            "node": "k8s-gen4-02.sdsc.optiputer.net", 
            "port": "2094",
            "interface": "enp1s0f0",
            "vlan": "10.16.23.6",
            "redi_port": "2213",
            "nvmes": ["/nvme1/", "/nvme2/", "/nvme3/"]
        },
        {
            "node": "k8s-gen4-02.sdsc.optiputer.net", 
            "port": "2095",
            "interface": "enp1s0f1",
            "vlan": "10.16.25.6",
            "redi_port": "2213",
            "nvmes": ["/nvme4/", "/nvme5/", "/nvme6/"]
        },
        {
            "node": "k8s-gen4-02.sdsc.optiputer.net", 
            "port": "2096",
            "interface": "enp33s0f0",
            "vlan": "10.0.11.6",
            "redi_port": "2213",
            "nvmes": ["/nvme7/", "/nvme8/", "/nvme9/"]
        },
        {
            "node": "k8s-gen4-02.sdsc.optiputer.net", 
            "port": "2097",
            "interface": "enp33s0f1",
            "vlan": "10.0.12.6 ",
            "redi_port": "2213",
            "nvmes": ["/nvme10/", "/nvme11/", "/nvme12/"]
        }
    ]
    write_deployments(dst_configs, base_dir="dst-servers", server_name="dst-origin", redi_name="dst-redi")

    src_configs = [
        {
            "node": "k8s-gen4-07.ultralight.org", 
            "port": "2094",
            "interface": "enp33s0.3911",
            "vlan": "10.0.11.100",
            "redi_port": "1094",
            "nvmes": ["/ramdisk"]
        }, 
        {
            "node": "k8s-gen4-07.ultralight.org", 
            "port": "2095",
            "interface": "enp33s0.3912",
            "vlan": "10.0.12.100",
            "redi_port": "1094",
            "nvmes": ["/ramdisk"]
        }, 
        {
            "node": "dtn-man239.northwestern.edu", 
            "port": "2094",
            "interface": "p1p1",
            "vlan": "10.16.23.1",
            "redi_port": "1094",
            "nvmes": ["/nvme1/", "/nvme2/", "/nvme3/"]
        }, 
        {
            "node": "dtn-man239.northwestern.edu", 
            "port": "2095",
            "interface": "p4p2",
            "vlan": "10.16.25.1",
            "redi_port": "1094",
            "nvmes": ["/nvme4/", "/nvme5/", "/nvme6/"]
        }, 
    ]
    write_deployments(src_configs, base_dir="src-servers", server_name="src-origin", redi_name="src-redi")
