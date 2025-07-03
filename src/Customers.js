```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => setCustomers(data));
    }, []);

    const handleAddCustomer = () => {
        setCustomers([...customers, newCustomer]);
        setNewCustomer({ name: '', email: '' });
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <input
                type="text"
                placeholder="Name"
                value={newCustomer.name}
                onChange={(e) => setNewCustomer({ ...newCustomer, name: e.target.value })}
            />
            <input
                type="email"
                placeholder="Email"
                value={newCustomer.email}
                onChange={(e) => setNewCustomer({ ...newCustomer, email: e.target.value })}
            />
            <button onClick={handleAddCustomer}>Add Customer</button>
            <ul>
                {customers.map((customer, index) => (
                    <li key={index}>
                        {customer.name} - {customer.email}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```