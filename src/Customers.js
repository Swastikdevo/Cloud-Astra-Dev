```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
    const [filter, setFilter] = useState('');

    useEffect(() => {
        // Fetch initial customer data
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const handleInputChange = (e) => {
        setNewCustomer({ ...newCustomer, [e.target.name]: e.target.value });
    };

    const addCustomer = async () => {
        const response = await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        });
        const data = await response.json();
        setCustomers([...customers, data]);
        setNewCustomer({ name: '', email: '' });
    };

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(filter.toLowerCase()));

    return (
        <div>
            <h1>Customer Management</h1>
            <input
                type="text"
                placeholder="Search Customers"
                value={filter}
                onChange={e => setFilter(e.target.value)}
            />
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
                <button onClick={addCustomer}>Add Customer</button>
            </div>
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