--
-- Dumping data for table `zones`
--

LOCK TABLES `zones` WRITE;
/*!40000 ALTER TABLE `zones` DISABLE KEYS */;
INSERT INTO `zones` VALUES (1,'example.com','2013-05-10 09:36:24','ns0.jinocloud.com','dnsadmin.jinocloud.com',86400,14400,7200,1209600,86400);
/*!40000 ALTER TABLE `zones` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `records`
--

LOCK TABLES `records` WRITE;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;
INSERT INTO `records` VALUES (1,1,'test','A',86400,'192.168.0.1'),(2,1,'test2','A',86400,'192.168.0.2'),(3,1,'test3','A',86400,'192.168.0.3'),(4,1,'test4','A',86400,'192.168.0.4'),(5,1,'test1','MX',86400,'test1.example.com');
/*!40000 ALTER TABLE `records` ENABLE KEYS */;
UNLOCK TABLES;

