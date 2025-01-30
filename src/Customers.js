```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

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
        const { name, value } = e.target;
        setNewCustomer((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        });
        const createdCustomer = await response.json();
        setCustomers((prev) => [...prev, createdCustomer]);
        setNewCustomer({ name: '', email: '' });
    };

    const deleteCustomer = async (id) => {
        await fetch(`/api/customers/${id}`, { method: 'DELETE' });
        setCustomers((prev) => prev.filter(customer => customer.id !== id));
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="name"
                    placeholder="Name"
                    value={newCustomer.name}
                    onChange={handleInputChange}
                    required
                />
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={newCustomer.email}
                    onChange={handleInputChange}
                    required
                />
                <button type="submit">Add Customer</button>
            </form>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email}
                        <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```