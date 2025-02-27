```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [filter, setFilter] = useState('');

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
    };

    const addCustomer = async () => {
        const newCustomer = { name, email };
        await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        });
        setName('');
        setEmail('');
        fetchCustomers();
    };

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div>
            <h2>Customer Management</h2>
            <input 
                type="text" 
                value={name} 
                placeholder="Name" 
                onChange={(e) => setName(e.target.value)} 
            />
            <input 
                type="email" 
                value={email} 
                placeholder="Email" 
                onChange={(e) => setEmail(e.target.value)} 
            />
            <button onClick={addCustomer}>Add Customer</button>
            <input 
                type="text" 
                value={filter} 
                placeholder="Filter by name" 
                onChange={(e) => setFilter(e.target.value)} 
            />
            <ul>
                {filteredCustomers.map((customer) => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```