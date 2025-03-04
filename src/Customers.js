```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [filter, setFilter] = useState('');
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
    };

    const handleAddCustomer = async () => {
        const response = await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        });
        const updatedCustomer = await response.json();
        setCustomers([...customers, updatedCustomer]);
        setNewCustomer({ name: '', email: '' });
    };

    const handleFilterChange = (event) => {
        setFilter(event.target.value);
    };

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management</h1>
            <input
                type="text"
                placeholder="Filter by name"
                value={filter}
                onChange={handleFilterChange}
            />
            <div>
                <h2>Add New Customer</h2>
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
            </div>
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```