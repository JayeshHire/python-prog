# Factory Method  

Factory method is an interface which helps in creation of object inside the superclass, but subclasses alters the type of object that will be created.

Example:
Suppose you created a logistics app for transporting goods via trucks. 

 ------------------------
|       Logistics        |
|                        |
 ------------------------
             | 
            \ /
 -------------------------
|       (Utility class)   |
|       Transport         |
|                         |
 -------------------------
             | (Creates instance of)
            \ /
 -------------------------
|       Truck             |
|                         |
 -------------------------

The app works great for one type of transport. 

The problem arises when the app grows and you have to add new entities in your existing codebase.
For example, your app grows and shipping companies reach out to you, so they could also use your logistics app. Now you would have to make changes in instance creation by adding conditional statements in your app. If we look closely here only the type of `Transport` for the logistics app is changing. If we made the object creation for the `Transport` class independent of the type of logistics then different types of objects can be created based on the demand for the logistics support.

This is where factory method can be helpful. It can decouple the object creation for the road logistics as well as ship logistics. Even more different logistics classes can be easily added, without creating a tightly coupled system.

Here's an example of the new implementation

 -----------------------------------------------------------
|       LogisticSupCls                                      |
|       - define delivery method                            |
|       - define an abstract createTransport method         |
 -----------------------------------------------------------
            |
            |
            |             
           \ /             
 ----------------------------------------------------------------
|       LogisticSubCls                                           |
|       - define createTransport method                          |
 ----------------------------------------------------------------
            
