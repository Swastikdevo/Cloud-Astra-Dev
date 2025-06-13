```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    useEffect(() => {
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewCustomer((prev) => ({ ...prev, [name]: value }));
    };

    const handleAddCustomer = async () => {
        const response = await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        });
        const data = await response.json();
        setCustomers((prev) => [...prev, data]);
        setNewCustomer({ name: '', email: '' });
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <div>
                <input
                    type="text"
                    name="name"
                    placeholder="Customer Name"
                    value={newCustomer.name}
                    onChange={handleInputChange}
                />
                <input
                    type="email"
                    name="email"
                    placeholder="Customer Email"
                    value={newCustomer.email}
                    onChange={handleInputChange}
                />
                <button onClick={handleAddCustomer}>Add Customer</button>
            </div>
            <ul>
                {customers.map((customer) => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```