1. The data in the table isn't in 'first normal form' because the 'detailing' column contains more than one value. For the table to first normal form, all attributes in the relation have to be single valued attributes.

2. Given,

- Date & Time → candidate key, both of these are used to find the other attributes uniquely.
- A person's phone number doesn't change and is unique 
	→ A phone number can determine a person uniquely 

However, there shouldn't be any transitive dependencies in third normal form. (Owner's phone # → Owner's last name)


3.

NewTable(Date, Time, Owner_Phone_Number, Detailing)

Date,Time → Owner_Phone_Number, Detailing

NewTable2(Owner_Phone_Number, Owner_Last_Name, Vehicle_Plate, Vehicle_Model)

Owner_Phone_Number → Owner_Last_Name, Vehicle_Plate, Vehicle_Model

NewTable and NewTable2 can be joined together using Owner_Phone_Number