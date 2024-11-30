# **FinTech Application Deployment**

This repository contains the source code and configuration files to deploy the FinTech Portfolio Management application to an AWS EKS Kubernetes cluster. The deployment includes a Kafka cluster and topics managed by the **Strimzi Kafka Operator**.

---

## **CI/CD Pipeline Overview**

The CI/CD pipeline is designed to automate the deployment process, ensuring all components are set up in the correct order:

1. Install and configure `kubectl`.
2. Update `kubeconfig` to connect to the AWS EKS cluster.
3. Deploy the **Strimzi Kafka Operator**.
4. Deploy the Kafka cluster.
5. Create required Kafka topics.
6. Deploy the application and its services.

---

## **Pipeline Steps**

### **Step 1: Set up `kubectl`**
The pipeline installs `kubectl` and verifies its installation:
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

### **Step 2: Configure `kubeconfig`**
The pipeline uses the AWS CLI to configure `kubeconfig` for access to the AWS EKS cluster:
```bash
aws eks update-kubeconfig --region us-east-1 --name <EKS_CLUSTER_NAME>
```

### **Step 3: Deploy Strimzi Kafka Operator**
The **Strimzi Kafka Operator** manages Kafka clusters and topics declaratively. It is deployed using the `strimzi-operator.yaml` manifest:
```bash
kubectl apply -f app/k8s/strimzi/strimzi-operator.yaml
kubectl wait --for=condition=Available --timeout=300s deployment/strimzi-cluster-operator -n kafka
```

### **Step 4: Deploy Kafka Cluster**
The Kafka cluster is deployed using the `kafka-cluster.yaml` manifest:
```bash
kubectl apply -f app/k8s/strimzi/kafka-cluster.yaml
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka
```

### **Step 5: Create Kafka Topics**
Kafka topics are created using the `kafka-topics.yaml` manifest:
```bash
kubectl apply -f app/k8s/strimzi/kafka-topics.yaml
```

### **Step 6: Deploy the Application**
The application and its services are deployed using Kubernetes manifests:
```bash
kubectl apply -f app/k8s/deployment.yaml
kubectl apply -f app/k8s/service.yaml
```

---

## **Kafka Setup**

### **Strimzi Kafka Operator**
- **Manifest**: Located at `app/k8s/strimzi/strimzi-operator.yaml`.
- **Purpose**: Manages Kafka clusters and topics within the Kubernetes ecosystem.

### **Kafka Cluster**
- **Manifest**: Located at `app/k8s/strimzi/kafka-cluster.yaml`.
- **Configuration**:
  - 3 Kafka broker replicas.
  - 3 Zookeeper replicas.
  - Persistent storage with 10Gi for Kafka and 5Gi for Zookeeper.

### **Kafka Topics**
- **Manifest**: Located at `app/k8s/strimzi/kafka-topics.yaml`.
- **Topics**:
  - `stock-prices`: Publishes real-time stock prices.
  - `user-transactions`: Captures user actions like buy/sell transactions.
  - `portfolio-updates`: Outputs aggregated portfolio updates.
  - `alerts`: Publishes risk alerts or anomaly detections.

---

## **Pipeline Execution**

### **Triggering the Pipeline**
The pipeline is automatically triggered on a push to the `main` branch. Ensure all manifests are correctly updated before committing changes.

### **Environment Variables and Secrets**
Ensure the following secrets are configured in the CI/CD environment:
- `AWS_ACCESS_KEY_ID`: AWS access key.
- `AWS_SECRET_ACCESS_KEY`: AWS secret key.
- `EKS_CLUSTER_NAME`: Name of the EKS cluster.
- `DOCKER_USERNAME`: Docker Hub username.
- `DOCKER_PASSWORD`: Docker Hub password.

---

## **Known Issues**
- Ensure the Strimzi Kafka Operator is fully deployed before creating the Kafka cluster.
- Add readiness checks to avoid race conditions between Kafka cluster and topic creation.

---

## **Contributing**

1. Clone the repository.
2. Make changes in a feature branch.
3. Update relevant manifests and this `README.md` as needed.
4. Submit a pull request for review.

---

This updated `README.md` ensures that all team members understand the CI/CD pipeline workflow and Kafka setup process. It documents the order of deployment and provides clear instructions for each step.
