```javascript
import React, { useState, useEffect } from 'react';

const CustomerManager = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
    const [filter, setFilter] = useState('');

    useEffect(() => {
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const addCustomer = () => {
        setCustomers([...customers, newCustomer]);
        setNewCustomer({ name: '', email: '' });
    };

    const filteredCustomers = customers.filter(customer => customer.name.includes(filter));

    return (
        <div>
            <h2>Customer Management</h2>
            <input
                type="text"
                placeholder="Search customer"
                value={filter}
                onChange={e => setFilter(e.target.value)}
            />
            <ul>
                {filteredCustomers.map((customer, index) => (
                    <li key={index}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
            <input
                type="text"
                placeholder="Customer Name"
                value={newCustomer.name}
                onChange={e => setNewCustomer({ ...newCustomer, name: e.target.value })}
            />
            <input
                type="email"
                placeholder="Customer Email"
                value={newCustomer.email}
                onChange={e => setNewCustomer({ ...newCustomer, email: e.target.value })}
            />
            <button onClick={addCustomer}>Add Customer</button>
        </div>
    );
};

export default CustomerManager;
```