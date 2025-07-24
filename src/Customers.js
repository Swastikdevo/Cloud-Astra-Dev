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
        setNewCustomer({...newCustomer, [name]: value});
    };

    const addCustomer = async (e) => {
        e.preventDefault();
        await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        });
        setCustomers([...customers, newCustomer]);
        setNewCustomer({ name: '', email: '' });
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <form onSubmit={addCustomer}>
                <input type="text" name="name" value={newCustomer.name} onChange={handleInputChange} placeholder="Customer Name" required />
                <input type="email" name="email" value={newCustomer.email} onChange={handleInputChange} placeholder="Customer Email" required />
                <button type="submit">Add Customer</button>
            </form>
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