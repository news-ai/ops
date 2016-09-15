Deploying:

```
kubectl create -f service-account.yaml
kubectl create -f es-svc.yaml
kubectl create -f es-rc.yaml
```

Getting pods:

`kubectl get pods`

Getting logs:

`kubectl logs es-kfymw`

Scaling replicas:

`kubectl scale --replicas=3 rc es`

Accessing ES information:

`kubectl get service elasticsearch`
