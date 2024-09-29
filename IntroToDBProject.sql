create table customeraccount(
CustomerID int primary key auto_increment,
FName varchar(20) not null,
MName varchar(20) not null,
LName varchar(20) not null,
Birthdate date not null,
Gender varchar(6),
Address varchar(100),
PhoneNumber varchar(13),
Email varchar(30));

create table orders(
OrderID int primary key auto_increment,
CustomerID int not null,
ShippingAddress varchar(100),
foreign key (CustomerID) references customeraccount(CustomerID));

create table product(
ProductID int primary key auto_increment,
Name varchar(20) not null,
Manufacturer varchar(20),
Category varchar(20),
Price decimal(10,2));

create table orderline(
OrderLineID int primary key auto_increment,
OrderedQty int,
OrderID int not null,
ProductID int not null,
foreign key (OrderID) references orders(OrderID),
foreign key (ProductID) references product(ProductID));

create table vendor(
VendorID int primary key auto_increment,
Name varchar(20) not null,
Country varchar(20));

create table warehouse(
WarehouseID int primary key auto_increment,
Location varchar(100));

create table storedproduct(
SPID int primary key auto_increment,
WarehouseQty int,
ManufacturingDate date,
ExpirationDate date,
ProductID int not null,
VendorID int not null,
WarehouseID int not null,
foreign key (ProductID) references product(ProductID),
foreign key (VendorID) references vendor(VendorID),
foreign key (WarehouseID) references warehouse(WarehouseID));

create table staff(
StaffID int primary key auto_increment,
FName varchar(20) not null,
MName varchar(20) not null,
LName varchar(20) not null,
Birthdate date not null,
Gender varchar(6),
Address varchar(100),
Email varchar(30),
ManagerID int,
WarehouseID int not null,
foreign key (ManagerID) references staff(StaffID),
foreign key (WarehouseID) references warehouse(WarehouseID));

create table phonenumber(
PhoneNumber varchar(13) not null,
StaffID int not null,
foreign key (StaffID) references staff(StaffID),
primary key (StaffID,PhoneNumber));

insert into customeraccount (FName, MName, LName, Birthdate, Gender, Address, PhoneNumber, Email) values ("Ahmed","Mohammed","Mohamady", "2004-4-4", "male", "1 El Rasafa St.","+201552514589","ahmedmohamady@gmail.com");
insert into customeraccount (FName, MName, LName, Birthdate, Gender, Address, PhoneNumber, Email) values ("Al-Hussain","Yasser","El-Saaed", "2003-3-10", "male", "1 El Alexandria St.","+201225493155","alhussain@gmail.com");
insert into customeraccount (FName, MName, LName, Birthdate, Gender, Address, PhoneNumber, Email) values ("Omar","Hafez","Maamon", "2004-6-6", "male", "1 El Alexandria St.","+201002954883","omartigar@gmail.com");

insert into orders (CustomerID,ShippingAddress) values (1,"1 El Rasafa St.");
insert into orders (CustomerID,ShippingAddress) values (1,"2 El Araby St.");
insert into orders (CustomerID,ShippingAddress) values (2,"1 El Alexandria St.");

insert into product (Name,Manufacturer,Category,Price) values ("Mix","Juhayna","Food",8.75);
insert into product (Name,Manufacturer,Category,Price) values ("Lotus Biscoff","Lotus Bakeries","Food",120);
insert into product (Name,Manufacturer,Category,Price) values ('43" The Sero QLED 4K',"Samsung","Electronics",1500);

insert into orderline (OrderedQty,OrderID,ProductID) values (100,3,1);
insert into orderline (OrderedQty,OrderID,ProductID) values (5,3,2);
insert into orderline (OrderedQty,OrderID,ProductID) values (1,3,3);

insert into vendor (Name, Country) values ("Zoro for Exports", "South America");
insert into vendor (Name, Country) values ("Mared Washweshny", "Australia");
insert into vendor (Name, Country) values ("Dina Farms", "Egypt");

insert into warehouse (Location) value ("Cairo");
insert into warehouse (Location) value ("Alexandria");
insert into warehouse (Location) value ("Aswan");

insert into storedproduct (WarehouseQty, ManufacturingDate, ExpirationDate, ProductID, VendorID, WarehouseID) values (1000, "2023-10-1", "2024-6-5",1,1,2);
insert into storedproduct (WarehouseQty, ManufacturingDate, ExpirationDate, ProductID, VendorID, WarehouseID) values (500, "2022-1-10", "2023-2-9",1,1,1);
insert into storedproduct (WarehouseQty, ManufacturingDate, ProductID, VendorID, WarehouseID) values (1000, "2020-6-8", 3,2,1);

insert into staff (FName, MName, LName, Birthdate, Gender, Address, Email, WarehouseID) values ("Mohammed","Mahmoud","Maamon","1976-10-6","male","11 El Doki St.","mohammedmaamon@yahoo.com",1);
insert into staff (FName, MName, LName, Birthdate, Gender, Address, Email, ManagerID, WarehouseID) values ("Yasmine","Nader","Ali","1988-10-6","female","22 El Zamalek St.","yasmine887@yahoo.com",1,1);
insert into staff (FName, MName, LName, Birthdate, Gender, Address, Email, ManagerID, WarehouseID) values ("Emad","Hamza","Naaeem","1987-11-2","male","65 Smouha St","emadhamza@gmail.com",1,1);

insert into phonenumber (PhoneNumber, StaffID) values ("201554865779",1);
insert into phonenumber (PhoneNumber, StaffID) values ("201226544792",1);
insert into phonenumber (PhoneNumber, StaffID) values ("201009532216",2);