# RRTF Driver Scheduling System

## Objective
Collaborate with Rum River Tree Farm & Nursery to design and implement a system that automates the creation of itineraries and routes for drivers delivering landscape products.

[Summary Video](https://www.youtube.com/watch?v=ORq-fZG99fQ)

## Product

![Landscape Scheduling 1](https://user-images.githubusercontent.com/104173135/205522513-6e8fd7bb-adde-4438-8ea5-b442fcca211f.png)
![Landscape Scheduling 2](https://user-images.githubusercontent.com/104173135/205522520-f3018b81-a1a9-48f1-bc57-014fba05d9d9.png)
![Landscape Scheduling 3](https://user-images.githubusercontent.com/104173135/205522527-e8bf2c9b-597f-4fee-aa35-d07c490dfc9a.png)
![Landscape Scheduling 4](https://user-images.githubusercontent.com/104173135/205522529-a04d8089-84e9-4653-a003-337028d30c5d.png)

## UML Diagrams

### Activity Diagram
![image](https://user-images.githubusercontent.com/104173135/205523240-47d6dbf6-1fac-4301-a615-ac1c022cb8bc.png)

### System Sequence Diagram
![image](https://user-images.githubusercontent.com/104173135/205523264-edcafc1a-a35a-42ee-aa04-5ec219705e79.png)

### Class Diagram
![image](https://user-images.githubusercontent.com/104173135/205523290-2df4c576-06a0-44ac-9c59-870f93530516.png)

## Business Needs Statement
Rum River Tree Farm & Nursery is a private company located in Oak Grove, Minnesota, which opened in 1964. They focus on cultivating Christmas trees and nursery stock for wholesale and retail distribution and provide services for delivering and installing their products during the summer. They own more than 1000 acres of land around Minnesota and employ 25-40 employees throughout the year. They sell more than 100,000 Christmas trees during the winter and supplement their income with landscape services in the Christmas tree offseason. Their delivery and installation schedules for nursery and landscape items utilize an archaic paper and Microsoft Excel-based approach, containing multiple shortcomings that restrict the company's future growth.

The current system is initiated by a customer placing an order over the phone or in person. The order is documented on a computer, whereby an invoice is created that reflects details about the customer and their order. If the customer requests a delivery, the purchase and shipping address is placed in an Excel spreadsheet and is grouped by geographic region of the state by Rum River Tree Farm's receptionist. In addition, the receptionist identifies if a skid steer and class A vehicle are required to handle the order items. The addresses are plugged into Google Maps to determine close proximities. When a sufficient number of orders exist within close proximity, they are assigned a route and date to be completed. Additionally, orders are prioritized by nearness to Rum River Tree Farm's location; however, they also consider the date the order was placed. Monthly driver schedules are put in a word document, and on the day of their delivery, the receptionist hands drivers a schedule that displays their destinations, the number of items to deliver and install, and the approximate time each stop will take.

Rum River Tree Farm's current paper and Microsoft Excel-based method for creating a driver's schedule has multiple shortcomings restricting the company's future growth. The introduction of an automated system would increase productivity by reducing time spent coordinating a schedule manually, providing a more efficient route for drivers, and improving communication between operational users. The new system will collect invoices and create daily itineraries using predetermined criteria, and it will produce a plan that maximizes a driver's time by calculating the approximate length of their day and providing an efficient route. The new system will enable the company to allocate its resources toward more relevant business tasks and facilitate continued company growth.
