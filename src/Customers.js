```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const addCustomer = async () => {
        const newCustomer = { name, email };
        await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        });
        setCustomers([...customers, newCustomer]);
        setName('');
        setEmail('');
    };

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management</h1>
            <input
                type="text"
                placeholder="Search customers"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <ul>
                {filteredCustomers.map((customer, index) => (
                    <li key={index}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
            <input
                type="text"
                placeholder="Customer Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <input
                type="email"
                placeholder="Customer Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <button onClick={addCustomer}>Add Customer</button>
        </div>
    );
};

export default CustomerManagement;
```