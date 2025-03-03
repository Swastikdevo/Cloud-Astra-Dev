```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '', phone: '' });

    useEffect(() => {
        // Simulating fetching customer data from an API
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewCustomer({ ...newCustomer, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setCustomers([...customers, newCustomer]);
        setNewCustomer({ name: '', email: '', phone: '' });
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <form onSubmit={handleSubmit}>
                <input type="text" name="name" value={newCustomer.name} onChange={handleChange} placeholder="Name" required />
                <input type="email" name="email" value={newCustomer.email} onChange={handleChange} placeholder="Email" required />
                <input type="tel" name="phone" value={newCustomer.phone} onChange={handleChange} placeholder="Phone" required />
                <button type="submit">Add Customer</button>
            </form>
            <ul>
                {customers.map((customer, index) => (
                    <li key={index}>{customer.name} - {customer.email} - {customer.phone}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```