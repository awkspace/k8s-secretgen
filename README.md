# k8s-secretgen

Idempotently generate secrets for k8s.

## Example

Create a file called `.k8s-secrets.yml`:

``` yaml
---
name: my-secret
key: my-secret-key
---
name: my-other-secret
key: my-other-secret-key
length: 32
```

Then run:

``` bash
k8s-secretgen --namespace=my-namespace
```
