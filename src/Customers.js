```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
    const [filter, setFilter] = useState('');

    useEffect(() => {
        // Simulated fetch from an API
        const fetchCustomers = async () => {
            const data = await fetch('/api/customers').then(res => res.json());
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const handleChange = (e) => {
        setNewCustomer({ ...newCustomer, [e.target.name]: e.target.value });
    };

    const handleAddCustomer = () => {
        setCustomers([...customers, { ...newCustomer, id: Date.now() }]);
        setNewCustomer({ name: '', email: '' });
    };

    const handleDeleteCustomer = (id) => {
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management</h1>
            <input
                type="text"
                name="filter"
                placeholder="Filter by name"
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
            />
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
            <button onClick={handleAddCustomer}>Add Customer</button>
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} ({customer.email})
                        <button onClick={() => handleDeleteCustomer(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```