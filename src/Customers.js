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

    const addCustomer = () => {
        fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        })
        .then(response => response.json())
        .then(customer => {
            setCustomers([...customers, customer]);
            setNewCustomer({ name: '', email: '' });
        });
    };

    return (
        <div>
            <h2>Customer Management</h2>
            <input 
                type="text" 
                name="name" 
                placeholder="Customer Name" 
                value={newCustomer.name} 
                onChange={handleChange} 
            />
            <input 
                type="email" 
                name="email" 
                placeholder="Customer Email" 
                value={newCustomer.email} 
                onChange={handleChange} 
            />
            <button onClick={addCustomer}>Add Customer</button>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```