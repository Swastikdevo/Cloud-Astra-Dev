```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '', phone: '' });
    
    const fetchCustomers = async () => {
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
    };

    useEffect(() => {
        fetchCustomers();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewCustomer({ ...newCustomer, [name]: value });
    };

    const handleAddCustomer = async (e) => {
        e.preventDefault();
        await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer)
        });
        setNewCustomer({ name: '', email: '', phone: '' });
        fetchCustomers();
    };

    const handleDeleteCustomer = async (id) => {
        await fetch(`/api/customers/${id}`, { method: 'DELETE' });
        fetchCustomers();
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <form onSubmit={handleAddCustomer}>
                <input name="name" value={newCustomer.name} onChange={handleChange} placeholder="Name" required />
                <input name="email" value={newCustomer.email} onChange={handleChange} placeholder="Email" required />
                <input name="phone" value={newCustomer.phone} onChange={handleChange} placeholder="Phone" required />
                <button type="submit">Add Customer</button>
            </form>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email} - {customer.phone}
                        <button onClick={() => handleDeleteCustomer(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```