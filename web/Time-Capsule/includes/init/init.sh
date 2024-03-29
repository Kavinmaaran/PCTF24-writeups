mariadb -u root -p$MYSQL_ROOT_PASSWORD --execute \
"USE $MYSQL_DATABASE;
CREATE TABLE messages ( id INT(11) AUTO_INCREMENT, user VARCHAR(100) NOT NULL, storedname VARCHAR(100) NOT NULL, date DATE NOT NULL, PRIMARY KEY (id) );
CREATE TABLE user ( id INT(11) NOT NULL AUTO_INCREMENT, public_id VARCHAR(50) UNIQUE, name VARCHAR(100) UNIQUE, password VARCHAR(255), PRIMARY KEY (id) );
CREATE TABLE not_admin_user ( id INT(11) NOT NULL AUTO_INCREMENT, public_id VARCHAR(50) UNIQUE, name VARCHAR(100) UNIQUE, password VARCHAR(255), PRIMARY KEY (id) );
INSERT INTO  messages(id,user,storedname,date) values(1,'block','block','2222-12-12');
INSERT INTO  messages(id,user,storedname,date) values(12643,'admin','blahblah','2222-12-12');
INSERT INTO  messages(id,user,storedname,date) values(23143,'block1','block1','2222-12-12');
INSERT INTO user(public_id,name,password) values('979d2015-f2d9-40ac-9336-e61659394360','admin','pbkdf2:sha256:600000\$6KuI7sn4RhmpIZQk\$5e1a5923a20c6263265fa2f6c31f36f662d78a8916b646ce1a55829182b1c975');
INSERT INTO not_admin_user(public_id,name,password) values('979d2015-f2d9-40ac-9336-e71293840130','admin','pbkdf2:sha256:600000\$z5xh5PenLd9ue32A\$7a7bcf1e1652f53d595a91a9c369b0f0d98deb4274abc244ff5e2d8fe7b76007');


CREATE USER '$ROMYSQL_USER'@'%' IDENTIFIED BY '$ROMYSQL_PASSWORD';
GRANT SELECT ON $MYSQL_DATABASE.messages TO '$ROMYSQL_USER'@'%' IDENTIFIED BY '$ROMYSQL_PASSWORD';
FLUSH PRIVILEGES;

REVOKE ALL PRIVILEGES ON $MYSQL_DATABASE.* FROM '$MYSQL_USER'@'%';
GRANT SELECT,INSERT ON $MYSQL_DATABASE.messages TO '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
FLUSH PRIVILEGES;
GRANT SELECT,INSERT ON $MYSQL_DATABASE.not_admin_user TO '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
FLUSH PRIVILEGES;
GRANT SELECT ON $MYSQL_DATABASE.user TO '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
FLUSH PRIVILEGES;"
