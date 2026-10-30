# MongoDB (INF-05)

The database of the app. It saves every visit to the web page.

- Installed with `kubectl`, in the `default` namespace (as in the project schema).
- Official `mongo:8.0` image, one copy (StatefulSet) with its own 1Gi disk, so the data stays after a restart.
- Address inside the cluster: `mongodb.default.svc.cluster.local:27017`
- The root password is only in the Kubernetes Secret `mongodb-secret`. MongoDB and the app both read it from there.

## Install

Create the Secret once (choose your own password):

```
kubectl create secret generic mongodb-secret --from-literal=MONGO_PASSWORD=<your-password>
```

Install MongoDB:

```
kubectl apply -f infra/mongodb/mongodb.yaml
```

Check that it is running (`1/1` and `Running`):

```
kubectl get pods -l app=mongodb
```
