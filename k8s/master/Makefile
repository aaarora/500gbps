delete:
	- kubectl delete -k ./deployments/master-01/
	- kubectl delete -k ./deployments/master-02/
create:
	- kubectl apply -k ./deployments/master-01/
	- kubectl apply -k ./deployments/master-02/
upload:
	- kubectl cp tpc $(shell kubectl get pods -l k8s-app=tpc-master-01 -o jsonpath="{.items[0].metadata.name}"):/home/
	- kubectl cp tpc $(shell kubectl get pods -l k8s-app=tpc-master-02 -o jsonpath="{.items[0].metadata.name}"):/home/
