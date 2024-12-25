```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => setCustomers(data));
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewCustomer({ ...newCustomer, [name]: value });
    };

    const handleAddCustomer = () => {
        setCustomers([...customers, newCustomer]);
        setNewCustomer({ name: '', email: '' });
    };

    return (
        <div>
            <h1>Customer Management System</h1>
            <input
                name="name"
                value={newCustomer.name}
                onChange={handleChange}
                placeholder="Customer Name"
            />
            <input
                name="email"
                value={newCustomer.email}
                onChange={handleChange}
                placeholder="Customer Email"
            />
            <button onClick={handleAddCustomer}>Add Customer</button>
            <ul>
                {customers.map((customer, index) => (
                    <li key={index}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```