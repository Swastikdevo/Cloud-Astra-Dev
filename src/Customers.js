```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [name, setName] = useState("");

    const addCustomer = () => {
        if (name) {
            setCustomers([...customers, { id: Date.now(), name }]);
            setName("");
        }
    };

    const removeCustomer = (id) => {
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    return (
        <div>
            <h2>Customer Management System</h2>
            <input 
                type="text" 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                placeholder="Enter customer name" 
            />
            <button onClick={addCustomer}>Add Customer</button>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} 
                        <button onClick={() => removeCustomer(customer.id)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```