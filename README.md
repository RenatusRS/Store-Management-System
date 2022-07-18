**Run Tests**

```commandline
python main.py --type all --with-authentication --authentication-address http://127.0.0.1:5002 --jwt-secret JWT_SECRET_KEY --roles-field role --administrator-role admin --customer-role customer --warehouse-role warehouse --customer-address http://127.0.0.1:5003 --warehouse-address http://127.0.0.1:5004 --administrator-address http://127.0.0.1:5001
```

**Swarm Commands**

Initialize

```commandline
docker swarm init
```

Deploy

```commandline
docker stack deploy --compose-file swarm.yaml swarm
```

Test Connection

```commandline
docker stack services swarm
```

Quit

```commandline
docker swarm leave --force
```

**Reset Database**

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