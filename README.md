# **Store Management System**
> Project for **E-Business Infrastructure** / **Infrastruktura za Elektronsko Poslovanje** class.

## **Introduction**
Web service-based system designed for multi-user functionality, focused on managing a retail store. The system is divided into two main sections, one for managing user accounts and another for handling store operations.

It has been built using **Python** with **Flask** and **SQLAlchemy** libraries and is deployable using **Docker** containers. Configuration files are provided to launch the entire system on a cluster of computers using **Docker Swarm**.

## **Requirements**
- **Python 3.9+**
- **Docker 20.10+**

For Python dependencies, refer to the `requirements.txt` file for specific package versions.

## **How-To Run**
Before running, make sure that ports **8080**, **5001**, **5002**, **5003**, and **5004** are free.

To initialize and run the services, execute the following commands:

```bash
docker swarm init
docker stack deploy --compose-file swarm.yaml swarm
```

To check the status of the services:
```bash
docker stack services swarm
```

To shut down the system:
```bash
docker swarm leave --force
```

### **Running Tests**
To run the tests, execute:

```bash
python tests/main.py --type all --with-authentication --authentication-address http://127.0.0.1:5002 --jwt-secret JWT_SECRET_KEY --roles-field role --administrator-role admin --customer-role customer --warehouse-role warehouse --customer-address http://127.0.0.1:5003 --warehouse-address http://127.0.0.1:5004 --administrator-address http://127.0.0.1:5001
```

### **Database Reset Commands**
If you need to reset the database, execute these SQL commands:

```sql
DELETE FROM product_orders;
ALTER TABLE product_orders AUTO_INCREMENT = 0;

DELETE FROM product_categories;
ALTER TABLE product_categories AUTO_INCREMENT = 0;

DELETE FROM products;
ALTER TABLE products AUTO_INCREMENT = 0;

DELETE FROM categories;
ALTER TABLE categories AUTO_INCREMENT = 0;

DELETE FROM orders;
ALTER TABLE orders AUTO_INCREMENT = 0;
```
